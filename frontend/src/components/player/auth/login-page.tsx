import type React from "react"
import { useState } from "react"
import { Eye, EyeOff, Loader2 } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Card, CardContent } from "@/components/ui/card"
import { useToast } from "@/hooks/use-toast"
import { loginPlayer, type LoginRequest, type ApiError } from "@/services/player/authService"
import cricketPlayerImage from "@/assets/cricket-player.png"

interface LoginPageProps {
  onBack: () => void;
  onLogin: () => void;
  onForgotPassword: () => void;
  onSignUp: () => void;
}

export function LoginForm({ onBack, onLogin, onForgotPassword, onSignUp }: LoginPageProps) {
  const [formData, setFormData] = useState<LoginRequest>({
    email: "",
    password: "",
    sportType: "cricket",
  })
  const [showPassword, setShowPassword] = useState(false)
  const [isLoading, setIsLoading] = useState(false)
  const { toast } = useToast()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)
    
    try {
      const response = await loginPlayer(formData)
      
      if (response.success) {
        toast({
          title: "Login Successful",
          description: "Welcome back! Redirecting to dashboard...",
          variant: "default",
        })
        
        // Redirect to dashboard after successful login
        setTimeout(() => {
          onLogin()
        }, 1000)
      }
    } catch (error: any) {
      const apiError = error as ApiError
      
      toast({
        title: "Login Failed",
        description: apiError.message || "Please check your credentials and try again.",
        variant: "destructive",
      })
      
      // Handle specific field errors
      if (apiError.errors) {
        console.error('Field errors:', apiError.errors)
      }
    } finally {
      setIsLoading(false)
    }
  }

  const handleInputChange = (field: keyof LoginRequest, value: string) => {
    setFormData((prev) => ({
      ...prev,
      [field]: value,
    }))
  }

  return (
    <div className="w-full max-w-7xl mx-auto grid lg:grid-cols-3 gap-8 items-center min-h-screen px-4 py-8">
      {/* Left side - Login Form (takes 2 columns) */}
      <div className="lg:col-span-2 flex justify-center">
        <Card className="w-full max-w-2xl border border-gray-300 shadow-sm bg-white hover:border-[#344FA5] hover:shadow-lg transition-all duration-300 ease-in-out">
          <CardContent className="p-8">
            {/* Login Heading */}
            <h1 className="text-2xl font-semibold text-black text-center mb-8">
              Login
            </h1>

            <form onSubmit={handleSubmit} className="space-y-6">
              {/* Email Field */}
              <div className="space-y-2">
                <Label htmlFor="email" className="text-base font-normal text-black">
                  Email
                </Label>
                <Input
                  id="email"
                  type="email"
                  placeholder="Enter Email"
                  value={formData.email}
                  onChange={(e) => handleInputChange("email", e.target.value)}
                  className="h-11 text-sm border-gray-300 rounded-lg hover:border-[#344FA5] focus:border-[#344FA5] transition-colors placeholder:text-gray-500"
                  required
                  disabled={isLoading}
                />
              </div>

              {/* Password Field */}
              <div className="space-y-2">
                <Label htmlFor="password" className="text-base font-normal text-black">
                  Password
                </Label>
                <div className="relative">
                  <Input
                    id="password"
                    type={showPassword ? "text" : "password"}
                    placeholder="Enter Password"
                    value={formData.password}
                    onChange={(e) => handleInputChange("password", e.target.value)}
                    className="h-11 text-sm border-gray-300 rounded-lg hover:border-[#344FA5] focus:border-[#344FA5] transition-colors placeholder:text-gray-500 pr-10"
                    required
                    disabled={isLoading}
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute inset-y-0 right-0 flex items-center pr-3 text-gray-400 hover:text-gray-600"
                    disabled={isLoading}
                  >
                    {showPassword ? (
                      <EyeOff className="h-4 w-4" />
                    ) : (
                      <Eye className="h-4 w-4" />
                    )}
                  </button>
                </div>
              </div>

              {/* Sport Type Field */}
              <div className="space-y-2">
                <Label htmlFor="sportType" className="text-base font-normal text-black">
                  Sport Type
                </Label>
                <Select 
                  value={formData.sportType} 
                  onValueChange={(value) => handleInputChange("sportType", value)}
                  disabled={isLoading}
                >
                  <SelectTrigger className="h-11 text-sm border-gray-300 rounded-lg hover:border-[#344FA5] focus:border-[#344FA5] transition-colors">
                    <SelectValue placeholder="Select Sport Type" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="cricket">Cricket</SelectItem>
                    <SelectItem value="football">Football</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              {/* Forgot Password Link */}
              <div className="text-right">
                <button
                  type="button"
                  onClick={onForgotPassword}
                  className="text-sm text-black hover:text-[#344FA5] transition-colors border-none bg-transparent cursor-pointer"
                  disabled={isLoading}
                >
                  Forgot Password?
                </button>
              </div>

              {/* Submit Button */}
               <div className="flex justify-center">
                    <Button
                      type="submit"
                      disabled={isLoading}
                      className="bg-[#344FA5] hover:bg-[#2a3f8f] text-white text-base font-medium rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                      style={{ width: '160px', height: '55px' }}
                    >
                      {isLoading ? (
                        <>
                          <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                          Logging in...
                        </>
                      ) : (
                        'Login'
                      )}
                    </Button>
               </div>
              

              {/* Sign Up Link */}
              <div className="text-center pt-4">
                <p className="text-sm text-black">
                  You don't have an account?{" "}
                  <button
                    type="button"
                    onClick={onSignUp}
                    className="text-[#344FA5] hover:underline font-medium border-none bg-transparent cursor-pointer"
                    disabled={isLoading}
                  >
                    Sign up
                  </button>
                </p>
              </div>
            </form>
          </CardContent>
        </Card>
      </div>

      {/* Right side - Illustration (takes 1 column) */}
      <div className="hidden lg:flex justify-center items-center">
        <div className="w-full max-w-sm">
          <img
            src={cricketPlayerImage || "/placeholder.svg"}
            alt="Person working illustration"
            className="w-full h-auto object-contain"
          />
        </div>
      </div>
    </div>
  )
}