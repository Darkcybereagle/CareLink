import React, { createContext, useContext, useEffect, useState } from "react";
import {
  clearToken,
  createPatientProfile,
  getMe,
  getPatientProfile,
  login,
  register,
  saveToken,
  User,
  PatientProfile,
} from "../api/client";

type AuthContextValue = {
  user: User | null;
  profile: PatientProfile | null;
  loading: boolean;
  signIn: (email: string, password: string) => Promise<"home" | "onboarding">;
  signUp: (name: string, email: string, password: string) => Promise<void>;
  finishOnboarding: (payload: Parameters<typeof createPatientProfile>[0]) => Promise<void>;
  signOut: () => Promise<void>;
  refreshProfile: () => Promise<void>;
};

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [profile, setProfile] = useState<PatientProfile | null>(null);
  const [loading, setLoading] = useState(true);

  async function loadSession() {
    try {
      const me = await getMe();
      setUser(me);
      try {
        setProfile(await getPatientProfile());
      } catch {
        setProfile(null);
      }
    } catch {
      setUser(null);
      setProfile(null);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadSession();
  }, []);

  async function signIn(email: string, password: string) {
    const result = await login(email, password);
    await saveToken(result.access_token);
    const me = await getMe();
    setUser(me);
    try {
      const patientProfile = await getPatientProfile();
      setProfile(patientProfile);
      return "home";
    } catch {
      setProfile(null);
      return "onboarding";
    }
  }

  async function signUp(name: string, email: string, password: string) {
    const result = await register(name, email, password);
    await saveToken(result.access_token);
    setUser(await getMe());
    setProfile(null);
  }

  async function finishOnboarding(payload: Parameters<typeof createPatientProfile>[0]) {
    const created = await createPatientProfile(payload);
    setProfile(created);
  }

  async function signOut() {
    await clearToken();
    setUser(null);
    setProfile(null);
  }

  async function refreshProfile() {
    try {
      setProfile(await getPatientProfile());
    } catch {
      setProfile(null);
    }
  }

  return (
    <AuthContext.Provider value={{ user, profile, loading, signIn, signUp, finishOnboarding, signOut, refreshProfile }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const value = useContext(AuthContext);
  if (!value) throw new Error("useAuth must be used inside AuthProvider");
  return value;
}
