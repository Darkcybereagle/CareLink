import React, { useState } from "react";
import { Alert, Pressable, SafeAreaView, ScrollView, StyleSheet, Text, TextInput } from "react-native";
import { NativeStackScreenProps } from "@react-navigation/native-stack";
import { RootStackParamList } from "../../App";
import { useAuth } from "../auth/AuthContext";
import { colors, radius, spacing } from "../theme";

type Props = NativeStackScreenProps<RootStackParamList, "Onboarding">;

export default function OnboardingScreen({ navigation }: Props) {
  const { finishOnboarding } = useAuth();
  const [phone, setPhone] = useState("");
  const [dob, setDob] = useState("");
  const [gender, setGender] = useState("");
  const [address, setAddress] = useState("");
  const [emergencyName, setEmergencyName] = useState("");
  const [emergencyPhone, setEmergencyPhone] = useState("");
  const [busy, setBusy] = useState(false);

  async function submit() {
    if (dob && !/^\d{4}-\d{2}-\d{2}$/.test(dob)) {
      return Alert.alert("Date of birth", "Use YYYY-MM-DD.");
    }
    setBusy(true);
    try {
      await finishOnboarding({
        phone: phone || undefined,
        date_of_birth: dob || undefined,
        gender: gender || undefined,
        address: address || undefined,
        emergency_contact_name: emergencyName || undefined,
        emergency_contact_phone: emergencyPhone || undefined,
      });
      navigation.reset({ index: 0, routes: [{ name: "Home" }] });
    } catch (error) {
      Alert.alert("Profile not saved", error instanceof Error ? error.message : "Please try again.");
    } finally { setBusy(false); }
  }

  return (
    <SafeAreaView style={styles.safe}>
      <ScrollView contentContainerStyle={styles.content}>
        <Text style={styles.brand}>CareLink <Text style={styles.ai}>AI</Text></Text>
        <Text style={styles.title}>Let's set up your care profile</Text>
        <Text style={styles.subtitle}>These details help CareLink coordinate care. You can update them later.</Text>
        <TextInput style={styles.input} placeholder="Phone number" keyboardType="phone-pad" value={phone} onChangeText={setPhone} />
        <TextInput style={styles.input} placeholder="Date of birth (YYYY-MM-DD)" value={dob} onChangeText={setDob} />
        <TextInput style={styles.input} placeholder="Gender (optional)" value={gender} onChangeText={setGender} />
        <TextInput style={styles.input} placeholder="Address" value={address} onChangeText={setAddress} />
        <Text style={styles.section}>Emergency contact</Text>
        <TextInput style={styles.input} placeholder="Contact name" value={emergencyName} onChangeText={setEmergencyName} />
        <TextInput style={styles.input} placeholder="Contact phone" keyboardType="phone-pad" value={emergencyPhone} onChangeText={setEmergencyPhone} />
        <Pressable style={styles.primary} onPress={submit} disabled={busy}><Text style={styles.primaryText}>{busy ? "Saving..." : "Continue to CareLink"}</Text></Pressable>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safe: { flex: 1, backgroundColor: colors.background },
  content: { padding: spacing.lg },
  brand: { fontSize: 22, fontWeight: "800", color: colors.text, marginBottom: spacing.xl },
  ai: { color: colors.primary },
  title: { fontSize: 30, fontWeight: "800", color: colors.text },
  subtitle: { color: colors.muted, marginTop: spacing.sm, marginBottom: spacing.xl, lineHeight: 21 },
  input: { backgroundColor: colors.surface, borderWidth: 1, borderColor: colors.border, borderRadius: radius.md, padding: 15, marginBottom: spacing.md, fontSize: 16 },
  section: { color: colors.text, fontSize: 18, fontWeight: "800", marginVertical: spacing.sm },
  primary: { backgroundColor: colors.primary, borderRadius: radius.pill, paddingVertical: 16, alignItems: "center", marginTop: spacing.md },
  primaryText: { color: "#fff", fontWeight: "800", fontSize: 16 },
});
