"use client"

import { ChevronRight } from 'lucide-react'
import { cn } from "@/lib/utils"
import { ProfileSummary, type ProfileSummaryProps } from "@/components/player/profile/profile-summary"
import type { LucideIcon } from "lucide-react"

export type SideMenuItem = {
  icon: LucideIcon
  label: string
  href?: string
}

export type SideMenuProps = {
  items: SideMenuItem[]
  activeLabel?: string
  onSelect?: (label: string) => void
  collapsed?: boolean
  hovered?: boolean
  onToggleCollapse?: () => void
  hideCollapseOnMobile?: boolean
  footer?: React.ReactNode
  profile: Omit<ProfileSummaryProps, "collapsed" | "hovered">
}

export function SideMenu({
  items,
  activeLabel,
  onSelect,
  collapsed = false,
  hovered = false,
  onToggleCollapse,
  hideCollapseOnMobile = true,
  footer,
  profile,
}: SideMenuProps) {
  return (
    <div className="flex flex-col h-full bg-white/95 backdrop-blur-sm transition-all duration-300 ease-in-out">
      <ProfileSummary {...profile} collapsed={collapsed} hovered={hovered} />

      {/* Navigation */}
      <nav className="flex-1 p-4 relative">
        {/* Dotted backdrop */}
        <div className="absolute inset-0 opacity-5 pointer-events-none">
          <div
            className="absolute inset-0"
            style={{ backgroundImage: "radial-gradient(#344FA5 0.5px, transparent 0.5px)", backgroundSize: "12px 12px" }}
          />
        </div>

        <div className="space-y-2 relative">
          {items.map((item, index) => {
            const isActive = activeLabel === item.label
            const content = (
              <div
                className={cn(
                  "w-full flex items-center gap-3 rounded-xl text-left transition-all duration-300 group relative overflow-hidden",
                  collapsed && !hovered ? "px-2 py-2 justify-center" : "px-3 py-3",
                  isActive
                    ? "bg-gradient-to-r from-[#344FA5] to-[#4A5FB8] text-white shadow-lg transform scale-105"
                    : "text-gray-600 hover:bg-gray-50/80 hover:text-gray-900 hover:transform hover:scale-102",
                )}
                style={{ animationDelay: `${index * 100}ms` }}
              >
                {isActive && <div className="absolute inset-0 bg-white/10 backdrop-blur-sm rounded-xl" />}

                <div
                  className={cn(
                    "rounded-lg relative z-10 transition-all duration-300 flex-shrink-0 p-1.5",
                    isActive ? "bg-white/20" : "bg-gray-100 group-hover:bg-gray-200",
                  )}
                >
                  <item.icon className={cn("w-4 h-4", isActive ? "text-white" : "text-gray-700 group-hover:text-gray-900")} />
                </div>

                <span
                  className={cn(
                    "font-semibold text-sm relative z-10 transition-all duration-300 ease-in-out whitespace-nowrap",
                    collapsed && !hovered ? "opacity-0 w-0 overflow-hidden ml-0" : "opacity-100 ml-0",
                  )}
                >
                  {item.label}
                </span>

                {isActive && (
                  <ChevronRight
                    className={cn(
                      "text-white absolute right-4 animate-bounce transition-all duration-300",
                      collapsed && !hovered ? "opacity-0 w-0" : "opacity-100 w-4 h-4",
                    )}
                  />
                )}
              </div>
            )

            return (
              <div key={item.label} className="relative group">
                {onSelect ? (
                  <button
                    type="button"
                    onClick={() => onSelect(item.label)}
                    className="w-full text-left"
                    aria-current={isActive ? "page" : undefined}
                  >
                    {content}
                  </button>
                ) : item.href ? (
                  <a href={item.href} className="w-full block" aria-current={isActive ? "page" : undefined}>
                    {content}
                  </a>
                ) : (
                  <div>{content}</div>
                )}

                {collapsed && !hovered && (
                  <div className="absolute left-full top-1/2 -translate-y-1/2 ml-3 px-3 py-2 bg-gray-900 text-white text-xs rounded-lg opacity-0 group-hover:opacity-100 transition-opacity duration-200 pointer-events-none z-50 whitespace-nowrap shadow-lg">
                    {item.label}
                    <div className="absolute right-full top-1/2 -translate-y-1/2 border-4 border-transparent border-r-gray-900" />
                  </div>
                )}
              </div>
            )
          })}
        </div>
      </nav>

      {/* Collapse/Expand Toggle */}
      {onToggleCollapse && (
        <div className={cn("px-4 pb-2", hideCollapseOnMobile && "hidden lg:block")}>
          <button
            onClick={onToggleCollapse}
            className="w-full flex items-center p-2 text-gray-500 hover:text-[#344FA5] hover:bg-gray-50 rounded-lg transition-all duration-300 group justify-center"
          >
            <ChevronRight className="w-4 h-4" style={{ transform: collapsed ? "rotate(180deg)" : "rotate(0deg)" }} />
            <span className="ml-2 text-sm font-medium">{collapsed ? "Expand" : "Collapse"}</span>
          </button>
        </div>
      )}

      {/* Optional footer (e.g. Logout button) */}
      {footer && <div className="p-4 border-t border-gray-100/50 bg-gradient-to-b from-transparent to-gray-50/50">{footer}</div>}
    </div>
  )
}
