"use client"
import { Users, Trophy, Target, TrendingUp, Activity, Play } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { useState } from "react"

export const Dashboard = () => {
  // Add custom styles for animations
  const chartStyles = `
    @keyframes grow {
      from { height: 0; }
      to { height: var(--target-height); }
    }
    .animate-grow {
      animation: grow 1s ease-out forwards;
    }
  `

  const dashboardStats = [
    { label: "Matches", value: "120", icon: Trophy, color: "text-[#344FA5]" },
    { label: "Runs", value: "6000", icon: Target, color: "text-green-600" },
    { label: "Strike Rate", value: "280", icon: TrendingUp, color: "text-orange-600" },
    { label: "Wickets", value: "60", icon: Activity, color: "text-purple-600" },
  ]

  const ballSpeedData = [
    { day: "Mon", value: 85 },
    { day: "Tue", value: 92 },
    { day: "Wed", value: 78 },
    { day: "Thu", value: 88 },
    { day: "Fri", value: 95 },
    { day: "Sat", value: 90 },
    { day: "Sun", value: 72 },
  ]

  const recentVideos = [
    {
      title: "Match Session",
      thumbnail: "/placeholder.svg?height=200&width=300&text=Match+Highlights",
      tag: "HIGHLIGHTS",
    },
    {
      title: "Training Session",
      thumbnail: "/placeholder.svg?height=200&width=300&text=Training+Session",
      tag: "PRACTICE",
    },
    { title: "Behind the scenes", thumbnail: "/placeholder.svg?height=200&width=300&text=Behind+Scenes", tag: "BTS" },
  ]

  const matchSessions = [
    { title: "Match Session", location: "Stadium A", image: "/placeholder.svg?height=48&width=48&text=Stadium+A" },
    { title: "Training Session", location: "Stadium B", image: "/placeholder.svg?height=48&width=48&text=Stadium+B" },
  ]

  const [selectedDate, setSelectedDate] = useState("2025-01-08")
  const [selectedMatchType, setSelectedMatchType] = useState("")

  const handleSubmit = () => {
    if (!selectedMatchType) {
      alert("Please select a match type")
      return
    }

    const formData = {
      datePlayed: selectedDate,
      matchType: selectedMatchType,
      submittedAt: new Date().toISOString(),
    }

    console.log("Form submitted:", formData)
    alert(`Match details submitted successfully!\n\nDate: ${selectedDate}\nMatch Type: ${selectedMatchType}`)
  }

  const handleVideoPlay = (videoTitle) => {
    console.log(`Playing video: ${videoTitle}`)
    alert(`Now playing: ${videoTitle}`)
  }

  return (
    <>
      <style>{chartStyles}</style>
      <div className="space-y-6 p-4 md:p-6">
        {/* Welcome Header */}
        <div className="bg-gradient-to-r from-[#344FA5] to-[#4A5FB8] rounded-2xl p-6 text-white">
          <h2 className="text-2xl font-bold mb-2">WELCOME Back, Kane!</h2>
          <p className="text-blue-100">Ready for another great performance?</p>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
          {dashboardStats.map((stat, index) => (
            <Card
              key={index}
              className="border-0 shadow-md hover:shadow-lg transition-all duration-300 hover:scale-105"
            >
              <CardContent className="p-4 md:p-6 text-center">
                <div className="flex items-center justify-center mb-3">
                  <div className="p-3 bg-gray-50 rounded-xl">
                    <stat.icon className={`w-5 h-5 md:w-6 md:h-6 ${stat.color}`} />
                  </div>
                </div>
                <p className="text-xs md:text-sm text-gray-600 mb-1">{stat.label}</p>
                <p className="text-xl md:text-2xl font-bold text-gray-900">{stat.value}</p>
              </CardContent>
            </Card>
          ))}
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Ball Speed & Performance */}
          <Card className="border-0 shadow-md">
            <CardHeader className="pb-4">
              <CardTitle className="text-lg">Ball Speed & Batsman Performance</CardTitle>
              <div className="flex flex-col sm:flex-row sm:items-center gap-4 sm:gap-6 text-sm">
                <div>
                  <span className="text-2xl md:text-3xl font-bold">145 km/h</span>
                  <span className="text-[#344FA5] ml-2">(Ball Speed)</span>
                  <p className="text-green-600 text-xs">Last 7 Days +5%</p>
                </div>
                <div>
                  <span className="text-2xl md:text-3xl font-bold">80%</span>
                  <span className="text-purple-600 ml-2">(Batsman Performance)</span>
                  <p className="text-green-600 text-xs">Last 7 Days +6%</p>
                </div>
              </div>
            </CardHeader>
            <CardContent>
              <div className="relative">
                {/* Chart container with proper sizing */}
                <div className="h-48 p-4 bg-gradient-to-t from-gray-50 to-transparent rounded-lg">
                  <div className="flex items-end justify-between h-full gap-3 relative">
                    {/* Grid lines for better readability */}
                    <div className="absolute inset-0 flex flex-col justify-between opacity-20">
                      {[100, 75, 50, 25, 0].map((line, idx) => (
                        <div key={idx} className="w-full border-t border-gray-300"></div>
                      ))}
                    </div>

                    {/* Y-axis labels */}
                    <div className="absolute -left-8 h-full flex flex-col justify-between text-xs text-gray-500">
                      {[100, 75, 50, 25, 0].map((val, idx) => (
                        <span key={idx} className="transform -translate-y-1">
                          {val}
                        </span>
                      ))}
                    </div>

                    {/* Bars */}
                    {ballSpeedData.map((data, index) => {
                      const maxValue = Math.max(...ballSpeedData.map((d) => d.value))
                      const heightPercentage = (data.value / maxValue) * 100

                      return (
                        <div key={index} className="flex flex-col items-center flex-1 relative group">
                          {/* Tooltip */}
                          <div className="absolute -top-8 left-1/2 transform -translate-x-1/2 bg-gray-900 text-white px-2 py-1 rounded text-xs opacity-0 group-hover:opacity-100 transition-opacity duration-200 pointer-events-none z-10 whitespace-nowrap">
                            {data.value} km/h
                            <div className="absolute top-full left-1/2 transform -translate-x-1/2 border-l-4 border-r-4 border-t-4 border-transparent border-t-gray-900"></div>
                          </div>

                          {/* Bar with enhanced styling */}
                          <div
                            className="w-full bg-gradient-to-t from-[#344FA5] to-[#4A5FB8] rounded-t-lg transition-all duration-700 ease-out hover:from-[#2A3F85] hover:to-[#344FA5] shadow-sm hover:shadow-md relative overflow-hidden min-w-[24px] animate-[grow_1s_ease-out] transform hover:scale-105"
                            style={{
                              height: `${heightPercentage}%`,
                              animationDelay: `${index * 100}ms`,
                              animationFillMode: "both",
                            }}
                          >
                            {/* Shine effect */}
                            <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent transform -skew-x-12 translate-x-[-100%] group-hover:translate-x-[100%] transition-transform duration-1000"></div>

                            {/* Value label on top of bar */}
                            <div className="absolute -top-5 left-1/2 transform -translate-x-1/2 text-xs font-semibold text-gray-700 opacity-0 group-hover:opacity-100 transition-opacity duration-200">
                              {data.value}
                            </div>
                          </div>

                          {/* Day label with enhanced styling */}
                          <span className="text-xs text-gray-600 mt-3 font-medium group-hover:text-[#344FA5] transition-colors duration-200">
                            {data.day}
                          </span>
                        </div>
                      )
                    })}
                  </div>
                </div>

                {/* Legend */}
                <div className="flex items-center justify-center mt-4 gap-6 text-sm">
                  <div className="flex items-center gap-2">
                    <div className="w-3 h-3 bg-gradient-to-t from-[#344FA5] to-[#4A5FB8] rounded"></div>
                    <span className="text-gray-600">Ball Speed (km/h)</span>
                  </div>
                  <div className="text-gray-500 text-xs">Hover for details</div>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Players Network */}
          <Card className="border-0 shadow-md">
            <CardHeader className="pb-4">
              <CardTitle className="text-lg">Players Network</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex justify-between">
                <div className="text-center">
                  <div className="flex items-center justify-center gap-2 mb-2">
                    <Users className="w-4 h-4 text-[#344FA5]" />
                    <span className="text-sm text-gray-600">Follower</span>
                  </div>
                  <p className="text-xl font-bold">280</p>
                </div>
                <div className="text-center">
                  <div className="flex items-center justify-center gap-2 mb-2">
                    <Users className="w-4 h-4 text-green-600" />
                    <span className="text-sm text-gray-600">Following</span>
                  </div>
                  <p className="text-xl font-bold">56</p>
                </div>
              </div>

              <div className="space-y-3">
                <div>
                  <label className="text-sm text-gray-600">Date Played</label>
                  <div className="mt-1 p-3 border border-gray-200 rounded-lg">
                    <input
                      type="date"
                      value={selectedDate}
                      onChange={(e) => setSelectedDate(e.target.value)}
                      className="text-sm w-full bg-transparent border-none outline-none"
                    />
                  </div>
                </div>

                <div>
                  <label className="text-sm text-gray-600">Match Type</label>
                  <div className="mt-1">
                    <select
                      value={selectedMatchType}
                      onChange={(e) => setSelectedMatchType(e.target.value)}
                      className="w-full p-3 border border-gray-200 rounded-lg text-sm bg-white"
                    >
                      <option value="">Select Match Type</option>
                      <option value="ODI">ODI (One Day International)</option>
                      <option value="T20">T20 (Twenty20)</option>
                      <option value="Test">Test Match</option>
                      <option value="Practice">Practice Match</option>
                    </select>
                  </div>
                </div>
              </div>

              <Button
                onClick={handleSubmit}
                className="w-full bg-[#344FA5] hover:bg-[#2A3F85] transition-colors duration-200"
              >
                Submit
              </Button>
            </CardContent>
          </Card>
        </div>

        {/* Recent Score & Sessions */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <Card className="border-0 shadow-md">
            <CardHeader className="pb-4">
              <CardTitle className="text-lg">Recent Score Progression</CardTitle>
              <div>
                <span className="text-3xl font-bold">250</span>
                <p className="text-green-600 text-sm">Last 7 Days +10%</p>
              </div>
            </CardHeader>
            <CardContent>
              <div className="h-32 flex items-center">
                <svg className="w-full h-full" viewBox="0 0 300 100">
                  <path
                    d="M0,80 Q50,60 100,70 T200,40 T300,50"
                    stroke="#344FA5"
                    strokeWidth="3"
                    fill="none"
                    className="animate-pulse"
                  />
                </svg>
              </div>
              <div className="flex justify-between text-xs text-gray-600 mt-2">
                <span>Mon</span>
                <span>Tue</span>
                <span>Wed</span>
                <span>Thu</span>
                <span>Fri</span>
                <span>Sat</span>
                <span>Sun</span>
              </div>
            </CardContent>
          </Card>

          <Card className="border-0 shadow-md">
            <CardHeader className="pb-4">
              <CardTitle className="text-lg">Match & Practice Session</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              {matchSessions.map((session, index) => (
                <div
                  key={index}
                  className="flex items-center gap-3 p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors duration-200"
                >
                  <img
                    src={session.image || "/placeholder.svg"}
                    alt={session.title}
                    className="w-12 h-12 rounded-lg object-cover bg-blue-100"
                  />
                  <div className="flex-1">
                    <p className="font-semibold text-sm">{session.title}</p>
                    <p className="text-xs text-[#344FA5]">{session.location}</p>
                  </div>
                </div>
              ))}
            </CardContent>
          </Card>
        </div>

        {/* Recent Videos */}
        <Card className="border-0 shadow-md">
          <CardHeader className="pb-4">
            <CardTitle className="text-lg">Recent Videos & Images</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {recentVideos.map((video, index) => (
                <div key={index} className="relative group cursor-pointer" onClick={() => handleVideoPlay(video.title)}>
                  <div className="aspect-video bg-gray-100 rounded-lg flex items-center justify-center relative overflow-hidden">
                    <img
                      src={video.thumbnail || "/placeholder.svg"}
                      alt={video.title}
                      className="w-full h-full object-cover"
                    />
                    <div className="absolute inset-0 bg-black/30 flex items-center justify-center">
                      <Play className="w-8 h-8 text-white group-hover:text-[#344FA5] transition-colors" />
                    </div>
                    <Badge className="absolute top-2 left-2 bg-[#344FA5] text-white text-xs">{video.tag}</Badge>
                  </div>
                  <p className="text-sm font-medium mt-2 text-center">{video.title}</p>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </>
  )
}
