"use client"

import { ProfileManagement } from "@/components/player/profile/profile-management"
import { ProfileShell } from "@/components/layout/profile-shell"

export default function profile_page() {
  const handleLogout = () => {
    console.log("Logging out...")
  }

  return (
    <ProfileShell title="Profile" onLogout={handleLogout}>
      <ProfileManagement />
    </ProfileShell>
  )
}
