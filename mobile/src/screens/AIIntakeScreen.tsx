import React, { useState } from "react";
import { Alert, Pressable, SafeAreaView, ScrollView, StyleSheet, Text, TextInput, View } from "react-native";
import { NativeStackScreenProps } from "@react-navigation/native-stack";
import { RootStackParamList } from "../../App";
import { submitAIIntake, AIIntakeResponse } from "../api/client";
import { colors, radius, spacing } from "../theme";

type Props = NativeStackScreenProps<RootStackParamList, "AIIntake">;

export default function AIIntakeScreen({ navigation }: Props) {
  const [symptoms, setSymptoms] = useState("");
  const [duration, setDuration] = useState("");
  const [busy, setBusy] = useState(false);
  const [result, setResult] = useState<AIIntakeResponse | null>(null);

  async function submit() {
    if (symptoms.trim().length < 3) return Alert.alert("CareLink AI", "Tell me briefly what you are experiencing.");
    setBusy(true);
    try {
      setResult(await submitAIIntake(symptoms.trim(), duration.trim()));
    } catch (error) {
      Alert.alert("CareLink AI", error instanceof Error ? error.message : "Unable to process the intake.");
    } finally { setBusy(false); }
  }

  return (
    <SafeAreaView style={styles.safe}>
      <ScrollView contentContainerStyle={styles.content}>
        <Pressable onPress={() => navigation.goBack()}><Text style={styles.back}>‹ Back</Text></Pressable>
        <Text style={styles.brand}>CareLink <Text style={styles.ai}>AI</Text></Text>
        <Text style={styles.title}>Tell me how you feel</Text>
        <Text style={styles.subtitle}>I can help organize what you tell me and identify when urgent professional care should take priority.</Text>

        <Text style={styles.label}>What are you experiencing?</Text>
        <TextInput style={[styles.input, styles.multiline]} multiline textAlignVertical="top" placeholder="For example: I have been having..." value={symptoms} onChangeText={setSymptoms} />
        <Text style={styles.label}>How long has this been happening?</Text>
        <TextInput style={styles.input} placeholder="For example: since yesterday" value={duration} onChangeText={setDuration} />

        <View style={styles.notice}>
          <Text style={styles.noticeTitle}>Important</Text>
          <Text style={styles.noticeText}>CareLink AI is for intake, guidance and routing. It does not replace a qualified healthcare professional.</Text>
        </View>

        <Pressable style={styles.primary} onPress={submit} disabled={busy}>
          <Text style={styles.primaryText}>{busy ? "Reviewing..." : "Continue"}</Text>
        </Pressable>

        {result && (
          <View style={[styles.result, result.urgency === "emergency" ? styles.danger : undefined]}>
            <Text style={styles.resultTitle}>{result.urgency === "emergency" ? "Urgent attention needed" : "Your CareLink pathway"}</Text>
            <Text style={styles.resultText}>{result.safety_message}</Text>
            <Text style={styles.label}>Summary</Text>
            <Text style={styles.resultText}>{result.summary}</Text>
            <Text style={styles.label}>Next step</Text>
            <Text style={styles.resultText}>{result.next_step}</Text>
            <Text style={styles.label}>Clinician handoff</Text>
            <Text style={styles.resultText}>{result.clinician_handoff}</Text>
          </View>
        )}
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safe: { flex: 1, backgroundColor: colors.background },
  content: { padding: spacing.lg },
  back: { color: colors.primaryDark, fontWeight: "800", marginBottom: spacing.lg },
  brand: { fontSize: 21, fontWeight: "800", color: colors.text },
  ai: { color: colors.primary },
  title: { fontSize: 30, fontWeight: "800", color: colors.text, marginTop: spacing.lg },
  subtitle: { color: colors.muted, lineHeight: 22, marginTop: spacing.sm, marginBottom: spacing.xl },
  label: { color: colors.text, fontWeight: "800", marginTop: spacing.md, marginBottom: spacing.xs },
  input: { backgroundColor: colors.surface, borderWidth: 1, borderColor: colors.border, borderRadius: radius.md, padding: 15, fontSize: 16 },
  multiline: { minHeight: 130 },
  notice: { backgroundColor: colors.blueSoft, borderRadius: radius.md, padding: spacing.md, marginTop: spacing.lg },
  noticeTitle: { color: colors.text, fontWeight: "800" },
  noticeText: { color: colors.muted, lineHeight: 20, marginTop: 4 },
  primary: { backgroundColor: colors.primary, borderRadius: radius.pill, paddingVertical: 16, alignItems: "center", marginTop: spacing.lg },
  primaryText: { color: "#fff", fontWeight: "800", fontSize: 16 },
  result: { backgroundColor: colors.surface, borderRadius: radius.lg, padding: spacing.lg, marginTop: spacing.xl, borderWidth: 1, borderColor: colors.border },
  danger: { backgroundColor: colors.dangerSoft, borderColor: "#F3B5B5" },
  resultTitle: { fontSize: 20, fontWeight: "800", color: colors.text },
  resultText: { color: colors.text, lineHeight: 22, marginTop: 4 },
});
