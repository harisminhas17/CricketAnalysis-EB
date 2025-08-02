import { useEffect } from "react";
import { useAppSelector, useAppDispatch } from "@/hooks/redux";
import { setCurrentState, setFirstLaunch } from "@/store/slices/appSlice";
import { SplashScreen } from "@/components/ui/splash-screen";
import { LoadingScreen } from "@/components/ui/loading-screen";
import { LoginForm } from "@/components/player/auth/login-page";
import { SignUpPage } from "@/components/player/auth/signup-page";
import { ForgotPasswordPage } from "@/components/player/auth/forgot-password-page";
import { OTPVerificationPage } from "@/components/player/auth/otp-verification-page";
import { ResetPasswordPage } from "@/components/player/auth/reset-password-page";
import { OnboardingCarousel } from "@/components/player/onboarding/onboarding-carousel";
import { HomePage } from "./home-page";

const Index = () => {
  const dispatch = useAppDispatch();
  const { currentState, isFirstLaunch } = useAppSelector((state) => state.app);

  return (
    <div className="min-h-screen">
      {currentState === "splash" && (
        <SplashScreen onComplete={() => dispatch(setCurrentState("loading"))} />
      )}

      {currentState === "loading" && (
        <LoadingScreen onComplete={() => {
          if (isFirstLaunch) {
            dispatch(setCurrentState("onboarding"));
          } else {
            dispatch(setCurrentState("login"));
          }
        }} />
      )}

      {currentState === "onboarding" && (
        <OnboardingCarousel onComplete={() => {
          dispatch(setFirstLaunch(false));
          dispatch(setCurrentState("login"));
        }} />
      )}

      {currentState === "login" && (
        <LoginForm
          onBack={() => dispatch(setCurrentState("login"))}
          onLogin={() => dispatch(setCurrentState("home"))}
          onForgotPassword={() => dispatch(setCurrentState("forgot-password"))}
          onSignUp={() => dispatch(setCurrentState("signup"))}
        />
      )}

      {currentState === "signup" && (
        <SignUpPage
          onBack={() => dispatch(setCurrentState("login"))}
          onSignUp={() => dispatch(setCurrentState("login"))}
          onLogin={() => dispatch(setCurrentState("login"))}
        />
      )}

      {currentState === "forgot-password" && (
        <ForgotPasswordPage
          onBack={() => dispatch(setCurrentState("login"))}
          onRecover={() => dispatch(setCurrentState("otp-verification"))}
        />
      )}

      {currentState === "otp-verification" && (
        <OTPVerificationPage
          onBack={() => dispatch(setCurrentState("forgot-password"))}
          onVerify={() => dispatch(setCurrentState("reset-password"))}
        />
      )}

      {currentState === "reset-password" && (
        <ResetPasswordPage
          onBack={() => dispatch(setCurrentState("otp-verification"))}
          onReset={() => dispatch(setCurrentState("login"))}
        />
      )}

      {currentState === "home" && (
        <HomePage
          onLogout={() => dispatch(setCurrentState("login"))}
        />
      )}
    </div>
  );
};

export default Index;
