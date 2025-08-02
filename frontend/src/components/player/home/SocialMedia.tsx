import React from 'react';
import { 
  Hash, Calendar, Users, Video, Plus, Heart, 
  MessageCircle, Share, Camera, Play
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Badge } from "@/components/ui/badge";

export const SocialMedia = () => {
  const suggestedPlayers = [
    { name: "Zakary Glen Foulkes", team: "Team Newzealand", avatar: "https://images.pexels.com/photos/220453/pexels-photo-220453.jpeg" },
    { name: "Jacob Andrew Duffy", team: "Team Newzealand", avatar: "https://images.pexels.com/photos/220453/pexels-photo-220453.jpeg" },
    { name: "Mitchell Josef", team: "Team Newzealand", avatar: "https://images.pexels.com/photos/220453/pexels-photo-220453.jpeg" },
  ];

  const trendingTopics = ["#AsiaCup2025", "#Viral100", "#BabarKing"];
  
  const upcomingMatches = [
    { title: "Next Match", teams: "Team Newzealand vs. Pakistan", time: "Today 3:00 PM" },
    { title: "Following Match", teams: "Team Newzealand vs. Australia", time: "Tomorrow 5:00 PM" },
  ];

  const posts = [
    {
      id: 1,
      user: "Kane Williamson",
      team: "Team Newzealand",
      time: "Yesterday",
      content: "Scored 78 runs today!",
      description: "Incredible performance at the stadium! #CricketFever #KaneOnFire",
      image: "https://images.pexels.com/photos/1661950/pexels-photo-1661950.jpeg",
      likes: 11,
      comments: 6,
      shares: 5,
    },
    {
      id: 2,
      user: "Kane Williamson",
      team: "Team Newzealand",
      time: "2 days ago",
      content: "Great training session with the team!",
      description: "Working hard for the upcoming matches. Team spirit is high! #TeamWork #Cricket",
      image: "https://images.pexels.com/photos/1661950/pexels-photo-1661950.jpeg",
      likes: 24,
      comments: 12,
      shares: 8,
    },
  ];

  return (
    <div className="space-y-6 p-4 md:p-6">
      <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">
        {/* Main Feed */}
        <div className="xl:col-span-2 space-y-6">
          {/* Post Creation */}
          <Card className="border-0 shadow-md">
            <CardContent className="p-4">
              <div className="flex items-center gap-3">
                <Avatar className="flex-shrink-0">
                  <AvatarImage src="https://images.pexels.com/photos/220453/pexels-photo-220453.jpeg" />
                  <AvatarFallback className="bg-[#344FA5] text-white">KW</AvatarFallback>
                </Avatar>
                <Input 
                  placeholder="What's your match update?"
                  className="flex-1 border-gray-200 rounded-full focus:border-[#344FA5] transition-colors duration-200"
                />
                <div className="hidden sm:flex gap-2">
                  <Button size="sm" variant="ghost" className="rounded-full hover:bg-[#344FA5]/10 hover:text-[#344FA5]">
                    <Hash className="w-4 h-4" />
                  </Button>
                  <Button size="sm" variant="ghost" className="rounded-full hover:bg-[#344FA5]/10 hover:text-[#344FA5]">
                    <Camera className="w-4 h-4" />
                  </Button>
                  <Button size="sm" variant="ghost" className="rounded-full hover:bg-[#344FA5]/10 hover:text-[#344FA5]">
                    <Video className="w-4 h-4" />
                  </Button>
                </div>
                <Button size="sm" className="sm:hidden rounded-full bg-[#344FA5] hover:bg-[#2A3F85]">
                  <Plus className="w-4 h-4" />
                </Button>
              </div>
            </CardContent>
          </Card>

          {/* Posts */}
          {posts.map((post) => (
            <Card key={post.id} className="border-0 shadow-md hover:shadow-lg transition-all duration-300">
              <CardContent className="p-6">
                <div className="flex items-center gap-3 mb-4">
                  <Avatar className="flex-shrink-0">
                    <AvatarImage src="https://images.pexels.com/photos/220453/pexels-photo-220453.jpeg" />
                    <AvatarFallback className="bg-[#344FA5] text-white">KW</AvatarFallback>
                  </Avatar>
                  <div className="min-w-0 flex-1">
                    <h4 className="font-semibold text-foreground truncate">{post.user}</h4>
                    <p className="text-sm text-muted-foreground truncate">{post.team}</p>
                  </div>
                  <span className="text-sm text-muted-foreground flex-shrink-0">{post.time}</span>
                </div>
                
                <h3 className="text-lg font-semibold mb-2">{post.content}</h3>
                <p className="text-muted-foreground mb-4">{post.description}</p>
                
                <div className="relative rounded-xl h-48 sm:h-64 mb-4 overflow-hidden">
                  <img 
                    src={post.image} 
                    alt="Cricket post"
                    className="w-full h-full object-cover"
                  />
                  <div className="absolute inset-0 bg-gradient-to-t from-black/20 to-transparent"></div>
                </div>
                
                <div className="flex items-center justify-between pt-4 border-t border-gray-100">
                  <div className="flex items-center gap-6">
                    <button className="flex items-center gap-2 text-muted-foreground hover:text-red-500 transition-colors duration-200 group">
                      <Heart className="w-5 h-5 group-hover:scale-110 transition-transform duration-200" />
                      <span className="text-sm">{post.likes}</span>
                    </button>
                    <button className="flex items-center gap-2 text-muted-foreground hover:text-[#344FA5] transition-colors duration-200 group">
                      <MessageCircle className="w-5 h-5 group-hover:scale-110 transition-transform duration-200" />
                      <span className="text-sm">{post.comments}</span>
                    </button>
                    <button className="flex items-center gap-2 text-muted-foreground hover:text-green-500 transition-colors duration-200 group">
                      <Share className="w-5 h-5 group-hover:scale-110 transition-transform duration-200" />
                      <span className="text-sm">{post.shares}</span>
                    </button>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        {/* Right Sidebar */}
        <div className="space-y-6">
          {/* Suggested Players */}
          <Card className="border-0 shadow-md">
            <CardContent className="p-4">
              <h3 className="font-semibold mb-4">Suggested Players</h3>
              <div className="space-y-3">
                {suggestedPlayers.map((player, index) => (
                  <div key={index} className="flex items-center justify-between gap-3">
                    <div className="flex items-center gap-3 min-w-0 flex-1">
                      <Avatar className="w-10 h-10 flex-shrink-0">
                        <AvatarImage src={player.avatar} />
                        <AvatarFallback className="bg-[#344FA5] text-white">{player.name.slice(0, 2)}</AvatarFallback>
                      </Avatar>
                      <div className="min-w-0 flex-1">
                        <p className="font-medium text-sm truncate">{player.name}</p>
                        <p className="text-xs text-muted-foreground truncate">{player.team}</p>
                      </div>
                    </div>
                    <Button 
                      size="sm" 
                      variant="outline" 
                      className="flex-shrink-0 rounded-full border-[#344FA5] text-[#344FA5] hover:bg-[#344FA5] hover:text-white transition-colors duration-200"
                    >
                      Follow
                    </Button>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Trending */}
          <Card className="border-0 shadow-md">
            <CardContent className="p-4">
              <h3 className="font-semibold mb-4">Trending</h3>
              <div className="space-y-3">
                {trendingTopics.map((topic, index) => (
                  <div key={index} className="flex items-center gap-2 p-2 hover:bg-gray-50 rounded-lg cursor-pointer transition-colors duration-200">
                    <Hash className="w-4 h-4 text-[#344FA5] flex-shrink-0" />
                    <span className="text-[#344FA5] font-medium">{topic}</span>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Upcoming Matches */}
          <Card className="border-0 shadow-md">
            <CardContent className="p-4">
              <h3 className="font-semibold mb-4">Upcoming Matches</h3>
              <div className="space-y-4">
                {upcomingMatches.map((match, index) => (
                  <div key={index} className="flex items-center gap-3 p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors duration-200">
                    <div className="w-10 h-10 bg-[#344FA5]/10 rounded-lg flex items-center justify-center flex-shrink-0">
                      <Calendar className="w-5 h-5 text-[#344FA5]" />
                    </div>
                    <div className="min-w-0 flex-1">
                      <p className="font-medium text-sm">{match.title}</p>
                      <p className="text-xs text-muted-foreground truncate">{match.teams}</p>
                      <p className="text-xs text-muted-foreground">{match.time}</p>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
};