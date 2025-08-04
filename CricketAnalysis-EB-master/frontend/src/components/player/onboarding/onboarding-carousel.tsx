import { useState } from "react";
import { Button } from "@/components/ui/button";
import cricketTeam from "@/assets/cricket-team.png";
import cricketAnalytics from "@/assets/cricket-analytics.png";
import cricketAction from "@/assets/cricket-action.png";

interface OnboardingCarouselProps {
  onComplete: () => void;
}

const onboardingSlides = [
  {
    id: 1,
    image: cricketTeam,
    title: "Track Your Performance",
    description: "Monitor your runs, wickets, and match insights in real-time.",
  },
  {
    id: 2,
    image: cricketAnalytics,
    title: "Share Your Highlights",
    description: "Upload cricket moments and videos to build your profile.",
  },
  {
    id: 3,
    image: cricketAction,
    title: "Connect with Other Players",
    description: "Follow players, compare stats, and rise on the leaderboard.",
  }
];

export const OnboardingCarousel = ({ onComplete }: OnboardingCarouselProps) => {
  const [currentSlide, setCurrentSlide] = useState(0);

  const nextSlide = () => {
    if (currentSlide < onboardingSlides.length - 1) {
      setCurrentSlide(currentSlide + 1);
    } else {
      onComplete();
    }
  };

  const slide = onboardingSlides[currentSlide];

  return (
    <div className="min-h-screen bg-white flex flex-col items-center justify-center p-4 font-[Poppins]">
      <div className="flex-1 flex flex-col justify-center items-center w-full max-w-2xl mx-auto text-center">
        <div className="mb-8 w-full flex flex-col items-center">
          <img 
            src={slide.image} 
            alt={slide.title}
            className="w-full max-w-2xl mx-auto mb-6 animate-fade-in rounded-lg object-contain max-h-[300px] sm:max-h-[400px]"
            style={{ height: 'auto' }}
          />
          <h1 className="font-bold mb-3 text-foreground text-[32px]">
            {slide.title}
          </h1>
          <p className="text-muted-foreground mb-2 text-[16px]">
            {slide.description}
          </p>
        </div>
        {/* Progress indicators */}
        <div className="flex justify-center gap-2 mb-8">
          {onboardingSlides.map((_, index) => (
            <div
              key={index}
              className={`h-2 rounded-full transition-all duration-300 ${
                index === currentSlide 
                  ? '' 
                  : 'w-2 bg-gray-300'
              }`}
              style={index === currentSlide ? { width: 32, backgroundColor: '#344FA5' } : undefined}
            />
          ))}
        </div>
      </div>
      <div className="w-full max-w-xs mx-auto pb-6">
        <Button 
          variant="auth" 
          onClick={nextSlide}
          className="w-full"
        >
          {currentSlide === onboardingSlides.length - 1 ? 'Get Started' : 'Next'}
        </Button>
      </div>
    </div>
  );
};