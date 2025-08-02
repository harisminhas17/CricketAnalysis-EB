import { Provider } from 'react-redux';
import { store } from './store/store';
import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Index from "./pages/player/Index";
import NotFound from "./pages/NotFound";
import { HomePage } from "./pages/player/home-page";
import { LoginForm } from "./components/player/auth/login-page";
import { SignUpPage } from "./components/player/auth/signup-page";
import { ForgotPasswordPage } from "./components/player/auth/forgot-password-page";
import { OTPVerificationPage } from "./components/player/auth/otp-verification-page";
import { ResetPasswordPage } from "./components/player/auth/reset-password-page";
import { OnboardingCarousel } from "./components/player/onboarding/onboarding-carousel";

const queryClient = new QueryClient();

const App = () => (
  <Provider store={store}>
    <QueryClientProvider client={queryClient}>
      <TooltipProvider>
        <Toaster />
        <Sonner />
        <BrowserRouter>
          <Routes>
            <Route path="/" element={<Index />} />
            
            {/* Authentication Routes */}
            <Route path="/login" element={<LoginForm onBack={() => {}} onLogin={() => {}} onForgotPassword={() => {}} onSignUp={() => {}} />} />
            <Route path="/signup" element={<SignUpPage onBack={() => {}} onSignUp={() => {}} onLogin={() => {}} />} />
            <Route path="/forgot-password" element={<ForgotPasswordPage onBack={() => {}} onRecover={() => {}} />} />
            <Route path="/otp-verification" element={<OTPVerificationPage onBack={() => {}} onVerify={() => {}} />} />
            <Route path="/reset-password" element={<ResetPasswordPage onBack={() => {}} onReset={() => {}} />} />
            
            {/* Main Application Routes */}
            <Route path="/home" element={<HomePage onLogout={() => {}} />} />
            <Route path="/dashboard" element={<HomePage onLogout={() => {}} />} />
            
            {/* Onboarding Routes */}
            <Route path="/onboarding" element={<OnboardingCarousel onComplete={() => {}} />} />
            
            {/* ADD ALL CUSTOM ROUTES ABOVE THE CATCH-ALL "*" ROUTE */}
            <Route path="*" element={<NotFound />} />
          </Routes>
        </BrowserRouter>
      </TooltipProvider>
    </QueryClientProvider>
  </Provider>
);

export default App;
