"use client"

import { useMemo, useRef, useState } from "react"
import { Camera, User, Globe, Shield, Mail, Eye, EyeOff, Trash2, KeyRound, Languages, Clock, CheckCircle2, AlertTriangle, Settings2, Pencil, CalendarIcon, MapPin } from 'lucide-react'
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Badge } from "@/components/ui/badge"
import { Switch } from "@/components/ui/switch"
import { Separator } from "@/components/ui/separator"
import { Dialog, DialogContent, DialogFooter, DialogHeader, DialogTitle } from "@/components/ui/dialog"
import { useToast } from "@/hooks/use-toast"
import { CropperModal } from "./cropper-modal"
import { cn } from "@/lib/utils"
import { SuggestInput, type SuggestOption } from "@/components/ui/suggest-input"

type Profile = {
  fullName: string
  user_name: string
  email: string
  emailVerified: boolean
  gender: "male" | "female" | "other" | ""
  nationality: string
  language: string
  timezone: string
  address: string
  city: string
  state: string
  zip_code: string
  country: string
  date_of_birth: string
  profile_image: string | null
}

const LANGUAGES = [
  { code: "en", label: "English" },
  { code: "hi", label: "हिन्दी (Hindi)" },
  { code: "ur", label: "اردو (Urdu)" },
  { code: "bn", label: "বাংলা (Bengali)" },
  { code: "ta", label: "தமிழ் (Tamil)" },
]

function passwordStrength(password: string) {
  let score = 0
  if (password.length >= 8) score++
  if (/[A-Z]/.test(password)) score++
  if (/[0-9]/.test(password)) score++
  if (/[^A-Za-z0-9]/.test(password)) score++
  return score
}

export function ProfileManagement() {
  const { toast } = useToast()
  const brandBtn = "bg-[#344FA5] hover:bg-[#2A3F85]"

  const initial: Profile = {
    fullName: "Kane Williamson",
    user_name: "kane.w",
    email: "kane@example.com",
    emailVerified: true,
    gender: "male",
    nationality: "New Zealand",
    language: "en",
    timezone: Intl.DateTimeFormat().resolvedOptions().timeZone || "UTC",
    address: "1 Cricket Lane",
    city: "Auckland",
    state: "Auckland",
    zip_code: "1010",
    country: "New Zealand",
    date_of_birth: "1990-08-08",
    profile_image: "/placeholder.svg?height=160&width=160",
  }

  const [profile, setProfile] = useState<Profile>(initial)
  const [pending, setPending] = useState(false)
  const [showPassword, setShowPassword] = useState(false)
  const [password, setPassword] = useState("")
  const [changePwOpen, setChangePwOpen] = useState(false)
  const [deleteOpen, setDeleteOpen] = useState(false)

  const [currentPw, setCurrentPw] = useState("")
  const [newPw, setNewPw] = useState("")
  const [confirmPw, setConfirmPw] = useState("")
  const newPwScore = passwordStrength(newPw)

  // Avatar upload + crop
  const [cropOpen, setCropOpen] = useState(false)
  const [uploadPreview, setUploadPreview] = useState<string | null>(null)
  const fileInputRef = useRef<HTMLInputElement>(null)

  const [countryCode, setCountryCode] = useState<string | null>(null)

  const headerBadges = useMemo(
    () => [
      { label: "Pro", tone: "default" as const },
      { label: "Verified", tone: "success" as const, show: profile.emailVerified },
    ],
    [profile.emailVerified],
  )

  const onSelectFile = (file: File) => {
    if (!file.type.startsWith("image/")) {
      toast({ title: "Invalid file", description: "Please upload a JPG or PNG image.", variant: "destructive" })
      return
    }
    if (file.size > 5 * 1024 * 1024) {
      toast({ title: "Too large", description: "Max upload size is 5MB.", variant: "destructive" })
      return
    }
    const reader = new FileReader()
    reader.onload = (e) => {
      setUploadPreview(e.target?.result as string)
      setCropOpen(true)
    }
    reader.readAsDataURL(file)
  }

  const handleDrop: React.DragEventHandler<HTMLDivElement> = (e) => {
    e.preventDefault()
    const file = e.dataTransfer.files?.[0]
    if (file) onSelectFile(file)
  }

  const handleSave = async () => {
    setPending(true)
    await new Promise((r) => setTimeout(r, 1200))
    setPending(false)
    toast({ title: "Profile updated", description: "Your changes have been saved." })
  }

  const handleCancel = () => {
    setProfile(initial)
    setPassword("")
    toast({ title: "Changes discarded" })
  }

  const handleDelete = async () => {
    setPending(true)
    await new Promise((r) => setTimeout(r, 900))
    setPending(false)
    setDeleteOpen(false)
    toast({ title: "Account deleted", description: "Your account has been scheduled for deletion." })
  }

  const emailStatus = profile.emailVerified ? (
    <Badge variant="outline" className="gap-1 text-green-600 border-green-300">
      <CheckCircle2 className="w-3 h-3" />
      Verified
    </Badge>
  ) : (
    <Badge variant="outline" className="gap-1 text-amber-600 border-amber-300">
      <AlertTriangle className="w-3 h-3" />
      Unverified
    </Badge>
  )

  // Fetchers for suggestions
  const fetchCountries = async (q: string): Promise<SuggestOption[]> => {
    const query = q.trim().toLowerCase()
    if (!query) return []
    try {
      const url = "https://restcountries.com/v3.1/all?fields=name,cca2,cca3,altSpellings"
      const res = await fetch(url, { cache: "no-store" as RequestCache })
      if (!res.ok) return []
      const data = (await res.json()) as any[]
      const items = data
        .map((c) => ({
          name: c?.name?.common as string,
          code: (c?.cca2 as string) || "",
          alt: ((c?.altSpellings as string[]) || []).join(" ").toLowerCase(),
        }))
        .filter((c) => c.name?.toLowerCase().includes(query) || c.alt.includes(query))
        .slice(0, 10)
        .map((c) => ({ label: c.name, value: c.name, subtitle: c.code, meta: c }))
      return items
    } catch {
      return []
    }
  }

  const fetchNationalities = async (q: string): Promise<SuggestOption[]> => {
    const query = q.trim().toLowerCase()
    if (!query) return []
    try {
      const url = "https://restcountries.com/v3.1/all?fields=name,cca2,demonyms"
      const res = await fetch(url, { cache: "no-store" as RequestCache })
      if (!res.ok) return []
      const data = (await res.json()) as any[]
      const pool: { demonym: string; country: string }[] = []
      for (const c of data) {
        const country = c?.name?.common as string
        const dem = c?.demonyms?.eng
        if (dem?.m) pool.push({ demonym: dem.m as string, country })
        if (dem?.f && dem.f !== dem.m) pool.push({ demonym: dem.f as string, country })
      }
      return pool
        .filter((d) => d.demonym.toLowerCase().includes(query) || d.country.toLowerCase().includes(query))
        .slice(0, 12)
        .map((n) => ({ label: n.demonym, value: n.demonym, subtitle: n.country }))
    } catch {
      return []
    }
  }

  const fetchStates = async (q: string): Promise<SuggestOption[]> => {
    const query = q.trim()
    if (!query) return []
    try {
      const params = new URLSearchParams({
        q: query,
        format: "json",
        addressdetails: "1",
        limit: "10",
      })
      if (countryCode && countryCode.length === 2) {
        params.set("countrycodes", countryCode.toLowerCase())
      }
      const url = `https://nominatim.openstreetmap.org/search?${params.toString()}`
      const r = await fetch(url, { cache: "no-store" as RequestCache })
      if (!r.ok) return []
      const data = (await r.json()) as any[]

      const seen = new Set<string>()
      const pool: { state: string; country: string }[] = []
      for (const row of data) {
        const addr = row.address || {}
        const state = addr.state || addr.region || addr.state_district
        const countryName = addr.country
        if (!state) continue
        if (seen.has(state)) continue
        seen.add(state)
        pool.push({ state, country: countryName })
        if (pool.length >= 12) break
      }
      return pool
        .filter((s) => s.state.toLowerCase().includes(query.toLowerCase()))
        .map((s) => ({ label: s.state, value: s.state, subtitle: s.country, meta: s }))
    } catch {
      return []
    }
  }

  const fetchCities = async (q: string): Promise<SuggestOption[]> => {
    const query = q.trim()
    if (!query) return []
    try {
      const params = new URLSearchParams({
        q: query,
        format: "json",
        addressdetails: "1",
        limit: "10",
      })
      if (countryCode && countryCode.length === 2) {
        params.set("countrycodes", countryCode.toLowerCase())
      }
      const url = `https://nominatim.openstreetmap.org/search?${params.toString()}`
      const r = await fetch(url, { cache: "no-store" as RequestCache })
      if (!r.ok) return []
      const data = (await r.json()) as any[]

      const seen = new Set<string>()
      const items: SuggestOption[] = []
      for (const row of data) {
        const addr = row.address || {}
        const city =
          addr.city ||
          addr.town ||
          addr.village ||
          addr.hamlet ||
          row.namedetails?.name ||
          (row.display_name?.split(",")[0] as string | undefined)
        const state = addr.state || addr.region || addr.state_district
        const countryName = addr.country
        if (!city) continue
        const key = `${city}-${state}-${countryName}`
        if (seen.has(key)) continue
        seen.add(key)
        items.push({
          label: city,
          value: city,
          subtitle: [state, countryName].filter(Boolean).join(", "),
          meta: { city, state, country: countryName },
        })
        if (items.length >= 10) break
      }
      return items
    } catch {
      return []
    }
  }

  return (
    <main className="min-h-screen bg-gray-50">
      {/* Top header / overview */}
      <section className="bg-white border-b">
        <div className="mx-auto max-w-6xl px-4 sm:px-6 py-6 md:py-8">
          <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-6">
            {/* Left: avatar + name */}
            <div className="flex items-center gap-4 md:gap-6">
              <div className="relative">
                <img
                  src={profile.profile_image || "/placeholder.svg?height=160&width=160&query=profile%20avatar"}
                  alt="Profile photo"
                  className="w-24 h-24 md:w-28 md:h-28 rounded-full object-cover ring-4 ring-white shadow-md"
                />
                <button
                  aria-label="Edit profile picture"
                  onClick={() => fileInputRef.current?.click()}
                  className="absolute bottom-1 right-1 p-2 rounded-full bg-white shadow hover:bg-gray-50 border"
                >
                  <Camera className="w-4 h-4" />
                </button>
                <input
                  ref={fileInputRef}
                  type="file"
                  accept="image/png,image/jpeg"
                  className="hidden"
                  onChange={(e) => {
                    const file = e.target.files?.[0]
                    if (file) onSelectFile(file)
                  }}
                />
              </div>
              <div>
                <div className="flex items-center flex-wrap gap-2">
                  {/* Use Username instead of Full Name */}
                  <h1 className="text-2xl md:text-3xl font-bold text-gray-900">{profile.user_name}</h1>
                  <span className="inline-flex items-center gap-1 text-sm text-[#344FA5]">
                    <Globe className="w-4 h-4" />
                    {profile.nationality || "Nationality"}
                  </span>
                </div>
                <div className="mt-1 text-sm text-muted-foreground">@{profile.user_name}</div>
                <div className="mt-2 flex items-center gap-2">
                  {headerBadges.map(
                    (b, i) =>
                      (b.show ?? true) && (
                        <Badge key={i} variant={b.tone === "success" ? "default" : "secondary"} className="rounded-full">
                          {b.label}
                        </Badge>
                      ),
                  )}
                </div>
              </div>
            </div>

            {/* Right: actions */}
            <div className="flex items-center gap-2 md:gap-3">
              <Button variant="outline" className="gap-2">
                <Pencil className="w-4 h-4" />
                Edit Profile
              </Button>
              <Button className={cn("gap-2", brandBtn)}>
                <Settings2 className="w-4 h-4" />
                Account Settings
              </Button>
            </div>
          </div>
        </div>
      </section>

      {/* Body */}
      <div className="mx-auto max-w-6xl px-4 sm:px-6 py-6 md:py-8 space-y-6">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Profile Form (spans 2 cols) */}
          <Card className="lg:col-span-2">
            <CardHeader>
              <CardTitle className="text-lg">Profile Information</CardTitle>
            </CardHeader>
            <CardContent className="space-y-6">
              {/* Username only (Full Name removed) */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="space-y-2 md:col-span-2">
                  <Label htmlFor="user_name">Username</Label>
                  <Input
                    id="user_name"
                    value={profile.user_name}
                    onChange={(e) => {
                      const v = e.target.value
                      setProfile((p) => ({ ...p, user_name: v, fullName: v })) // keep them in sync
                    }}
                    placeholder="e.g. jane.doe"
                  />
                </div>
              </div>

              {/* Email and DOB (non-editable) */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {/* Email - disabled */}
                <div className="space-y-2">
                  <Label htmlFor="email" className="flex items-center gap-2">
                    <Mail className="w-4 h-4 text-muted-foreground" />
                    Email Address
                  </Label>
                  <div className="flex gap-2">
                    <Input
                      id="email"
                      type="email"
                      className="flex-1"
                      value={profile.email}
                      readOnly
                      disabled
                    />
                    <div className="flex items-center">{emailStatus}</div>
                  </div>
                </div>

                {/* DOB - disabled */}
                <div className="space-y-2">
                  <Label htmlFor="dob" className="flex items-center gap-2">
                    <CalendarIcon className="w-4 h-4 text-muted-foreground" />
                    Date of Birth
                  </Label>
                  <Input
                    id="dob"
                    type="date"
                    value={profile.date_of_birth}
                    readOnly
                    disabled
                  />
                </div>
              </div>

              {/* Gender (non-editable) + Nationality */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {/* Gender - non-editable */}
                <div className="space-y-2">
                  <Label className="flex items-center gap-2">
                    <User className="w-4 h-4 text-muted-foreground" />
                    Gender
                  </Label>
                  <div className="grid grid-cols-3 gap-2">
                    {["male", "female", "other"].map((g) => (
                      <div
                        key={g}
                        className={cn(
                          "px-3 py-2 rounded-md border text-sm capitalize cursor-not-allowed pointer-events-none select-none",
                          profile.gender === g ? "border-[#344FA5] text-[#344FA5] bg-[#344FA5]/5" : "border-gray-200 bg-muted/30 text-muted-foreground",
                        )}
                        aria-disabled="true"
                      >
                        {g}
                      </div>
                    ))}
                  </div>
                  <p className="text-xs text-muted-foreground">Gender is locked and cannot be edited.</p>
                </div>

                {/* Nationality suggest */}
                <div className="space-y-2">
                  <Label className="flex items-center gap-2">
                    <Globe className="w-4 h-4 text-muted-foreground" />
                    Nationality
                  </Label>
                  <SuggestInput
                    value={profile.nationality}
                    onChange={(v) => setProfile((p) => ({ ...p, nationality: v }))}
                    fetcher={fetchNationalities}
                    placeholder="Start typing nationality (e.g., New Zealander)"
                  />
                </div>
              </div>

              {/* Country + State/Province */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {/* Country suggest */}
                <div className="space-y-2">
                  <Label className="flex items-center gap-2">
                    <MapPin className="w-4 h-4 text-muted-foreground" />
                    Country
                  </Label>
                  <SuggestInput
                    value={profile.country}
                    onChange={(v) => setProfile((p) => ({ ...p, country: v }))}
                    onSelect={(opt) => {
                      setCountryCode(opt.subtitle || null)
                      setProfile((p) => ({ ...p, country: opt.label }))
                    }}
                    fetcher={fetchCountries}
                    placeholder="Type a country name"
                  />
                </div>

                {/* State/Province suggest */}
                <div className="space-y-2">
                  <Label className="flex items-center gap-2">
                    <MapPin className="w-4 h-4 text-muted-foreground" />
                    State/Province
                  </Label>
                  <SuggestInput
                    value={profile.state}
                    onChange={(v) => setProfile((p) => ({ ...p, state: v }))}
                    fetcher={fetchStates}
                    placeholder="Type a state/province"
                  />
                </div>
              </div>

              {/* Address + City + ZIP + Language */}
              <div className="grid grid-cols-1 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="address" className="flex items-center gap-2">
                    <MapPin className="w-4 h-4 text-muted-foreground" />
                    Address
                  </Label>
                  <Input
                    id="address"
                    value={profile.address}
                    onChange={(e) => setProfile((p) => ({ ...p, address: e.target.value }))}
                    placeholder="Street address"
                  />
                </div>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="city">City</Label>
                    <SuggestInput
                      value={profile.city}
                      onChange={(v) => setProfile((p) => ({ ...p, city: v }))}
                      fetcher={fetchCities}
                      placeholder="Type a city"
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="zip">ZIP/Postal Code</Label>
                    <Input
                      id="zip"
                      value={profile.zip_code}
                      onChange={(e) => setProfile((p) => ({ ...p, zip_code: e.target.value }))}
                      placeholder="ZIP code"
                    />
                  </div>
                  <div className="space-y-2">
                    <Label className="flex items-center gap-2">
                      <Languages className="w-4 h-4 text-muted-foreground" />
                      Language
                    </Label>
                    <select
                      className="w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
                      value={profile.language}
                      onChange={(e) => setProfile((p) => ({ ...p, language: e.target.value }))}
                    >
                      {LANGUAGES.map((l) => (
                        <option key={l.code} value={l.code}>
                          {l.label}
                        </option>
                      ))}
                    </select>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Profile Picture Upload Panel */}
          <Card>
            <CardHeader>
              <CardTitle className="text-lg">Profile Photo</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div
                className={cn(
                  "rounded-xl border-2 border-dashed p-4 text-center cursor-pointer bg-white/60 hover:bg-white",
                )}
                onClick={() => fileInputRef.current?.click()}
                onDragOver={(e) => e.preventDefault()}
                onDrop={handleDrop}
                aria-label="Upload new photo"
              >
                <div className="flex flex-col items-center gap-2">
                  <div className="w-20 h-20 rounded-full overflow-hidden ring-2 ring-white shadow">
                    <img
                      src={profile.profile_image || "/placeholder.svg?height=160&width=160&query=profile%20avatar"}
                      alt="Current profile"
                      className="w-full h-full object-cover"
                    />
                  </div>
                  <p className="text-sm text-muted-foreground">Drag & drop or click to upload a new photo</p>
                  <Button variant="secondary" className="gap-2">
                    <Camera className="w-4 h-4" />
                    Upload Photo
                  </Button>
                  <p className="text-xs text-muted-foreground">JPG or PNG, max 5MB</p>
                </div>
              </div>
              <input
                ref={fileInputRef}
                type="file"
                accept="image/png,image/jpeg"
                className="hidden"
                onChange={(e) => {
                  const file = e.target.files?.[0]
                  if (file) onSelectFile(file)
                }}
              />
            </CardContent>
          </Card>
        </div>

        {/* Security Settings */}
        <Card>
          <CardHeader>
            <CardTitle className="text-lg">Security</CardTitle>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="md:col-span-2 space-y-2">
                <Label className="flex items-center gap-2">
                  <Shield className="w-4 h-4 text-muted-foreground" />
                  Two-Factor Authentication
                </Label>
                <div className="flex items-center justify-between rounded-lg border p-3">
                  <p className="text-sm text-muted-foreground">Add an extra layer of security to your account.</p>
                  <div className="flex items-center gap-3">
                    <Switch disabled />
                    <Badge variant="outline">Disabled</Badge>
                  </div>
                </div>
              </div>
              <div className="space-y-2">
                <Label>Password Strength</Label>
                <div className="h-2 rounded-full bg-gray-200 overflow-hidden">
                  <div
                    className="h-full transition-all"
                    style={{
                      width: `${(passwordStrength(password) / 4) * 100}%`,
                      background: passwordStrength(password) >= 3 ? "linear-gradient(90deg,#16a34a,#22c55e)" : "linear-gradient(90deg,#f59e0b,#ef4444)",
                    }}
                  />
                </div>
                <p className="text-xs text-muted-foreground">Use 8+ characters with a mix of uppercase, numbers, and symbols.</p>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Footer actions */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div className="flex items-center gap-4">
            <Button onClick={handleSave} disabled={pending} className={cn("min-w-40", brandBtn)}>
              {pending ? "Saving..." : "Save Changes"}
            </Button>
            <Button variant="outline" onClick={handleCancel} disabled={pending}>
              Cancel
            </Button>
          </div>
          <div className="flex items-center gap-4">
            <a href="#" className="text-sm text-muted-foreground hover:underline">
              Privacy Policy
            </a>
            <a href="#" className="text-sm text-muted-foreground hover:underline">
              Terms of Use
            </a>
            <Separator orientation="vertical" className="hidden sm:block" />
            <button className="text-sm text-red-600 hover:underline inline-flex items-center gap-2" onClick={() => setDeleteOpen(true)}>
              <Trash2 className="w-4 h-4" />
              Delete Account
            </button>
          </div>
        </div>
      </div>

      {/* Change Password Dialog */}
      <Dialog open={changePwOpen} onOpenChange={setChangePwOpen}>
        <DialogContent className="max-w-md">
          <DialogHeader>
            <DialogTitle>Change Password</DialogTitle>
          </DialogHeader>
          <div className="space-y-4">
            <div className="space-y-2">
              <Label>Current password</Label>
              <Input type="password" value={currentPw} onChange={(e) => setCurrentPw(e.target.value)} placeholder="Current password" />
            </div>
            <div className="space-y-2">
              <Label>New password</Label>
              <Input type="password" value={newPw} onChange={(e) => setNewPw(e.target.value)} placeholder="New password" />
              <div className="h-2 bg-gray-200 rounded-full overflow-hidden">
                <div
                  className="h-full transition-all"
                  style={{
                    width: `${(newPwScore / 4) * 100}%`,
                    background: newPwScore >= 3 ? "linear-gradient(90deg,#16a34a,#22c55e)" : "linear-gradient(90deg,#f59e0b,#ef4444)",
                  }}
                />
              </div>
              <p className="text-xs text-muted-foreground">Strength: {["Very Weak", "Weak", "Fair", "Good", "Strong"][newPwScore]}</p>
            </div>
            <div className="space-y-2">
              <Label>Confirm new password</Label>
              <Input type="password" value={confirmPw} onChange={(e) => setConfirmPw(e.target.value)} placeholder="Confirm new password" />
              {newPw && confirmPw && newPw !== confirmPw && <p className="text-xs text-red-600">Passwords do not match.</p>}
            </div>
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setChangePwOpen(false)}>
              Cancel
            </Button>
            <Button
              className={brandBtn}
              onClick={async () => {
                if (!currentPw || !newPw || newPw !== confirmPw) {
                  toast({ title: "Check fields", description: "Please fill out all fields correctly.", variant: "destructive" })
                  return
                }
                setPending(true)
                await new Promise((r) => setTimeout(r, 1000))
                setPending(false)
                setChangePwOpen(false)
                setPassword("")
                setCurrentPw("")
                setNewPw("")
                setConfirmPw("")
                toast({ title: "Password updated" })
              }}
            >
              Update Password
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* Delete Account Confirmation */}
      <Dialog open={deleteOpen} onOpenChange={setDeleteOpen}>
        <DialogContent className="max-w-md">
          <DialogHeader>
            <DialogTitle className="flex items-center gap-2">
              <AlertTriangle className="w-5 h-5 text-red-600" />
              Delete Account
            </DialogTitle>
          </DialogHeader>
          <p className="text-sm text-muted-foreground">This action is permanent and cannot be undone. All your data will be removed. Are you sure you want to continue?</p>
          <DialogFooter>
            <Button variant="outline" onClick={() => setDeleteOpen(false)}>
              Cancel
            </Button>
            <Button variant="destructive" onClick={handleDelete} disabled={pending}>
              {pending ? "Deleting..." : "Delete Account"}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* Cropper */}
      <CropperModal
        open={cropOpen}
        onOpenChange={setCropOpen}
        imageUrl={uploadPreview}
        onCropped={(dataUrl) => {
          setProfile((p) => ({ ...p, profile_image: dataUrl }))
          toast({ title: "Profile photo updated" })
          setUploadPreview(null)
        }}
      />
    </main>
  )
}
