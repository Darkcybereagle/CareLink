import React, { useState } from "react";
import { Alert, KeyboardAvoidingView, Platform, Pressable, SafeAreaView, StyleSheet, Text, TextInput, View } from "react-native";
import { NativeStackScreenProps } from "@react-navigation/native-stack";
import { RootStackParamList } from "../../App";
import { useAuth } from "../auth/AuthContext";
import { colors, radius, spacing } from "../theme";

type Props = NativeStackScreenProps<RootStackParamList, "Login">;

export default function LoginScreen({ navigation }: Props) {
  const { signIn } = useAuth();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [busy, setBusy] = useState(false);

  async function submit() {
    if (!email || !password) return Alert.alert("CareLink", "Enter your email and password.");
    setBusy(true);
    try {
      const destination = await signIn(email.trim(), password);
      navigation.reset({ index: 0, routes: [{ name: destination === "home" ? "Home" : "Onboarding" }] });
    } catch (error) {
      Alert.alert("Login failed", error instanceof Error ? error.message : "Please try again.");
    } finally { setBusy(false); }
  }

  return (
    <SafeAreaView style={styles.safe}>
      <KeyboardAvoidingView behavior={Platform.OS === "ios" ? "padding" : undefined} style={styles.wrap}>
        <Text style={styles.brand}>CareLink <Text style={styles.ai}>AI</Text></Text>
        <Text style={styles.title}>Welcome back</Text>
        <Text style={styles.subtitle}>Sign in to continue your care journey.</Text>
        <TextInput style={styles.input} placeholder="Email" autoCapitalize="none" keyboardType="email-address" value={email} onChangeText={setEmail} />
        <TextInput style={styles.input} placeholder="Password" secureTextEntry value={password} onChangeText={setPassword} />
        <Pressable style={styles.primary} onPress={submit} disabled={busy}><Text style={styles.primaryText}>{busy ? "Signing in..." : "Sign in"}</Text></Pressable>
        <Pressable onPress={() => navigation.navigate("Register")}><Text style={styles.link}>Create a CareLink account</Text></Pressable>
      </KeyboardAvoidingView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safe: { flex: 1, backgroundColor: colors.background, padding: spacing.lg },
  wrap: { flex: 1, justifyContent: "center" },
  brand: { fontSize: 22, fontWeight: "800", color: colors.text, marginBottom: spacing.xl },
  ai: { color: colors.primary },
  title: { fontSize: 30, fontWeight: "800", color: colors.text },
  subtitle: { color: colors.muted, marginTop: spacing.sm, marginBottom: spacing.xl },
  input: { backgroundColor: colors.surface, borderWidth: 1, borderColor: colors.border, borderRadius: radius.md, padding: 15, marginBottom: spacing.md, fontSize: 16 },
  primary: { backgroundColor: colors.primary, borderRadius: radius.pill, paddingVertical: 16, alignItems: "center", marginTop: spacing.sm },
  primaryText: { color: "#fff", fontWeight: "800", fontSize: 16 },
  link: { color: colors.primaryDark, textAlign: "center", marginTop: spacing.lg, fontWeight: "700" },
});
