import * as SecureStore from "expo-secure-store";

const API_URL = (process.env.EXPO_PUBLIC_API_URL || "http://127.0.0.1:8000").replace(/\/$/, "");
const TOKEN_KEY = "carelink_access_token";

async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  const token = await SecureStore.getItemAsync(TOKEN_KEY);
  const headers = new Headers(options.headers);
  headers.set("Content-Type", "application/json");
  if (token) headers.set("Authorization", `Bearer ${token}`);

  const response = await fetch(`${API_URL}${path}`, { ...options, headers });
  const body = await response.json().catch(() => ({}));

  if (!response.ok) {
    throw new Error(body.detail || "CareLink request failed");
  }
  return body as T;
}

export type User = {
  id: number;
  full_name: string;
  email: string;
  role: string;
  is_active: boolean;
};

export type PatientProfile = {
  id: number;
  user_id: number;
  phone: string | null;
  date_of_birth: string | null;
  gender: string | null;
  address: string | null;
  emergency_contact_name: string | null;
  emergency_contact_phone: string | null;
};

export async function saveToken(token: string) {
  await SecureStore.setItemAsync(TOKEN_KEY, token);
}

export async function clearToken() {
  await SecureStore.deleteItemAsync(TOKEN_KEY);
}

export async function getMe() {
  return request<User>("/api/v1/users/me");
}

export async function getPatientProfile() {
  return request<PatientProfile>("/api/v1/users/me/patient-profile");
}

export async function register(full_name: string, email: string, password: string) {
  return request<{ access_token: string; token_type: string }>("/api/v1/auth/register", {
    method: "POST",
    body: JSON.stringify({ full_name, email, password }),
  });
}

export async function login(email: string, password: string) {
  return request<{ access_token: string; token_type: string }>("/api/v1/auth/login", {
    method: "POST",
    body: JSON.stringify({ email, password }),
  });
}

export async function createPatientProfile(payload: {
  phone?: string;
  date_of_birth?: string;
  gender?: string;
  address?: string;
  emergency_contact_name?: string;
  emergency_contact_phone?: string;
}) {
  return request<PatientProfile>("/api/v1/users/me/patient-profile", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export type AIIntakeResponse = {
  urgency: "emergency" | "urgent" | "routine";
  safety_message: string;
  summary: string;
  next_step: string;
  clinician_handoff: string;
};

export async function submitAIIntake(symptoms: string, duration?: string) {
  return request<AIIntakeResponse>("/api/v1/ai/intake", {
    method: "POST",
    body: JSON.stringify({ symptoms, duration: duration || null }),
  });
}
