import { useState, useEffect } from "react";
import { ArrowLeft } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { InputOTP, InputOTPGroup, InputOTPSeparator, InputOTPSlot } from "@/components/ui/input-otp";
import cricketPlayer from "@/assets/cricket-player.png";

interface OTPVerificationPageProps {
  onBack: () => void;
  onVerify: () => void;
}

export const OTPVerificationPage = ({ onBack, onVerify }: OTPVerificationPageProps) => {
  const [otp, setOtp] = useState("");
  const [timeLeft, setTimeLeft] = useState(180); // 3 minutes

  useEffect(() => {
    if (timeLeft > 0) {
      const timer = setTimeout(() => setTimeLeft(timeLeft - 1), 1000);
      return () => clearTimeout(timer);
    }
  }, [timeLeft]);

  const formatTime = (seconds: number) => {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    return `${minutes.toString().padStart(2, '0')}:${remainingSeconds.toString().padStart(2, '0')}`;
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (otp.length === 5) {
      onVerify();
    }
  };

  const handleResend = () => {
    setTimeLeft(180);
    setOtp("");
  };

  return (
    <div className="w-full max-w-7xl mx-auto grid lg:grid-cols-3 gap-8 items-center min-h-screen px-4 py-8">
      {/* Left side - OTP Verification Form (takes 2 columns) */}
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

            {/* OTP Verification Heading */}
            <h1 className="text-2xl font-semibold text-black text-center mb-2">
              Check your phone
            </h1>
            <p className="text-sm text-center text-gray-600 mb-8">
              We've sent the code to your phone
            </p>
            <form onSubmit={handleSubmit} className="space-y-6">
              <div className="flex justify-center">
                <InputOTP 
                  maxLength={5} 
                  value={otp} 
                  onChange={setOtp}
                  className="gap-2"
                >
                  <InputOTPGroup>
                    <InputOTPSlot index={0} className="w-12 h-12 border-2 border-gray-200 focus:border-primary" />
                    <InputOTPSlot index={1} className="w-12 h-12 border-2 border-gray-200 focus:border-primary" />
                    <InputOTPSlot index={2} className="w-12 h-12 border-2 border-gray-200 focus:border-primary" />
                    <InputOTPSlot index={3} className="w-12 h-12 border-2 border-gray-200 focus:border-primary" />
                    <InputOTPSlot index={4} className="w-12 h-12 border-2 border-gray-200 focus:border-primary" />
                  </InputOTPGroup>
                </InputOTP>
              </div>
              
              <div className="text-center">
                <p className="text-sm text-gray-600 mb-4">
                  Code expires in: <span className="font-medium">{formatTime(timeLeft)}</span>
                </p>
              </div>
              
              <div className="flex justify-center">
                <Button
                  type="submit"
                  disabled={otp.length !== 5}
                  className="bg-[#344FA5] hover:bg-[#2a3f8f] text-white text-base font-medium rounded-lg transition-colors"
                  style={{ width: '160px', height: '55px' }}
                >
                  Verify
                </Button>
              </div>
              
              <div className="flex justify-center">
                <Button
                  type="button"
                  onClick={handleResend}
                  disabled={timeLeft > 0}
                  className="bg-gray-100 hover:bg-gray-200 text-gray-700 text-base font-medium rounded-lg transition-colors"
                  style={{ width: '160px', height: '55px' }}
                >
                  Send Again
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