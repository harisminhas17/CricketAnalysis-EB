import api from '@/lib/api';

// Types for API requests and responses
export interface LoginRequest {
  email: string;
  password: string;
  sportType: string;
}

export interface RegisterRequest {
  // Personal Information
  name: string;
  email: string;
  password: string;
  sportType: string;
  
  // Contact & Location
  phoneNo: string;
  address: string;
  gender: string;
  nationality: string;
  
  // Profile
  dateOfBirth: string;
  profileImage?: File;
  
  // Player Details
  roleInTeam: string;
  battingStyle: string;
  bowlingStyle: string;
}

export interface AuthResponse {
  success: boolean;
  message: string;
  data?: {
    token: string;
    user: {
      id: string;
      name: string;
      email: string;
      sportType: string;
      profileImage?: string;
    };
  };
  error?: string;
}

export interface ApiError {
  message: string;
  status: number;
  errors?: Record<string, string[]>;
}

// Login API function
export const loginPlayer = async (loginData: LoginRequest): Promise<AuthResponse> => {
  try {
    const response = await api.post('/playerLogin', loginData);
    
    // Store token and user data in localStorage
    if (response.data.success && response.data.data?.token) {
      localStorage.setItem('authToken', response.data.data.token);
      localStorage.setItem('userData', JSON.stringify(response.data.data.user));
    }
    
    return response.data;
  } catch (error: any) {
    console.error('Login error:', error);
    
    // Handle different error scenarios
    if (error.response?.data) {
      throw {
        message: error.response.data.message || 'Login failed',
        status: error.response.status,
        errors: error.response.data.errors,
      } as ApiError;
    }
    
    throw {
      message: 'Network error. Please check your connection.',
      status: 0,
    } as ApiError;
  }
};

// Register API function
export const registerPlayer = async (registerData: RegisterRequest): Promise<AuthResponse> => {
  try {
    // Create FormData for file upload
    const formData = new FormData();
    
    // Append all form fields
    Object.entries(registerData).forEach(([key, value]) => {
      if (key === 'profileImage' && value instanceof File) {
        formData.append('profileImage', value);
      } else if (value !== null && value !== undefined) {
        formData.append(key, String(value));
      }
    });
    
    const response = await api.post('/playerRegister', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    
    // Store token and user data if registration is successful
    if (response.data.success && response.data.data?.token) {
      localStorage.setItem('authToken', response.data.data.token);
      localStorage.setItem('userData', JSON.stringify(response.data.data.user));
    }
    
    return response.data;
  } catch (error: any) {
    console.error('Registration error:', error);
    
    if (error.response?.data) {
      throw {
        message: error.response.data.message || 'Registration failed',
        status: error.response.status,
        errors: error.response.data.errors,
      } as ApiError;
    }
    
    throw {
      message: 'Network error. Please check your connection.',
      status: 0,
    } as ApiError;
  }
};

// Logout function
export const logoutPlayer = () => {
  localStorage.removeItem('authToken');
  localStorage.removeItem('userData');
};

// Get current user data
export const getCurrentUser = () => {
  const userData = localStorage.getItem('userData');
  return userData ? JSON.parse(userData) : null;
};

// Check if user is authenticated
export const isAuthenticated = (): boolean => {
  const token = localStorage.getItem('authToken');
  return !!token;
};