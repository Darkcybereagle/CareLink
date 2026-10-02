export type CareLinkAppRole = "patient" | "provider";

const rawRole = (process.env.EXPO_PUBLIC_APP_ROLE || "patient").toLowerCase();
export const APP_ROLE: CareLinkAppRole = rawRole === "provider" ? "provider" : "patient";
export const IS_PROVIDER_APP = APP_ROLE === "provider";
export const IS_PATIENT_APP = APP_ROLE === "patient";
