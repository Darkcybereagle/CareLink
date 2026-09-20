import React from "react";
import { SafeAreaView, StyleSheet, Text, View, Pressable } from "react-native";
import { NativeStackScreenProps } from "@react-navigation/native-stack";
import { RootStackParamList } from "../../App";
import { colors, radius, spacing } from "../theme";

type Props = NativeStackScreenProps<RootStackParamList, "Welcome">;

export default function WelcomeScreen({ navigation }: Props) {
  return (
    <SafeAreaView style={styles.safe}>
      <View style={styles.hero}>
        <View style={styles.logo}><Text style={styles.logoText}>C</Text></View>
        <Text style={styles.brand}>CareLink <Text style={styles.ai}>AI</Text></Text>
        <Text style={styles.title}>Healthcare that starts with listening.</Text>
        <Text style={styles.subtitle}>
          Tell CareLink how you feel, get guided to the right care, and stay connected to healthcare professionals.
        </Text>
        <View style={styles.card}>
          <Text style={styles.cardIcon}>♥</Text>
          <Text style={styles.cardTitle}>Your care. One simple link.</Text>
          <Text style={styles.cardText}>AI-assisted intake, care guidance and secure connection to care.</Text>
        </View>
      </View>
      <View style={styles.actions}>
        <Pressable style={styles.primary} onPress={() => navigation.navigate("Register")}>
          <Text style={styles.primaryText}>Get started</Text>
        </Pressable>
        <Pressable style={styles.secondary} onPress={() => navigation.navigate("Login")}>
          <Text style={styles.secondaryText}>I already have an account</Text>
        </Pressable>
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safe: { flex: 1, backgroundColor: colors.background, padding: spacing.lg },
  hero: { flex: 1, justifyContent: "center" },
  logo: { width: 58, height: 58, borderRadius: radius.md, backgroundColor: colors.primary, alignItems: "center", justifyContent: "center", marginBottom: spacing.md },
  logoText: { color: "#fff", fontSize: 32, fontWeight: "800" },
  brand: { fontSize: 24, fontWeight: "800", color: colors.text },
  ai: { color: colors.primary },
  title: { fontSize: 34, lineHeight: 40, fontWeight: "800", color: colors.text, marginTop: spacing.xl },
  subtitle: { fontSize: 16, lineHeight: 24, color: colors.muted, marginTop: spacing.md },
  card: { marginTop: spacing.xl, backgroundColor: colors.surface, borderRadius: radius.lg, padding: spacing.lg, borderWidth: 1, borderColor: colors.border },
  cardIcon: { fontSize: 24, color: colors.primary },
  cardTitle: { marginTop: spacing.sm, fontSize: 18, fontWeight: "700", color: colors.text },
  cardText: { marginTop: spacing.xs, color: colors.muted, lineHeight: 21 },
  actions: { gap: spacing.sm },
  primary: { backgroundColor: colors.primary, borderRadius: radius.pill, paddingVertical: 16, alignItems: "center" },
  primaryText: { color: "#fff", fontSize: 16, fontWeight: "800" },
  secondary: { paddingVertical: 14, alignItems: "center" },
  secondaryText: { color: colors.primaryDark, fontWeight: "700" },
});
