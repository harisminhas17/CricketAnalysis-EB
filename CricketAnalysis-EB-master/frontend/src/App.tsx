// App.tsx

import { Provider } from 'react-redux';
import { store } from './store/store';
import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route /* , Navigate */ } from "react-router-dom";



//import Index from "./pages/player/Index";
//import { HomePage } from "./pages/player/home‑page";
//import { LoginForm } from "./components/player/auth/login‑page";
//import { SignUpPage } from "./components/player/auth/signup‑page";
//import { ForgotPasswordPage } from "./components/player/auth/forgot‑password‑page";
//import { OTPVerificationPage } from "./components/player/auth/otp‑verification‑page";
//import { ResetPasswordPage } from "./components/player/auth/reset‑password‑page";
//import { OnboardingCarousel } from "./components/player/onboarding/onboarding‑carousel";
 

// ✅ Superadmin imports remain active
import Signup1 from "./pages/superadmin/signup1";
import Signup2 from "./pages/superadmin/signup2";
import Signup3 from "./pages/superadmin/signup3";
import Signin from "./pages/superadmin/signin";
const queryClient = new QueryClient();

const App: React.FC = () => (
  <Provider store={store}>
    <QueryClientProvider client={queryClient}>
      <TooltipProvider>
        <Toaster />
        <Sonner />
        <BrowserRouter>
          <Routes>
            {/* Player routes commented out so only Superadmin routes show */}
            {/*
              <Route path="/" element={<Index />} />
              <Route
                path="/login"
                element={<LoginForm
                  onBack={() => {}}
                  onLogin={() => {}}
                  onForgotPassword={() => {}}
                  onSignUp={() => {}}
                />}
              />
              <Route
                path="/signup"
                element={<SignUpPage
                  onBack={() => {}}
                  onSignUp={() => {}}
                  onLogin={() => {}}
                />}
              />
              <Route
                path="/forgot-password"
                element={<ForgotPasswordPage onBack={() => {}} onRecover={() => {}} />}
              />
              <Route
                path="/otp-verification"
                element={<OTPVerificationPage onBack={() => {}} onVerify={() => {}} />}
              />
              <Route
                path="/reset-password"
                element={<ResetPasswordPage onBack={() => {}} onReset={() => {}} />}
              />
              <Route path="/home" element={<HomePage onLogout={() => {}} />} />
              <Route path="/dashboard" element={<HomePage onLogout={() => {}} />} />
              <Route
                path="/onboarding"
                element={<OnboardingCarousel onComplete={() => {}} />}
              />
            */}

            {/* 👇 These Superadmin routes stay active */}
            <Route path="/superadmin/signup1" element={<Signup1 />} />
            <Route path="/superadmin/signup2" element={<Signup2 />} />
            <Route path="/superadmin/signup3" element={<Signup3 />} />
            <Route path="/superadmin/signin" element={<Signin />} />
           
            

            {/* Catch-all fallback (Only signup flows will render) */}
            <Route path="*" element={<Signup1 />} />
          </Routes>
        </BrowserRouter>
      </TooltipProvider>
    </QueryClientProvider>
  </Provider>
);

export default App;
