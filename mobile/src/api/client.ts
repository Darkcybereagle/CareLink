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

export async function register(full_name: string, email: string, password: string, role: "patient" | "doctor" | "nurse" = "patient") {
  return request<{ access_token: string; token_type: string }>("/api/v1/auth/register", {
    method: "POST",
    body: JSON.stringify({ full_name, email, password, role }),
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

export type ProviderCard = { id: number; full_name: string; provider_type: string; specialty: string | null; facility_name: string | null; city: string | null; verification_status: string; is_available: boolean; };
export type HospitalCard = { id: number; name: string; address: string; city: string; phone: string | null; services: string | null; };
export type Appointment = { id: number; patient_id: number; provider_id: number; scheduled_at: string; reason: string; status: string; notes: string | null; };
export type HomeVisit = { id: number; patient_id: number; provider_id: number | null; address: string; requested_at: string; reason: string; status: string; };
export type NotificationItem = { id: number; title: string; body: string; is_read: boolean; created_at: string; };
export type FollowUp = { id: number; patient_id: number; provider_id: number; scheduled_at: string; note: string; completed: boolean; };
export type ProviderProfile = { id: number; user_id: number; provider_type: string; specialty: string | null; license_number: string | null; phone: string | null; facility_name: string | null; city: string | null; bio: string | null; verification_status: string; is_available: boolean; };
export type ProviderAvailability = { id: number; provider_id: number; day_of_week: number; start_time: string; end_time: string; };
export type PatientSummary = { intake_id: number; patient_id: number; patient_name: string; symptoms: string; duration: string | null; urgency: string; summary: string; clinician_handoff: string; created_at: string; };
export type MessageItem = { id: number; thread_id: number; sender_id: number; body: string; created_at: string; };

export async function discoverProviders(city?: string, specialty?: string) {
  const params = new URLSearchParams();
  if (city) params.set("city", city);
  if (specialty) params.set("specialty", specialty);
  const query = params.toString();
  return request<ProviderCard[]>(query ? "/api/v1/care/providers?" + query : "/api/v1/care/providers");
}
export async function discoverHospitals(city?: string) { return request<HospitalCard[]>(city ? "/api/v1/care/hospitals?city=" + encodeURIComponent(city) : "/api/v1/care/hospitals"); }
export async function requestAppointment(provider_id: number, scheduled_at: string, reason: string) { return request<Appointment>("/api/v1/care/appointments", { method: "POST", body: JSON.stringify({ provider_id, scheduled_at, reason }) }); }
export async function getPatientAppointments() { return request<Appointment[]>("/api/v1/care/appointments"); }
export async function requestHomeVisit(address: string, reason: string, provider_id?: number) { return request<HomeVisit>("/api/v1/care/home-visits", { method: "POST", body: JSON.stringify({ address, reason, provider_id: provider_id ?? null }) }); }
export async function getPatientHomeVisits() { return request<HomeVisit[]>("/api/v1/care/home-visits"); }
export async function createThread(provider_id: number) { return request<{ id: number; patient_id: number; provider_id: number; created_at: string }>("/api/v1/care/threads", { method: "POST", body: JSON.stringify({ provider_id }) }); }
export async function getMessages(id: number) { return request<MessageItem[]>("/api/v1/care/threads/" + id + "/messages"); }
export async function sendMessage(id: number, body: string) { return request<MessageItem>("/api/v1/care/threads/" + id + "/messages", { method: "POST", body: JSON.stringify({ body }) }); }
export async function getNotifications() { return request<NotificationItem[]>("/api/v1/care/notifications"); }
export async function markNotificationRead(id: number) { return request<NotificationItem>("/api/v1/care/notifications/" + id + "/read", { method: "PATCH" }); }
export async function createFollowUp(provider_id: number, scheduled_at: string, note: string) { return request<FollowUp>("/api/v1/care/follow-ups", { method: "POST", body: JSON.stringify({ provider_id, scheduled_at, note }) }); }
export async function getPatientFollowUps() { return request<FollowUp[]>("/api/v1/care/follow-ups"); }

export async function createProviderProfile(payload: { provider_type: string; specialty?: string; license_number?: string; phone?: string; facility_name?: string; city?: string; bio?: string }) { return request<ProviderProfile>("/api/v1/providers/me/profile", { method: "POST", body: JSON.stringify(payload) }); }
export async function getProviderProfile() { return request<ProviderProfile>("/api/v1/providers/me"); }
export async function addProviderAvailability(payload: { day_of_week: number; start_time: string; end_time: string }) { return request<ProviderAvailability>("/api/v1/providers/me/availability", { method: "POST", body: JSON.stringify(payload) }); }
export async function getProviderAvailability() { return request<ProviderAvailability[]>("/api/v1/providers/me/availability"); }
export async function getProviderAppointments() { return request<Appointment[]>("/api/v1/providers/appointments"); }
export async function updateProviderAppointment(id: number, status: string) { return request<Appointment>("/api/v1/providers/appointments/" + id + "/status", { method: "PATCH", body: JSON.stringify({ status }) }); }
export async function getProviderHomeVisits() { return request<HomeVisit[]>("/api/v1/providers/home-visits"); }
export async function updateProviderHomeVisit(id: number, status: string) { return request<HomeVisit>("/api/v1/providers/home-visits/" + id + "/status", { method: "PATCH", body: JSON.stringify({ status }) }); }
export async function getProviderAISummaries() { return request<PatientSummary[]>("/api/v1/providers/ai-summaries"); }
export async function getProviderNotifications() { return request<NotificationItem[]>("/api/v1/providers/notifications"); }
export async function getProviderFollowUps() { return request<FollowUp[]>("/api/v1/providers/follow-ups"); }
export async function completeProviderFollowUp(id: number) { return request<FollowUp>("/api/v1/providers/follow-ups/" + id + "/complete", { method: "PATCH" }); }
export async function getProviderMessages(id: number) { return request<MessageItem[]>("/api/v1/providers/threads/" + id + "/messages"); }
export async function sendProviderMessage(id: number, body: string) { return request<MessageItem>("/api/v1/providers/threads/" + id + "/messages", { method: "POST", body: JSON.stringify({ body }) }); }

export type ProviderThread = { id: number; patient_id: number; provider_id: number; created_at: string; };
export async function getProviderThreads() { return request<ProviderThread[]>("/api/v1/providers/threads"); }
