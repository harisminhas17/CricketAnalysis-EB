"use client"

import type React from "react"
import { useState } from "react"
import { Search, BarChart3, Menu, User, Users, Activity, Target, Globe, Bell, ChevronRight } from 'lucide-react'
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Sheet, SheetContent, SheetTrigger } from "@/components/ui/sheet"
import { Dashboard } from "@/components/player/home/Dashboard"
import { SocialMedia } from "@/components/player/home/SocialMedia"
import { cn } from "@/lib/utils"
import { motion, AnimatePresence } from "framer-motion"
import { StatsModule } from "@/components/player/home/StatsModule"
import { BallTracking } from "@/components/player/home/BallTracking"
import { Following } from "@/components/player/home/Following"
import { ProfileManagement } from "@/components/player/profile/profile-management"
import { SideMenu, type SideMenuItem } from "@/components/navigation/side-menu"


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
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false)
  const [sidebarHovered, setSidebarHovered] = useState(false)

  const [notificationData, setNotificationData] = useState([
    { id: 1, title: "Match Performance Update", message: "Your batting average has improved by 15% this week!", time: "2 minutes ago", type: "performance", unread: true },
    { id: 2, title: "Team Practice Session", message: "Tomorrow's practice session at 9:00 AM has been confirmed.", time: "1 hour ago", type: "schedule", unread: true },
    { id: 3, title: "New Follower", message: "Steve Smith started following you.", time: "3 hours ago", type: "social", unread: false },
    { id: 4, title: "Match Statistics Ready", message: "Your detailed match analysis for last game is now available.", time: "1 day ago", type: "stats", unread: false },
    { id: 5, title: "Training Video Uploaded", message: "New bowling technique video has been added to your library.", time: "2 days ago", type: "content", unread: false },
    { id: 6, title: "Weekly Performance Report", message: "Your comprehensive performance analysis for this week is ready.", time: "3 days ago", type: "stats", unread: false },
    { id: 7, title: "Team Meeting Reminder", message: "Don't forget about the team strategy meeting tomorrow at 2 PM.", time: "4 days ago", type: "schedule", unread: false },
    { id: 8, title: "Achievement Unlocked", message: "Congratulations! You've achieved 'Century Maker' milestone.", time: "5 days ago", type: "performance", unread: false },
    { id: 9, title: "Equipment Check", message: "Reminder: Equipment inspection scheduled for next Monday.", time: "1 week ago", type: "schedule", unread: false },
    { id: 10, title: "New Training Program", message: "Advanced batting techniques course is now available in your dashboard.", time: "1 week ago", type: "content", unread: false },
  ])

  const unreadCount = notificationData.filter((n) => n.unread).length

  const handleViewAllNotifications = () => {
    setShowNotifications(false)
    setShowAllNotifications(true)
  }

  const handleMarkAsRead = (notificationId: number) => {
    setNotificationData((prev) => prev.map((n) => (n.id === notificationId ? { ...n, unread: false } : n)))
  }

  const handleMarkAllAsRead = () => {
    setNotificationData((prev) => prev.map((n) => ({ ...n, unread: false })))
  }

  const handleViewDetails = (notification: any) => {
    if (notification.unread) handleMarkAsRead(notification.id)
    alert(`${notification.title}

${notification.message}

Time: ${notification.time}`)
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

  // Sample players
  const players = [
    { id: 1, name: "Kane Williamson", team: "New Zealand", role: "Batsman" },
    { id: 2, name: "Virat Kohli", team: "India", role: "Batsman" },
    { id: 3, name: "Steve Smith", team: "Australia", role: "Batsman" },
    { id: 4, name: "Joe Root", team: "England", role: "Batsman" },
    { id: 5, name: "Babar Azam", team: "Pakistan", role: "Batsman" },
    { id: 6, name: "Pat Cummins", team: "Australia", role: "Bowler" },
    { id: 7, name: "Jasprit  Bumrah", team: "India", role: "Bowler" },
    { id: 8, name: "Trent Boult", team: "New Zealand", role: "Bowler" },
    { id: 9, name: "Kagiso Rabada", team: "South Africa", role: "Bowler" },
    { id: 10, name: "Ben Stokes", team: "England", role: "All-rounder" },
  ]

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
  }

  const items: SideMenuItem[] = [
    { icon: BarChart3, label: "Dashboard" },
    { icon: Globe, label: "Social Media" },
    { icon: Activity, label: "Stats" },
    { icon: Target, label: "Ball Track" },
    { icon: Users, label: "Following" },
    { icon: User, label: "Profile" },
  ]

  const menuFooter = (
    <Button
      variant="outline"
      onClick={onLogout}
      className="w-full border-2 border-gray-200 hover:border-red-300 hover:text-red-600 transition-all duration-300 group relative overflow-hidden bg-white/80 backdrop-blur-sm hover:shadow-md"
    >
      <span className="absolute inset-0 bg-red-500/10 scale-x-0 group-hover:scale-x-100 transition-transform duration-300 origin-left rounded-md" />
      <User className="relative z-10 group-hover:scale-110 transition-transform duration-300 flex-shrink-0 w-4 h-4 mr-2" />
      <span className="relative z-10">Logout</span>
    </Button>
  )

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="flex">
        {/* Desktop Sidebar */}
        <div
          className={cn(
            "hidden lg:block bg-white shadow-lg border-r border-gray-100 min-h-screen transition-all duration-300 ease-in-out relative z-30",
            sidebarCollapsed && !sidebarHovered ? "w-16" : "w-56 xl:w-64",
          )}
          onMouseEnter={() => setSidebarHovered(true)}
          onMouseLeave={() => setSidebarHovered(false)}
        >
          <SideMenu
            items={items}
            activeLabel={activeTab}
            onSelect={(label) => {
              setActiveTab(label)
              setSidebarOpen(false)
            }}
            collapsed={sidebarCollapsed}
            hovered={sidebarHovered}
            onToggleCollapse={() => setSidebarCollapsed((v) => !v)}
            profile={{
              name: "Kane Williamson",
              team: "Team Newzealand",
              status: "Professional Cricketer",
            }}
            footer={menuFooter}
          />
        </div>

        {/* Mobile Sidebar */}
        <Sheet open={sidebarOpen} onOpenChange={setSidebarOpen}>
          <SheetContent side="left" className="p-0 w-80 lg:hidden">
            <SideMenu
              items={items}
              activeLabel={activeTab}
              onSelect={(label) => {
                setActiveTab(label)
                setSidebarOpen(false)
              }}
              collapsed={false}
              hovered={true}
              profile={{
                name: "Kane Williamson",
                team: "Team Newzealand",
                status: "Professional Cricketer",
              }}
              footer={menuFooter}
              // hide collapse on mobile
              onToggleCollapse={undefined}
            />
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
                      <span className="absolute inset-0 bg-gray-100/80 scale-0 group-hover:scale-100 transition-transform duration-300 rounded-full" />
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
                {/* Search */}
                <div className="relative hidden md:block group">
                  <div className="absolute inset-0 bg-gray-100/50 rounded-xl blur-sm group-hover:bg-gray-100/80 transition-colors duration-300" />
                  <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 w-4 h-4 z-10" />
                  <Input
                    placeholder="Search Player"
                    value={searchQuery}
                    onChange={handleSearchChange}
                    onFocus={() => searchQuery.length > 0 && setShowSuggestions(true)}
                    onBlur={() => setTimeout(() => setShowSuggestions(false), 200)}
                    className="pl-10 w-48 lg:w-64 xl:w-80 bg-white/80 border-gray-100/80 focus:border-[#344FA5]/30 focus:ring-[#344FA5]/20 rounded-xl transition-all duration-300 relative z-10"
                  />

                  {/* Suggestions */}
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
                            <div className="absolute inset-0 bg-gradient-to-r from-transparent via-[#344FA5]/5 to-transparent -translate-x-full group-hover:translate-x-full transition-transform duration-1000 ease-in-out" />

                            <div className="relative">
                              <div className="absolute inset-0 bg-gradient-to-r from-[#344FA5]/20 to-[#4A5FB8]/20 rounded-full blur-sm opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
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
                    <span className="absolute inset-0 bg-gray-100/80 scale-0 group-hover:scale-100 transition-transform duration-300 rounded-full" />
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
                    className={cn(
                      "absolute top-full right-0 mt-2 w-80 bg-white/95 backdrop-blur-sm border border-gray-200/80 rounded-xl shadow-xl z-50 transform transition-all duration-300 ease-out",
                      showNotifications ? "opacity-100 translate-y-0 scale-100" : "opacity-0 -translate-y-2 scale-95 pointer-events-none",
                    )}
                  >
                    <div className="p-4 border-b border-gray-100 flex items-center justify-between">
                      <h3 className="font-semibold text-gray-900">Notifications</h3>
                      {unreadCount > 0 && (
                        <span className="text-xs bg-red-100 text-red-600 px-2 py-1 rounded-full">{unreadCount} new</span>
                      )}
                    </div>

                    <div className="max-h-80 overflow-y-auto">
                      {notificationData.slice(0, 5).map((notification) => (
                        <div
                          key={notification.id}
                          onClick={() => handleViewDetails(notification)}
                          className={cn(
                            "p-4 border-b border-gray-50 last:border-b-0 hover:bg-gray-50 transition-colors duration-150 cursor-pointer",
                            notification.unread ? "bg-blue-50/50" : "",
                          )}
                        >
                          <div className="flex items-start gap-3">
                            <div className="text-xl">{getNotificationIcon(notification.type)}</div>
                            <div className="flex-1 min-w-0">
                              <div className="flex items-center gap-2 mb-1">
                                <h4
                                  className={cn(
                                    "text-sm font-medium text-gray-900 truncate",
                                    notification.unread ? "font-semibold" : "",
                                  )}
                                >
                                  {notification.title}
                                </h4>
                                {notification.unread && <div className="w-2 h-2 bg-blue-500 rounded-full flex-shrink-0" />}
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

                    <div className="p-3 border-t border-gray-100">
                      <button
                        onClick={handleViewAllNotifications}
                        className="w-full text-center text-sm text-[#344FA5] hover:text-[#2A3F85] font-medium transition-colors duration-150 hover:bg-blue-50 py-2 px-3 rounded-lg"
                      >
                        View All Notifications
                      </button>
                    </div>
                  </div>

                  {showNotifications && <div className="fixed inset-0 z-40" onClick={() => setShowNotifications(false)} />}
                </div>

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
            {activeTab === "Profile" && <ProfileManagement />}
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
            <div className="p-6 border-b border-gray-200/80 bg-gradient-to-r from-[#344FA5] to-[#4A5FB8] text-white">
              <div className="flex items-center justify-between">
                <div>
                  <h2 className="text-2xl font-bold flex items-center gap-2">All Notifications</h2>
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
                      <span className="absolute inset-0 bg-white/10 scale-x-0 group-hover:scale-x-100 transition-transform duration-300 origin-left rounded-md" />
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
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d={"M6 18L18 6M6 6l12 12"} />
                    </svg>
                  </motion.button>
                </div>
              </div>
            </div>

            <div className="overflow-y-auto max-h-[calc(90vh-200px)]">
              {notificationData.map((n) => (
                <div
                  key={n.id}
                  className={cn(
                    "p-6 border-b border-gray-100/50 last:border-b-0 hover:bg-gray-50/80 transition-all duration-300",
                    n.unread ? "bg-blue-50/30 border-l-4 border-l-blue-500" : "",
                  )}
                >
                  <div className="flex items-start gap-4">
                    <div className="text-2xl flex-shrink-0">{getNotificationIcon(n.type)}</div>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-start justify-between gap-4 mb-2">
                        <h3 className={cn("text-lg font-semibold text-gray-900", n.unread ? "font-bold" : "")}>
                          {n.title}
                        </h3>
                        <span className="text-sm text-gray-500 whitespace-nowrap">{n.time}</span>
                      </div>
                      <p className="text-gray-700 leading-relaxed">{n.message}</p>
                    </div>
                  </div>
                </div>
              ))}
            </div>

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
  }
  return <HomePage onLogout={handleLogout} />
}
