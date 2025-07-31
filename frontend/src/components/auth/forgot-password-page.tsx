import { useState } from "react";
import { ArrowLeft, Mail } from "lucide-react";
import { Button } from "../ui/button";
import { Input } from "../ui/input";
import { Label } from "../ui/label";
import { Card, CardContent } from "../ui/card";
import cricketPlayer from "@/assets/cricket-player.png";

interface ForgotPasswordPageProps {
  onBack: () => void;
  onRecover: () => void;
}

export const ForgotPasswordPage = ({ onBack, onRecover }: ForgotPasswordPageProps) => {
  const [email, setEmail] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onRecover();
  };

  return (
    <div className="w-full max-w-7xl mx-auto grid lg:grid-cols-3 gap-8 items-center min-h-screen px-4 py-8">
      {/* Left side - Forgot Password Form (takes 2 columns) */}
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

            {/* Password Recovery Heading */}
            <h1 className="text-2xl font-semibold text-black text-center mb-2">
              Password Recovery
            </h1>
            <p className="text-sm text-center text-gray-600 mb-8">
              Enter your email to recover your password
            </p>

            <form onSubmit={handleSubmit} className="space-y-6">
              {/* Email Field */}
              <div className="space-y-2">
                <Label htmlFor="email" className="text-base font-normal text-black">
                  Email
                </Label>
                <div className="relative">
                  <Input
                    id="email"
                    type="email"
                    placeholder="pakizasardar10@gmail.com"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    className="h-11 text-sm border-gray-300 rounded-lg hover:border-[#344FA5] focus:border-[#344FA5] transition-colors placeholder:text-gray-500 pl-12"
                    required
                  />
                  <Mail className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
                </div>
              </div>

              {/* Submit Button */}
              <div className="flex justify-center">
                <Button
                  type="submit"
                  className="bg-[#344FA5] hover:bg-[#2a3f8f] text-white text-base font-medium rounded-lg transition-colors"
                  style={{ width: '200px', height: '60px' }}
                >
                  Recover Password
                </Button>
              </div>
            </form>
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