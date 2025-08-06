"use client"

import { useState } from "react"
import { Download, Filter, TrendingUp, Trophy, Target, Activity, Search, BarChart3 } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Badge } from "@/components/ui/badge"
import { motion, AnimatePresence } from "framer-motion"

export const StatsModule = () => {
  const [selectedFilter, setSelectedFilter] = useState("all")
  const [searchQuery, setSearchQuery] = useState("")
  const [selectedPeriod, setSelectedPeriod] = useState("career")

  const careerStats = [
    { label: "Total Matches", value: "120", icon: Trophy, color: "text-blue-600", change: "+5%" },
    { label: "Total Runs", value: "6,847", icon: Target, color: "text-green-600", change: "+12%" },
    { label: "Average Strike Rate", value: "142.5", icon: TrendingUp, color: "text-orange-600", change: "+8%" },
    { label: "Total Wickets", value: "89", icon: Activity, color: "text-purple-600", change: "+15%" },
  ]

  const matchHistory = [
    {
      id: 1,
      date: "2024-01-15",
      opponent: "Australia",
      type: "ODI",
      venue: "Eden Park",
      runs: 89,
      balls: 67,
      strikeRate: 132.8,
      wickets: 2,
      result: "Won",
    },
    {
      id: 2,
      date: "2024-01-12",
      opponent: "India",
      type: "T20",
      venue: "MCG",
      runs: 45,
      balls: 32,
      strikeRate: 140.6,
      wickets: 1,
      result: "Lost",
    },
    {
      id: 3,
      date: "2024-01-08",
      opponent: "England",
      type: "Test",
      venue: "Lord's",
      runs: 156,
      balls: 234,
      strikeRate: 66.7,
      wickets: 0,
      result: "Draw",
    },
    {
      id: 4,
      date: "2024-01-05",
      opponent: "Pakistan",
      type: "ODI",
      venue: "Oval",
      runs: 78,
      balls: 89,
      strikeRate: 87.6,
      wickets: 3,
      result: "Won",
    },
    {
      id: 5,
      date: "2024-01-01",
      opponent: "South Africa",
      type: "T20",
      venue: "Wanderers",
      runs: 34,
      balls: 28,
      strikeRate: 121.4,
      wickets: 1,
      result: "Won",
    },
  ]

  const performanceData = [
    { month: "Jan", runs: 450, wickets: 8, matches: 5 },
    { month: "Feb", runs: 380, wickets: 6, matches: 4 },
    { month: "Mar", runs: 520, wickets: 12, matches: 6 },
    { month: "Apr", runs: 290, wickets: 4, matches: 3 },
    { month: "May", runs: 610, wickets: 15, matches: 7 },
    { month: "Jun", runs: 480, wickets: 9, matches: 5 },
  ]

  const filteredMatches = matchHistory.filter((match) => {
    const matchesFilter = selectedFilter === "all" || match.type.toLowerCase() === selectedFilter
    const matchesSearch =
      match.opponent.toLowerCase().includes(searchQuery.toLowerCase()) ||
      match.venue.toLowerCase().includes(searchQuery.toLowerCase())
    return matchesFilter && matchesSearch
  })

  const handleExportStats = () => {
    // Simulate PDF export
    const statsData = {
      careerStats,
      matchHistory: filteredMatches,
      exportDate: new Date().toISOString(),
    }

    console.log("Exporting stats:", statsData)

    // Create a downloadable file
    const dataStr = JSON.stringify(statsData, null, 2)
    const dataBlob = new Blob([dataStr], { type: "application/json" })
    const url = URL.createObjectURL(dataBlob)
    const link = document.createElement("a")
    link.href = url
    link.download = `cricket-stats-${new Date().toISOString().split("T")[0]}.json`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    URL.revokeObjectURL(url)
  }

  return (
    <div className="space-y-6 p-4 md:p-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-2xl font-bold text-gray-900">Performance Statistics</h2>
          <p className="text-gray-600">Comprehensive analysis of your cricket performance</p>
        </div>
        <div className="flex items-center gap-3">
          <Select value={selectedPeriod} onValueChange={setSelectedPeriod}>
            <SelectTrigger className="w-32">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="career">Career</SelectItem>
              <SelectItem value="year">This Year</SelectItem>
              <SelectItem value="month">This Month</SelectItem>
              <SelectItem value="week">This Week</SelectItem>
            </SelectContent>
          </Select>
          <Button onClick={handleExportStats} className="bg-[#344FA5] hover:bg-[#2A3F85]">
            <Download className="w-4 h-4 mr-2" />
            Export
          </Button>
        </div>
      </div>

      {/* Career Stats Cards */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        {careerStats.map((stat, index) => (
          <motion.div
            key={index}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
          >
            <Card className="border-0 shadow-md hover:shadow-lg transition-all duration-300 hover:scale-105">
              <CardContent className="p-4 md:p-6 text-center">
                <div className="flex items-center justify-center mb-3">
                  <div className="p-3 bg-gray-50 rounded-xl">
                    <stat.icon className={`w-5 h-5 md:w-6 md:h-6 ${stat.color}`} />
                  </div>
                </div>
                <p className="text-xs md:text-sm text-gray-600 mb-1">{stat.label}</p>
                <p className="text-xl md:text-2xl font-bold text-gray-900">{stat.value}</p>
                <p className="text-xs text-green-600 mt-1">{stat.change} from last period</p>
              </CardContent>
            </Card>
          </motion.div>
        ))}
      </div>

      {/* Performance Chart */}
      <Card className="border-0 shadow-md">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <BarChart3 className="w-5 h-5 text-[#344FA5]" />
            Performance Trends
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="h-64 p-4 bg-gradient-to-t from-gray-50 to-transparent rounded-lg">
            <div className="flex items-end justify-between h-full gap-3 relative">
              {/* Grid lines */}
              <div className="absolute inset-0 flex flex-col justify-between opacity-20">
                {[100, 75, 50, 25, 0].map((line, idx) => (
                  <div key={idx} className="w-full border-t border-gray-300"></div>
                ))}
              </div>

              {/* Y-axis labels */}
              <div className="absolute -left-8 h-full flex flex-col justify-between text-xs text-gray-500">
                {[600, 450, 300, 150, 0].map((val, idx) => (
                  <span key={idx} className="transform -translate-y-1">
                    {val}
                  </span>
                ))}
              </div>

              {/* Bars */}
              {performanceData.map((data, index) => {
                const maxValue = Math.max(...performanceData.map((d) => d.runs))
                const heightPercentage = (data.runs / maxValue) * 100

                return (
                  <div key={index} className="flex flex-col items-center flex-1 relative group">
                    <div className="absolute -top-12 left-1/2 transform -translate-x-1/2 bg-gray-900 text-white px-2 py-1 rounded text-xs opacity-0 group-hover:opacity-100 transition-opacity duration-200 pointer-events-none z-10 whitespace-nowrap">
                      Runs: {data.runs}
                      <br />
                      Wickets: {data.wickets}
                      <br />
                      Matches: {data.matches}
                    </div>

                    <div
                      className="w-full bg-gradient-to-t from-[#344FA5] to-[#4A5FB8] rounded-t-lg transition-all duration-700 ease-out hover:from-[#2A3F85] hover:to-[#344FA5] shadow-sm hover:shadow-md relative overflow-hidden min-w-[24px] transform hover:scale-105"
                      style={{
                        height: `${heightPercentage}%`,
                        animationDelay: `${index * 100}ms`,
                      }}
                    >
                      <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent transform -skew-x-12 translate-x-[-100%] group-hover:translate-x-[100%] transition-transform duration-1000"></div>
                    </div>

                    <span className="text-xs text-gray-600 mt-3 font-medium group-hover:text-[#344FA5] transition-colors duration-200">
                      {data.month}
                    </span>
                  </div>
                )
              })}
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Match History */}
      <Card className="border-0 shadow-md">
        <CardHeader>
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
            <CardTitle>Match History</CardTitle>
            <div className="flex items-center gap-3">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
                <Input
                  placeholder="Search matches..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="pl-10 w-64"
                />
              </div>
              <Select value={selectedFilter} onValueChange={setSelectedFilter}>
                <SelectTrigger className="w-32">
                  <Filter className="w-4 h-4 mr-2" />
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Types</SelectItem>
                  <SelectItem value="odi">ODI</SelectItem>
                  <SelectItem value="t20">T20</SelectItem>
                  <SelectItem value="test">Test</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>
        </CardHeader>
        <CardContent>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-gray-200">
                  <th className="text-left py-3 px-4 font-semibold text-gray-700">Date</th>
                  <th className="text-left py-3 px-4 font-semibold text-gray-700">Opponent</th>
                  <th className="text-left py-3 px-4 font-semibold text-gray-700">Type</th>
                  <th className="text-left py-3 px-4 font-semibold text-gray-700">Venue</th>
                  <th className="text-left py-3 px-4 font-semibold text-gray-700">Runs</th>
                  <th className="text-left py-3 px-4 font-semibold text-gray-700">Strike Rate</th>
                  <th className="text-left py-3 px-4 font-semibold text-gray-700">Wickets</th>
                  <th className="text-left py-3 px-4 font-semibold text-gray-700">Result</th>
                </tr>
              </thead>
              <tbody>
                <AnimatePresence>
                  {filteredMatches.map((match, index) => (
                    <motion.tr
                      key={match.id}
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      exit={{ opacity: 0, y: -20 }}
                      transition={{ delay: index * 0.05 }}
                      className="border-b border-gray-100 hover:bg-gray-50 transition-colors duration-200"
                    >
                      <td className="py-3 px-4 text-sm text-gray-900">{match.date}</td>
                      <td className="py-3 px-4 text-sm font-medium text-gray-900">{match.opponent}</td>
                      <td className="py-3 px-4">
                        <Badge variant="outline" className="text-xs">
                          {match.type}
                        </Badge>
                      </td>
                      <td className="py-3 px-4 text-sm text-gray-600">{match.venue}</td>
                      <td className="py-3 px-4 text-sm font-semibold text-gray-900">{match.runs}</td>
                      <td className="py-3 px-4 text-sm text-gray-900">{match.strikeRate}</td>
                      <td className="py-3 px-4 text-sm text-gray-900">{match.wickets}</td>
                      <td className="py-3 px-4">
                        <Badge
                          className={`text-xs ${
                            match.result === "Won"
                              ? "bg-green-100 text-green-800"
                              : match.result === "Lost"
                                ? "bg-red-100 text-red-800"
                                : "bg-yellow-100 text-yellow-800"
                          }`}
                        >
                          {match.result}
                        </Badge>
                      </td>
                    </motion.tr>
                  ))}
                </AnimatePresence>
              </tbody>
            </table>
          </div>

          {filteredMatches.length === 0 && (
            <div className="text-center py-8 text-gray-500">
              <Trophy className="w-12 h-12 mx-auto mb-4 text-gray-300" />
              <p>No matches found matching your criteria</p>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  )
}
