import { useState, useRef } from "react";
import { ArrowLeft, Upload, Loader2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Textarea } from "@/components/ui/textarea";
import { Card, CardContent } from "@/components/ui/card";
import { useToast } from "@/hooks/use-toast";
import { registerPlayer, type RegisterRequest, type ApiError } from "@/services/player/authService";
import { SuggestInput, SuggestOption } from '@/components/ui/suggest-input';
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
    sport_type: "cricket",
    phone_number: "",
    gender: "",
    date_of_birth: "",
    login_type: "manual", // Hidden from UI but still sent to backend
    profile_image: undefined,
    address: "",
    nationality_id: undefined,
    role_id: undefined,
    batting_style: "",
    bowling_style: "",
    dominant_hand: ""
  });

  const [nationalitySearch, setNationalitySearch] = useState("");
  const [roleSearch, setRoleSearch] = useState("");

  const updateFormData = (field: string, value: any) => {
    setFormData(prev => {
      const updated = { ...prev, [field]: value };
      console.log(`Updated ${field}:`, value, 'Full form data:', updated);
      return updated;
    });
  };

  const validateCurrentStep = (): boolean => {
    switch (currentStep) {
      case 1:
        if (!formData.name || !formData.email || !formData.password || !formData.sport_type) {
          toast({
            title: "Missing Information",
            description: "Please fill in all required fields on this step.",
            variant: "destructive",
          });
          return false;
        }
        break;
      case 2:
        if (!formData.phone_number || !formData.address || !formData.gender || !formData.nationality_id) {
          toast({
            title: "Missing Information", 
            description: "Please fill in all required fields on this step.",
            variant: "destructive",
          });
          return false;
        }
        break;
      case 3:
        if (!formData.date_of_birth) {
          toast({
            title: "Missing Information",
            description: "Please enter your date of birth.",
            variant: "destructive",
          });
          return false;
        }
        break;
      case 4:
        if (!formData.role_id || !formData.batting_style || !formData.bowling_style || !formData.dominant_hand) {
          toast({
            title: "Missing Information",
            description: "Please complete all player details.",
            variant: "destructive",
          });
          return false;
        }
        break;
    }
    return true;
  };

  const handleNext = () => {
    if (!validateCurrentStep()) {
      return;
    }

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
    if (!validateCurrentStep()) return;
    setIsLoading(true);

    try {
      const response = await registerPlayer(formData);

      // Accept status 200 and a success message as success
      const isSuccess =
        response.success === true ||
        (response.status === 200 &&
          typeof response.message === "string" &&
          response.message.toLowerCase().includes("registered successfully"));

      if (isSuccess) {
        toast({
          title: "Registration Successful!",
          description: response.message || "Your account has been created.",
          variant: "default",
        });
        onLogin(); // Redirect to login page
      } else {
        toast({
          title: "Registration Failed",
          description: response.message || "Unknown error occurred.",
          variant: "destructive",
        });
      }
    } catch (error: any) {
      toast({
        title: "Registration Error",
        description: error.message || "Something went wrong.",
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleProfileImageUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      if (file.size > 5 * 1024 * 1024) {
        toast({
          title: "File Too Large",
          description: "Please select an image smaller than 5MB.",
          variant: "destructive",
        });
        return;
      }
      updateFormData('profile_image', file);
    }
  };

  const fetchNationalities = async (q: string): Promise<SuggestOption[]> => {
    const query = q.trim();
    if (query.length < 2) return [];
    try {
      const url = `http://18.139.29.162/api/getNationalities?name=${encodeURIComponent(query)}`;
      const res = await fetch(url, { cache: "no-store" as RequestCache });
      if (!res.ok) return [];
      const resData = await res.json();
      if (!resData.records || !Array.isArray(resData.records)) return [];
      return resData.records.map((n: { id: number; name: string }) => ({
        label: n.name,
        value: String(n.id),
      }));
    } catch {
      return [];
    }
  };

  const fetchPlayerRoles = async (q: string): Promise<SuggestOption[]> => {
    const query = q.trim();
    if (query.length < 2) return [];
    try {
      const url = `http://18.139.29.162/api/getPlayerRoles?name=${encodeURIComponent(query)}`;
      const res = await fetch(url, { cache: "no-store" as RequestCache });
      if (!res.ok) return [];
      const resData = await res.json();
      if (!resData.records || !Array.isArray(resData.records)) return [];
      return resData.records
        .filter((r: { sport_type: string }) => r.sport_type === formData.sport_type)
        .map((r: { id: number; name: string }) => ({
          label: r.name,
          value: String(r.id),
        }));
    } catch {
      return [];
    }
  };

  const renderStep = () => {
    switch (currentStep) {
      case 1:
        return (
          <div className="space-y-6">
            <h2 className="text-lg font-medium text-center mb-6 text-black">Personal Information</h2>
            <div className="space-y-2">
              <Label htmlFor="name" className="text-base font-normal text-black">Name *</Label>
              <Input
                id="name"
                type="text"
                placeholder="Enter Name"
                value={formData.name}
                onChange={(e) => updateFormData('name', e.target.value)}
                className="h-11 text-sm border-gray-300 rounded-lg hover:border-[#344FA5] focus:border-[#344FA5] transition-colors placeholder:text-gray-500"
                required
                disabled={isLoading}
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="email" className="text-base font-normal text-black">Email *</Label>
              <Input
                id="email"
                type="email"
                placeholder="Enter Email"
                value={formData.email}
                onChange={(e) => updateFormData('email', e.target.value)}
                className="h-11 text-sm border-gray-300 rounded-lg hover:border-[#344FA5] focus:border-[#344FA5] transition-colors placeholder:text-gray-500"
                required
                disabled={isLoading}
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="password" className="text-base font-normal text-black">Password *</Label>
              <Input
                id="password"
                type="password"
                placeholder="Enter Password"
                value={formData.password}
                onChange={(e) => updateFormData('password', e.target.value)}
                className="h-11 text-sm border-gray-300 rounded-lg hover:border-[#344FA5] focus:border-[#344FA5] transition-colors placeholder:text-gray-500"
                required
                disabled={isLoading}
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="sport_type" className="text-base font-normal text-black">Sport Type *</Label>
              <Select 
                value={formData.sport_type} 
                onValueChange={(value) => updateFormData('sport_type', value)}
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
          </div>
        );

      case 2:
        return (
          <div className="space-y-6">
            <h2 className="text-lg font-medium text-center mb-6 text-black">Contact Details</h2>
            <div className="space-y-2">
              <Label htmlFor="phone_number" className="text-base font-normal text-black">Phone Number *</Label>
              <Input
                id="phone_number"
                type="tel"
                placeholder="Enter Phone Number"
                value={formData.phone_number}
                onChange={(e) => updateFormData('phone_number', e.target.value)}
                className="h-11 text-sm border-gray-300 rounded-lg hover:border-[#344FA5] focus:border-[#344FA5] transition-colors placeholder:text-gray-500"
                required
                disabled={isLoading}
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="address" className="text-base font-normal text-black">Address *</Label>
              <Textarea
                id="address"
                placeholder="Enter Address"
                value={formData.address}
                onChange={(e) => updateFormData('address', e.target.value)}
                className="rounded-lg border-gray-300 hover:border-[#344FA5] focus:border-[#344FA5] transition-colors text-sm min-h-[80px] placeholder:text-gray-500"
                required
                disabled={isLoading}
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="gender" className="text-base font-normal text-black">Gender *</Label>
              <Select 
                value={formData.gender} 
                onValueChange={(value) => updateFormData('gender', value)}
                disabled={isLoading}
              >
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
              <Label htmlFor="nationality" className="text-base font-normal text-black">Nationality *</Label>
              <SuggestInput
                value={nationalitySearch}
                onChange={(value) => setNationalitySearch(value)}
                onSelect={(option) => {
                  updateFormData('nationality_id', parseInt(option.value));
                  setNationalitySearch(option.label);
                }}
                fetcher={fetchNationalities}
                placeholder="Type to search nationalities"
                inputClassName="h-11 text-sm border-gray-300 rounded-lg hover:border-[#344FA5] focus:border-[#344FA5] transition-colors placeholder:text-gray-500"
                emptyText="No nationalities found"
              />
            </div>
          </div>
        );

      case 3:
        return (
          <div className="space-y-6">
            <h2 className="text-lg font-medium text-center mb-6 text-black">Profile Setup</h2>
            <div className="space-y-2">
              <Label htmlFor="profile_image" className="text-base font-normal text-black">Profile Image (Optional)</Label>
              <div className="relative">
                <Input
                  id="profile_image"
                  type="file"
                  accept="image/*"
                  onChange={handleProfileImageUpload}
                  className="hidden"
                  disabled={isLoading}
                />
                <Label
                  htmlFor="profile_image"
                  className="flex items-center justify-center h-32 rounded-lg border-2 border-dashed border-gray-300 hover:border-[#344FA5] cursor-pointer text-sm text-gray-500 transition-colors"
                >
                  <div className="text-center">
                    <Upload className="w-8 h-8 mx-auto mb-2" />
                    <p>{formData.profile_image ? formData.profile_image.name : "Upload Profile Image (Optional)"}</p>
                    <p className="text-xs text-gray-400 mt-1">PNG, JPG up to 5MB</p>
                  </div>
                </Label>
                {formData.profile_image && (
                  <div className="mt-2 text-center">
                    <img
                      src={URL.createObjectURL(formData.profile_image)}
                      alt="Profile Preview"
                      className="w-20 h-20 rounded-full mx-auto object-cover"
                    />
                  </div>
                )}
              </div>
            </div>
            <div className="space-y-2">
              <Label htmlFor="date_of_birth" className="text-base font-normal text-black">Date of Birth *</Label>
              <Input
                id="date_of_birth"
                type="date"
                value={formData.date_of_birth}
                onChange={(e) => updateFormData('date_of_birth', e.target.value)}
                className="h-11 text-sm border-gray-300 rounded-lg hover:border-[#344FA5] focus:border-[#344FA5] transition-colors"
                required
                disabled={isLoading}
                max={new Date().toISOString().split('T')[0]}
              />
            </div>
          </div>
        );

      case 4:
        return (
          <div className="space-y-6">
            <h2 className="text-lg font-medium text-center mb-6 text-black">Player Details</h2>
            <div className="space-y-2">
              <Label htmlFor="role" className="text-base font-normal text-black">Role in Team *</Label>
              <SuggestInput
                value={roleSearch}
                onChange={(value) => setRoleSearch(value)}
                onSelect={(option) => {
                  updateFormData('role_id', parseInt(option.value));
                  setRoleSearch(option.label);
                }}
                fetcher={fetchPlayerRoles}
                placeholder="Type to search player roles"
                inputClassName="h-11 text-sm border-gray-300 rounded-lg hover:border-[#344FA5] focus:border-[#344FA5] transition-colors placeholder:text-gray-500"
                emptyText="No roles found"
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="batting_style" className="text-base font-normal text-black">Batting Style *</Label>
              <Select 
                value={formData.batting_style} 
                onValueChange={(value) => updateFormData('batting_style', value)}
                disabled={isLoading}
              >
                <SelectTrigger className="h-11 text-sm border-gray-300 rounded-lg hover:border-[#344FA5] focus:border-[#344FA5] transition-colors">
                  <SelectValue placeholder="Select Batting Style" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="right">Right-handed</SelectItem>
                  <SelectItem value="left">Left-handed</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div className="space-y-2">
              <Label htmlFor="bowling_style" className="text-base font-normal text-black">Bowling Style *</Label>
              <Select 
                value={formData.bowling_style} 
                onValueChange={(value) => updateFormData('bowling_style', value)}
                disabled={isLoading}
              >
                <SelectTrigger className="h-11 text-sm border-gray-300 rounded-lg hover:border-[#344FA5] focus:border-[#344FA5] transition-colors">
                  <SelectValue placeholder="Select Bowling Style" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="right">Right-arm</SelectItem>
                  <SelectItem value="left">Left-arm</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div className="space-y-2">
              <Label htmlFor="dominant_hand" className="text-base font-normal text-black">Dominant Hand *</Label>
              <Select
                value={formData.dominant_hand}
                onValueChange={value => updateFormData('dominant_hand', value)}
                disabled={isLoading}
              >
                <SelectTrigger className="h-11 text-sm border-gray-300 rounded-lg hover:border-[#344FA5] focus:border-[#344FA5] transition-colors">
                  <SelectValue placeholder="Select Dominant Hand" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="right">Right</SelectItem>
                  <SelectItem value="left">Left</SelectItem>
                  <SelectItem value="ambidextrous">Ambidextrous</SelectItem>
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

export default SignUpPage;