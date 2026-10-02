import React, { createContext, useContext, useEffect, useState } from "react";
import {
  clearToken, createPatientProfile, getMe, getPatientProfile, getProviderProfile,
  login, register, saveToken, User, PatientProfile, ProviderProfile,
} from "../api/client";
import { APP_ROLE } from "../config";

type Destination = "home" | "onboarding" | "provider" | "providerSetup";
type AuthContextValue = {
  user: User | null; profile: PatientProfile | null; providerProfile: ProviderProfile | null; loading: boolean;
  signIn: (email: string, password: string) => Promise<Destination>;
  signUp: (name: string, email: string, password: string, role?: "patient" | "doctor" | "nurse") => Promise<Destination>;
  finishOnboarding: (payload: Parameters<typeof createPatientProfile>[0]) => Promise<void>;
  signOut: () => Promise<void>; refreshProfile: () => Promise<void>;
};
const AuthContext = createContext<AuthContextValue | undefined>(undefined);

function roleAllowed(role: string) {
  return APP_ROLE === "patient" ? role === "patient" : role === "doctor" || role === "nurse";
}
function wrongAppMessage() {
  return APP_ROLE === "patient" ? "This account belongs in the CareLink Provider app." : "This account belongs in the CareLink Patient app.";
}

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [profile, setProfile] = useState<PatientProfile | null>(null);
  const [providerProfile, setProviderProfile] = useState<ProviderProfile | null>(null);
  const [loading, setLoading] = useState(true);

  async function loadSession() {
    try {
      const me = await getMe();
      if (!roleAllowed(me.role)) { await clearToken(); setUser(null); setProfile(null); setProviderProfile(null); return; }
      setUser(me);
      if (me.role === "patient") { try { setProfile(await getPatientProfile()); } catch { setProfile(null); } }
      else { try { setProviderProfile(await getProviderProfile()); } catch { setProviderProfile(null); } }
    } catch { setUser(null); setProfile(null); setProviderProfile(null); }
    finally { setLoading(false); }
  }
  useEffect(() => { loadSession(); }, []);

  async function signIn(email: string, password: string): Promise<Destination> {
    const result = await login(email, password); await saveToken(result.access_token);
    const me = await getMe();
    if (!roleAllowed(me.role)) { await clearToken(); throw new Error(wrongAppMessage()); }
    setUser(me);
    if (me.role === "patient") {
      try { setProfile(await getPatientProfile()); return "home"; } catch { setProfile(null); return "onboarding"; }
    }
    try { setProviderProfile(await getProviderProfile()); return "provider"; } catch { setProviderProfile(null); return "providerSetup"; }
  }

  async function signUp(name: string, email: string, password: string, role = "patient" as "patient" | "doctor" | "nurse") {
    if (!roleAllowed(role)) throw new Error(wrongAppMessage());
    const result = await register(name, email, password, role); await saveToken(result.access_token);
    const me = await getMe(); setUser(me);
    if (role === "patient") { setProfile(null); return "onboarding"; }
    setProviderProfile(null); return "providerSetup";
  }

  async function finishOnboarding(payload: Parameters<typeof createPatientProfile>[0]) { setProfile(await createPatientProfile(payload)); }
  async function signOut() { await clearToken(); setUser(null); setProfile(null); setProviderProfile(null); }
  async function refreshProfile() {
    if (user?.role === "patient") { try { setProfile(await getPatientProfile()); } catch { setProfile(null); } }
    else if (user?.role === "doctor" || user?.role === "nurse") { try { setProviderProfile(await getProviderProfile()); } catch { setProviderProfile(null); } }
  }
  return <AuthContext.Provider value={{ user, profile, providerProfile, loading, signIn, signUp, finishOnboarding, signOut, refreshProfile }}>{children}</AuthContext.Provider>;
}
export function useAuth() { const value = useContext(AuthContext); if (!value) throw new Error("useAuth must be used inside AuthProvider"); return value; }
