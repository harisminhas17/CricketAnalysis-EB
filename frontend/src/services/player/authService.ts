import api from '@/lib/api';

// Updated LoginRequest interface
export interface LoginRequest {
  email?: string;
  phone_number?: string;
  password: string;
  sport_type: string;
  login_type: string;
}

export interface RegisterRequest {
  // Personal Information
  name: string;
  email: string;
  password: string;
  sport_type: string;
  login_type: string;

  // Contact & Location
  phone_number: string;
  address: string;
  gender: string;
  nationality_id: number;

  // Profile
  date_of_birth: string;
  profile_image?: File;

  // Player Details
  role_id: number;
  batting_style: string;
  bowling_style: string;
  dominant_hand: string;
}

export interface AuthResponse {
  success: boolean;
  message: string;
  status?: number; // <-- Add this line
  data?: {
    token: string;
    user: {
      id: string;
      name: string;
      email: string;
      sport_type: string;
      profile_image?: string;
    };
  };
  error?: string;
}

export interface ApiError {
  message: string;
  status: number;
  errors?: Record<string, string[]>;
}

export const loginPlayer = async (loginData: LoginRequest): Promise<AuthResponse> => {
  try {
    const payload = {
      ...loginData,
      ...(loginData.email ? { email: loginData.email } : {}),
      ...(loginData.phone_number ? { phone_number: loginData.phone_number } : {}),
      login_type: 'manual'
    };

    const response = await api.post('/playerLogin', payload);

    if (!response.data) {
      throw {
        message: 'No response data received from server',
        status: 500,
      } as ApiError;
    }

    // Accept any status if message says login successful and token exists
    if (
      typeof response.data.message === "string" &&
      response.data.message.toLowerCase().includes("login successful") &&
      response.data.data?.token
    ) {
      localStorage.setItem('authToken', response.data.data.token);
      localStorage.setItem('userData', JSON.stringify(response.data.data.user));
      // Always return success: true, regardless of status code
      return {
        success: true,
        message: response.data.message || 'Login successful',
        status: response.data.status,
        data: response.data.data
      };
    }

    // Otherwise, treat as error
    throw {
      message: response.data.message || 'Login failed: Invalid credentials',
      status: response.data.status || 401,
      errors: response.data.errors,
    } as ApiError;
  } catch (error: any) {
    console.error('Login error:', error);

    if (error.response?.data) {
      // Handle backend validation errors
      if (error.response.status === 400 && error.response.data.errors) {
        const errorMessages = Object.entries(error.response.data.errors)
          .map(([field, messages]) => `${field}: ${(messages as string[]).join(', ')}`)
          .join('; ');

        throw {
          message: errorMessages || 'Validation failed',
          status: error.response.status,
          errors: error.response.data.errors,
        } as ApiError;
      }

      throw {
        message: error.response.data.message ||
          (error.response.status === 401 ? 'Invalid credentials' :
            error.response.status === 404 ? 'Account not found' : 'Login failed'),
        status: error.response.status,
        errors: error.response.data.errors,
      } as ApiError;
    }

    if (error.request) {
      throw {
        message: 'No response received from server. Please check your connection.',
        status: 0,
      } as ApiError;
    }

    throw {
      message: error.message || 'An unexpected error occurred',
      status: error.status || 500,
    } as ApiError;
  }
};

// Update the registerPlayer function in authService.ts
export const registerPlayer = async (registerData: RegisterRequest): Promise<AuthResponse> => {
  try {
    const formData = new FormData();

    // Required fields - add null checks
    formData.append('name', registerData.name || '');
    formData.append('email', registerData.email || '');
    formData.append('password', registerData.password || '');
    formData.append('sport_type', registerData.sport_type || 'cricket');
    formData.append('login_type', registerData.login_type || 'manual');
    formData.append('phone_number', registerData.phone_number || '');
    formData.append('address', registerData.address || '');
    formData.append('gender', registerData.gender || '');
    formData.append('nationality_id', String(registerData.nationality_id || ''));
    formData.append('date_of_birth', registerData.date_of_birth || '');
    formData.append('role_id', String(registerData.role_id || ''));
    formData.append('batting_style', registerData.batting_style || '');
    formData.append('bowling_style', registerData.bowling_style || '');
    formData.append('dominant_hand', registerData.dominant_hand || '');

    // Optional profile image
    if (registerData.profile_image) {
      formData.append('profile_image', registerData.profile_image);
    }

    const response = await api.post('/playerRegister', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });

    // FIX: Accept status 200 and success message as success
    if (
      response.data?.success === true ||
      (typeof response.data?.message === "string" &&
        response.data.message.toLowerCase().includes("registered successfully"))
    ) {
      return {
        success: true,
        message: response.data.message || 'Registration successful',
        status: response.data.status,
        data: response.data.data
      };
    }

    // If not successful, throw error as before
    throw {
      message: response.data.message || 'Registration failed',
      status: response.data.status || 400,
      errors: response.data.errors,
    } as ApiError;
  } catch (error: any) {
    console.error('Registration error:', error);

    // Improved error handling
    if (error.response) {
      const { status, data } = error.response;
      throw {
        message: data?.message ||
          (status === 400 ? 'Invalid request data' :
            status === 409 ? 'Email already exists' :
            status === 422 ? 'Validation failed' : 'Registration failed'),
        status: status,
        errors: data?.errors,
      } as ApiError;
    } else if (error.request) {
      throw {
        message: 'No response from server. Check your connection.',
        status: 0,
      } as ApiError;
    } else {
      throw {
        message: error.message || 'Registration failed',
        status: error.status || 500,
      } as ApiError;
    }
  }
};