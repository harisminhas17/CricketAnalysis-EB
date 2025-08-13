import axios, { AxiosResponse } from "axios";


const API_BASE = "http://18.139.29.162/api/";


const api = axios.create({
  baseURL: API_BASE,
  headers: {
    "Content-Type": "application/json",
  },
});



// Login
export interface LoginRequest {
  email: string;
  password: string;
}
export interface LoginResponse {
  token: string;
  userId: string;
  name: string;
}

// Signup Step 1
export interface SignupStep1Request {
  name: string;
  email: string;
  password: string;
}
export interface SignupStep1Response {
  message: string;
}

// Signup Step 2
export interface SignupStep2Request {
  address: string;
  phone: string;
}
export interface SignupStep2Response {
  message: string;
}

// Forgot Password - Email
export interface ForgotPasswordEmailRequest {
  email: string;
}
export interface ForgotPasswordEmailResponse {
  message: string;
}

// Forgot Password - Verify Code
export interface VerifyCodeRequest {
  code: string;
}
export interface VerifyCodeResponse {
  message: string;
}

// Forgot Password - Reset Password
export interface ResetPasswordRequest {
  newPassword: string;
}
export interface ResetPasswordResponse {
  message: string;
}

// Dashboard Data
export interface DashboardData {
  username: string;
  stats: any;
}



// Login
export const login = (
  data: LoginRequest
): Promise<AxiosResponse<LoginResponse>> =>
  api.post("/login", data);

// Signup Step 1
export const signupStep1 = (
  data: SignupStep1Request
): Promise<AxiosResponse<SignupStep1Response>> =>
  api.post("/signup/step1", data);

// Signup Step 2
export const signupStep2 = (
  data: SignupStep2Request
): Promise<AxiosResponse<SignupStep2Response>> =>
  api.post("/signup/step2", data);

// Forgot Password - Enter Email
export const requestPasswordReset = (
  data: ForgotPasswordEmailRequest
): Promise<AxiosResponse<ForgotPasswordEmailResponse>> =>
  api.post("/forgot-password", data);

// Forgot Password - Verify Code
export const verifyCode = (
  data: VerifyCodeRequest
): Promise<AxiosResponse<VerifyCodeResponse>> =>
  api.post("/verify-code", data);

// Forgot Password - Reset Password
export const resetPassword = (
  data: ResetPasswordRequest
): Promise<AxiosResponse<ResetPasswordResponse>> =>
  api.post("/reset-password", data);

// Dashboard Data
export const getDashboardData = (): Promise<AxiosResponse<DashboardData>> =>
  api.get("/dashboard");

export default api;
