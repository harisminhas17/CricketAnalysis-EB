import { useState } from "react";
import { ArrowLeft, Eye, EyeOff, Check } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent } from "@/components/ui/card";
import cricketPlayer from "@/assets/cricket-player.png";

interface ResetPasswordPageProps {
  onBack: () => void;
  onReset: () => void;
}

export const ResetPasswordPage = ({ onBack, onReset }: ResetPasswordPageProps) => {
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);

  const requirements = [
    { text: "Your password must contain", met: password.length > 0 },
    { text: "Contains at least 6 digit", met: password.length >= 6 },
    { text: "Contains a number", met: /\d/.test(password) },
  ];

  const passwordsMatch = password === confirmPassword;

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const allRequirementsMet = requirements.every(req => req.met);
    if (allRequirementsMet && passwordsMatch) {
      onReset();
    }
  };

  return (
    <div className="w-full max-w-7xl mx-auto grid lg:grid-cols-3 gap-8 items-center min-h-screen px-4 py-8">
      {/* Left side - Reset Password Form */}
      <div className="lg:col-span-2 flex justify-center">
        <Card className="w-full max-w-2xl border border-gray-300 shadow-sm bg-white hover:border-[#344FA5] hover:shadow-lg transition-all duration-300 ease-in-out">
          <CardContent className="p-8">
            <button
              onClick={onBack}
              type="button"
              className="hover:bg-gray-100 p-2 rounded-full transition-colors mb-6 inline-flex items-center"
            >
              <ArrowLeft className="w-5 h-5 text-gray-600" />
            </button>

            {/* Headings */}
            <h1 className="text-2xl font-semibold text-black text-center mb-2">
              Recover PASSWORD
            </h1>
            <p className="text-sm text-center text-gray-600 mb-8">
              Please enter your new password
            </p>

            <form onSubmit={handleSubmit} className="space-y-6">
              {/* New Password Field */}
              <div className="space-y-2">
                <Label htmlFor="password" className="text-base font-normal text-black">
                  New Password
                </Label>
                <div className="relative">
                  <Input
                    id="password"
                    type={showPassword ? "text" : "password"}
                    placeholder="Enter new password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    className="h-11 text-sm border-gray-300 rounded-lg hover:border-[#344FA5] focus:border-[#344FA5] transition-colors placeholder:text-gray-500 pr-10"
                    required
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute inset-y-0 right-0 flex items-center pr-3 text-gray-400 hover:text-gray-600"
                  >
                    {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                  </button>
                </div>
              </div>

              {/* Password Requirements */}
              <div className="space-y-3">
                {requirements.map((requirement, index) => (
                  <div key={index} className="flex items-center gap-2">
                    <div
                      className={`w-5 h-5 rounded-full flex items-center justify-center ${
                        requirement.met ? "bg-[#344FA5]" : "bg-gray-200"
                      }`}
                    >
                      {requirement.met && <Check className="w-3 h-3 text-white" />}
                    </div>
                    <span
                      className={`text-sm ${
                        requirement.met ? "text-[#344FA5]" : "text-gray-600"
                      }`}
                    >
                      {requirement.text}
                    </span>
                  </div>
                ))}
              </div>

              {/* Confirm Password Field */}
              <div className="space-y-2">
                <Label htmlFor="confirm-password" className="text-base font-normal text-black">
                  Confirm Password
                </Label>
                <div className="relative">
                  <Input
                    id="confirm-password"
                    type={showConfirmPassword ? "text" : "password"}
                    placeholder="Re-enter new password"
                    value={confirmPassword}
                    onChange={(e) => setConfirmPassword(e.target.value)}
                    className="h-11 text-sm border-gray-300 rounded-lg hover:border-[#344FA5] focus:border-[#344FA5] transition-colors placeholder:text-gray-500 pr-10"
                    required
                  />
                  <button
                    type="button"
                    onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                    className="absolute inset-y-0 right-0 flex items-center pr-3 text-gray-400 hover:text-gray-600"
                  >
                    {showConfirmPassword ? (
                      <EyeOff className="h-4 w-4" />
                    ) : (
                      <Eye className="h-4 w-4" />
                    )}
                  </button>
                </div>
                {!passwordsMatch && confirmPassword.length > 0 && (
                  <p className="text-sm text-red-500">Passwords do not match</p>
                )}
              </div>

              {/* Submit Button */}
              <div className="flex justify-center">
                <Button
                  type="submit"
                  disabled={!requirements.every(req => req.met) || !passwordsMatch}
                  className="bg-[#344FA5] hover:bg-[#2a3f8f] text-white text-base font-medium rounded-lg transition-colors disabled:bg-gray-300 disabled:cursor-not-allowed"
                  style={{ width: "160px", height: "55px" }}
                >
                  Done
                </Button>
              </div>
            </form>
          </CardContent>
        </Card>
      </div>

      {/* Right side - Illustration */}
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
