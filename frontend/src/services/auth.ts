/** Authentication service for the Todo application. */

import { User } from '../types';
import { authAPI } from './api';

// Store the current user
let currentUser: User | null = null;

// Check if user is logged in
export const isAuthenticated = (): boolean => {
  return !!getToken();
};

// Get the current user
export const getCurrentUser = (): User | null => {
  return currentUser;
};

// Login function
export const login = async (email: string, password: string): Promise<{user: User, token: string}> => {
  try {
    const response = await authAPI.login(email, password);
    const { access_token } = response.data;

    // Store the token in localStorage
    setToken(access_token);

    // For now, return a mock user object
    // In a real app, you'd fetch user details using the token
    const user: User = {
      id: 'mock-user-id',
      email,
      name: 'Mock User', // In a real app, this would come from the API
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    };

    currentUser = user;

    return { user, token: access_token };
  } catch (error) {
    throw new Error('Login failed. Please check your credentials.');
  }
};

// Register function
export const register = async (email: string, name: string, password: string): Promise<{user: User, token: string}> => {
  try {
    const response = await authAPI.register({ email, name, password });
    const { access_token } = response.data; // Assuming the API returns a token upon registration

    // Store the token in localStorage
    setToken(access_token);

    // For now, return a mock user object
    // In a real app, you'd use the actual user data from the response
    const user: User = {
      id: 'mock-user-id',
      email,
      name,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    };

    currentUser = user;

    return { user, token: access_token };
  } catch (error) {
    throw new Error('Registration failed. Please try again.');
  }
};

// Logout function
export const logout = (): void => {
  removeToken();
  currentUser = null;
};

// Get token from localStorage
export const getToken = (): string | null => {
  return localStorage.getItem('access_token');
};

// Set token in localStorage
export const setToken = (token: string): void => {
  localStorage.setItem('access_token', token);
};

// Remove token from localStorage
export const removeToken = (): void => {
  localStorage.removeItem('access_token');
};

// Verify token validity (in a real app, this would make an API call)
export const verifyToken = async (): Promise<boolean> => {
  const token = getToken();
  if (!token) {
    return false;
  }

  try {
    // Decode the token to check expiration
    const payload = decodeTokenPayload(token);
    const currentTime = Math.floor(Date.now() / 1000);

    // Check if token is expired
    return payload.exp > currentTime;
  } catch (error) {
    console.error('Error verifying token:', error);
    return false;
  }
};

// Decode JWT payload without verification (for expiration check)
export const decodeTokenPayload = (token: string): { exp: number, sub: string, [key: string]: any } => {
  try {
    const parts = token.split('.');
    if (parts.length !== 3) {
      throw new Error('Invalid token format');
    }

    // Decode the payload part of the JWT (second part)
    const payload = JSON.parse(atob(parts[1]));
    return payload;
  } catch (error) {
    throw new Error(`Invalid token: ${error}`);
  }
};

// Check if token is about to expire (within 5 minutes)
export const isTokenExpiringSoon = (bufferMinutes: number = 5): boolean => {
  const token = getToken();
  if (!token) {
    return true; // If no token, treat as expired
  }

  try {
    const payload = decodeTokenPayload(token);
    const currentTime = Math.floor(Date.now() / 1000);
    const bufferSeconds = bufferMinutes * 60;

    // Check if token expires within the buffer time
    return payload.exp - currentTime < bufferSeconds;
  } catch (error) {
    return true; // If we can't decode the token, treat as expired
  }
};

// Refresh token (placeholder - would call refresh endpoint in real app)
export const refreshToken = async (): Promise<string | null> => {
  // In a real application, you would call a refresh token endpoint
  // For now, return null indicating refresh is not possible
  return null;
};