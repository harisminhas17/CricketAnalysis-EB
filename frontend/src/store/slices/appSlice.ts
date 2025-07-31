import { createSlice, PayloadAction } from '@reduxjs/toolkit';

type AppState = 
  | "splash" 
  | "loading" 
  | "login" 
  | "signup" 
  | "forgot-password" 
  | "otp-verification" 
  | "reset-password" 
  | "onboarding" 
  | "home";

interface AppSliceState {
  currentState: AppState;
  isFirstLaunch: boolean;
}

const initialState: AppSliceState = {
  currentState: "splash",
  isFirstLaunch: true,
};

const appSlice = createSlice({
  name: 'app',
  initialState,
  reducers: {
    setCurrentState: (state, action: PayloadAction<AppState>) => {
      state.currentState = action.payload;
    },
    setFirstLaunch: (state, action: PayloadAction<boolean>) => {
      state.isFirstLaunch = action.payload;
    },
  },
});

export const { setCurrentState, setFirstLaunch } = appSlice.actions;
export default appSlice.reducer;