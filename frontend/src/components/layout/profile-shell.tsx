"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Sheet, SheetContent, SheetTrigger } from "@/components/ui/sheet"
import { cn } from "@/lib/utils"
import { BarChart3, Globe, Activity, Target, Users, Menu } from 'lucide-react'
import { SideMenu, type SideMenuItem } from "@/components/navigation/side-menu"

type ProfileShellProps = {
  title?: string
  onLogout?: () => void
  children: React.ReactNode
}

export function ProfileShell({ title = "Profile", onLogout, children }: ProfileShellProps) {
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false)
  const [sidebarHovered, setSidebarHovered] = useState(false)

  const sidebarItems: SideMenuItem[] = [
    { icon: BarChart3, label: "Dashboard", href: "/" },
    { icon: Globe, label: "Social Media", href: "/" },
    { icon: Activity, label: "Stats", href: "/" },
    { icon: Target, label: "Ball Track", href: "/" },
    { icon: Users, label: "Following", href: "/" },
  ]

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
            items={sidebarItems}
            collapsed={sidebarCollapsed}
            hovered={sidebarHovered}
            onToggleCollapse={() => setSidebarCollapsed((v) => !v)}
            profile={{
              name: "Kane Williamson",
              team: "Team Newzealand",
              status: "Professional Cricketer",
            }}
          />
        </div>

        {/* Mobile Sidebar */}
        <Sheet open={sidebarOpen} onOpenChange={setSidebarOpen}>
          <SheetContent side="left" className="p-0 w-72 lg:hidden">
            <SideMenu
              items={sidebarItems}
              collapsed={false}
              hovered={true}
              profile={{
                name: "Kane Williamson",
                team: "Team Newzealand",
                status: "Professional Cricketer",
              }}
            />
          </SheetContent>
        </Sheet>

        {/* Main Content */}
        <div className="flex-1 min-w-0 relative">
          {/* Header */}
          <div className="bg-white/95 backdrop-blur-sm border-b border-gray-100/50 p-4 lg:p-6 sticky top-0 z-40 shadow-sm">
            <div className="flex items-center justify-between gap-4">
              <div className="flex items-center gap-4 min-w-0 flex-1">
                {/* Mobile menu button */}
                <Sheet open={sidebarOpen} onOpenChange={setSidebarOpen}>
                  <SheetTrigger asChild>
                    <Button
                      variant="ghost"
                      size="icon"
                      className="lg:hidden hover:bg-gray-100 rounded-xl group relative overflow-hidden flex-shrink-0"
                    >
                      <span className="absolute inset-0 bg-gray-100/80 scale-0 group-hover:scale-100 transition-transform duration-300 rounded-full" />
                      <Menu className="w-5 h-5 relative z-10" />
                    </Button>
                  </SheetTrigger>
                </Sheet>
                <h1 className="text-xl lg:text-2xl font-bold bg-gradient-to-r from-[#344FA5] to-[#4A5FB8] text-transparent bg-clip-text truncate">
                  {title}
                </h1>
              </div>
              <div className="flex items-center gap-2 lg:gap-3 flex-shrink-0">
                <Button variant="outline" onClick={onLogout} className="rounded-xl border-gray-200 bg-transparent hidden md:inline-flex">
                  Logout
                </Button>
              </div>
            </div>
          </div>

          {/* Content */}
          <div className="flex-1 overflow-auto relative z-10">{children}</div>
        </div>
      </div>
    </div>
  )
}
