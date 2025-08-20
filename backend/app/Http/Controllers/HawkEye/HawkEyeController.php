<?php

namespace App\Http\Controllers\HawkEye;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Storage;
use Illuminate\Support\Facades\File;
use Illuminate\Support\Facades\Log;

class HawkEyeController extends Controller
{
    public function showTestPage()
    {
        return view('hawk-eye.test-upload');
    }

    private function getPythonExe(): string
    {
        // Use system Python 3.13 which has all required packages
        $systemPython = 'C:\Users\haris\AppData\Local\Programs\Python\Python313\python.exe';
        if (file_exists($systemPython)) return $systemPython;

        // Fallback to system python
        return 'python';
    }

    private function buildPythonCommand(string $pythonScript, string $videoPath, string $outputDir): string
    {
        $pythonExe = $this->getPythonExe();

        // Windows CMD env chaining - removed problematic OPENCV_VIDEOIO_PRIORITY_MSMF
        $env = 'set PYTHONUNBUFFERED=1 && set KMP_DUPLICATE_LIB_OK=TRUE';

        $cmd = 'cmd /C ' . $env . ' && ' .
               '"' . $pythonExe . '" "' . $pythonScript . '" ' .
               '--video "' . $videoPath . '" ' .
               '--out "' . $outputDir . '" ' .
               '--conf 0.25 --iou 0.7 --device cpu';

        Log::info("Built Python command", [
            'python_exe' => $pythonExe,
            'script' => $pythonScript,
            'video_path' => $videoPath,
            'output_dir' => $outputDir,
            'full_command' => $cmd
        ]);

        return $cmd;
    }

    public function processVideo(Request $request)
    {
        $request->validate([
            'video' => 'required|file|max:102400'
        ], [
            'video.required' => 'Video file is required',
            'video.file' => 'Uploaded content must be a file',
            'video.max' => 'Video size must be less than 100MB'
        ]);

        try {
            $video = $request->file('video');

            if (!$video->isValid()) {
                throw new \Exception('Invalid file upload: ' . $video->getError());
            }

            $allowedExtensions = ['mp4', 'avi', 'mov', 'm4v', 'webm'];
            $fileExtension = strtolower($video->getClientOriginalExtension());
            if (!in_array($fileExtension, $allowedExtensions)) {
                throw new \Exception("File extension '{$fileExtension}' not allowed. Allowed: " . implode(', ', $allowedExtensions));
            }

            Log::info("File received:", [
                'original_name' => $video->getClientOriginalName(),
                'mime_type' => $video->getMimeType(),
                'size' => $video->getSize(),
                'extension' => $video->getClientOriginalExtension(),
                'is_valid' => $video->isValid(),
                'error' => $video->getError()
            ]);

            $filename = time() . '_' . $video->getClientOriginalName();

            $uploadDir = 'hawk-eye/upload_videos';
            $resultsDir = 'hawk-eye/result_videos';

            $fullUploadDir = storage_path('app' . DIRECTORY_SEPARATOR . str_replace('/', DIRECTORY_SEPARATOR, $uploadDir));
            $fullResultsDir = storage_path('app' . DIRECTORY_SEPARATOR . str_replace('/', DIRECTORY_SEPARATOR, $resultsDir));

            if (!is_dir($fullUploadDir)) {
                mkdir($fullUploadDir, 0755, true);
            }
            if (!is_dir($fullResultsDir)) {
                mkdir($fullResultsDir, 0755, true);
            }

            // Store video
            $uploadPath = $video->storeAs($uploadDir, $filename, 'local');
            $fullVideoPath = storage_path('app' . DIRECTORY_SEPARATOR . str_replace('/', DIRECTORY_SEPARATOR, $uploadPath));

            if (!file_exists($fullVideoPath)) {
                $directPath = $fullUploadDir . DIRECTORY_SEPARATOR . $filename;
                if (move_uploaded_file($video->getPathname(), $directPath)) {
                    $fullVideoPath = $directPath;
                    $uploadPath = $uploadDir . '/' . $filename;
                } else {
                    throw new \Exception("Failed to store video file.");
                }
            }

            $analysisId = time() . '_' . uniqid();
            $outputDir = storage_path("app" . DIRECTORY_SEPARATOR . str_replace('/', DIRECTORY_SEPARATOR, $resultsDir) . DIRECTORY_SEPARATOR . $analysisId);

            // Resolve python script path
            $pythonScript = base_path('../Hawk-Eye/cricket-hawk-eye/yolo-model/detect_ball.py');
            if (!file_exists($pythonScript)) {
                $pythonScript = base_path('../../Hawk-Eye/cricket-hawk-eye/yolo-model/detect_ball.py');
            }
            if (!file_exists($pythonScript)) {
                $pythonScript = 'G:/Projects/CricketAnalysis-EB/Hawk-Eye/cricket-hawk-eye/yolo-model/detect_ball.py';
            }
            if (!file_exists($pythonScript)) {
                throw new \Exception("Python script not found at: " . $pythonScript);
            }

            if (!file_exists($fullVideoPath)) {
                throw new \Exception("Video file not found at: " . $fullVideoPath);
            }

            // Build & run command with env
            $cmd = $this->buildPythonCommand($pythonScript, $fullVideoPath, $outputDir);
            Log::info("Executing command: " . $cmd);

            set_time_limit(900); // 15 minutes
            $result = shell_exec($cmd . " 2>&1");

            // Additional output analysis
            $outputLength = strlen($result ?? '');
            $lineCount = substr_count($result ?? '', "\n");
            Log::info("Python output analysis", [
                'total_length' => $outputLength,
                'line_count' => $lineCount,
                'last_1000_chars' => substr($result ?? '', -1000)
            ]);

            Log::info("Python script output (first 5k): " . substr($result ?? '', 0, 5000));

            if ($result === null) {
                throw new \Exception("Python script execution failed - no output returned");
            }

            // Parse first JSON line
            $lines = preg_split('/\r\n|\r|\n/', trim($result));
            $jsonResult = null;
            $allJsonLines = [];

            // Collect all JSON lines for debugging
            foreach ($lines as $lineNum => $line) {
                $line = trim($line);
                if ($line !== '' && $line[0] === '{') {
                    $decoded = json_decode($line, true);
                    if (is_array($decoded)) {
                        $allJsonLines[] = [
                            'line_number' => $lineNum + 1,
                            'content' => $decoded
                        ];

                        // Look for the final success result (last complete JSON)
                        if (isset($decoded['success']) && $decoded['success'] === true) {
                            $jsonResult = $decoded;
                            Log::info("Found successful JSON result at line " . ($lineNum + 1), $decoded);
                            break;
                        }
                    }
                }
            }

            // If no success found, try to find any valid JSON with success=true
            if (!$jsonResult) {
                foreach (array_reverse($allJsonLines) as $jsonLine) {
                    if (isset($jsonLine['content']['success']) && $jsonLine['content']['success'] === true) {
                        $jsonResult = $jsonLine['content'];
                        Log::info("Found successful JSON result in reverse search at line " . $jsonLine['line_number'], $jsonLine['content']);
                        break;
                    }
                }
            }

            // Log all JSON lines found for debugging
            Log::info("All JSON lines found: " . count($allJsonLines), $allJsonLines);

            if ($jsonResult && !empty($jsonResult['success'])) {
                $this->organizeResults($outputDir, $resultsDir, $analysisId);

                // Log successful processing summary
                Log::info("Video processing completed successfully", [
                    'analysis_id' => $analysisId,
                    'frames_processed' => $jsonResult['frames'] ?? 'Unknown',
                    'detection_counts' => $jsonResult['counts'] ?? [],
                    'processing_time' => $jsonResult['video_processing_time'] ?? 'Unknown',
                    'upload_path' => $uploadPath,
                    'output_directory' => $outputDir
                ]);

                return response()->json([
                    'success' => true,
                    'message' => 'Video analysis completed successfully!',
                    'data' => [
                        'analysis_id' => $analysisId,
                        'detection_counts' => $jsonResult['counts'] ?? [],
                        'classes_detected' => $jsonResult['classes'] ?? [],
                        'annotated_video' => $jsonResult['annotated_relpath'] ?? null,
                        'upload_path' => $uploadPath,
                        'results_path' => "{$resultsDir}/{$analysisId}",
                        'frames' => $jsonResult['frames'] ?? null,
                        'model_load_time' => $jsonResult['model_load_time'] ?? null,
                        'inference_time' => $jsonResult['inference_time'] ?? null,
                        'video_processing_time' => $jsonResult['video_processing_time'] ?? null,
                    ]
                ]);
            } else {
                // Enhanced error reporting
                $errorDetails = [
                    'json_found' => $jsonResult ? 'Yes' : 'No',
                    'json_content' => $jsonResult,
                    'total_json_lines' => count($allJsonLines),
                    'last_json_line' => end($allJsonLines) ?: 'None',
                    'raw_output_preview' => substr($result, -1000) // Last 1000 chars
                ];

                Log::error("YOLO detection failed - detailed analysis", $errorDetails);

                return response()->json([
                    'success' => false,
                    'message' => 'YOLO detection failed: ' . ($jsonResult['error'] ?? 'Unknown error'),
                    'debug_output' => $result,
                    'debug_info' => $errorDetails
                ], 500);
            }

        } catch (\Exception $e) {
            Log::error("HawkEye Error: " . $e->getMessage());
            Log::error("Stack trace: " . $e->getTraceAsString());

            return response()->json([
                'success' => false,
                'message' => 'Error: ' . $e->getMessage(),
                'debug_info' => [
                    'file' => $e->getFile(),
                    'line' => $e->getLine()
                ]
            ], 500);
        }
    }

    private function organizeResults($outputDir, $resultsDir, $analysisId)
    {
        try {
            $organizedDir = storage_path("app/{$resultsDir}/{$analysisId}");

            Log::info("Organizing results", [
                'output_dir' => $outputDir,
                'organized_dir' => $organizedDir,
                'analysis_id' => $analysisId
            ]);

            if (is_dir($outputDir)) {
                Log::info("Output directory exists", ['path' => $outputDir]);

                $predDir = $outputDir . '/pred';
                if (is_dir($predDir)) {
                    Log::info("Pred directory found", ['path' => $predDir]);

                    // Create organized directory if it doesn't exist
                    if (!is_dir($organizedDir)) {
                        $created = mkdir($organizedDir, 0755, true);
                        if ($created) {
                            Log::info("Created organized directory", ['path' => $organizedDir]);
                        } else {
                            Log::error("Failed to create organized directory", ['path' => $organizedDir]);
                            throw new \Exception("Failed to create organized directory: {$organizedDir}");
                        }
                    }

                    // Copy pred directory contents
                    $this->copyDirectory($predDir, $organizedDir);
                    Log::info("Successfully copied pred directory contents", [
                        'from' => $predDir,
                        'to' => $organizedDir
                    ]);

                } else {
                    Log::warning("Pred directory not found", ['path' => $predDir]);
                }

                // Clean up temporary output directory
                $this->deleteDirectory($outputDir);
                Log::info("Cleaned up temporary output directory", ['path' => $outputDir]);

            } else {
                Log::warning("Output directory not found", ['path' => $outputDir]);
            }

        } catch (\Exception $e) {
            Log::error("Error in organizeResults", [
                'error' => $e->getMessage(),
                'output_dir' => $outputDir,
                'organized_dir' => $organizedDir ?? 'unknown'
            ]);
            throw $e;
        }
    }

    private function copyDirectory($source, $destination)
    {
        if (!is_dir($destination)) {
            mkdir($destination, 0755, true);
        }

        $dir = opendir($source);
        while (($file = readdir($dir)) !== false) {
            if ($file === '.' || $file === '..') continue;

            $sourcePath = $source . DIRECTORY_SEPARATOR . $file;
            $destPath = $destination . DIRECTORY_SEPARATOR . $file;

            if (is_dir($sourcePath)) {
                $this->copyDirectory($sourcePath, $destPath);
            } else {
                copy($sourcePath, $destPath);
            }
        }
        closedir($dir);
    }

    private function deleteDirectory($dir)
    {
        if (!is_dir($dir)) return;

        $files = array_diff(scandir($dir), ['.', '..']);
        foreach ($files as $file) {
            $path = $dir . DIRECTORY_SEPARATOR . $file;
            if (is_dir($path)) {
                $this->deleteDirectory($path);
            } else {
                unlink($path);
            }
        }
        rmdir($dir);
    }

    public function getAnalysisResults($analysisId)
    {
        $resultsPath = "hawk-eye/result_videos/{$analysisId}";

        if (!Storage::exists($resultsPath)) {
            return response()->json([
                'success' => false,
                'message' => 'Analysis results not found'
            ], 404);
        }

        $files = Storage::files($resultsPath);
        $annotatedVideo = null;
        foreach ($files as $file) {
            if (in_array(strtolower(pathinfo($file, PATHINFO_EXTENSION)), ['mp4', 'avi', 'mov'])) {
                $annotatedVideo = $file;
                break;
            }
        }

        return response()->json([
            'success' => true,
            'data' => [
                'analysis_id' => $analysisId,
                'annotated_video' => $annotatedVideo ? Storage::url($annotatedVideo) : null,
                'all_files' => $files
            ]
        ]);
    }

    public function processTestingClip()
    {
        try {
            set_time_limit(900);

            $videoPath = base_path('testingclip.mp4');
            if (!file_exists($videoPath)) {
                throw new \Exception("Testing clip not found at: " . $videoPath);
            }

            $resultsDir = 'hawk-eye/result_videos';
            $analysisId = 'testing_' . time() . '_' . uniqid();
            $outputDir = storage_path("app" . DIRECTORY_SEPARATOR . str_replace('/', DIRECTORY_SEPARATOR, $resultsDir) . DIRECTORY_SEPARATOR . $analysisId);

            $fullResultsDir = storage_path('app' . DIRECTORY_SEPARATOR . str_replace('/', DIRECTORY_SEPARATOR, $resultsDir));
            if (!is_dir($fullResultsDir)) {
                mkdir($fullResultsDir, 0755, true);
            }

            $pythonScript = base_path('../Hawk-Eye/cricket-hawk-eye/yolo-model/detect_ball.py');
            if (!file_exists($pythonScript)) {
                $pythonScript = base_path('../../Hawk-Eye/cricket-hawk-eye/yolo-model/detect_ball.py');
            }
            if (!file_exists($pythonScript)) {
                $pythonScript = 'G:/Projects/CricketAnalysis-EB/Hawk-Eye/cricket-hawk-eye/yolo-model/detect_ball.py';
            }
            if (!file_exists($pythonScript)) {
                throw new \Exception("Python script not found at: " . $pythonScript);
            }

            // optional smoke: test --help
            $helpCmd = 'cmd /C set PYTHONUNBUFFERED=1 && "' . $this->getPythonExe() . '" "' . $pythonScript . '" --help';
            $helpOut = shell_exec($helpCmd . ' 2>&1');
            Log::info("detect_ball.py --help -> " . substr($helpOut ?? '', 0, 1000));

            $cmd = $this->buildPythonCommand($pythonScript, $videoPath, $outputDir);
            Log::info("Processing testing clip with command: " . $cmd);

            $t0 = microtime(true);
            $result = shell_exec($cmd . " 2>&1");
            $elapsed = round(microtime(true) - $t0, 2);
            Log::info("YOLO processing completed in {$elapsed} seconds");
            Log::info("Python script output (first 5k): " . substr($result ?? '', 0, 5000));

            // Additional output analysis
            $outputLength = strlen($result ?? '');
            $lineCount = substr_count($result ?? '', "\n");
            Log::info("Python output analysis", [
                'total_length' => $outputLength,
                'line_count' => $lineCount,
                'last_1000_chars' => substr($result ?? '', -1000),
                'processing_time' => $elapsed
            ]);

            if ($result === null) {
                throw new \Exception("Python script execution failed - no output returned");
            }

            // Enhanced JSON parsing logic
            $lines = preg_split('/\r\n|\r|\n/', trim($result));
            $jsonResult = null;
            $allJsonLines = [];

            // Collect all JSON lines for debugging
            foreach ($lines as $lineNum => $line) {
                $line = trim($line);
                if ($line !== '' && $line[0] === '{') {
                    $decoded = json_decode($line, true);
                    if (is_array($decoded)) {
                        $allJsonLines[] = [
                            'line_number' => $lineNum + 1,
                            'content' => $decoded
                        ];

                        // Look for the final success result (last complete JSON)
                        if (isset($decoded['success']) && $decoded['success'] === true) {
                            $jsonResult = $decoded;
                            Log::info("Found successful JSON result at line " . ($lineNum + 1), $decoded);
                            break;
                        }
                    }
                }
            }

            // If no success found, try to find any valid JSON with success=true
            if (!$jsonResult) {
                foreach (array_reverse($allJsonLines) as $jsonLine) {
                    if (isset($jsonLine['content']['success']) && $jsonLine['content']['success'] === true) {
                        $jsonResult = $jsonLine['content'];
                        Log::info("Found successful JSON result in reverse search at line " . $jsonLine['line_number'], $jsonLine['content']);
                        break;
                    }
                }
            }

            // Log all JSON lines found for debugging
            Log::info("All JSON lines found: " . count($allJsonLines), $allJsonLines);

            if ($jsonResult && !empty($jsonResult['success'])) {
                // Log before organizing results
                Log::info("About to organize results", [
                    'output_dir' => $outputDir,
                    'analysis_id' => $analysisId,
                    'results_dir' => $resultsDir
                ]);

                // Check if output directory exists before organizing
                if (is_dir($outputDir)) {
                    Log::info("Output directory exists before organizing", [
                        'path' => $outputDir,
                        'contents' => scandir($outputDir)
                    ]);
                } else {
                    Log::warning("Output directory does not exist before organizing", ['path' => $outputDir]);
                }

                $this->organizeResults($outputDir, $resultsDir, $analysisId);

                // Log successful processing summary
                Log::info("Testing clip processing completed successfully", [
                    'analysis_id' => $analysisId,
                    'frames_processed' => $jsonResult['frames'] ?? 'Unknown',
                    'detection_counts' => $jsonResult['counts'] ?? [],
                    'processing_time' => $jsonResult['video_processing_time'] ?? $elapsed,
                    'total_time' => $elapsed,
                    'output_directory' => $outputDir
                ]);

                return response()->json([
                    'success' => true,
                    'message' => 'Testing clip analysis completed successfully!',
                    'data' => [
                        'analysis_id' => $analysisId,
                        'detection_counts' => $jsonResult['counts'] ?? [],
                        'classes_detected' => $jsonResult['classes'] ?? [],
                        'annotated_video' => $jsonResult['annotated_relpath'] ?? null,
                        'input_video' => $videoPath,
                        'results_path' => "{$resultsDir}/{$analysisId}",
                        'frames' => $jsonResult['frames'] ?? null,
                        'model_load_time' => $jsonResult['model_load_time'] ?? null,
                        'inference_time' => $jsonResult['inference_time'] ?? null,
                        'video_processing_time' => $jsonResult['video_processing_time'] ?? null,
                    ]
                ]);
            } else {
                // Enhanced error reporting
                $errorDetails = [
                    'json_found' => $jsonResult ? 'Yes' : 'No',
                    'json_content' => $jsonResult,
                    'total_json_lines' => count($allJsonLines),
                    'last_json_line' => end($allJsonLines) ?: 'None',
                    'raw_output_preview' => substr($result, -1000) // Last 1000 chars
                ];

                Log::error("YOLO detection failed - detailed analysis", $errorDetails);

                return response()->json([
                    'success' => false,
                    'message' => 'YOLO detection failed: ' . ($jsonResult['error'] ?? 'Unknown error'),
                    'debug_output' => $result,
                    'debug_info' => $errorDetails
                ], 500);
            }

        } catch (\Exception $e) {
            Log::error("Testing Clip Processing Error: " . $e->getMessage());
            Log::error("Stack trace: " . $e->getTraceAsString());

            return response()->json([
                'success' => false,
                'message' => 'Error: ' . $e->getMessage(),
                'debug_info' => [
                    'file' => $e->getFile(),
                    'line' => $e->getLine()
                ]
            ], 500);
        }
    }
}
