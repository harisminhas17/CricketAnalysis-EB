"use client"

import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Sparkles } from 'lucide-react'
import { cn } from "@/lib/utils"

export type ProfileSummaryProps = {
  name: string
  team: string
  status?: string
  avatarSrc?: string
  initials?: string
  profileHref?: string
  collapsed?: boolean
  hovered?: boolean
}

export function ProfileSummary({
  name,
  team,
  status = "Professional Cricketer",
  avatarSrc = "/placeholder.svg?height=72&width=72&text=KW",
  initials = "KW",
  profileHref = "/profile",
  collapsed = false,
  hovered = false,
}: ProfileSummaryProps) {
  return (
    <div className="p-4 lg:p-6 border-b border-gray-100/50 relative overflow-hidden">
      {/* Subtle decorative gradients */}
      <div className="absolute -top-12 -right-12 w-32 h-32 bg-gradient-to-br from-[#344FA5]/10 to-[#344FA5]/5 rounded-full blur-xl" />
      <div className="absolute -bottom-8 -left-8 w-24 h-24 bg-gradient-to-tr from-[#344FA5]/10 to-[#344FA5]/5 rounded-full blur-lg" />

      <div className="relative flex items-center gap-3 lg:gap-4">
        <div className="relative group flex-shrink-0">
          <div className="absolute inset-0 bg-gradient-to-r from-[#344FA5] to-[#4A5FB8] rounded-full blur-md opacity-50 group-hover:opacity-70 transition-all duration-500" />
          <a href={profileHref} aria-label="Open profile" className="block">
            <Avatar className="border-2 border-white shadow-lg relative hover:scale-105 transition-all duration-300 w-10 h-10 lg:w-12 lg:h-12">
              <AvatarImage src={avatarSrc || "/placeholder.svg"} className="object-cover" />
              <AvatarFallback className="bg-gradient-to-br from-[#344FA5] to-[#4A5FB8] text-white font-bold text-sm lg:text-base">
                {initials}
              </AvatarFallback>
            </Avatar>
          </a>
          <div className="absolute -bottom-1 -right-1 w-3 h-3 lg:w-3.5 lg:h-3.5 bg-green-500 border-2 border-white rounded-full shadow-md animate-pulse" />
        </div>

        <div
          className={cn(
            "flex-1 min-w-0 transition-all duration-300 ease-in-out",
            collapsed && !hovered ? "opacity-0 w-0 overflow-hidden ml-0" : "opacity-100 ml-0",
          )}
        >
          <h3 className="font-bold text-sm lg:text-base text-gray-900 flex items-center truncate">
            {name}
            <span className="ml-2 inline-flex items-center justify-center flex-shrink-0">
              <Sparkles className="w-3 h-3 text-yellow-500" />
            </span>
          </h3>
          <p className="text-xs lg:text-sm text-[#344FA5] font-medium truncate">{team}</p>
          <p className="text-xs text-gray-500 flex items-center gap-1 truncate">
            <span className="inline-block w-1.5 h-1.5 lg:w-2 lg:h-2 bg-green-500 rounded-full flex-shrink-0" />
            {status}
          </p>
        </div>
      </div>
    </div>
  )
}
