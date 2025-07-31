import { useState } from "react";
import { ArrowLeft, Upload } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Checkbox } from "@/components/ui/checkbox";
import { Textarea } from "@/components/ui/textarea";
import { Card, CardContent } from "@/components/ui/card";
import cricketPlayer from "@/assets/cricket-player.png";

interface SignUpPageProps {
  onBack: () => void;
  onSignUp: () => void;
  onLogin: () => void;
}

interface FormData {
  // Personal Information
  name: string;
  email: string;
  password: string;
  dateOfBirth: string;
  
  // Player Details
  nationality: string;
  roleInTeam: string;
  battingStyle: string;
  bowlingStyle: string;
  
  // Performance & Upload
  clipFile: File | null;
  tag: string;
  title: string;
  description: string;
  
  // Access & Permission
  assignToSession: string;
  grantAccessTo: string;
  accessType: string[];
}

export const SignUpPage = ({ onBack, onSignUp, onLogin }: SignUpPageProps) => {
  const [currentStep, setCurrentStep] = useState(1);
  const [formData, setFormData] = useState<FormData>({
    name: "",
    email: "",
    password: "",
    dateOfBirth: "",
    nationality: "",
    roleInTeam: "",
    battingStyle: "",
    bowlingStyle: "",
    clipFile: null,
    tag: "",
    title: "",
    description: "",
    assignToSession: "",
    grantAccessTo: "",
    accessType: []
  });

  const updateFormData = (field: keyof FormData, value: any) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const handleNext = () => {
    if (currentStep < 4) {
      setCurrentStep(currentStep + 1);
    } else {
      onSignUp();
    }
  };

  const handleBack = () => {
    if (currentStep > 1) {
      setCurrentStep(currentStep - 1);
    } else {
      onBack();
    }
  };

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      updateFormData('clipFile', file);
    }
  };

  const handleAccessTypeChange = (accessType: string, checked: boolean) => {
    const currentAccessTypes = formData.accessType;
    if (checked) {
      updateFormData('accessType', [...currentAccessTypes, accessType]);
    } else {
      updateFormData('accessType', currentAccessTypes.filter(type => type !== accessType));
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
              <Label htmlFor="dob" className="text-base font-normal text-black">Date of Birth</Label>
              <Input
                id="dob"
                type="date"
                placeholder="Enter Date"
                value={formData.dateOfBirth}
                onChange={(e) => updateFormData('dateOfBirth', e.target.value)}
                max={new Date().toISOString().split('T')[0]}
                className="h-11 text-sm border-gray-300 rounded-lg hover:border-[#344FA5] focus:border-[#344FA5] transition-colors placeholder:text-gray-500"
                required
              />
            </div>
          </div>
        );

      case 2:
        return (
          <div className="space-y-6">
            <h2 className="text-lg font-medium text-center mb-6 text-black">Player Details</h2>
            
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
                </SelectContent>
              </Select>
            </div>
            
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

      case 3:
        return (
          <div className="space-y-6">
            <h2 className="text-lg font-medium text-center mb-6 text-black">Performance & Upload</h2>
            
            <div className="space-y-2">
              <Label htmlFor="clip" className="text-base font-normal text-black">Clip Upload</Label>
              <div className="relative">
                <Input
                  id="clip"
                  type="file"
                  accept="video/*"
                  onChange={handleFileUpload}
                  className="hidden"
                />
                <Label
                  htmlFor="clip"
                  className="flex items-center justify-center h-11 rounded-lg border-2 border-dashed border-gray-300 hover:border-[#344FA5] cursor-pointer text-sm text-gray-500 transition-colors"
                >
                  <Upload className="w-4 h-4 mr-2" />
                  {formData.clipFile ? formData.clipFile.name : "Upload clip"}
                </Label>
              </div>
            </div>
            
            <div className="space-y-2">
              <Label htmlFor="tag" className="text-base font-normal text-black">Tag</Label>
              <Input
                id="tag"
                type="text"
                placeholder="Enter Tag"
                value={formData.tag}
                onChange={(e) => updateFormData('tag', e.target.value)}
                className="h-11 text-sm border-gray-300 rounded-lg hover:border-[#344FA5] focus:border-[#344FA5] transition-colors placeholder:text-gray-500"
              />
            </div>
            
            <div className="space-y-2">
              <Label htmlFor="title" className="text-base font-normal text-black">Title</Label>
              <Input
                id="title"
                type="text"
                placeholder="Enter Title"
                value={formData.title}
                onChange={(e) => updateFormData('title', e.target.value)}
                className="h-11 text-sm border-gray-300 rounded-lg hover:border-[#344FA5] focus:border-[#344FA5] transition-colors placeholder:text-gray-500"
              />
            </div>
            
            <div className="space-y-2">
              <Label htmlFor="description" className="text-base font-normal text-black">Description</Label>
              <Textarea
                id="description"
                placeholder="Enter Description"
                value={formData.description}
                onChange={(e) => updateFormData('description', e.target.value)}
                className="rounded-lg border-gray-300 hover:border-[#344FA5] focus:border-[#344FA5] transition-colors text-sm min-h-[80px] placeholder:text-gray-500"
              />
            </div>
          </div>
        );

      case 4:
        return (
          <div className="space-y-6">
            <h2 className="text-lg font-medium text-center mb-6 text-black">Access & Permission</h2>
            
            <div className="space-y-2">
              <Label htmlFor="session" className="text-base font-normal text-black">Assign to session</Label>
              <Select value={formData.assignToSession} onValueChange={(value) => updateFormData('assignToSession', value)}>
                <SelectTrigger className="h-11 text-sm border-gray-300 rounded-lg hover:border-[#344FA5] focus:border-[#344FA5] transition-colors">
                  <SelectValue placeholder="Select Session" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="training1">Training Session 1</SelectItem>
                  <SelectItem value="training2">Training Session 2</SelectItem>
                  <SelectItem value="match1">Match Session 1</SelectItem>
                  <SelectItem value="practice">Practice Session</SelectItem>
                </SelectContent>
              </Select>
            </div>
            
            <div className="space-y-2">
              <Label htmlFor="access" className="text-base font-normal text-black">Grant Access To</Label>
              <Select value={formData.grantAccessTo} onValueChange={(value) => updateFormData('grantAccessTo', value)}>
                <SelectTrigger className="h-11 text-sm border-gray-300 rounded-lg hover:border-[#344FA5] focus:border-[#344FA5] transition-colors">
                  <SelectValue placeholder="Access Type" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="coach">Coach</SelectItem>
                  <SelectItem value="team">Team Members</SelectItem>
                  <SelectItem value="public">Public</SelectItem>
                  <SelectItem value="private">Private</SelectItem>
                </SelectContent>
              </Select>
            </div>
            
            <div className="space-y-4">
              <Label className="text-base font-normal text-black">Access Type</Label>
              <div className="space-y-3">
                <div className="flex items-center space-x-2">
                  <Checkbox
                    id="video"
                    checked={formData.accessType.includes('video')}
                    onCheckedChange={(checked) => handleAccessTypeChange('video', checked as boolean)}
                  />
                  <Label htmlFor="video" className="text-sm text-black">Video</Label>
                </div>
                <div className="flex items-center space-x-2">
                  <Checkbox
                    id="stats"
                    checked={formData.accessType.includes('stats')}
                    onCheckedChange={(checked) => handleAccessTypeChange('stats', checked as boolean)}
                  />
                  <Label htmlFor="stats" className="text-sm text-black">Stats</Label>
                </div>
                <div className="flex items-center space-x-2">
                  <Checkbox
                    id="all"
                    checked={formData.accessType.includes('all')}
                    onCheckedChange={(checked) => handleAccessTypeChange('all', checked as boolean)}
                  />
                  <Label htmlFor="all" className="text-sm text-black">All</Label>
                </div>
              </div>
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
                  className="bg-[#344FA5] hover:bg-[#2a3f8f] text-white text-base font-medium rounded-lg transition-colors"
                  style={{ width: '160px', height: '55px' }}
                >
                  {currentStep === 4 ? 'Sign up' : 'Next'}
                </Button>
              </div>
            </form>
            
            {currentStep === 4 && (
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