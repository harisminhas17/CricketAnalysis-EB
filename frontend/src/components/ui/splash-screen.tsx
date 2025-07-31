import { useEffect } from "react";
import cricketLogo from "@/assets/cricket-logo.svg";

interface SplashScreenProps {
  onComplete: () => void;
}

export const SplashScreen = ({ onComplete }: SplashScreenProps) => {
  useEffect(() => {
    const timer = setTimeout(() => {
      onComplete();
    }, 2000);

    return () => clearTimeout(timer);
  }, [onComplete]);

  return (
    <div className="min-h-screen bg-white flex flex-col items-center justify-center">
      <div className="animate-fade-in">
        <img 
          src={cricketLogo} 
          alt="CricketZone" 
          className="w-48 h-48 mb-8 animate-pulse"
        />
    
       
      </div>
    </div>
  );
};