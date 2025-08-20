<?php
/**
 * Test runner for Hawk-Eye video detection.
 * Place this file in: G:\Projects\CricketAnalysis-EB\backend\test_testing_clip.php
 * Run: php test_testing_clip.php
 *
 * Modes:
 *  - "laravel" (default): uses HawkEyeController::processTestingClip()
 *  - "direct" : runs detect_ball.py directly with streaming output (useful for debugging)
 */

// ------------------------ USER CONFIG ------------------------
$MODE = 'laravel'; // "laravel" or "direct"

// Match your earlier setup:
$PYTHON_EXE = 'C:\\Users\\haris\\AppData\\Local\\Programs\\Python\\Python313\\python.exe'; // system Python 3.13 with all packages
$PY_SCRIPT  = 'G:\\Projects\\CricketAnalysis-EB\\Hawk-Eye\\cricket-hawk-eye\\yolo-model\\detect_ball.py';
$VIDEO_PATH = 'G:\\Projects\\CricketAnalysis-EB\\backend\\testingclip.mp4';
$OUT_DIR    = 'G:\\Projects\\CricketAnalysis-EB\\backend\\storage\\app\\hawk-eye\\result_videos\\manual_test';

// ------------------------ ENHANCED LOGGING ------------------------
$LOG_LEVEL = 'DEBUG'; // 'INFO', 'DEBUG', 'VERBOSE'
$START_TIME = microtime(true);

function logMessage($level, $message, $data = null) {
    global $LOG_LEVEL, $START_TIME;

    $levels = ['INFO' => 1, 'DEBUG' => 2, 'VERBOSE' => 3];
    $currentLevel = $levels[$LOG_LEVEL] ?? 1;
    $requestedLevel = $levels[$level] ?? 1;

    if ($requestedLevel <= $currentLevel) {
        $elapsed = round(microtime(true) - $START_TIME, 3);
        $timestamp = date('H:i:s');
        $memory = formatBytes(memory_get_usage(true));

        echo "[{$timestamp}] [{$level}] [{$elapsed}s] [{$memory}] {$message}\n";

        if ($data !== null) {
            if (is_array($data) || is_object($data)) {
                echo "   📊 Data: " . json_encode($data, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES) . "\n";
            } else {
                echo "   📊 Data: {$data}\n";
            }
        }
    }
}

function logStep($stepNumber, $stepName, $details = '') {
    logMessage('INFO', "🔄 STEP {$stepNumber}: {$stepName}");
    if ($details) {
        logMessage('DEBUG', "   📝 {$details}");
    }
}

function logSuccess($message, $data = null) {
    logMessage('INFO', "✅ SUCCESS: {$message}", $data);
}

function logError($message, $error = null) {
    logMessage('INFO', "❌ ERROR: {$message}", $error);
}

function logWarning($message, $data = null) {
    logMessage('INFO', "⚠️  WARNING: {$message}", $data);
}

function logInfo($message, $data = null) {
    logMessage('INFO', "ℹ️  {$message}", $data);
}

function logDebug($message, $data = null) {
    logMessage('DEBUG', "🔍 DEBUG: {$message}", $data);
}

function logVerbose($message, $data = null) {
    logMessage('VERBOSE', "🔬 VERBOSE: {$message}", $data);
}

// -------------------------------------------------------------

// ------------------------ UTILITIES --------------------------
function getSystemResources() {
    $memory = memory_get_usage(true);
    $memoryPeak = memory_get_peak_usage(true);
    $diskFree = @disk_free_space('.');
    $diskTotal = @disk_total_space('.');
    $diskUsed = $diskTotal !== false && $diskFree !== false ? ($diskTotal - $diskFree) : 0;

    // CPU info (Windows)
    $cpuInfo = [];
    if (function_exists('shell_exec')) {
        $cpuOutput = @shell_exec('wmic cpu get name /value 2>nul');
        if ($cpuOutput) {
            $cpuInfo['name'] = trim(explode('=', $cpuOutput)[1] ?? 'Unknown');
        }
    }

    return [
        'memory_current' => $memory,
        'memory_peak' => $memoryPeak,
        'disk_free' => $diskFree ?: 0,
        'disk_total' => $diskTotal ?: 0,
        'disk_used' => $diskUsed,
        'cpu_info' => $cpuInfo,
        'php_version' => PHP_VERSION,
        'php_extensions' => get_loaded_extensions(),
        'os_info' => php_uname()
    ];
}

function formatBytes($bytes, $precision = 2) {
    $units = ['B','KB','MB','GB','TB'];
    $i = 0;
    while ($bytes > 1024 && $i < count($units)-1) {
        $bytes /= 1024;
        $i++;
    }
    return round($bytes, $precision) . ' ' . $units[$i];
}

function logSystemStatus($step, $info = '') {
    $r = getSystemResources();
    logInfo("📊 SYSTEM STATUS - {$step}");
    logDebug("   💾 Memory Usage: " . formatBytes($r['memory_current']) . " (Peak: " . formatBytes($r['memory_peak']) . ")");
    if ($r['disk_total'] > 0) {
        logDebug("   💿 Disk Usage: " . formatBytes($r['disk_used']) . " / " . formatBytes($r['disk_total']) . " (Free: " . formatBytes($r['disk_free']) . ")");
    }
    if (!empty($r['cpu_info']['name'])) {
        logDebug("   🖥️  CPU: " . $r['cpu_info']['name']);
    }
    logDebug("   🐘 PHP Version: " . $r['php_version']);
    logDebug("   🕐 Timestamp: " . date('Y-m-d H:i:s'));
    if ($info) logDebug("   ℹ️  {$info}");
}

function ensureDir($dir) {
    if (!is_dir($dir)) {
        $result = @mkdir($dir, 0755, true);
        if ($result) {
            logDebug("📁 Directory created: {$dir}");
        } else {
            logWarning("📁 Failed to create directory: {$dir}");
        }
        return $result;
    }
    logDebug("📁 Directory exists: {$dir}");
    return true;
}

function checkFileExists($filePath, $description = '') {
    $exists = file_exists($filePath);
    $size = $exists ? filesize($filePath) : 0;
    $modified = $exists ? filemtime($filePath) : 0;

    if ($exists) {
        logSuccess("📄 File found: {$description}", [
            'path' => $filePath,
            'size' => formatBytes($size),
            'modified' => date('Y-m-d H:i:s', $modified),
            'permissions' => substr(sprintf('%o', fileperms($filePath)), -4)
        ]);
    } else {
        logError("📄 File NOT found: {$description}", [
            'path' => $filePath,
            'reason' => 'File does not exist or path is incorrect'
        ]);
    }

    return $exists;
}

function validateEnvironment() {
    logStep(0, "Environment Validation", "Checking system requirements");

    // Check PHP version
    if (version_compare(PHP_VERSION, '8.0.0', '<')) {
        logError("PHP version too old", ['current' => PHP_VERSION, 'required' => '8.0.0+']);
        return false;
    }
    logSuccess("PHP version OK", ['version' => PHP_VERSION]);

    // Check required extensions
    $requiredExtensions = ['json', 'fileinfo', 'curl'];
    foreach ($requiredExtensions as $ext) {
        if (!extension_loaded($ext)) {
            logError("Required PHP extension missing", ['extension' => $ext]);
            return false;
        }
    }
    logSuccess("Required PHP extensions OK", ['extensions' => $requiredExtensions]);

    // Check Python executable
    if (!file_exists($GLOBALS['PYTHON_EXE'])) {
        logError("Python executable not found", ['path' => $GLOBALS['PYTHON_EXE']]);
        return false;
    }
    logSuccess("Python executable found", ['path' => $GLOBALS['PYTHON_EXE']]);

    // Check Python script
    if (!file_exists($GLOBALS['PY_SCRIPT'])) {
        logError("Python script not found", ['path' => $GLOBALS['PY_SCRIPT']]);
        return false;
    }
    logSuccess("Python script found", ['path' => $GLOBALS['PY_SCRIPT']]);

    // Check video file
    if (!file_exists($GLOBALS['VIDEO_PATH'])) {
        logError("Video file not found", ['path' => $GLOBALS['VIDEO_PATH']]);
        return false;
    }
    logSuccess("Video file found", ['path' => $GLOBALS['VIDEO_PATH']]);

    return true;
}
// -------------------------------------------------------------

logInfo("🚀 Starting test_testing_clip.php with enhanced logging");
logInfo("📋 Configuration", [
    'mode' => $MODE,
    'python_exe' => $PYTHON_EXE,
    'python_script' => $PY_SCRIPT,
    'video_path' => $VIDEO_PATH,
    'output_dir' => $OUT_DIR,
    'log_level' => $LOG_LEVEL
]);

logSystemStatus("Script Start");

// Validate environment first
if (!validateEnvironment()) {
    logError("Environment validation failed - exiting");
    exit(1);
}

if (!file_exists($VIDEO_PATH)) {
    logError("testingclip not found at specified path", ['path' => $VIDEO_PATH]);
    exit(1);
}

// -------------------- DIRECT MODE (streaming) ----------------
if ($MODE === 'direct') {
    logStep(1, "Direct Python Mode", "Running Python script directly with streaming output");

    ensureDir($OUT_DIR);

    // env + command; prefer FFMPEG + unbuffered python
    $envPrefix = 'set PYTHONUNBUFFERED=1 && set OPENCV_VIDEOIO_PRIORITY_MSMF=0 && set KMP_DUPLICATE_LIB_OK=TRUE';
    $cmd = 'cmd /C ' . $envPrefix . ' && "' . $PYTHON_EXE . '" "' . $PY_SCRIPT . '" ' .
           '--video "' . $VIDEO_PATH . '" --out "' . $OUT_DIR . '" ' .
           '--conf 0.25 --iou 0.7 --device cpu';

    logInfo("▶️  Running Python command", ['command' => $cmd]);

    // Use proc_open for live output
    $descriptorspec = [
        0 => ["pipe", "r"],   // stdin
        1 => ["pipe", "w"],   // stdout
        2 => ["pipe", "w"],   // stderr
    ];

    logDebug("Starting process with proc_open");
    $process = proc_open($cmd, $descriptorspec, $pipes, __DIR__);

    if (!is_resource($process)) {
        logError("Failed to start process with proc_open");
        exit(1);
    }
    logSuccess("Process started successfully", ['pid' => proc_get_status($process)['pid'] ?? 'unknown']);

    // Non-blocking streams
    stream_set_blocking($pipes[1], false);
    stream_set_blocking($pipes[2], false);

    $start = microtime(true);
    $buffer = '';
    $lastJson = null;
    $lineCount = 0;
    $lastProgress = 0;

    logInfo("⏱️  Streaming output started (Ctrl+C to stop)");

    while (true) {
        $status = proc_get_status($process);
        $out = stream_get_contents($pipes[1]);
        $err = stream_get_contents($pipes[2]);

        if ($out !== false && $out !== '') {
            echo $out;
            $buffer .= $out;
            $lineCount += substr_count($out, "\n");

            // Log progress every 50 lines
            if ($lineCount - $lastProgress >= 50) {
                logDebug("Progress update", ['lines_processed' => $lineCount, 'buffer_size' => formatBytes(strlen($buffer))]);
                $lastProgress = $lineCount;
            }
        }

        if ($err !== false && $err !== '') {
            // print stderr too (sometimes OpenCV logs go here)
            echo $err;
            $buffer .= $err;
            logWarning("Python stderr output", ['error' => trim($err)]);
        }

        if (!$status['running']) {
            logInfo("Process stopped running", ['exit_code' => $status['exitcode'] ?? 'unknown']);
            break;
        }

        usleep(50000); // 50ms delay
    }

    // Clean up
    foreach ($pipes as $p) {
        if (is_resource($p)) fclose($p);
    }
    $exitCode = proc_close($process);

    logInfo("🔚 Process cleanup completed", ['exit_code' => $exitCode, 'total_lines' => $lineCount]);

    // Try to find the last JSON line
    $lines = preg_split('/\r\n|\r|\n/', trim($buffer));
    foreach (array_reverse($lines) as $line) {
        $line = trim($line);
        if ($line !== '' && $line[0] === '{') {
            $lastJson = json_decode($line, true);
            if (is_array($lastJson)) {
                logDebug("Found JSON output", ['json' => $lastJson]);
                break;
            }
        }
    }

    $elapsed = round(microtime(true) - $start, 2);

    if ($lastJson && !empty($lastJson['success'])) {
        logSuccess("Direct mode completed successfully", [
            'frames' => $lastJson['frames'] ?? '?',
            'fps' => $lastJson['fps'] ?? '?',
            'counts' => $lastJson['counts'] ?? [],
            'output' => $OUT_DIR . DIRECTORY_SEPARATOR . ($lastJson['annotated_relpath'] ?? 'pred/annotated.mp4'),
            'processing_time' => $lastJson['video_processing_time'] ?? $elapsed,
            'total_time' => $elapsed
        ]);
    } else {
        logError("Direct mode failed", [
            'json_output' => $lastJson,
            'error' => $lastJson['error'] ?? 'Could not parse JSON from output',
            'total_time' => $elapsed
        ]);
    }

    logSystemStatus("Direct Mode End");
    exit(0);
}

// -------------------- LARAVEL MODE (default) -----------------
logStep(1, "Laravel Mode", "Bootstrapping Laravel framework and using HawkEyeController");

logSystemStatus("Laravel Bootstrap Start");

try {
    logDebug("Loading Composer autoloader");
    require_once __DIR__ . '/vendor/autoload.php';
    logSuccess("Composer autoloader loaded");

    logDebug("Loading Laravel bootstrap/app.php");
    /** @var \Illuminate\Foundation\Application $app */
    $app = require_once __DIR__ . '/bootstrap/app.php';
    logSuccess("Laravel app instance created");

    logDebug("Booting Laravel kernel");
    $app->make('Illuminate\Contracts\Console\Kernel')->bootstrap();
    logSuccess("Laravel kernel bootstrapped successfully");

} catch (Throwable $e) {
    logError("Laravel bootstrap failed", [
        'error' => $e->getMessage(),
        'file' => $e->getFile(),
        'line' => $e->getLine()
    ]);
    exit(1);
}

logSystemStatus("Laravel Bootstrap Complete", "Laravel framework loaded successfully");

use App\Http\Controllers\HawkEye\HawkEyeController;
use Illuminate\Http\Request;

try {
    logStep(2, "Controller Initialization", "Creating and setting up HawkEyeController");

    $controller = new HawkEyeController();
    logSuccess("HawkEyeController created successfully", [
        'class' => get_class($controller),
        'methods' => get_class_methods($controller)
    ]);

    logStep(3, "Video Validation", "Checking test video file");

    $videoRealPath = realpath($VIDEO_PATH);
    if (!$videoRealPath) {
        logError("Could not resolve real path for video file", ['path' => $VIDEO_PATH]);
        exit(1);
    }

    $videoStats = [
        'real_path' => $videoRealPath,
        'size' => formatBytes(filesize($VIDEO_PATH)),
        'modified' => date('Y-m-d H:i:s', filemtime($VIDEO_PATH)),
        'permissions' => substr(sprintf('%o', fileperms($VIDEO_PATH)), -4),
        'readable' => is_readable($VIDEO_PATH) ? 'Yes' : 'No',
        'writable' => is_writable($VIDEO_PATH) ? 'Yes' : 'No'
    ];

    logSuccess("Video file validated", $videoStats);

    logStep(4, "YOLO Processing", "Calling processTestingClip() method");
    logSystemStatus("Pre-YOLO", "About to start video processing");

    $t0 = microtime(true);

    logDebug("Calling controller->processTestingClip()");
    /** @var \Illuminate\Http\JsonResponse $response */
    $response = $controller->processTestingClip();
    $elapsed = round(microtime(true) - $t0, 2);

    logSuccess("Controller method completed", [
        'response_time' => $elapsed . 's',
        'response_status' => $response->getStatusCode(),
        'response_headers' => $response->headers->all()
    ]);

    $payload = json_decode($response->getContent(), true);

    if (json_last_error() !== JSON_ERROR_NONE) {
        logError("Failed to decode JSON response", [
            'json_error' => json_last_error_msg(),
            'raw_content' => substr($response->getContent(), 0, 500) . '...'
        ]);
        exit(1);
    }

    logDebug("Response payload decoded", ['payload_keys' => array_keys($payload)]);

    if (!empty($payload['success'])) {
        logSuccess("Video processing completed successfully", [
            'analysis_id' => $payload['data']['analysis_id'] ?? '?',
            'frames' => $payload['data']['frames'] ?? '?',
            'detection_counts' => $payload['data']['detection_counts'] ?? [],
            'results_path' => $payload['data']['results_path'] ?? '?',
            'annotated_video' => $payload['data']['annotated_video'] ?? 'N/A'
        ]);

        // Show files in results folder
        $resultsAbs = __DIR__ . DIRECTORY_SEPARATOR . 'storage' . DIRECTORY_SEPARATOR . 'app' . DIRECTORY_SEPARATOR . str_replace('/', DIRECTORY_SEPARATOR, $payload['data']['results_path'] ?? '');

        if (is_dir($resultsAbs)) {
            logInfo("📂 Results directory contents");
            $files = scandir($resultsAbs);
            $totalSize = 0;
            $fileCount = 0;

            foreach ($files as $f) {
                if ($f === '.' || $f === '..') continue;
                $fp = $resultsAbs . DIRECTORY_SEPARATOR . $f;
                $sz = is_file($fp) ? filesize($fp) : 0;
                $totalSize += $sz;
                $fileCount++;

                logDebug("   File: {$f}", [
                    'type' => is_file($fp) ? 'FILE' : 'DIR',
                    'size' => is_file($fp) ? formatBytes($sz) : 'N/A',
                    'modified' => is_file($fp) ? date('Y-m-d H:i:s', filemtime($fp)) : 'N/A'
                ]);
            }

            logSuccess("Results summary", [
                'total_files' => $fileCount,
                'total_size' => formatBytes($totalSize),
                'results_path' => $resultsAbs
            ]);
        } else {
            logWarning("Results directory not found", ['path' => $resultsAbs]);
        }

    } else {
        logError("Video processing failed", [
            'message' => $payload['message'] ?? 'Unknown error',
            'success' => $payload['success'] ?? false
        ]);

        if (!empty($payload['debug_output'])) {
            logDebug("Debug output from controller", ['debug_output' => $payload['debug_output']]);
        }

        if (!empty($payload['debug_info'])) {
            logDebug("Debug info from controller", ['debug_info' => $payload['debug_info']]);
        }
    }

} catch (Throwable $e) {
    logError("Fatal error during processing", [
        'error' => $e->getMessage(),
        'file' => $e->getFile(),
        'line' => $e->getLine(),
        'trace' => $e->getTraceAsString()
    ]);
}

logSystemStatus("Script Completion", "Final system state");
logInfo("✨ Test completed", [
    'total_time' => round(microtime(true) - $START_TIME, 2) . 's',
    'completion_time' => date('Y-m-d H:i:s')
]);
