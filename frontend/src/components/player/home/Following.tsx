"use client"

import { useState } from "react"
import { Search, UserPlus, UserMinus, Users, UserCheck, Filter, Star, Shield } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Badge } from "@/components/ui/badge"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { motion, AnimatePresence } from "framer-motion"

export const Following = () => {
  const [searchQuery, setSearchQuery] = useState("")
  const [filterType, setFilterType] = useState("all")
  const [activeTab, setActiveTab] = useState("following")

  const [followingList, setFollowingList] = useState([
    {
      id: 1,
      name: "Virat Kohli",
      username: "@virat.kohli",
      team: "India",
      role: "Batsman",
      avatar: "/placeholder.svg?height=40&width=40&text=VK",
      verified: true,
      followers: "45.2M",
      isFollowing: true,
      mutualFollowers: 12,
      lastActive: "2 hours ago",
    },
    {
      id: 2,
      name: "Steve Smith",
      username: "@steve.smith",
      team: "Australia",
      role: "Batsman",
      avatar: "/placeholder.svg?height=40&width=40&text=SS",
      verified: true,
      followers: "2.8M",
      isFollowing: true,
      mutualFollowers: 8,
      lastActive: "1 day ago",
    },
    {
      id: 3,
      name: "Joe Root",
      username: "@joe.root",
      team: "England",
      role: "Batsman",
      avatar: "/placeholder.svg?height=40&width=40&text=JR",
      verified: true,
      followers: "1.9M",
      isFollowing: true,
      mutualFollowers: 15,
      lastActive: "3 hours ago",
    },
    {
      id: 4,
      name: "Babar Azam",
      username: "@babar.azam",
      team: "Pakistan",
      role: "Batsman",
      avatar: "/placeholder.svg?height=40&width=40&text=BA",
      verified: true,
      followers: "3.1M",
      isFollowing: true,
      mutualFollowers: 6,
      lastActive: "5 hours ago",
    },
    {
      id: 5,
      name: "Pat Cummins",
      username: "@pat.cummins",
      team: "Australia",
      role: "Bowler",
      avatar: "/placeholder.svg?height=40&width=40&text=PC",
      verified: false,
      followers: "890K",
      isFollowing: true,
      mutualFollowers: 4,
      lastActive: "1 hour ago",
    },
  ])

  const [followersList, setFollowersList] = useState([
    {
      id: 6,
      name: "Trent Boult",
      username: "@trent.boult",
      team: "New Zealand",
      role: "Bowler",
      avatar: "/placeholder.svg?height=40&width=40&text=TB",
      verified: true,
      followers: "1.2M",
      isFollowing: false,
      mutualFollowers: 3,
      lastActive: "30 minutes ago",
    },
    {
      id: 7,
      name: "Kagiso Rabada",
      username: "@kagiso.rabada",
      team: "South Africa",
      role: "Bowler",
      avatar: "/placeholder.svg?height=40&width=40&text=KR",
      verified: true,
      followers: "980K",
      isFollowing: true,
      mutualFollowers: 7,
      lastActive: "2 hours ago",
    },
    {
      id: 8,
      name: "Ben Stokes",
      username: "@ben.stokes",
      team: "England",
      role: "All-rounder",
      avatar: "/placeholder.svg?height=40&width=40&text=BS",
      verified: true,
      followers: "2.5M",
      isFollowing: false,
      mutualFollowers: 9,
      lastActive: "4 hours ago",
    },
    {
      id: 9,
      name: "Jasprit Bumrah",
      username: "@jasprit.bumrah",
      team: "India",
      role: "Bowler",
      avatar: "/placeholder.svg?height=40&width=40&text=JB",
      verified: true,
      followers: "3.8M",
      isFollowing: true,
      mutualFollowers: 11,
      lastActive: "6 hours ago",
    },
    {
      id: 10,
      name: "David Warner",
      username: "@david.warner",
      team: "Australia",
      role: "Batsman",
      avatar: "/placeholder.svg?height=40&width=40&text=DW",
      verified: true,
      followers: "4.2M",
      isFollowing: false,
      mutualFollowers: 5,
      lastActive: "1 day ago",
    },
  ])

  const handleFollow = (userId, listType) => {
    if (listType === "followers") {
      setFollowersList((prev) =>
        prev.map((user) => (user.id === userId ? { ...user, isFollowing: !user.isFollowing } : user)),
      )
    } else {
      setFollowingList((prev) =>
        prev.map((user) => (user.id === userId ? { ...user, isFollowing: !user.isFollowing } : user)),
      )
    }
  }

  const handleUnfollow = (userId) => {
    setFollowingList((prev) => prev.filter((user) => user.id !== userId))
  }

  const handleViewProfile = (user) => {
    console.log("Viewing profile:", user)
    // In a real app, this would navigate to the user's profile
    alert(`Viewing ${user.name}'s profile:

Team: ${user.team}
Role: ${user.role}
Followers: ${user.followers}
Username: ${user.username}
Last Active: ${user.lastActive}`)
  }

  const filterUsers = (users) => {
    return users.filter((user) => {
      const matchesSearch =
        user.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        user.team.toLowerCase().includes(searchQuery.toLowerCase()) ||
        user.username.toLowerCase().includes(searchQuery.toLowerCase())

      const matchesFilter =
        filterType === "all" ||
        (filterType === "verified" && user.verified) ||
        (filterType === "recent" && user.lastActive.includes("hour")) ||
        (filterType === "team" && user.team === "New Zealand")

      return matchesSearch && matchesFilter
    })
  }

  const filteredFollowing = filterUsers(followingList)
  const filteredFollowers = filterUsers(followersList)

  return (
    <div className="space-y-6 p-4 md:p-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-2xl font-bold text-gray-900">Social Network</h2>
          <p className="text-gray-600">Manage your cricket community connections</p>
        </div>
        <div className="flex items-center gap-2 text-sm text-gray-600">
          <Users className="w-4 h-4" />
          <span>
            {followingList.length} Following • {followersList.length} Followers
          </span>
        </div>
      </div>

      {/* Search and Filter */}
      <Card className="border-0 shadow-md">
        <CardContent className="p-4">
          <div className="flex flex-col sm:flex-row gap-4">
            <div className="relative flex-1">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
              <Input
                placeholder="Search by name, team, or username..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="pl-10"
              />
            </div>
            <Select value={filterType} onValueChange={setFilterType}>
              <SelectTrigger className="w-48">
                <Filter className="w-4 h-4 mr-2" />
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Users</SelectItem>
                <SelectItem value="verified">Verified Only</SelectItem>
                <SelectItem value="recent">Recently Active</SelectItem>
                <SelectItem value="team">Team Members</SelectItem>
              </SelectContent>
            </Select>
          </div>
        </CardContent>
      </Card>

      {/* Tabs */}
      <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
        <TabsList className="grid w-full grid-cols-2">
          <TabsTrigger value="following" className="flex items-center gap-2">
            <UserCheck className="w-4 h-4" />
            Following ({followingList.length})
          </TabsTrigger>
          <TabsTrigger value="followers" className="flex items-center gap-2">
            <Users className="w-4 h-4" />
            Followers ({followersList.length})
          </TabsTrigger>
        </TabsList>

        <TabsContent value="following" className="mt-6">
          <Card className="border-0 shadow-md">
            <CardHeader>
              <CardTitle>People You Follow</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <AnimatePresence>
                  {filteredFollowing.map((user, index) => (
                    <motion.div
                      key={user.id}
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      exit={{ opacity: 0, y: -20 }}
                      transition={{ delay: index * 0.05 }}
                      className="flex items-center justify-between p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors duration-200"
                    >
                      <div className="flex items-center gap-4 flex-1 min-w-0">
                        <div className="relative">
                          <Avatar className="w-12 h-12">
                            <AvatarImage src={user.avatar || "/placeholder.svg"} />
                            <AvatarFallback className="bg-[#344FA5] text-white">
                              {user.name
                                .split(" ")
                                .map((n) => n[0])
                                .join("")}
                            </AvatarFallback>
                          </Avatar>
                          {user.verified && (
                            <div className="absolute -bottom-1 -right-1 w-5 h-5 bg-blue-500 rounded-full flex items-center justify-center">
                              <Shield className="w-3 h-3 text-white" />
                            </div>
                          )}
                        </div>

                        <div className="flex-1 min-w-0">
                          <div className="flex items-center gap-2 mb-1">
                            <h4 className="font-semibold text-gray-900 truncate">{user.name}</h4>
                            {user.verified && (
                              <Badge variant="secondary" className="text-xs">
                                <Star className="w-3 h-3 mr-1" />
                                Verified
                              </Badge>
                            )}
                          </div>
                          <p className="text-sm text-gray-600 truncate">{user.username}</p>
                          <div className="flex items-center gap-4 mt-1 text-xs text-gray-500">
                            <span>
                              {user.team} • {user.role}
                            </span>
                            <span>{user.followers} followers</span>
                            <span>{user.mutualFollowers} mutual</span>
                          </div>
                        </div>
                      </div>

                      <div className="flex items-center gap-2 ml-4">
                        <Button
                          size="sm"
                          variant="outline"
                          onClick={() => handleViewProfile(user)}
                          className="hidden sm:flex"
                        >
                          View Profile
                        </Button>
                        <Button
                          size="sm"
                          variant="outline"
                          onClick={() => handleUnfollow(user.id)}
                          className="text-red-600 hover:text-red-700 hover:bg-red-50 border-red-200"
                        >
                          <UserMinus className="w-4 h-4 mr-1" />
                          Unfollow
                        </Button>
                      </div>
                    </motion.div>
                  ))}
                </AnimatePresence>
              </div>

              {filteredFollowing.length === 0 && (
                <div className="text-center py-8 text-gray-500">
                  <Users className="w-12 h-12 mx-auto mb-4 text-gray-300" />
                  <p>No users found matching your criteria</p>
                </div>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="followers" className="mt-6">
          <Card className="border-0 shadow-md">
            <CardHeader>
              <CardTitle>Your Followers</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <AnimatePresence>
                  {filteredFollowers.map((user, index) => (
                    <motion.div
                      key={user.id}
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      exit={{ opacity: 0, y: -20 }}
                      transition={{ delay: index * 0.05 }}
                      className="flex items-center justify-between p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors duration-200"
                    >
                      <div className="flex items-center gap-4 flex-1 min-w-0">
                        <div className="relative">
                          <Avatar className="w-12 h-12">
                            <AvatarImage src={user.avatar || "/placeholder.svg"} />
                            <AvatarFallback className="bg-[#344FA5] text-white">
                              {user.name
                                .split(" ")
                                .map((n) => n[0])
                                .join("")}
                            </AvatarFallback>
                          </Avatar>
                          {user.verified && (
                            <div className="absolute -bottom-1 -right-1 w-5 h-5 bg-blue-500 rounded-full flex items-center justify-center">
                              <Shield className="w-3 h-3 text-white" />
                            </div>
                          )}
                        </div>

                        <div className="flex-1 min-w-0">
                          <div className="flex items-center gap-2 mb-1">
                            <h4 className="font-semibold text-gray-900 truncate">{user.name}</h4>
                            {user.verified && (
                              <Badge variant="secondary" className="text-xs">
                                <Star className="w-3 h-3 mr-1" />
                                Verified
                              </Badge>
                            )}
                          </div>
                          <p className="text-sm text-gray-600 truncate">{user.username}</p>
                          <div className="flex items-center gap-4 mt-1 text-xs text-gray-500">
                            <span>
                              {user.team} • {user.role}
                            </span>
                            <span>{user.followers} followers</span>
                            <span>Active {user.lastActive}</span>
                          </div>
                        </div>
                      </div>

                      <div className="flex items-center gap-2 ml-4">
                        <Button
                          size="sm"
                          variant="outline"
                          onClick={() => handleViewProfile(user)}
                          className="hidden sm:flex"
                        >
                          View Profile
                        </Button>
                        <Button
                          size="sm"
                          onClick={() => handleFollow(user.id, "followers")}
                          className={`${
                            user.isFollowing
                              ? "bg-gray-200 text-gray-700 hover:bg-gray-300"
                              : "bg-[#344FA5] hover:bg-[#2A3F85] text-white"
                          }`}
                        >
                          {user.isFollowing ? (
                            <>
                              <UserCheck className="w-4 h-4 mr-1" />
                              Following
                            </>
                          ) : (
                            <>
                              <UserPlus className="w-4 h-4 mr-1" />
                              Follow Back
                            </>
                          )}
                        </Button>
                      </div>
                    </motion.div>
                  ))}
                </AnimatePresence>
              </div>

              {filteredFollowers.length === 0 && (
                <div className="text-center py-8 text-gray-500">
                  <Users className="w-12 h-12 mx-auto mb-4 text-gray-300" />
                  <p>No followers found matching your criteria</p>
                </div>
              )}
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}
