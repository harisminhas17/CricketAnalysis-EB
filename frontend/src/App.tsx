import { Provider } from 'react-redux';
import { store } from './store/store';
import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route, useNavigate } from "react-router-dom"; 
import Index from "./pages/player/Index";
import NotFound from "./pages/NotFound";
import { HomePage } from "./pages/player/home-page";
import { LoginForm } from "./components/player/auth/login-page";
import { SignUpPage } from "./components/player/auth/signup-page";
import { ForgotPasswordPage } from "./components/player/auth/forgot-password-page";
import { OTPVerificationPage } from "./components/player/auth/otp-verification-page";
import { ResetPasswordPage } from "./components/player/auth/reset-password-page";
import { OnboardingCarousel } from "./components/player/onboarding/onboarding-carousel";
import { BallTracking } from "./components/player/home/BallTracking";
import { Following } from "./components/player/home/Following";
import { StatsModule } from "./components/player/home/StatsModule";
import { ProfileManagement } from "./components/player/profile/profile-management";

const queryClient = new QueryClient();

const AppRoutes = () => {
  const navigate = useNavigate();

  const handleLogin = () => {
    navigate('/dashboard');
  };

  const handleSignUp = () => {
    navigate('/signup');
  };

  const handleForgotPassword = () => {
    navigate('/forgot-password');
  };

  const handleBack = () => {
    navigate(-1);
  };

  return (
    <Routes>
      <Route path="/" element={<Index />} />
      
      {/* Authentication Routes */}
      <Route 
            path="/login" 
        element={
          <LoginForm 
            onBack={handleBack} 
            onLogin={() => navigate('/dashboard')} // Explicitly navigate to dashboard
            onForgotPassword={handleForgotPassword} 
            onSignUp={() => navigate('/signup')} 
          />
        } 
      />
      <Route 
              path="/signup" 
        element={
          <SignUpPage 
            onBack={handleBack} 
            onSignUp={() => navigate('/login')} // Changed this to go to login after signup
            onLogin={() => navigate('/login')} 
          />
        } 
      />
      <Route path="/forgot-password" element={<ForgotPasswordPage onBack={() => {}} onRecover={() => {}} />} />
      <Route path="/otp-verification" element={<OTPVerificationPage onBack={() => {}} onVerify={() => {}} />} />
      <Route path="/reset-password" element={<ResetPasswordPage onBack={() => {}} onReset={() => {}} />} />
      
      {/* Main Application Routes */}
      <Route path="/home" element={<HomePage onLogout={() => {}} />} />
      <Route path="/dashboard" element={<HomePage onLogout={() => {}} />} />
      
      {/* Player Feature Routes */}
      <Route path="/ball-tracking" element={<BallTracking />} />
      <Route path="/following" element={<Following />} />
      <Route path="/stats" element={<StatsModule />} />
      <Route path="/statistics" element={<StatsModule />} />
      
      {/* Profile Routes */}
      <Route path="/profile" element={<ProfileManagement />} />
      <Route path="/profile/edit" element={<ProfileManagement />} />
      <Route path="/profile/settings" element={<ProfileManagement />} />
      
      {/* Onboarding Routes */}
      <Route path="/onboarding" element={<OnboardingCarousel onComplete={() => {}} />} />
      
      {/* ADD ALL CUSTOM ROUTES ABOVE THE CATCH-ALL "*" ROUTE */}
      <Route path="*" element={<NotFound />} />
    </Routes>
  );
};

const App = () => {
  return (
    <Provider store={store}>
      <QueryClientProvider client={queryClient}>
        <TooltipProvider>
          <Toaster />
          <Sonner />
          <BrowserRouter>
            <AppRoutes />
          </BrowserRouter>
        </TooltipProvider>
      </QueryClientProvider>
    </Provider>
  );
};

export default App;