import React, { useState } from "react";
import { Alert, KeyboardAvoidingView, Platform, Pressable, SafeAreaView, StyleSheet, Text, TextInput } from "react-native";
import { NativeStackScreenProps } from "@react-navigation/native-stack";
import { RootStackParamList } from "../../App";
import { useAuth } from "../auth/AuthContext";
import { colors, radius, spacing } from "../theme";

type Props = NativeStackScreenProps<RootStackParamList, "Register">;

export default function RegisterScreen({ navigation }: Props) {
  const { signUp } = useAuth();
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [busy, setBusy] = useState(false);

  async function submit() {
    if (!name || !email || password.length < 8) return Alert.alert("CareLink", "Enter your name, email and a password of at least 8 characters.");
    setBusy(true);
    try {
      await signUp(name.trim(), email.trim(), password);
      navigation.reset({ index: 0, routes: [{ name: "Onboarding" }] });
    } catch (error) {
      Alert.alert("Registration failed", error instanceof Error ? error.message : "Please try again.");
    } finally { setBusy(false); }
  }

  return (
    <SafeAreaView style={styles.safe}>
      <KeyboardAvoidingView behavior={Platform.OS === "ios" ? "padding" : undefined} style={styles.wrap}>
        <Text style={styles.brand}>CareLink <Text style={styles.ai}>AI</Text></Text>
        <Text style={styles.title}>Create your account</Text>
        <Text style={styles.subtitle}>A few details first. You can complete your patient profile next.</Text>
        <TextInput style={styles.input} placeholder="Full name" value={name} onChangeText={setName} />
        <TextInput style={styles.input} placeholder="Email" autoCapitalize="none" keyboardType="email-address" value={email} onChangeText={setEmail} />
        <TextInput style={styles.input} placeholder="Password (8+ characters)" secureTextEntry value={password} onChangeText={setPassword} />
        <Pressable style={styles.primary} onPress={submit} disabled={busy}><Text style={styles.primaryText}>{busy ? "Creating..." : "Create account"}</Text></Pressable>
        <Pressable onPress={() => navigation.navigate("Login")}><Text style={styles.link}>I already have an account</Text></Pressable>
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
  subtitle: { color: colors.muted, marginTop: spacing.sm, marginBottom: spacing.xl, lineHeight: 21 },
  input: { backgroundColor: colors.surface, borderWidth: 1, borderColor: colors.border, borderRadius: radius.md, padding: 15, marginBottom: spacing.md, fontSize: 16 },
  primary: { backgroundColor: colors.primary, borderRadius: radius.pill, paddingVertical: 16, alignItems: "center", marginTop: spacing.sm },
  primaryText: { color: "#fff", fontWeight: "800", fontSize: 16 },
  link: { color: colors.primaryDark, textAlign: "center", marginTop: spacing.lg, fontWeight: "700" },
});
