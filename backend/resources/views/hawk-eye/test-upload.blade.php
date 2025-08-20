<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="csrf-token" content="{{ csrf_token() }}">
    <title>Hawk-Eye Video Testing</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://unpkg.com/vue@3/dist/vue.global.js"></script>
</head>
<body class="bg-gray-100 min-h-screen">
    <div id="app" class="container mx-auto px-4 py-8">
        <!-- Header -->
        <div class="text-center mb-8">
            <h1 class="text-4xl font-bold text-gray-800 mb-2">🏏 Hawk-Eye AI Testing</h1>
            <p class="text-gray-600">Upload cricket video for ball detection analysis</p>
        </div>

        <!-- Upload Section -->
        <div class="bg-white rounded-lg shadow-lg p-6 mb-6">
            <h2 class="text-2xl font-semibold mb-4 text-gray-700">🎥 Video Upload</h2>

            <form @submit.prevent="uploadVideo" class="space-y-4">
                <div class="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center hover:border-blue-400 transition-colors">
                    <input
                        type="file"
                        ref="fileInput"
                        @change="handleFileSelect"
                        accept="video/*"
                        class="hidden"
                        id="videoFile"
                    >
                    <label for="videoFile" class="cursor-pointer">
                        <div class="text-6xl mb-4">🎥</div>
                        <p class="text-lg text-gray-600 mb-2">
                            <span class="text-blue-600 font-semibold">Click to upload</span> or drag and drop
                        </p>
                        <p class="text-sm text-gray-500">MP4, AVI, MOV up to 100MB</p>
                    </label>
                </div>

                <div v-if="selectedFile" class="bg-blue-50 p-4 rounded-lg">
                    <p class="text-blue-800">
                        <strong>Selected:</strong> <span v-text="selectedFile.name"></span>
                        (<span v-text="(selectedFile.size / 1024 / 1024).toFixed(2)"></span> MB)
                    </p>
                </div>

                <button
                    type="submit"
                    :disabled="!selectedFile || uploading"
                    class="w-full bg-blue-600 text-white py-3 px-6 rounded-lg font-semibold hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
                >
                    <span v-if="uploading">🔄 Processing...</span>
                    <span v-else>🚀 Analyze Video</span>
                </button>
            </form>
        </div>

        <!-- Testing Clip Section -->
        <div class="bg-white rounded-lg shadow-lg p-6 mb-6">
            <h2 class="text-2xl font-semibold mb-4 text-gray-700">🧪 Testing Clip Processing</h2>
            <p class="text-gray-600 mb-4">Process the testingclip.mp4 file directly from the backend folder</p>

            <button
                @click="processTestingClip"
                :disabled="processingTestingClip"
                class="w-full bg-green-600 text-white py-3 px-6 rounded-lg font-semibold hover:bg-green-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
            >
                <span v-if="processingTestingClip">🔄 Processing Testing Clip...</span>
                <span v-else>🎬 Process Testing Clip</span>
            </button>
        </div>

        <!-- Video Player Section -->
        <div v-if="videoUrl" class="bg-white rounded-lg shadow-lg p-6 mb-6">
            <h2 class="text-2xl font-semibold mb-4 text-gray-700"> Video Player</h2>
            <video
                :src="videoUrl"
                controls
                class="w-full rounded-lg shadow-md"
                preload="metadata"
            >
                Your browser does not support the video tag.
            </video>
        </div>

        <!-- Results Section -->
        <div v-if="analysisResult" class="bg-white rounded-lg shadow-lg p-6">
            <h2 class="text-2xl font-semibold mb-4 text-gray-700"> Analysis Results</h2>
            <div class="bg-green-50 p-4 rounded-lg">
                <pre class="text-sm text-green-800 whitespace-pre-wrap" v-text="analysisResult"></pre>
            </div>
        </div>

        <!-- Error Section -->
        <div v-if="error" class="bg-red-50 p-4 rounded-lg mt-4">
            <p class="text-red-800" v-text="error"></p>
        </div>
    </div>

    <script>
        const { createApp } = Vue;

        createApp({
            data() {
                return {
                    selectedFile: null,
                    videoUrl: null,
                    uploading: false,
                    analysisResult: null,
                    error: null,
                    processingTestingClip: false
                }
            },
            methods: {
                handleFileSelect(event) {
                    const file = event.target.files[0];
                    if (file && file.type.startsWith('video/')) {
                        this.selectedFile = file;
                        this.videoUrl = URL.createObjectURL(file);
                        this.error = null;
                        this.analysisResult = null;
                    } else {
                        this.error = 'Please select a valid video file.';
                        this.selectedFile = null;
                        this.videoUrl = null;
                    }
                },
                async uploadVideo() {
                    if (!this.selectedFile) return;

                    this.uploading = true;
                    this.error = null;
                    this.analysisResult = null;

                    const formData = new FormData();
                    formData.append('video', this.selectedFile);

                    try {
                        const response = await fetch('/testUpload', {
                            method: 'POST',
                            body: formData,
                            headers: {
                                'X-CSRF-TOKEN': document.querySelector('meta[name="csrf-token"]').getAttribute('content')
                            }
                        });

                        const result = await response.json();

                        if (response.ok) {
                            this.analysisResult = result.message || 'Analysis completed successfully!';
                        } else {
                            this.error = result.message || 'Analysis failed. Please try again.';
                        }
                    } catch (err) {
                        this.error = 'Network error. Please check your connection.';
                    } finally {
                        this.uploading = false;
                    }
                },
                async processTestingClip() {
                    this.processingTestingClip = true;
                    this.error = null;
                    this.analysisResult = null;

                    try {
                        const response = await fetch('/processTestingClip', {
                            method: 'POST',
                            headers: {
                                'X-CSRF-TOKEN': document.querySelector('meta[name="csrf-token"]').getAttribute('content')
                            }
                        });

                        const result = await response.json();

                        if (response.ok) {
                            this.analysisResult = result.message || 'Testing clip processed successfully!';
                        } else {
                            this.error = result.message || 'Failed to process testing clip.';
                        }
                    } catch (err) {
                        this.error = 'Network error. Please check your connection.';
                    } finally {
                        this.processingTestingClip = false;
                    }
                }
            }
        }).mount('#app');
    </script>
</body>
</html>
