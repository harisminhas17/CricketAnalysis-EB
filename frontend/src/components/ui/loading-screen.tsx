import { useEffect, useState } from "react";

interface LoadingScreenProps {
  onComplete: () => void;
}

export const LoadingScreen = ({ onComplete }: LoadingScreenProps) => {
  const [progress, setProgress] = useState(0);

  useEffect(() => {
    let frame = 0;
    const totalFrames = 60; // 1.5s at 60fps
    const interval = setInterval(() => {
      frame++;
      setProgress(frame / totalFrames);
      if (frame >= totalFrames) {
        clearInterval(interval);
        onComplete();
      }
    }, 25);
    return () => clearInterval(interval);
  }, [onComplete]);

  return (
    <div className="min-h-screen flex items-center justify-center bg-white">
      <div className="w-64 h-4 flex items-center">
        <div className="relative w-full h-2 bg-gray-100 rounded-full shadow-md">
          <div
            className="absolute top-0 left-0 h-2 bg-blue-800 rounded-full shadow"
            style={{ width: `${progress * 100}%`, transition: 'width 0.2s linear' }}
          />
        </div>
      </div>
    </div>
  );
};