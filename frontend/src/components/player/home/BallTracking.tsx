"use client"

import { useState, useRef } from "react"
import {
  Upload,
  Play,
  Eye,
  Trash2,
  Calendar,
  Clock,
  Target,
  Zap,
  Activity,
  TrendingUp,
  Download,
  Maximize2,
} from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog"
import { motion, AnimatePresence } from "framer-motion"

export const BallTracking = () => {
  const [uploadedFiles, setUploadedFiles] = useState([])
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [analysisProgress, setAnalysisProgress] = useState(0)
  const [selectedFile, setSelectedFile] = useState(null)
  const [selectedAnalysis, setSelectedAnalysis] = useState(null)
  const [isDragOver, setIsDragOver] = useState(false)
  const fileInputRef = useRef(null)

  const [analysisHistory] = useState([
    {
      id: 1,
      fileName: "match_highlights_01.mp4",
      uploadDate: "2024-01-15",
      uploadTime: "14:30",
      ballSpeed: "145.2 km/h",
      deliveryAngle: "12.5°",
      bounceLocation: "Good Length",
      pitchZone: "Off Stump",
      playerInvolved: "Kane Williamson",
      ballType: "Fast Ball",
      spinRate: "2,340 RPM",
      trajectory: "Rising",
      thumbnail: "/placeholder.svg?height=120&width=200&text=Video+Thumbnail",
      status: "completed",
      frameCount: 240,
      duration: "8.2s",
    },
    {
      id: 2,
      fileName: "training_session_02.mp4",
      uploadDate: "2024-01-14",
      uploadTime: "10:15",
      ballSpeed: "138.7 km/h",
      deliveryAngle: "8.3°",
      bounceLocation: "Short Length",
      pitchZone: "Middle Stump",
      playerInvolved: "Training Partner",
      ballType: "Medium Pace",
      spinRate: "1,890 RPM",
      trajectory: "Straight",
      thumbnail: "/placeholder.svg?height=120&width=200&text=Training+Video",
      status: "completed",
      frameCount: 180,
      duration: "6.1s",
    },
    {
      id: 3,
      fileName: "practice_drill_03.mp4",
      uploadDate: "2024-01-13",
      uploadTime: "16:45",
      ballSpeed: "152.1 km/h",
      deliveryAngle: "15.2°",
      bounceLocation: "Full Length",
      pitchZone: "Leg Stump",
      playerInvolved: "Coach",
      ballType: "Fast Ball",
      spinRate: "2,680 RPM",
      trajectory: "Swinging",
      thumbnail: "/placeholder.svg?height=120&width=200&text=Practice+Drill",
      status: "completed",
      frameCount: 300,
      duration: "10.5s",
    },
  ])

  const handleDragOver = (e) => {
    e.preventDefault()
    setIsDragOver(true)
  }

  const handleDragLeave = (e) => {
    e.preventDefault()
    setIsDragOver(false)
  }

  const handleDrop = (e) => {
    e.preventDefault()
    setIsDragOver(false)
    const files = Array.from(e.dataTransfer.files)
    processFiles(files)
  }

  const handleFileUpload = (event) => {
    const files = Array.from(event.target.files)
    processFiles(files)
  }

  const processFiles = (files) => {
    const validFiles = files.filter((file) => {
      const isValidType = file.type.startsWith("video/") || file.type.startsWith("image/")
      const isValidSize = file.size <= (file.type.startsWith("video/") ? 2 * 1024 * 1024 * 1024 : 20 * 1024 * 1024) // 2GB for video, 20MB for image
      return isValidType && isValidSize
    })

    const newFiles = validFiles.map((file) => ({
      id: Date.now() + Math.random(),
      file,
      name: file.name,
      size: file.size,
      type: file.type,
      uploadDate: new Date().toISOString().split("T")[0],
      uploadTime: new Date().toLocaleTimeString("en-US", { hour12: false, hour: "2-digit", minute: "2-digit" }),
      status: "uploaded",
      preview: URL.createObjectURL(file),
    }))

    setUploadedFiles((prev) => [...prev, ...newFiles])
  }

  const handleAnalyze = (fileId) => {
    setIsAnalyzing(true)
    setAnalysisProgress(0)
    setSelectedFile(fileId)

    // Simulate analysis progress
    const interval = setInterval(() => {
      setAnalysisProgress((prev) => {
        if (prev >= 100) {
          clearInterval(interval)
          setIsAnalyzing(false)

          // Update file status
          setUploadedFiles((prev) =>
            prev.map((file) =>
              file.id === fileId
                ? {
                    ...file,
                    status: "analyzed",
                    ballSpeed: `${(Math.random() * 50 + 120).toFixed(1)} km/h`,
                    deliveryAngle: `${(Math.random() * 20 + 5).toFixed(1)}°`,
                    bounceLocation: ["Good Length", "Short Length", "Full Length"][Math.floor(Math.random() * 3)],
                    pitchZone: ["Off Stump", "Middle Stump", "Leg Stump"][Math.floor(Math.random() * 3)],
                    ballType: ["Fast Ball", "Medium Pace", "Spin"][Math.floor(Math.random() * 3)],
                    spinRate: `${Math.floor(Math.random() * 1000 + 1500)} RPM`,
                    trajectory: ["Rising", "Straight", "Swinging"][Math.floor(Math.random() * 3)],
                    frameCount: Math.floor(Math.random() * 200 + 100),
                    duration: `${(Math.random() * 10 + 3).toFixed(1)}s`,
                  }
                : file,
            ),
          )

          return 100
        }
        return prev + Math.random() * 15
      })
    }, 200)
  }

  const handleDeleteFile = (fileId) => {
    setUploadedFiles((prev) => prev.filter((file) => file.id !== fileId))
  }

  const handleViewAnalysis = (analysis) => {
    setSelectedAnalysis(analysis)
  }

  const formatFileSize = (bytes) => {
    if (bytes === 0) return "0 Bytes"
    const k = 1024
    const sizes = ["Bytes", "KB", "MB", "GB"]
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return Number.parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + " " + sizes[i]
  }

  const AnalysisModal = ({ analysis, onClose }) => (
    <DialogContent className="max-w-4xl max-h-[90vh] overflow-y-auto">
      <DialogHeader>
        <DialogTitle className="flex items-center gap-2">
          <Target className="w-5 h-5 text-[#344FA5]" />
          Ball Tracking Analysis - {analysis.fileName || analysis.name}
        </DialogTitle>
      </DialogHeader>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Video/Image Preview */}
        <div className="space-y-4">
          <div className="aspect-video bg-gray-100 rounded-lg overflow-hidden relative">
            <img
              src={analysis.thumbnail || analysis.preview || "/placeholder.svg"}
              alt="Analysis preview"
              className="w-full h-full object-cover"
            />
            <div className="absolute inset-0 bg-black/30 flex items-center justify-center">
              <Button size="lg" className="bg-white/20 backdrop-blur-sm hover:bg-white/30">
                <Play className="w-6 h-6 mr-2" />
                Play Analysis
              </Button>
            </div>
          </div>

          {/* Interactive Timeline */}
          <div className="space-y-2">
            <div className="flex items-center justify-between text-sm text-gray-600">
              <span>Frame Analysis Timeline</span>
              <span>{analysis.duration || "N/A"}</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2 relative">
              <div className="bg-[#344FA5] h-2 rounded-full w-1/3"></div>
              <div className="absolute top-0 left-1/3 w-3 h-3 bg-[#344FA5] rounded-full transform -translate-y-0.5 cursor-pointer"></div>
            </div>
          </div>
        </div>

        {/* Analysis Data */}
        <div className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <Card className="p-4">
              <div className="flex items-center gap-2 mb-2">
                <Zap className="w-4 h-4 text-orange-500" />
                <span className="text-sm font-medium">Ball Speed</span>
              </div>
              <p className="text-2xl font-bold text-[#344FA5]">{analysis.ballSpeed}</p>
            </Card>

            <Card className="p-4">
              <div className="flex items-center gap-2 mb-2">
                <TrendingUp className="w-4 h-4 text-blue-500" />
                <span className="text-sm font-medium">Delivery Angle</span>
              </div>
              <p className="text-2xl font-bold text-[#344FA5]">{analysis.deliveryAngle}</p>
            </Card>

            <Card className="p-4">
              <div className="flex items-center gap-2 mb-2">
                <Target className="w-4 h-4 text-green-500" />
                <span className="text-sm font-medium">Bounce Location</span>
              </div>
              <p className="text-lg font-semibold">{analysis.bounceLocation}</p>
            </Card>

            <Card className="p-4">
              <div className="flex items-center gap-2 mb-2">
                <Activity className="w-4 h-4 text-purple-500" />
                <span className="text-sm font-medium">Pitch Zone</span>
              </div>
              <p className="text-lg font-semibold">{analysis.pitchZone}</p>
            </Card>
          </div>

          {/* Additional Metrics */}
          <div className="space-y-3">
            <div className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
              <span className="text-sm font-medium">Ball Type</span>
              <Badge variant="outline">{analysis.ballType}</Badge>
            </div>
            <div className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
              <span className="text-sm font-medium">Spin Rate</span>
              <span className="font-semibold">{analysis.spinRate || "N/A"}</span>
            </div>
            <div className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
              <span className="text-sm font-medium">Trajectory</span>
              <span className="font-semibold">{analysis.trajectory || "N/A"}</span>
            </div>
            <div className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
              <span className="text-sm font-medium">Player Involved</span>
              <span className="font-semibold">{analysis.playerInvolved || "Current User"}</span>
            </div>
          </div>

          {/* Action Buttons */}
          <div className="flex gap-2 pt-4">
            <Button className="flex-1 bg-[#344FA5] hover:bg-[#2A3F85]">
              <Download className="w-4 h-4 mr-2" />
              Export Report
            </Button>
            <Button variant="outline" className="flex-1 bg-transparent">
              <Maximize2 className="w-4 h-4 mr-2" />
              Full Screen
            </Button>
          </div>
        </div>
      </div>

      {/* Pitch Map */}
      <div className="mt-6">
        <h3 className="text-lg font-semibold mb-4">Pitch Map Visualization</h3>
        <div className="bg-green-100 rounded-lg p-6 relative" style={{ aspectRatio: "22/20" }}>
          <div className="absolute inset-4 border-2 border-white rounded-lg">
            <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-2 h-2 bg-red-500 rounded-full"></div>
            <div className="absolute top-1/4 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-1 h-8 bg-white"></div>
            <div className="absolute bottom-1/4 left-1/2 transform -translate-x-1/2 translate-y-1/2 w-1 h-8 bg-white"></div>
          </div>
          <div className="absolute bottom-2 left-2 text-xs text-gray-600">Ball Landing Zone: {analysis.pitchZone}</div>
        </div>
      </div>
    </DialogContent>
  )

  return (
    <div className="space-y-6 p-4 md:p-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-2xl font-bold text-gray-900">AI Ball Tracking Analysis</h2>
          <p className="text-gray-600">Advanced computer vision for cricket performance insights</p>
        </div>
        <div className="flex items-center gap-2">
          <Badge variant="outline" className="text-green-600 border-green-200">
            <div className="w-2 h-2 bg-green-500 rounded-full mr-2"></div>
            AI Engine Active
          </Badge>
        </div>
      </div>

      {/* Upload Section */}
      <Card className="border-0 shadow-md">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Upload className="w-5 h-5 text-[#344FA5]" />
            Media Upload & Analysis
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div
            className={`border-2 border-dashed rounded-lg p-8 text-center transition-all duration-300 cursor-pointer ${
              isDragOver
                ? "border-[#344FA5] bg-[#344FA5]/5 scale-105"
                : "border-gray-300 hover:border-[#344FA5] hover:bg-gray-50"
            }`}
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
            onClick={() => fileInputRef.current?.click()}
          >
            <motion.div animate={{ y: isDragOver ? -5 : 0 }} transition={{ duration: 0.2 }}>
              <Upload
                className={`w-12 h-12 mx-auto mb-4 transition-colors duration-300 ${
                  isDragOver ? "text-[#344FA5]" : "text-gray-400"
                }`}
              />
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                {isDragOver ? "Drop files here" : "Upload Cricket Media"}
              </h3>
              <p className="text-gray-600 mb-4">Drag and drop your cricket videos or images here, or click to browse</p>
              <Button className="bg-[#344FA5] hover:bg-[#2A3F85]">Choose Files</Button>
              <div className="mt-4 text-xs text-gray-500 space-y-1">
                <p>Supported formats: MP4, MOV, AVI, JPG, PNG</p>
                <p>Max size: 2GB (video), 20MB (image)</p>
              </div>
            </motion.div>
          </div>
          <input
            ref={fileInputRef}
            type="file"
            multiple
            accept="video/*,image/*"
            onChange={handleFileUpload}
            className="hidden"
          />
        </CardContent>
      </Card>

      {/* Analysis Progress */}
      <AnimatePresence>
        {isAnalyzing && (
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -20 }}>
            <Card className="border-0 shadow-md border-l-4 border-l-[#344FA5]">
              <CardContent className="p-6">
                <div className="flex items-center gap-4">
                  <div className="w-12 h-12 bg-[#344FA5]/10 rounded-full flex items-center justify-center">
                    <Target className="w-6 h-6 text-[#344FA5] animate-spin" />
                  </div>
                  <div className="flex-1">
                    <h3 className="font-semibold text-gray-900 mb-2">AI Analysis in Progress...</h3>
                    <Progress value={analysisProgress} className="mb-2" />
                    <p className="text-sm text-gray-600">
                      {analysisProgress < 30 && "Detecting ball trajectory..."}
                      {analysisProgress >= 30 && analysisProgress < 60 && "Analyzing player positioning..."}
                      {analysisProgress >= 60 && analysisProgress < 90 && "Calculating ball metrics..."}
                      {analysisProgress >= 90 && "Finalizing analysis report..."}
                    </p>
                  </div>
                  <div className="text-right">
                    <div className="text-2xl font-bold text-[#344FA5]">{Math.round(analysisProgress)}%</div>
                    <div className="text-xs text-gray-500">Complete</div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Uploaded Files */}
      {uploadedFiles.length > 0 && (
        <Card className="border-0 shadow-md">
          <CardHeader>
            <CardTitle>Recent Uploads</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <AnimatePresence>
                {uploadedFiles.map((file, index) => (
                  <motion.div
                    key={file.id}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -20 }}
                    transition={{ delay: index * 0.1 }}
                    className="flex items-center gap-4 p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors duration-200"
                  >
                    <div className="w-16 h-16 bg-gray-200 rounded-lg overflow-hidden flex-shrink-0">
                      {file.preview ? (
                        <img
                          src={file.preview || "/placeholder.svg"}
                          alt={file.name}
                          className="w-full h-full object-cover"
                        />
                      ) : (
                        <div className="w-full h-full flex items-center justify-center">
                          {file.type?.startsWith("video/") ? (
                            <Play className="w-6 h-6 text-gray-500" />
                          ) : (
                            <Eye className="w-6 h-6 text-gray-500" />
                          )}
                        </div>
                      )}
                    </div>

                    <div className="flex-1 min-w-0">
                      <h4 className="font-medium text-gray-900 truncate">{file.name}</h4>
                      <p className="text-sm text-gray-600">
                        {formatFileSize(file.size)} • {file.uploadDate} at {file.uploadTime}
                      </p>
                      {file.status === "analyzed" && (
                        <div className="flex items-center gap-4 mt-2 text-xs">
                          <span className="flex items-center gap-1">
                            <Zap className="w-3 h-3 text-orange-500" />
                            {file.ballSpeed}
                          </span>
                          <span className="flex items-center gap-1">
                            <Target className="w-3 h-3 text-blue-500" />
                            {file.bounceLocation}
                          </span>
                          <span className="flex items-center gap-1">
                            <Activity className="w-3 h-3 text-green-500" />
                            {file.ballType}
                          </span>
                        </div>
                      )}
                    </div>

                    <div className="flex items-center gap-2">
                      <Badge
                        className={`text-xs ${
                          file.status === "uploaded"
                            ? "bg-blue-100 text-blue-800"
                            : file.status === "analyzed"
                              ? "bg-green-100 text-green-800"
                              : "bg-gray-100 text-gray-800"
                        }`}
                      >
                        {file.status === "uploaded" ? "Ready" : file.status === "analyzed" ? "Analyzed" : "Processing"}
                      </Badge>

                      {file.status === "uploaded" && (
                        <Button
                          size="sm"
                          onClick={() => handleAnalyze(file.id)}
                          className="bg-[#344FA5] hover:bg-[#2A3F85]"
                          disabled={isAnalyzing}
                        >
                          Analyze
                        </Button>
                      )}

                      {file.status === "analyzed" && (
                        <Dialog>
                          <DialogTrigger asChild>
                            <Button size="sm" variant="outline" onClick={() => handleViewAnalysis(file)}>
                              <Eye className="w-4 h-4 mr-1" />
                              View
                            </Button>
                          </DialogTrigger>
                          <AnalysisModal analysis={file} onClose={undefined} />
                        </Dialog>
                      )}

                      <Button
                        size="sm"
                        variant="ghost"
                        onClick={() => handleDeleteFile(file.id)}
                        className="text-red-600 hover:text-red-700 hover:bg-red-50"
                      >
                        <Trash2 className="w-4 h-4" />
                      </Button>
                    </div>
                  </motion.div>
                ))}
              </AnimatePresence>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Analysis History */}
      <Card className="border-0 shadow-md">
        <CardHeader>
          <CardTitle>Analysis History</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {analysisHistory.map((analysis, index) => (
              <motion.div
                key={analysis.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
                className="bg-white border border-gray-200 rounded-lg overflow-hidden hover:shadow-md transition-shadow duration-300"
              >
                <div className="aspect-video bg-gray-100 relative">
                  <img
                    src={analysis.thumbnail || "/placeholder.svg"}
                    alt={analysis.fileName}
                    className="w-full h-full object-cover"
                  />
                  <div className="absolute inset-0 bg-black/30 flex items-center justify-center opacity-0 hover:opacity-100 transition-opacity duration-300">
                    <Dialog>
                      <DialogTrigger asChild>
                        <Button
                          size="sm"
                          className="bg-white/20 backdrop-blur-sm hover:bg-white/30"
                          onClick={() => handleViewAnalysis(analysis)}
                        >
                          <Eye className="w-4 h-4 mr-1" />
                          View Analysis
                        </Button>
                      </DialogTrigger>
                      <AnalysisModal analysis={analysis} onClose={undefined} />
                    </Dialog>
                  </div>
                </div>

                <div className="p-4">
                  <h4 className="font-medium text-gray-900 truncate mb-2">{analysis.fileName}</h4>

                  <div className="space-y-2 text-sm">
                    <div className="flex items-center justify-between">
                      <span className="text-gray-600">Ball Speed:</span>
                      <span className="font-medium text-[#344FA5]">{analysis.ballSpeed}</span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-gray-600">Angle:</span>
                      <span className="font-medium">{analysis.deliveryAngle}</span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-gray-600">Zone:</span>
                      <span className="font-medium">{analysis.pitchZone}</span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-gray-600">Type:</span>
                      <Badge variant="outline" className="text-xs">
                        {analysis.ballType}
                      </Badge>
                    </div>
                  </div>

                  <div className="flex items-center justify-between mt-4 pt-3 border-t border-gray-100">
                    <div className="flex items-center gap-1 text-xs text-gray-500">
                      <Calendar className="w-3 h-3" />
                      {analysis.uploadDate}
                    </div>
                    <div className="flex items-center gap-1 text-xs text-gray-500">
                      <Clock className="w-3 h-3" />
                      {analysis.uploadTime}
                    </div>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
