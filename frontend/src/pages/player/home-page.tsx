"use client"

import type React from "react"
import { useState } from "react"
import {
  Search,
  BarChart3,
  Menu,
  User,
  Users,
  Activity,
  Target,
  Globe,
  Bell,
  Sparkles,
  ChevronRight,
} from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Sheet, SheetContent, SheetTrigger } from "@/components/ui/sheet"
import { Dashboard } from "@/components/player/home/Dashboard"
import { SocialMedia } from "@/components/player/home/SocialMedia"
import { cn } from "@/lib/utils"
import { motion, AnimatePresence } from "framer-motion"
import { StatsModule } from "@/components/player/home/StatsModule"
import { BallTracking } from "@/components/player/home/BallTracking"
import { Following } from "@/components/player/home/Following"

interface HomePageProps {
  onLogout: () => void
}

export const HomePage = ({ onLogout }: HomePageProps) => {
  const [activeTab, setActiveTab] = useState("Dashboard")
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const [searchQuery, setSearchQuery] = useState("")
  const [showSuggestions, setShowSuggestions] = useState(false)
  const [showNotifications, setShowNotifications] = useState(false)
  const [showAllNotifications, setShowAllNotifications] = useState(false)
  const [notificationData, setNotificationData] = useState([
    {
      id: 1,
      title: "Match Performance Update",
      message: "Your batting average has improved by 15% this week!",
      time: "2 minutes ago",
      type: "performance",
      unread: true,
    },
    {
      id: 2,
      title: "Team Practice Session",
      message: "Tomorrow's practice session at 9:00 AM has been confirmed.",
      time: "1 hour ago",
      type: "schedule",
      unread: true,
    },
    {
      id: 3,
      title: "New Follower",
      message: "Steve Smith started following you.",
      time: "3 hours ago",
      type: "social",
      unread: false,
    },
    {
      id: 4,
      title: "Match Statistics Ready",
      message: "Your detailed match analysis for last game is now available.",
      time: "1 day ago",
      type: "stats",
      unread: false,
    },
    {
      id: 5,
      title: "Training Video Uploaded",
      message: "New bowling technique video has been added to your library.",
      time: "2 days ago",
      type: "content",
      unread: false,
    },
    {
      id: 6,
      title: "Weekly Performance Report",
      message: "Your comprehensive performance analysis for this week is ready.",
      time: "3 days ago",
      type: "stats",
      unread: false,
    },
    {
      id: 7,
      title: "Team Meeting Reminder",
      message: "Don't forget about the team strategy meeting tomorrow at 2 PM.",
      time: "4 days ago",
      type: "schedule",
      unread: false,
    },
    {
      id: 8,
      title: "Achievement Unlocked",
      message: "Congratulations! You've achieved 'Century Maker' milestone.",
      time: "5 days ago",
      type: "performance",
      unread: false,
    },
    {
      id: 9,
      title: "Equipment Check",
      message: "Reminder: Equipment inspection scheduled for next Monday.",
      time: "1 week ago",
      type: "schedule",
      unread: false,
    },
    {
      id: 10,
      title: "New Training Program",
      message: "Advanced batting techniques course is now available in your dashboard.",
      time: "1 week ago",
      type: "content",
      unread: false,
    },
  ])

  const unreadCount = notificationData.filter((n) => n.unread).length

  const handleViewAllNotifications = () => {
    setShowNotifications(false)
    setShowAllNotifications(true)
  }

  const handleMarkAsRead = (notificationId: number) => {
    setNotificationData((prev) =>
      prev.map((notification) =>
        notification.id === notificationId ? { ...notification, unread: false } : notification,
      ),
    )
    console.log(`Notification ${notificationId} marked as read`)
  }

  const handleMarkAllAsRead = () => {
    setNotificationData((prev) => prev.map((notification) => ({ ...notification, unread: false })))
    console.log("All notifications marked as read")
  }

  const handleViewDetails = (notification: any) => {
    // Mark as read when viewing details
    if (notification.unread) {
      handleMarkAsRead(notification.id)
    }

    // Show notification details (you can customize this based on notification type)
    const detailsMessage = getNotificationDetails(notification)
    alert(detailsMessage)
    console.log("Viewing notification details:", notification)
  }

  const getNotificationDetails = (notification: any) => {
    switch (notification.type) {
      case "performance":
        return `Performance Details:\n\n${notification.title}\n\n${notification.message}\n\nDetailed analysis:\n• Current batting average: 87.5\n• Improvement: +15% from last week\n• Matches played: 8\n• Best score: 156*\n\nTime: ${notification.time}`

      case "schedule":
        return `Schedule Details:\n\n${notification.title}\n\n${notification.message}\n\nEvent details:\n• Date: Tomorrow\n• Time: 9:00 AM\n• Location: Main Cricket Ground\n• Duration: 3 hours\n• Coach: Mike Johnson\n\nTime: ${notification.time}`

      case "social":
        return `Social Update:\n\n${notification.title}\n\n${notification.message}\n\nProfile details:\n• Player: Steve Smith\n• Team: Australia\n• Role: Batsman\n• Following: 1,234\n• Followers: 567,890\n\nTime: ${notification.time}`

      case "stats":
        return `Statistics Details:\n\n${notification.title}\n\n${notification.message}\n\nMatch analysis includes:\n• Batting performance\n• Bowling analysis\n• Fielding statistics\n• Comparison with previous matches\n• Areas for improvement\n\nTime: ${notification.time}`

      case "content":
        return `Content Details:\n\n${notification.title}\n\n${notification.message}\n\nVideo information:\n• Duration: 15 minutes\n• Coach: Professional Trainer\n• Skill level: Advanced\n• Topics covered: Bowling techniques\n• Available in: HD Quality\n\nTime: ${notification.time}`

      default:
        return `${notification.title}\n\n${notification.message}\n\nTime: ${notification.time}`
    }
  }

  const getNotificationIcon = (type: string) => {
    switch (type) {
      case "performance":
        return "📈"
      case "schedule":
        return "📅"
      case "social":
        return "👥"
      case "stats":
        return "📊"
      case "content":
        return "🎥"
      default:
        return "🔔"
    }
  }

  // Sample player data - in a real app, this would come from an API
  const players = [
    { id: 1, name: "Kane Williamson", team: "New Zealand", role: "Batsman" },
    { id: 2, name: "Virat Kohli", team: "India", role: "Batsman" },
    { id: 3, name: "Steve Smith", team: "Australia", role: "Batsman" },
    { id: 4, name: "Joe Root", team: "England", role: "Batsman" },
    { id: 5, name: "Babar Azam", team: "Pakistan", role: "Batsman" },
    { id: 6, name: "Pat Cummins", team: "Australia", role: "Bowler" },
    { id: 7, name: "Jasprit Bumrah", team: "India", role: "Bowler" },
    { id: 8, name: "Trent Boult", team: "New Zealand", role: "Bowler" },
    { id: 9, name: "Kagiso Rabada", team: "South Africa", role: "Bowler" },
    { id: 10, name: "Ben Stokes", team: "England", role: "All-rounder" },
  ]

  // Filter players based on search query
  const filteredPlayers = players.filter(
    (player) =>
      player.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      player.team.toLowerCase().includes(searchQuery.toLowerCase()),
  )

  const handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value
    setSearchQuery(value)
    setShowSuggestions(value.length > 0)
  }

  const handlePlayerSelect = (playerName: string) => {
    setSearchQuery(playerName)
    setShowSuggestions(false)
    // Here you can add logic to navigate to player profile or perform search
    console.log("Selected player:", playerName)
  }

  const sidebarItems = [
    { icon: BarChart3, label: "Dashboard" },
    { icon: Globe, label: "Social Media" },
    { icon: Activity, label: "Stats" },
    { icon: Target, label: "Ball Track" },
    { icon: Users, label: "Following" },
  ]

  const [sidebarCollapsed, setSidebarCollapsed] = useState(false)
  const [sidebarHovered, setSidebarHovered] = useState(false)

  const SidebarContent = () => (
    <div className="flex flex-col h-full bg-white/95 backdrop-blur-sm transition-all duration-300 ease-in-out">
      {/* Profile Section */}
      <div className="p-4 lg:p-6 border-b border-gray-100/50 relative overflow-hidden">
        {/* Background decorative elements */}
        <div className="absolute -top-12 -right-12 w-32 h-32 bg-gradient-to-br from-[#344FA5]/10 to-[#344FA5]/5 rounded-full blur-xl"></div>
        <div className="absolute -bottom-8 -left-8 w-24 h-24 bg-gradient-to-tr from-[#344FA5]/10 to-[#344FA5]/5 rounded-full blur-lg"></div>

        <div className="relative flex items-center gap-3 lg:gap-4">
          <div className="relative group flex-shrink-0">
            <div className="absolute inset-0 bg-gradient-to-r from-[#344FA5] to-[#4A5FB8] rounded-full blur-md opacity-50 group-hover:opacity-70 transition-all duration-500 animate-pulse"></div>
            <Avatar
              className={`border-4 border-white shadow-xl relative hover:scale-105 transition-all duration-300 ${
                sidebarCollapsed && !sidebarHovered ? "w-10 h-10" : "w-12 h-12 lg:w-14 lg:h-14"
              }`}
            >
              <AvatarImage src="/placeholder.svg?height=72&width=72&text=KW" className="object-cover" />
              <AvatarFallback
                className={`bg-gradient-to-br from-[#344FA5] to-[#4A5FB8] text-white font-bold ${
                  sidebarCollapsed && !sidebarHovered ? "text-sm" : "text-base lg:text-lg"
                }`}
              >
                KW
              </AvatarFallback>
            </Avatar>
            <div
              className={`absolute -bottom-1 -right-1 bg-green-500 border-2 border-white rounded-full shadow-md animate-pulse ${
                sidebarCollapsed && !sidebarHovered ? "w-3 h-3" : "w-4 h-4 lg:w-5 lg:h-5"
              }`}
            ></div>
          </div>

          {/* Profile Info - Better spacing and typography */}
          <div
            className={`flex-1 min-w-0 transition-all duration-300 ease-in-out ${
              sidebarCollapsed && !sidebarHovered ? "opacity-0 w-0 overflow-hidden ml-0" : "opacity-100 ml-0"
            }`}
          >
            <h3 className="font-bold text-sm lg:text-base xl:text-lg text-gray-900 flex items-center truncate">
              Kane Williamson
              <span className="ml-2 inline-flex items-center justify-center flex-shrink-0">
                <Sparkles className="w-3 h-3 lg:w-4 lg:h-4 text-yellow-500" />
              </span>
            </h3>
            <p className="text-xs lg:text-sm text-[#344FA5] font-medium truncate">Team Newzealand</p>
            <p className="text-xs text-gray-500 flex items-center gap-1 truncate">
              <span className="inline-block w-1.5 h-1.5 lg:w-2 lg:h-2 bg-green-500 rounded-full flex-shrink-0"></span>
              Professional Cricketer
            </p>
          </div>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 p-4 relative">
        {/* Subtle background pattern */}
        <div className="absolute inset-0 opacity-5">
          <div
            className="absolute inset-0"
            style={{
              backgroundImage: "radial-gradient(#344FA5 0.5px, transparent 0.5px)",
              backgroundSize: "12px 12px",
            }}
          ></div>
        </div>

        <div className={`space-y-3 relative ${sidebarCollapsed && !sidebarHovered ? "space-y-2" : ""}`}>
          {sidebarItems.map((item, index) => (
            <div key={item.label} className="relative group">
              <button
                onClick={() => {
                  setActiveTab(item.label)
                  setSidebarOpen(false)
                }}
                className={cn(
                  "w-full flex items-center gap-3 rounded-xl text-left transition-all duration-300 group relative overflow-hidden",
                  sidebarCollapsed && !sidebarHovered ? "px-2 py-3 justify-center" : "px-4 py-4",
                  activeTab === item.label
                    ? "bg-gradient-to-r from-[#344FA5] to-[#4A5FB8] text-white shadow-lg transform scale-105"
                    : "text-gray-600 hover:bg-gray-50/80 hover:text-gray-900 hover:transform hover:scale-102",
                )}
                style={{ animationDelay: `${index * 100}ms` }}
              >
                {/* Glassmorphism effect for active item */}
                {activeTab === item.label && (
                  <div className="absolute inset-0 bg-white/10 backdrop-blur-sm rounded-xl"></div>
                )}

                {/* Hover shine effect */}
                <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent -translate-x-full group-hover:translate-x-full transition-transform duration-1000 ease-in-out"></div>

                <div
                  className={cn(
                    "rounded-lg relative z-10 transition-all duration-300 flex-shrink-0",
                    sidebarCollapsed && !sidebarHovered ? "p-1.5" : "p-2",
                    activeTab === item.label ? "bg-white/20" : "bg-gray-100 group-hover:bg-gray-200",
                  )}
                >
                  <item.icon
                    className={cn(
                      "transition-all duration-300",
                      sidebarCollapsed && !sidebarHovered ? "w-4 h-4" : "w-5 h-5",
                      activeTab === item.label ? "text-white" : "text-gray-700 group-hover:text-gray-900",
                    )}
                  />
                </div>

                {/* Label - Hidden when collapsed and not hovered */}
                <span
                  className={`font-semibold relative z-10 transition-all duration-300 ease-in-out whitespace-nowrap ${
                    sidebarCollapsed && !sidebarHovered ? "opacity-0 w-0 overflow-hidden ml-0" : "opacity-100 ml-0"
                  }`}
                >
                  {item.label}
                </span>

                {/* Active indicator */}
                {activeTab === item.label && (
                  <ChevronRight
                    className={`text-white absolute right-4 animate-bounce transition-all duration-300 ${
                      sidebarCollapsed && !sidebarHovered ? "opacity-0 w-0" : "opacity-100 w-4 h-4"
                    }`}
                  />
                )}
              </button>

              {/* Tooltip for collapsed state */}
              {sidebarCollapsed && !sidebarHovered && (
                <div className="absolute left-full top-1/2 transform -translate-y-1/2 ml-3 px-3 py-2 bg-gray-900 text-white text-sm rounded-lg opacity-0 group-hover:opacity-100 transition-opacity duration-200 pointer-events-none z-50 whitespace-nowrap shadow-lg">
                  {item.label}
                  <div className="absolute right-full top-1/2 transform -translate-y-1/2 border-4 border-transparent border-r-gray-900"></div>
                </div>
              )}
            </div>
          ))}
        </div>
      </nav>

      {/* Collapse/Expand Toggle Button */}
      <div className={`px-4 pb-2 ${sidebarCollapsed && !sidebarHovered ? "px-2" : ""}`}>
        <button
          onClick={() => setSidebarCollapsed(!sidebarCollapsed)}
          className={`w-full flex items-center p-2 text-gray-500 hover:text-[#344FA5] hover:bg-gray-50 rounded-lg transition-all duration-300 group ${
            sidebarCollapsed && !sidebarHovered ? "justify-center" : "justify-center"
          }`}
        >
          <motion.div animate={{ rotate: sidebarCollapsed ? 180 : 0 }} transition={{ duration: 0.3 }}>
            <ChevronRight className="w-5 h-5" />
          </motion.div>
          {(!sidebarCollapsed || sidebarHovered) && (
            <span
              className={`ml-2 text-sm font-medium transition-all duration-300 ${
                sidebarCollapsed && !sidebarHovered ? "opacity-0 w-0 overflow-hidden" : "opacity-100"
              }`}
            >
              {sidebarCollapsed ? "Expand" : "Collapse"}
            </span>
          )}
        </button>
      </div>

      {/* Footer */}
      <div
        className={`p-4 border-t border-gray-100/50 bg-gradient-to-b from-transparent to-gray-50/50 ${
          sidebarCollapsed && !sidebarHovered ? "px-2" : ""
        }`}
      >
        <Button
          variant="outline"
          onClick={onLogout}
          className={`w-full border-2 border-gray-200 hover:border-red-300 hover:text-red-600 transition-all duration-300 group relative overflow-hidden bg-white/80 backdrop-blur-sm hover:shadow-md ${
            sidebarCollapsed && !sidebarHovered ? "px-2 py-2" : ""
          }`}
        >
          <span className="absolute inset-0 bg-red-500/10 scale-x-0 group-hover:scale-x-100 transition-transform duration-300 origin-left rounded-md"></span>
          <User
            className={`relative z-10 group-hover:scale-110 transition-transform duration-300 flex-shrink-0 ${
              sidebarCollapsed && !sidebarHovered ? "w-4 h-4 mr-0" : "w-4 h-4 mr-2"
            }`}
          />
          <span
            className={`relative z-10 transition-all duration-300 ${
              sidebarCollapsed && !sidebarHovered ? "opacity-0 w-0 overflow-hidden ml-0" : "opacity-100 ml-0"
            }`}
          >
            Logout
          </span>
        </Button>
      </div>
    </div>
  )

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="flex">
        {/* Desktop Sidebar */}
        <div
          className={`hidden lg:block bg-white shadow-lg border-r border-gray-100 min-h-screen transition-all duration-300 ease-in-out relative z-30 ${
            sidebarCollapsed && !sidebarHovered ? "w-20" : "w-64 xl:w-80"
          }`}
          onMouseEnter={() => setSidebarHovered(true)}
          onMouseLeave={() => setSidebarHovered(false)}
        >
          <SidebarContent />
        </div>

        {/* Mobile Sidebar */}
        <Sheet open={sidebarOpen} onOpenChange={setSidebarOpen}>
          <SheetContent side="left" className="p-0 w-80 lg:hidden">
            <SidebarContent />
          </SheetContent>
        </Sheet>

        {/* Main Content */}
        <div className="flex-1 min-w-0 relative">
          {/* Header */}
          <div className="bg-white/95 backdrop-blur-sm border-b border-gray-100/50 p-4 lg:p-6 sticky top-0 z-40 shadow-sm">
            <div className="flex items-center justify-between gap-4">
              <div className="flex items-center gap-4 min-w-0 flex-1">
                <Sheet open={sidebarOpen} onOpenChange={setSidebarOpen}>
                  <SheetTrigger asChild>
                    <Button
                      variant="ghost"
                      size="icon"
                      className="lg:hidden hover:bg-gray-100 rounded-xl group relative overflow-hidden flex-shrink-0"
                    >
                      <span className="absolute inset-0 bg-gray-100/80 scale-0 group-hover:scale-100 transition-transform duration-300 rounded-full"></span>
                      <Menu className="w-6 h-6 relative z-10 group-hover:rotate-3 transition-transform duration-300" />
                    </Button>
                  </SheetTrigger>
                </Sheet>

                <motion.h1
                  key={activeTab}
                  initial={{ opacity: 0, y: -10 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: 10 }}
                  transition={{ duration: 0.3 }}
                  className="text-xl lg:text-2xl font-bold bg-gradient-to-r from-[#344FA5] to-[#4A5FB8] text-transparent bg-clip-text truncate"
                >
                  {activeTab}
                </motion.h1>
              </div>

              <div className="flex items-center gap-2 lg:gap-4 flex-shrink-0">
                {/* Search - Hidden on small screens */}
                <div className="relative hidden md:block group">
                  <div className="absolute inset-0 bg-gray-100/50 rounded-xl blur-sm group-hover:bg-gray-100/80 transition-colors duration-300"></div>
                  <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4 z-10" />
                  <Input
                    placeholder="Search Player"
                    value={searchQuery}
                    onChange={handleSearchChange}
                    onFocus={() => searchQuery.length > 0 && setShowSuggestions(true)}
                    onBlur={() => setTimeout(() => setShowSuggestions(false), 200)}
                    className="pl-10 w-48 lg:w-64 xl:w-80 bg-white/80 border-gray-100/80 focus:border-[#344FA5]/30 focus:ring-[#344FA5]/20 rounded-xl transition-all duration-300 relative z-10"
                  />

                  {/* Search Suggestions Dropdown */}
                  <AnimatePresence>
                    {showSuggestions && filteredPlayers.length > 0 && (
                      <motion.div
                        initial={{ opacity: 0, y: 10, scale: 0.95 }}
                        animate={{ opacity: 1, y: 0, scale: 1 }}
                        exit={{ opacity: 0, y: 10, scale: 0.95 }}
                        transition={{ duration: 0.2 }}
                        className="absolute top-full left-0 right-0 mt-2 bg-white/95 backdrop-blur-sm border border-gray-200/50 rounded-xl shadow-xl z-50 max-h-64 overflow-y-auto"
                      >
                        {filteredPlayers.slice(0, 5).map((player, index) => (
                          <motion.button
                            key={player.id}
                            initial={{ opacity: 0, y: 10 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ delay: index * 0.03 }}
                            onClick={() => handlePlayerSelect(player.name)}
                            className="w-full px-4 py-3 text-left hover:bg-gray-50/80 transition-colors duration-150 border-b border-gray-100 last:border-b-0 flex items-center gap-3 relative group"
                          >
                            {/* Hover effect */}
                            <div className="absolute inset-0 bg-gradient-to-r from-transparent via-[#344FA5]/5 to-transparent -translate-x-full group-hover:translate-x-full transition-transform duration-1000 ease-in-out"></div>

                            <div className="relative">
                              <div className="absolute inset-0 bg-gradient-to-r from-[#344FA5]/20 to-[#4A5FB8]/20 rounded-full blur-sm opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
                              <div className="w-8 h-8 bg-[#344FA5] rounded-full flex items-center justify-center text-white text-sm font-bold relative z-10">
                                {player.name
                                  .split(" ")
                                  .map((n) => n[0])
                                  .join("")
                                  .slice(0, 2)}
                              </div>
                            </div>
                            <div className="flex-1">
                              <p className="font-medium text-gray-900">{player.name}</p>
                              <p className="text-sm text-gray-500">
                                {player.team} • {player.role}
                              </p>
                            </div>
                            <ChevronRight className="w-4 h-4 text-gray-400 opacity-0 group-hover:opacity-100 transition-opacity duration-300 group-hover:translate-x-1 transition-transform" />
                          </motion.button>
                        ))}

                        {filteredPlayers.length > 5 && (
                          <div className="px-4 py-2 text-sm text-gray-500 text-center border-t border-gray-100">
                            +{filteredPlayers.length - 5} more players
                          </div>
                        )}
                      </motion.div>
                    )}

                    {/* No results message */}
                    {showSuggestions && searchQuery.length > 0 && filteredPlayers.length === 0 && (
                      <motion.div
                        initial={{ opacity: 0, y: 10, scale: 0.95 }}
                        animate={{ opacity: 1, y: 0, scale: 1 }}
                        exit={{ opacity: 0, y: 10, scale: 0.95 }}
                        transition={{ duration: 0.2 }}
                        className="absolute top-full left-0 right-0 mt-2 bg-white/95 backdrop-blur-sm border border-gray-200/50 rounded-xl shadow-xl z-50"
                      >
                        <div className="px-4 py-6 text-center text-gray-500">
                          <Search className="w-8 h-8 mx-auto mb-2 text-gray-300 animate-pulse" />
                          <p>No players found for "{searchQuery}"</p>
                        </div>
                      </motion.div>
                    )}
                  </AnimatePresence>
                </div>

                {/* Mobile search button */}
                <Button variant="ghost" size="icon" className="md:hidden hover:bg-gray-100 rounded-xl flex-shrink-0">
                  <Search className="w-5 h-5" />
                </Button>

                {/* Notifications */}
                <div className="relative flex-shrink-0">
                  <Button
                    variant="ghost"
                    size="icon"
                    onClick={() => setShowNotifications(!showNotifications)}
                    className="hover:bg-gray-100 rounded-xl relative group overflow-hidden"
                  >
                    <span className="absolute inset-0 bg-gray-100/80 scale-0 group-hover:scale-100 transition-transform duration-300 rounded-full"></span>
                    <Bell className="w-5 h-5 relative z-10 group-hover:scale-110 transition-transform duration-300" />
                    {unreadCount > 0 && (
                      <motion.span
                        initial={{ scale: 0 }}
                        animate={{ scale: 1 }}
                        className="absolute -top-1 -right-1 w-5 h-5 bg-gradient-to-r from-red-500 to-red-600 text-white text-xs rounded-full flex items-center justify-center shadow-sm"
                      >
                        {unreadCount}
                      </motion.span>
                    )}
                  </Button>

                  {/* Notifications Panel */}
                  <div
                    className={`absolute top-full right-0 mt-2 w-80 bg-white/95 backdrop-blur-sm border border-gray-200/80 rounded-xl shadow-xl z-50 transform transition-all duration-300 ease-out ${
                      showNotifications
                        ? "opacity-100 translate-y-0 scale-100"
                        : "opacity-0 -translate-y-2 scale-95 pointer-events-none"
                    }`}
                  >
                    {/* Header */}
                    <div className="p-4 border-b border-gray-100 flex items-center justify-between">
                      <h3 className="font-semibold text-gray-900">Notifications</h3>
                      {unreadCount > 0 && (
                        <span className="text-xs bg-red-100 text-red-600 px-2 py-1 rounded-full">
                          {unreadCount} new
                        </span>
                      )}
                    </div>

                    {/* Notifications List */}
                    <div className="max-h-80 overflow-y-auto">
                      {notificationData.slice(0, 5).map((notification, index) => (
                        <div
                          key={notification.id}
                          onClick={() => handleViewDetails(notification)}
                          className={`p-4 border-b border-gray-50 last:border-b-0 hover:bg-gray-50 transition-colors duration-150 cursor-pointer ${
                            notification.unread ? "bg-blue-50/50" : ""
                          }`}
                        >
                          <div className="flex items-start gap-3">
                            <div className="text-xl">{getNotificationIcon(notification.type)}</div>
                            <div className="flex-1 min-w-0">
                              <div className="flex items-center gap-2 mb-1">
                                <h4
                                  className={`text-sm font-medium text-gray-900 truncate ${
                                    notification.unread ? "font-semibold" : ""
                                  }`}
                                >
                                  {notification.title}
                                </h4>
                                {notification.unread && (
                                  <div className="w-2 h-2 bg-blue-500 rounded-full flex-shrink-0"></div>
                                )}
                              </div>
                              <p className="text-sm text-gray-600 line-clamp-2 mb-1">{notification.message}</p>
                              <p className="text-xs text-gray-400">{notification.time}</p>
                            </div>
                            {notification.unread && (
                              <button
                                onClick={(e) => {
                                  e.stopPropagation()
                                  handleMarkAsRead(notification.id)
                                }}
                                className="text-xs text-[#344FA5] hover:text-[#2A3F85] font-medium px-2 py-1 hover:bg-blue-100 rounded transition-colors duration-150 flex-shrink-0"
                              >
                                Mark as read
                              </button>
                            )}
                          </div>
                        </div>
                      ))}

                      {notificationData.length > 5 && (
                        <div className="px-4 py-2 text-sm text-gray-500 text-center border-t border-gray-100">
                          +{notificationData.length - 5} more notifications
                        </div>
                      )}
                    </div>

                    {/* Footer */}
                    <div className="p-3 border-t border-gray-100">
                      <button
                        onClick={handleViewAllNotifications}
                        className="w-full text-center text-sm text-[#344FA5] hover:text-[#2A3F85] font-medium transition-colors duration-150 hover:bg-blue-50 py-2 px-3 rounded-lg"
                      >
                        View All Notifications
                      </button>
                    </div>
                  </div>

                  {/* Overlay to close notifications when clicking outside */}
                  {showNotifications && (
                    <div className="fixed inset-0 z-40" onClick={() => setShowNotifications(false)}></div>
                  )}
                </div>

                {/* Logout button - Hidden on mobile */}
                <Button
                  variant="outline"
                  onClick={onLogout}
                  className="hidden lg:flex rounded-xl border-gray-200 hover:border-red-300 hover:text-red-600 transition-colors duration-200 bg-transparent flex-shrink-0"
                >
                  Logout
                </Button>
              </div>
            </div>
          </div>

          {/* Content Area */}
          <div className="flex-1 overflow-auto relative z-10">
            {activeTab === "Dashboard" && <Dashboard />}
            {activeTab === "Social Media" && <SocialMedia />}
            {activeTab === "Stats" && <StatsModule />}
            {activeTab === "Ball Track" && <BallTracking />}
            {activeTab === "Following" && <Following />}
          </div>
        </div>
      </div>

      {/* Full Notifications Modal */}
      {showAllNotifications && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm"
          onClick={() => setShowAllNotifications(false)}
        >
          <motion.div
            initial={{ opacity: 0, scale: 0.95, y: 20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.95, y: 20 }}
            transition={{ type: "spring", damping: 25, stiffness: 300 }}
            className="bg-white/95 backdrop-blur-md rounded-2xl shadow-2xl w-full max-w-2xl mx-4 max-h-[90vh] overflow-hidden transform transition-all duration-300 ease-out"
            onClick={(e) => e.stopPropagation()}
          >
            {/* Modal Header */}
            <div className="p-6 border-b border-gray-200/80 bg-gradient-to-r from-[#344FA5] to-[#4A5FB8] text-white">
              <div className="flex items-center justify-between">
                <div>
                  <h2 className="text-2xl font-bold flex items-center gap-2">
                    <Bell className="w-6 h-6 text-white/80" />
                    All Notifications
                  </h2>
                  <p className="text-blue-100 text-sm mt-1">
                    {unreadCount > 0 ? `${unreadCount} unread notifications` : "All caught up!"}
                  </p>
                </div>
                <div className="flex items-center gap-3">
                  {unreadCount > 0 && (
                    <motion.button
                      whileHover={{ scale: 1.05 }}
                      whileTap={{ scale: 0.95 }}
                      onClick={handleMarkAllAsRead}
                      className="px-4 py-2 bg-white/20 hover:bg-white/30 rounded-lg text-sm font-medium transition-all duration-300 relative overflow-hidden group"
                    >
                      <span className="absolute inset-0 bg-white/10 scale-x-0 group-hover:scale-x-100 transition-transform duration-300 origin-left rounded-md"></span>
                      <span className="relative z-10">Mark all as read</span>
                    </motion.button>
                  )}
                  <motion.button
                    whileHover={{ rotate: 90 }}
                    transition={{ type: "spring", stiffness: 300 }}
                    onClick={() => setShowAllNotifications(false)}
                    className="p-2 hover:bg-white/20 rounded-full transition-colors duration-300"
                  >
                    <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                    </svg>
                  </motion.button>
                </div>
              </div>
            </div>

            {/* Modal Content */}
            <div className="overflow-y-auto max-h-[calc(90vh-200px)] scrollbar-thin scrollbar-thumb-gray-200 scrollbar-track-transparent">
              <AnimatePresence>
                {notificationData.map((notification, index) => (
                  <motion.div
                    key={notification.id}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -20 }}
                    transition={{ delay: index * 0.05 }}
                    className={`p-6 border-b border-gray-100/50 last:border-b-0 hover:bg-gray-50/80 transition-all duration-300 ${
                      notification.unread ? "bg-blue-50/30 border-l-4 border-l-blue-500" : ""
                    }`}
                  >
                    <div className="flex items-start gap-4">
                      <motion.div
                        whileHover={{ scale: 1.1, rotate: 5 }}
                        transition={{ type: "spring", stiffness: 400 }}
                        className="text-2xl flex-shrink-0 relative"
                      >
                        <div className="absolute inset-0 bg-gray-100 rounded-full blur-md opacity-0 group-hover:opacity-70 transition-all duration-300"></div>
                        <span className="relative z-10">{getNotificationIcon(notification.type)}</span>
                      </motion.div>
                      <div className="flex-1 min-w-0">
                        <div className="flex items-start justify-between gap-4 mb-2">
                          <div className="flex items-center gap-3">
                            <h3
                              className={`text-lg font-semibold text-gray-900 ${
                                notification.unread ? "font-bold" : ""
                              }`}
                            >
                              {notification.title}
                            </h3>
                            {notification.unread && (
                              <motion.span
                                animate={{ scale: [1, 1.2, 1] }}
                                transition={{ repeat: Number.POSITIVE_INFINITY, duration: 2 }}
                                className="w-3 h-3 bg-blue-500 rounded-full flex-shrink-0"
                              ></motion.span>
                            )}
                          </div>
                          <div className="flex items-center gap-2">
                            <span className="text-sm text-gray-500 whitespace-nowrap">{notification.time}</span>
                            {notification.unread && (
                              <motion.button
                                whileHover={{ scale: 1.05 }}
                                whileTap={{ scale: 0.95 }}
                                onClick={() => handleMarkAsRead(notification.id)}
                                className="text-xs text-[#344FA5] hover:text-[#2A3F85] font-medium px-2 py-1 hover:bg-blue-50/80 rounded transition-all duration-300 relative overflow-hidden group"
                              >
                                <span className="absolute inset-0 bg-blue-100/50 scale-x-0 group-hover:scale-x-100 transition-transform duration-300 origin-left rounded-md"></span>
                                <span className="relative z-10">Mark as read</span>
                              </motion.button>
                            )}
                          </div>
                        </div>
                        <p className="text-gray-700 leading-relaxed">{notification.message}</p>
                        <div className="mt-3 flex items-center gap-4 flex-wrap">
                          <span className="text-xs text-gray-500 bg-gray-100/80 backdrop-blur-sm px-2 py-1 rounded-full capitalize shadow-sm">
                            {notification.type}
                          </span>
                          <motion.button
                            whileHover={{ scale: 1.05 }}
                            whileTap={{ scale: 0.95 }}
                            onClick={() => handleViewDetails(notification)}
                            className="text-xs text-[#344FA5] hover:text-[#2A3F85] font-medium hover:bg-blue-50/80 px-2 py-1 rounded transition-all duration-300 relative overflow-hidden group"
                          >
                            <span className="absolute inset-0 bg-blue-100/50 scale-x-0 group-hover:scale-x-100 transition-transform duration-300 origin-left rounded-md"></span>
                            <span className="relative z-10 flex items-center gap-1">
                              View Details
                              <ChevronRight className="w-3 h-3 group-hover:translate-x-1 transition-transform duration-300" />
                            </span>
                          </motion.button>
                        </div>
                      </div>
                    </div>
                  </motion.div>
                ))}
              </AnimatePresence>
            </div>

            {/* Modal Footer */}
            <div className="p-6 border-t border-gray-200/80 bg-gradient-to-b from-white/50 to-gray-50/80">
              <div className="flex items-center justify-between">
                <p className="text-sm text-gray-600">Showing {notificationData.length} notifications</p>
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={() => setShowAllNotifications(false)}
                  className="px-4 py-2 bg-gradient-to-r from-[#344FA5] to-[#4A5FB8] hover:from-[#3A57B5] hover:to-[#5269C2] text-white rounded-lg font-medium transition-all duration-300 shadow-md hover:shadow-lg"
                >
                  Close
                </motion.button>
              </div>
            </div>
          </motion.div>
        </motion.div>
      )}
    </div>
  )
}

export default function App() {
  const handleLogout = () => {
    console.log("Logging out...")
    // Add logout logic here
  }

  return <HomePage onLogout={handleLogout} />
}
