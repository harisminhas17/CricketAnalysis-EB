import { useState } from "react";
import { ArrowLeft, Upload, Loader2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Textarea } from "@/components/ui/textarea";
import { Card, CardContent } from "@/components/ui/card";
import { useToast } from "@/hooks/use-toast";
import { registerPlayer, type RegisterRequest, type ApiError } from "@/services/player/authService";
import cricketPlayer from "@/assets/cricket-player.png";

interface SignUpPageProps {
  onBack: () => void;
  onSignUp: () => void;
  onLogin: () => void;
}

export const SignUpPage = ({ onBack, onSignUp, onLogin }: SignUpPageProps) => {
  const [currentStep, setCurrentStep] = useState(1);
  const [isLoading, setIsLoading] = useState(false);
  const { toast } = useToast();
  
  const [formData, setFormData] = useState<RegisterRequest>({
    name: "",
    email: "",
    password: "",
    sportType: "cricket",
    phoneNo: "",
    address: "",
    gender: "",
    nationality: "",
    dateOfBirth: "",
    profileImage: undefined,
    roleInTeam: "",
    battingStyle: "",
    bowlingStyle: "",
  });

  const updateFormData = (field: keyof RegisterRequest, value: any) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const handleNext = () => {
    if (currentStep < 4) {
      setCurrentStep(currentStep + 1);
    } else {
      handleSubmit();
    }
  };

  const handleBack = () => {
    if (currentStep > 1) {
      setCurrentStep(currentStep - 1);
    } else {
      onBack();
    }
  };

  const handleSubmit = async () => {
    setIsLoading(true);
    
    try {
      const response = await registerPlayer(formData);
      
      if (response.success) {
        toast({
          title: "Registration Successful",
          description: "Welcome! Your account has been created successfully.",
          variant: "default",
        });
        
        // Redirect to dashboard after successful registration
        setTimeout(() => {
          onSignUp();
        }, 1000);
      }
    } catch (error: any) {
      const apiError = error as ApiError;
      
      toast({
        title: "Registration Failed",
        description: apiError.message || "Please check your information and try again.",
        variant: "destructive",
      });
      
      // Handle specific field errors
      if (apiError.errors) {
        console.error('Field errors:', apiError.errors);
      }
    } finally {
      setIsLoading(false);
    }
  };

  const handleProfileImageUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      updateFormData('profileImage', file);
    }
  };

  const renderStep = () => {
    switch (currentStep) {
      case 1:
        return (
          <div className="space-y-6">
            <h2 className="text-lg font-medium text-center mb-6 text-black">Personal Information</h2>
            
            <div className="space-y-2">
              <Label htmlFor="name" className="text-base font-normal text-black">Name</Label>
              <Input
                id="name"
                type="text"
                placeholder="Enter Name"
                value={formData.name}
                onChange={(e) => updateFormData('name', e.target.value)}
                className="h-11 text-sm border-gray-300 rounded-lg hover:border-[#344FA5] focus:border-[#344FA5] transition-colors placeholder:text-gray-500"
                required
              />
            </div>
            
            <div className="space-y-2">
              <Label htmlFor="email" className="text-base font-normal text-black">Email</Label>
              <Input
                id="email"
                type="email"
                placeholder="Enter Email"
                value={formData.email}
                onChange={(e) => updateFormData('email', e.target.value)}
                className="h-11 text-sm border-gray-300 rounded-lg hover:border-[#344FA5] focus:border-[#344FA5] transition-colors placeholder:text-gray-500"
                required
              />
            </div>
            
            <div className="space-y-2">
              <Label htmlFor="password" className="text-base font-normal text-black">Password</Label>
              <Input
                id="password"
                type="password"
                placeholder="Enter Password"
                value={formData.password}
                onChange={(e) => updateFormData('password', e.target.value)}
                className="h-11 text-sm border-gray-300 rounded-lg hover:border-[#344FA5] focus:border-[#344FA5] transition-colors placeholder:text-gray-500"
                required
              />
            </div>
            
            <div className="space-y-2">
              <Label htmlFor="sportType" className="text-base font-normal text-black">Sport Type</Label>
              <Select value={formData.sportType} onValueChange={(value) => updateFormData('sportType', value)}>
                <SelectTrigger className="h-11 text-sm border-gray-300 rounded-lg hover:border-[#344FA5] focus:border-[#344FA5] transition-colors">
                  <SelectValue placeholder="Select Sport Type" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="cricket">Cricket</SelectItem>
                  <SelectItem value="football">Football</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>
        );

      case 2:
        return (
          <div className="space-y-6">
            <h2 className="text-lg font-medium text-center mb-6 text-black">Contact & Location Details</h2>
            
            <div className="space-y-2">
              <Label htmlFor="phoneNo" className="text-base font-normal text-black">Phone Number</Label>
              <Input
                id="phoneNo"
                type="tel"
                placeholder="Enter Phone Number"
                value={formData.phoneNo}
                onChange={(e) => updateFormData('phoneNo', e.target.value)}
                className="h-11 text-sm border-gray-300 rounded-lg hover:border-[#344FA5] focus:border-[#344FA5] transition-colors placeholder:text-gray-500"
                required
              />
            </div>
            
            <div className="space-y-2">
              <Label htmlFor="address" className="text-base font-normal text-black">Address</Label>
              <Textarea
                id="address"
                placeholder="Enter Address"
                value={formData.address}
                onChange={(e) => updateFormData('address', e.target.value)}
                className="rounded-lg border-gray-300 hover:border-[#344FA5] focus:border-[#344FA5] transition-colors text-sm min-h-[80px] placeholder:text-gray-500"
                required
              />
            </div>
            
            <div className="space-y-2">
              <Label htmlFor="gender" className="text-base font-normal text-black">Gender</Label>
              <Select value={formData.gender} onValueChange={(value) => updateFormData('gender', value)}>
                <SelectTrigger className="h-11 text-sm border-gray-300 rounded-lg hover:border-[#344FA5] focus:border-[#344FA5] transition-colors">
                  <SelectValue placeholder="Select Gender" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="male">Male</SelectItem>
                  <SelectItem value="female">Female</SelectItem>
                  <SelectItem value="other">Other</SelectItem>
                </SelectContent>
              </Select>
            </div>
            
            <div className="space-y-2">
              <Label htmlFor="nationality" className="text-base font-normal text-black">Nationality</Label>
              <Select value={formData.nationality} onValueChange={(value) => updateFormData('nationality', value)}>
                <SelectTrigger className="h-11 text-sm border-gray-300 rounded-lg hover:border-[#344FA5] focus:border-[#344FA5] transition-colors">
                  <SelectValue placeholder="Select Nationality" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="india">India</SelectItem>
                  <SelectItem value="australia">Australia</SelectItem>
                  <SelectItem value="england">England</SelectItem>
                  <SelectItem value="southafrica">South Africa</SelectItem>
                  <SelectItem value="newzealand">New Zealand</SelectItem>
                  <SelectItem value="westindies">West Indies</SelectItem>
                  <SelectItem value="pakistan">Pakistan</SelectItem>
                  <SelectItem value="srilanka">Sri Lanka</SelectItem>
                  <SelectItem value="bangladesh">Bangladesh</SelectItem>
                  <SelectItem value="afghanistan">Afghanistan</SelectItem>
                  <SelectItem value="zimbabwe">Zimbabwe</SelectItem>
                  <SelectItem value="ireland">Ireland</SelectItem>
                  <SelectItem value="netherlands">Netherlands</SelectItem>
                  <SelectItem value="usa">United States</SelectItem>
                  <SelectItem value="canada">Canada</SelectItem>
                  <SelectItem value="other">Other</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>
        );

      case 3:
        return (
          <div className="space-y-6">
            <h2 className="text-lg font-medium text-center mb-6 text-black">Profile Setup</h2>
            
            <div className="space-y-2">
              <Label htmlFor="profileImage" className="text-base font-normal text-black">Profile Image</Label>
              <div className="relative">
                <Input
                  id="profileImage"
                  type="file"
                  accept="image/*"
                  onChange={handleProfileImageUpload}
                  className="hidden"
                />
                <Label
                  htmlFor="profileImage"
                  className="flex items-center justify-center h-32 rounded-lg border-2 border-dashed border-gray-300 hover:border-[#344FA5] cursor-pointer text-sm text-gray-500 transition-colors"
                >
                  <div className="text-center">
                    <Upload className="w-8 h-8 mx-auto mb-2" />
                    <p>{formData.profileImage ? formData.profileImage.name : "Upload Profile Image"}</p>
                    <p className="text-xs text-gray-400 mt-1">PNG, JPG up to 5MB</p>
                  </div>
                </Label>
                {formData.profileImage && (
                  <div className="mt-2 text-center">
                    <img
                      src={URL.createObjectURL(formData.profileImage)}
                      alt="Profile Preview"
                      className="w-20 h-20 rounded-full mx-auto object-cover"
                    />
                  </div>
                )}
              </div>
            </div>
            
            <div className="space-y-2">
              <Label htmlFor="dateOfBirth" className="text-base font-normal text-black">Date of Birth</Label>
              <Input
                id="dateOfBirth"
                type="date"
                value={formData.dateOfBirth}
                onChange={(e) => updateFormData('dateOfBirth', e.target.value)}
                className="h-11 text-sm border-gray-300 rounded-lg hover:border-[#344FA5] focus:border-[#344FA5] transition-colors"
                required
              />
            </div>
          </div>
        );

      case 4:
        return (
          <div className="space-y-6">
            <h2 className="text-lg font-medium text-center mb-6 text-black">Player Details</h2>
            
            <div className="space-y-2">
              <Label htmlFor="role" className="text-base font-normal text-black">Role in Team</Label>
              <Select value={formData.roleInTeam} onValueChange={(value) => updateFormData('roleInTeam', value)}>
                <SelectTrigger className="h-11 text-sm border-gray-300 rounded-lg hover:border-[#344FA5] focus:border-[#344FA5] transition-colors">
                  <SelectValue placeholder="Select Role" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="batsman">Batsman</SelectItem>
                  <SelectItem value="bowler">Bowler</SelectItem>
                  <SelectItem value="allrounder">All-rounder</SelectItem>
                  <SelectItem value="wicketkeeper">Wicket-keeper</SelectItem>
                  <SelectItem value="captain">Captain</SelectItem>
                </SelectContent>
              </Select>
            </div>
            
            <div className="space-y-2">
              <Label htmlFor="batting" className="text-base font-normal text-black">Batting Style</Label>
              <Select value={formData.battingStyle} onValueChange={(value) => updateFormData('battingStyle', value)}>
                <SelectTrigger className="h-11 text-sm border-gray-300 rounded-lg hover:border-[#344FA5] focus:border-[#344FA5] transition-colors">
                  <SelectValue placeholder="Select Batting Style" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="righthanded">Right-handed</SelectItem>
                  <SelectItem value="lefthanded">Left-handed</SelectItem>
                </SelectContent>
              </Select>
            </div>
            
            <div className="space-y-2">
              <Label htmlFor="bowling" className="text-base font-normal text-black">Bowling Style</Label>
              <Select value={formData.bowlingStyle} onValueChange={(value) => updateFormData('bowlingStyle', value)}>
                <SelectTrigger className="h-11 text-sm border-gray-300 rounded-lg hover:border-[#344FA5] focus:border-[#344FA5] transition-colors">
                  <SelectValue placeholder="Select Bowling Style" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="rightarmfast">Right-arm Fast</SelectItem>
                  <SelectItem value="leftarmfast">Left-arm Fast</SelectItem>
                  <SelectItem value="rightarmmedium">Right-arm Medium</SelectItem>
                  <SelectItem value="leftarmmedium">Left-arm Medium</SelectItem>
                  <SelectItem value="rightspin">Right-arm Spin</SelectItem>
                  <SelectItem value="leftspin">Left-arm Spin</SelectItem>
                  <SelectItem value="none">None</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>
        );

      default:
        return null;
    }
  };

  return (
    <div className="w-full max-w-7xl mx-auto grid lg:grid-cols-3 gap-8 items-center min-h-screen px-4 py-8">
      {/* Left side - Sign Up Form (takes 2 columns) */}
      <div className="lg:col-span-2 flex justify-center">
        <Card className="w-full max-w-2xl border border-gray-300 shadow-sm bg-white hover:border-[#344FA5] hover:shadow-lg transition-all duration-300 ease-in-out">
          <CardContent className="p-8">
            <button
              onClick={handleBack}
              type="button"
              className="hover:bg-gray-100 p-2 rounded-full transition-colors mb-6 inline-flex items-center"
              disabled={isLoading}
            >
              <ArrowLeft className="w-5 h-5 text-gray-600" />
            </button>

            {/* Sign Up Heading */}
            <h1 className="text-2xl font-semibold text-black text-center mb-2">
              Sign up
            </h1>
            <p className="text-sm text-center text-gray-600 mb-8">
              Step {currentStep} of 4
            </p>
            <form onSubmit={(e) => { e.preventDefault(); handleNext(); }} className="space-y-6">
              {renderStep()}
              
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
                      {currentStep === 4 ? 'Creating...' : 'Processing...'}
                    </>
                  ) : (
                    currentStep === 4 ? 'Sign up' : 'Next'
                  )}
                </Button>
              </div>
            </form>
            
            {currentStep === 4 && !isLoading && (
              <div className="text-center pt-4">
                <p className="text-sm text-black">
                  Already have an account?{" "}
                  <button
                    type="button"
                    onClick={onLogin}
                    className="text-[#344FA5] hover:underline font-medium border-none bg-transparent cursor-pointer"
                  >
                    Log in
                  </button>
                </p>
              </div>
            )}
          </CardContent>
        </Card>
      </div>
      {/* Right side - Illustration (takes 1 column) */}
      <div className="hidden lg:flex justify-center items-center">
        <div className="w-full max-w-sm">
          <img
            src={cricketPlayer || "/placeholder.svg"}
            alt="Cricket Player"
            className="w-full h-auto object-contain"
          />
        </div>
      </div>
    </div>
  );
};