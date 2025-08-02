import { useState } from "react";
import { 
  Search, BarChart3, Menu, User, Users, Activity, Target, 
  Globe, Bell
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Sheet, SheetContent, SheetTrigger } from "@/components/ui/sheet";
import { Dashboard } from "@/components/player/home/Dashboard";
import { SocialMedia } from "@/components/player/home/SocialMedia";

interface HomePageProps {
  onLogout: () => void;
}

export const HomePage = ({ onLogout }: HomePageProps) => {
  const [activeTab, setActiveTab] = useState("Dashboard");
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [showNotifications, setShowNotifications] = useState(false);
  const [showAllNotifications, setShowAllNotifications] = useState(false);
  const [notificationData, setNotificationData] = useState([
    {
      id: 1,
      title: "Match Performance Update",
      message: "Your batting average has improved by 15% this week!",
      time: "2 minutes ago",
      type: "performance",
      unread: true
    },
    {
      id: 2,
      title: "Team Practice Session",
      message: "Tomorrow's practice session at 9:00 AM has been confirmed.",
      time: "1 hour ago",
      type: "schedule",
      unread: true
    },
    {
      id: 3,
      title: "New Follower",
      message: "Steve Smith started following you.",
      time: "3 hours ago",
      type: "social",
      unread: false
    },
    {
      id: 4,
      title: "Match Statistics Ready",
      message: "Your detailed match analysis for last game is now available.",
      time: "1 day ago",
      type: "stats",
      unread: false
    },
    {
      id: 5,
      title: "Training Video Uploaded",
      message: "New bowling technique video has been added to your library.",
      time: "2 days ago",
      type: "content",
      unread: false
    },
    {
      id: 6,
      title: "Weekly Performance Report",
      message: "Your comprehensive performance analysis for this week is ready.",
      time: "3 days ago",
      type: "stats",
      unread: false
    },
    {
      id: 7,
      title: "Team Meeting Reminder",
      message: "Don't forget about the team strategy meeting tomorrow at 2 PM.",
      time: "4 days ago",
      type: "schedule",
      unread: false
    },
    {
      id: 8,
      title: "Achievement Unlocked",
      message: "Congratulations! You've achieved 'Century Maker' milestone.",
      time: "5 days ago",
      type: "performance",
      unread: false
    },
    {
      id: 9,
      title: "Equipment Check",
      message: "Reminder: Equipment inspection scheduled for next Monday.",
      time: "1 week ago",
      type: "schedule",
      unread: false
    },
    {
      id: 10,
      title: "New Training Program",
      message: "Advanced batting techniques course is now available in your dashboard.",
      time: "1 week ago",
      type: "content",
      unread: false
    }
  ]);

  const unreadCount = notificationData.filter(n => n.unread).length;

  const handleViewAllNotifications = () => {
    setShowNotifications(false);
    setShowAllNotifications(true);
  };

  const handleMarkAsRead = (notificationId: number) => {
    setNotificationData(prev => 
      prev.map(notification => 
        notification.id === notificationId 
          ? { ...notification, unread: false }
          : notification
      )
    );
    console.log(`Notification ${notificationId} marked as read`);
  };

  const handleMarkAllAsRead = () => {
    setNotificationData(prev => 
      prev.map(notification => ({ ...notification, unread: false }))
    );
    console.log("All notifications marked as read");
  };

  const handleViewDetails = (notification: any) => {
    // Mark as read when viewing details
    if (notification.unread) {
      handleMarkAsRead(notification.id);
    }
    
    // Show notification details (you can customize this based on notification type)
    const detailsMessage = getNotificationDetails(notification);
    alert(detailsMessage);
    console.log("Viewing notification details:", notification);
  };

  const getNotificationDetails = (notification: any) => {
    switch (notification.type) {
      case 'performance':
        return `Performance Details:\n\n${notification.title}\n\n${notification.message}\n\nDetailed analysis:\n• Current batting average: 87.5\n• Improvement: +15% from last week\n• Matches played: 8\n• Best score: 156*\n\nTime: ${notification.time}`;
      
      case 'schedule':
        return `Schedule Details:\n\n${notification.title}\n\n${notification.message}\n\nEvent details:\n• Date: Tomorrow\n• Time: 9:00 AM\n• Location: Main Cricket Ground\n• Duration: 3 hours\n• Coach: Mike Johnson\n\nTime: ${notification.time}`;
      
      case 'social':
        return `Social Update:\n\n${notification.title}\n\n${notification.message}\n\nProfile details:\n• Player: Steve Smith\n• Team: Australia\n• Role: Batsman\n• Following: 1,234\n• Followers: 567,890\n\nTime: ${notification.time}`;
      
      case 'stats':
        return `Statistics Details:\n\n${notification.title}\n\n${notification.message}\n\nMatch analysis includes:\n• Batting performance\n• Bowling analysis\n• Fielding statistics\n• Comparison with previous matches\n• Areas for improvement\n\nTime: ${notification.time}`;
      
      case 'content':
        return `Content Details:\n\n${notification.title}\n\n${notification.message}\n\nVideo information:\n• Duration: 15 minutes\n• Coach: Professional Trainer\n• Skill level: Advanced\n• Topics covered: Bowling techniques\n• Available in: HD Quality\n\nTime: ${notification.time}`;
      
      default:
        return `${notification.title}\n\n${notification.message}\n\nTime: ${notification.time}`;
    }
  };

  const getNotificationIcon = (type: string) => {
    switch (type) {
      case 'performance': return '📈';
      case 'schedule': return '📅';
      case 'social': return '👥';
      case 'stats': return '📊';
      case 'content': return '🎥';
      default: return '🔔';
    }
  };

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
  ];

  // Filter players based on search query
  const filteredPlayers = players.filter(player =>
    player.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    player.team.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setSearchQuery(value);
    setShowSuggestions(value.length > 0);
  };

  const handlePlayerSelect = (playerName: string) => {
    setSearchQuery(playerName);
    setShowSuggestions(false);
    // Here you can add logic to navigate to player profile or perform search
    console.log("Selected player:", playerName);
  };

  const sidebarItems = [
    { icon: BarChart3, label: "Dashboard" },
    { icon: Globe, label: "Social Media" },
    { icon: Activity, label: "Stats" },
    { icon: Target, label: "Ball Track" },
    { icon: Users, label: "Following" },
  ];

  const SidebarContent = () => (
    <div className="flex flex-col h-full bg-white">
      {/* Profile Section */}
      <div className="p-6 border-b border-gray-100">
        <div className="flex items-center gap-3">
          <div className="relative">
            <Avatar className="w-12 md:w-16 h-12 md:h-16 border-4 border-white shadow-lg">
              <AvatarImage src="https://images.pexels.com/photos/220453/pexels-photo-220453.jpeg" />
              <AvatarFallback className="bg-[#344FA5] text-white text-lg font-bold">KW</AvatarFallback>
            </Avatar>
            <div className="absolute -bottom-1 -right-1 w-5 h-5 bg-green-500 border-2 border-white rounded-full"></div>
          </div>
          <div className="flex-1">
            <h3 className="font-bold text-base md:text-lg text-gray-900">Kane Williamson</h3>
            <p className="text-sm text-[#344FA5] font-medium">Team Newzealand</p>
            <p className="text-xs text-gray-500">Professional Cricketer</p>
          </div>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 p-4">
        <div className="space-y-2">
          {sidebarItems.map((item) => (
            <button
              key={item.label}
              onClick={() => {
                setActiveTab(item.label);
                setSidebarOpen(false);
              }}
              className={`w-full flex items-center gap-3 px-4 py-4 rounded-xl text-left transition-all duration-300 group ${
                activeTab === item.label
                  ? 'bg-[#344FA5] text-white shadow-lg transform scale-105'
                  : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900 hover:transform hover:scale-102'
              }`}
            >
              <div className={`p-2 rounded-lg ${
                activeTab === item.label 
                  ? 'bg-white/20' 
                  : 'bg-gray-100 group-hover:bg-gray-200'
              }`}>
                <item.icon className={`w-5 h-5 ${
                  activeTab === item.label 
                    ? 'text-white' 
                    : 'text-gray-700 group-hover:text-gray-900'
                }`} />
              </div>
              <span className="font-semibold">{item.label}</span>
            </button>
          ))}
        </div>
      </nav>

      {/* Footer */}
      <div className="p-4 border-t border-gray-100">
        <Button 
          variant="outline" 
          onClick={onLogout}
          className="w-full border-2 border-gray-200 hover:border-red-300 hover:text-red-600 transition-all duration-200"
        >
          <User className="w-4 h-4 mr-2" />
          Logout
        </Button>
      </div>
    </div>
  );

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="flex">
        {/* Desktop Sidebar */}
        <div className="hidden lg:block w-64 xl:w-80 bg-white shadow-lg border-r border-gray-100 min-h-screen">
          <SidebarContent />
        </div>

        {/* Mobile Sidebar */}
        <Sheet open={sidebarOpen} onOpenChange={setSidebarOpen}>
          <SheetContent side="left" className="p-0 w-80 lg:hidden">
            <SidebarContent />
          </SheetContent>
        </Sheet>

        {/* Main Content */}
        <div className="flex-1 min-w-0">
          {/* Header */}
          <div className="bg-white border-b border-gray-100 p-4 sticky top-0 z-40 shadow-sm">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-4">
                <Sheet open={sidebarOpen} onOpenChange={setSidebarOpen}>
                  <SheetTrigger asChild>
                    <Button
                      variant="ghost"
                      size="icon"
                      className="lg:hidden hover:bg-gray-100 rounded-xl"
                    >
                      <Menu className="w-6 h-6" />
                    </Button>
                  </SheetTrigger>
                </Sheet>
                
                <h1 className="text-2xl font-bold text-gray-900">{activeTab}</h1>
              </div>
              
              <div className="flex items-center gap-4">
                <div className="relative hidden sm:block">
                  <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4 z-10" />
                  <Input 
                    placeholder="Search Player"
                    value={searchQuery}
                    onChange={handleSearchChange}
                    onFocus={() => searchQuery.length > 0 && setShowSuggestions(true)}
                    onBlur={() => setTimeout(() => setShowSuggestions(false), 200)}
                    className="pl-10 w-64 xl:w-80 bg-gray-50 border-gray-200 focus:border-[#344FA5] rounded-xl transition-colors duration-200"
                  />
                  
                  {/* Search Suggestions Dropdown */}
                  {showSuggestions && filteredPlayers.length > 0 && (
                    <div className="absolute top-full left-0 right-0 mt-2 bg-white border border-gray-200 rounded-xl shadow-lg z-50 max-h-64 overflow-y-auto">
                      {filteredPlayers.slice(0, 5).map((player) => (
                        <button
                          key={player.id}
                          onClick={() => handlePlayerSelect(player.name)}
                          className="w-full px-4 py-3 text-left hover:bg-gray-50 transition-colors duration-150 border-b border-gray-100 last:border-b-0 flex items-center gap-3"
                        >
                          <div className="w-8 h-8 bg-[#344FA5] rounded-full flex items-center justify-center text-white text-sm font-bold">
                            {player.name.split(' ').map(n => n[0]).join('').slice(0, 2)}
                          </div>
                          <div className="flex-1">
                            <p className="font-medium text-gray-900">{player.name}</p>
                            <p className="text-sm text-gray-500">{player.team} • {player.role}</p>
                          </div>
                        </button>
                      ))}
                      
                      {filteredPlayers.length > 5 && (
                        <div className="px-4 py-2 text-sm text-gray-500 text-center border-t border-gray-100">
                          +{filteredPlayers.length - 5} more players
                        </div>
                      )}
                    </div>
                  )}
                  
                  {/* No results message */}
                  {showSuggestions && searchQuery.length > 0 && filteredPlayers.length === 0 && (
                    <div className="absolute top-full left-0 right-0 mt-2 bg-white border border-gray-200 rounded-xl shadow-lg z-50">
                      <div className="px-4 py-6 text-center text-gray-500">
                        <Search className="w-8 h-8 mx-auto mb-2 text-gray-300" />
                        <p>No players found for "{searchQuery}"</p>
                      </div>
                    </div>
                  )}
                </div>
                
                <Button
                  variant="ghost"
                  size="icon"
                  className="sm:hidden hover:bg-gray-100 rounded-xl"
                >
                  <Search className="w-5 h-5" />
                </Button>

                {/* Notifications */}
                <div className="relative">
                  <Button
                    variant="ghost"
                    size="icon"
                    onClick={() => setShowNotifications(!showNotifications)}
                    className="hover:bg-gray-100 rounded-xl relative"
                  >
                    <Bell className="w-5 h-5" />
                    {unreadCount > 0 && (
                      <span className="absolute -top-1 -right-1 w-5 h-5 bg-red-500 text-white text-xs rounded-full flex items-center justify-center animate-pulse">
                        {unreadCount}
                      </span>
                    )}
                  </Button>

                  {/* Notifications Panel */}
                  <div className={`absolute top-full right-0 mt-2 w-80 bg-white border border-gray-200 rounded-xl shadow-lg z-50 transform transition-all duration-300 ease-out ${
                    showNotifications 
                      ? 'opacity-100 translate-y-0 scale-100' 
                      : 'opacity-0 -translate-y-2 scale-95 pointer-events-none'
                  }`}>
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
                            notification.unread ? 'bg-blue-50/50' : ''
                          }`}
                        >
                          <div className="flex items-start gap-3">
                            <div className="text-xl">
                              {getNotificationIcon(notification.type)}
                            </div>
                            <div className="flex-1 min-w-0">
                              <div className="flex items-center gap-2 mb-1">
                                <h4 className={`text-sm font-medium text-gray-900 truncate ${
                                  notification.unread ? 'font-semibold' : ''
                                }`}>
                                  {notification.title}
                                </h4>
                                {notification.unread && (
                                  <div className="w-2 h-2 bg-blue-500 rounded-full flex-shrink-0"></div>
                                )}
                              </div>
                              <p className="text-sm text-gray-600 line-clamp-2 mb-1">
                                {notification.message}
                              </p>
                              <p className="text-xs text-gray-400">
                                {notification.time}
                              </p>
                            </div>
                            {notification.unread && (
                              <button
                                onClick={(e) => {
                                  e.stopPropagation();
                                  handleMarkAsRead(notification.id);
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
                    <div 
                      className="fixed inset-0 z-40" 
                      onClick={() => setShowNotifications(false)}
                    ></div>
                  )}
                </div>
                
                <Button 
                  variant="outline" 
                  onClick={onLogout} 
                  className="hidden sm:flex rounded-xl border-gray-200 hover:border-red-300 hover:text-red-600 transition-colors duration-200"
                >
                  Logout
                </Button>
              </div>
            </div>
          </div>

          {/* Content Area */}
          <div className="flex-1 overflow-auto">
            {activeTab === "Dashboard" && <Dashboard />}
            {activeTab === "Social Media" && <SocialMedia />}
            {activeTab === "Stats" && <div className="text-center py-20 text-gray-500">Stats content coming soon...</div>}
            {activeTab === "Ball Track" && <div className="text-center py-20 text-gray-500">Ball Track content coming soon...</div>}
            {activeTab === "Following" && <div className="text-center py-20 text-gray-500">Following content coming soon...</div>}
          </div>
        </div>
      </div>

      {/* Full Notifications Modal */}
      {showAllNotifications && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm">
          <div className="bg-white rounded-2xl shadow-2xl w-full max-w-2xl mx-4 max-h-[90vh] overflow-hidden transform transition-all duration-300 ease-out">
            {/* Modal Header */}
            <div className="p-6 border-b border-gray-200 bg-gradient-to-r from-[#344FA5] to-[#4A5FB8] text-white">
              <div className="flex items-center justify-between">
                <div>
                  <h2 className="text-2xl font-bold">All Notifications</h2>
                  <p className="text-blue-100 text-sm mt-1">
                    {unreadCount > 0 ? `${unreadCount} unread notifications` : 'All caught up!'}
                  </p>
                </div>
                <div className="flex items-center gap-3">
                  {unreadCount > 0 && (
                    <button
                      onClick={handleMarkAllAsRead}
                      className="px-4 py-2 bg-white/20 hover:bg-white/30 rounded-lg text-sm font-medium transition-colors duration-150"
                    >
                      Mark all as read
                    </button>
                  )}
                  <button
                    onClick={() => setShowAllNotifications(false)}
                    className="p-2 hover:bg-white/20 rounded-lg transition-colors duration-150"
                  >
                    <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                    </svg>
                  </button>
                </div>
              </div>
            </div>

            {/* Modal Content */}
            <div className="overflow-y-auto max-h-[calc(90vh-200px)]">
              {notificationData.map((notification) => (
                <div
                  key={notification.id}
                  className={`p-6 border-b border-gray-100 last:border-b-0 hover:bg-gray-50 transition-colors duration-150 ${
                    notification.unread ? 'bg-blue-50/30 border-l-4 border-l-blue-500' : ''
                  }`}
                >
                  <div className="flex items-start gap-4">
                    <div className="text-2xl flex-shrink-0">
                      {getNotificationIcon(notification.type)}
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-start justify-between gap-4 mb-2">
                        <div className="flex items-center gap-3">
                          <h3 className={`text-lg font-semibold text-gray-900 ${
                            notification.unread ? 'font-bold' : ''
                          }`}>
                            {notification.title}
                          </h3>
                          {notification.unread && (
                            <span className="w-3 h-3 bg-blue-500 rounded-full flex-shrink-0"></span>
                          )}
                        </div>
                        <div className="flex items-center gap-2">
                          <span className="text-sm text-gray-500 whitespace-nowrap">
                            {notification.time}
                          </span>
                          {notification.unread && (
                            <button
                              onClick={() => handleMarkAsRead(notification.id)}
                              className="text-xs text-[#344FA5] hover:text-[#2A3F85] font-medium px-2 py-1 hover:bg-blue-50 rounded transition-colors duration-150"
                            >
                              Mark as read
                            </button>
                          )}
                        </div>
                      </div>
                      <p className="text-gray-700 leading-relaxed">
                        {notification.message}
                      </p>
                      <div className="mt-3 flex items-center gap-4">
                        <span className="text-xs text-gray-500 bg-gray-100 px-2 py-1 rounded-full capitalize">
                          {notification.type}
                        </span>
                        <button 
                          onClick={() => handleViewDetails(notification)}
                          className="text-xs text-[#344FA5] hover:text-[#2A3F85] font-medium hover:bg-blue-50 px-2 py-1 rounded transition-colors duration-150"
                        >
                          View Details
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>

            {/* Modal Footer */}
            <div className="p-6 border-t border-gray-200 bg-gray-50">
              <div className="flex items-center justify-between">
                <p className="text-sm text-gray-600">
                  Showing {notificationData.length} notifications
                </p>
                <button
                  onClick={() => setShowAllNotifications(false)}
                  className="px-4 py-2 bg-[#344FA5] hover:bg-[#2A3F85] text-white rounded-lg font-medium transition-colors duration-150"
                >
                  Close
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};