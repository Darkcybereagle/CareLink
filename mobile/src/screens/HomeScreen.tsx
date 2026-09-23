import React from "react";
import { Pressable, SafeAreaView, ScrollView, StyleSheet, Text, View } from "react-native";
import { NativeStackScreenProps } from "@react-navigation/native-stack";
import { RootStackParamList } from "../../App";
import { useAuth } from "../auth/AuthContext";
import { colors, radius, spacing } from "../theme";

type Props = NativeStackScreenProps<RootStackParamList, "Home">;

export default function HomeScreen({ navigation }: Props) {
  const { user, profile, signOut } = useAuth();
  const firstName = user?.full_name.split(" ")[0] || "there";

  return (
    <SafeAreaView style={styles.safe}>
      <ScrollView contentContainerStyle={styles.content}>
        <View style={styles.header}>
          <View>
            <Text style={styles.brand}>CareLink <Text style={styles.ai}>AI</Text></Text>
            <Text style={styles.greeting}>Good morning, {firstName} 👋</Text>
          </View>
          <Pressable onPress={signOut}><Text style={styles.signOut}>Sign out</Text></Pressable>
        </View>

        <View style={styles.hero}>
          <Text style={styles.heroTitle}>How are you feeling today?</Text>
          <Text style={styles.heroText}>Talk to CareLink about what you're experiencing. We'll help organize the next step.</Text>
          <Pressable style={styles.primary} onPress={() => navigation.navigate("AIIntake")}>
            <Text style={styles.primaryText}>Talk to CareLink</Text>
          </Pressable>
        </View>

        <Text style={styles.sectionTitle}>Care options</Text>
        <View style={styles.grid}>
          <View style={styles.option}><Text style={styles.icon}>✚</Text><Text style={styles.optionTitle}>Find a doctor</Text><Text style={styles.optionText}>Provider discovery comes next.</Text></View>
          <View style={styles.option}><Text style={styles.icon}>⌂</Text><Text style={styles.optionTitle}>Home care</Text><Text style={styles.optionText}>Request support when available.</Text></View>
          <View style={styles.option}><Text style={styles.icon}>⌖</Text><Text style={styles.optionTitle}>Find a hospital</Text><Text style={styles.optionText}>Hospital discovery comes next.</Text></View>
          <View style={styles.option}><Text style={styles.icon}>◷</Text><Text style={styles.optionTitle}>Appointments</Text><Text style={styles.optionText}>Appointment flow comes next.</Text></View>
        </View>

        <Pressable style={styles.action} onPress={() => navigation.navigate("CareDirectory")}><Text style={styles.actionTitle}>Find a doctor or hospital</Text><Text style={styles.actionText}>Discover care options near you.</Text></Pressable><View style={styles.grid}><Pressable style={styles.option} onPress={() => navigation.navigate("HomeVisit")}><Text style={styles.icon}>⌂</Text><Text style={styles.optionTitle}>Request home care</Text><Text style={styles.optionText}>Ask for professional care at home.</Text></Pressable><Pressable style={styles.option} onPress={() => navigation.navigate("Appointments")}><Text style={styles.icon}>◷</Text><Text style={styles.optionTitle}>Appointments</Text><Text style={styles.optionText}>View your appointment requests.</Text></Pressable><Pressable style={styles.option} onPress={() => navigation.navigate("Activity")}><Text style={styles.icon}>●</Text><Text style={styles.optionTitle}>Care activity</Text><Text style={styles.optionText}>Notifications, home visits and follow-ups.</Text></Pressable></View><View style={styles.profileCard}>
          <Text style={styles.profileTitle}>Your profile</Text>
          <Text style={styles.profileText}>{profile?.phone || "Phone not added"} · {profile?.address || "Address not added"}</Text>
        </View>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safe: { flex: 1, backgroundColor: colors.background },
  content: { padding: spacing.lg },
  header: { flexDirection: "row", justifyContent: "space-between", alignItems: "flex-start", marginBottom: spacing.lg },
  brand: { fontSize: 21, fontWeight: "800", color: colors.text },
  ai: { color: colors.primary },
  greeting: { fontSize: 18, fontWeight: "700", color: colors.text, marginTop: spacing.sm },
  signOut: { color: colors.muted, fontWeight: "700", paddingTop: 5 },
  hero: { backgroundColor: colors.blueSoft, borderRadius: radius.lg, padding: spacing.lg, borderWidth: 1, borderColor: colors.border },
  heroTitle: { fontSize: 26, fontWeight: "800", color: colors.text },
  heroText: { color: colors.muted, lineHeight: 22, marginTop: spacing.sm },
  primary: { backgroundColor: colors.primary, borderRadius: radius.pill, paddingVertical: 15, alignItems: "center", marginTop: spacing.lg },
  primaryText: { color: "#fff", fontWeight: "800", fontSize: 16 },
  sectionTitle: { fontSize: 20, fontWeight: "800", color: colors.text, marginTop: spacing.xl, marginBottom: spacing.md },
  grid: { gap: spacing.sm },
  option: { backgroundColor: colors.surface, borderRadius: radius.md, padding: spacing.md, borderWidth: 1, borderColor: colors.border },
  icon: { fontSize: 23, color: colors.primary },
  optionTitle: { fontSize: 17, fontWeight: "800", color: colors.text, marginTop: spacing.xs },
  optionText: { color: colors.muted, marginTop: 4 },
  action: { backgroundColor: colors.surface, borderRadius: radius.lg, padding: spacing.md, borderWidth: 1, borderColor: colors.border, marginTop: spacing.md },
  actionTitle: { fontSize: 17, fontWeight: "800", color: colors.text },
  actionText: { color: colors.muted, marginTop: 4 },
  profileCard: { marginTop: spacing.xl, backgroundColor: colors.surface, padding: spacing.md, borderRadius: radius.md, borderWidth: 1, borderColor: colors.border },
  profileTitle: { fontWeight: "800", color: colors.text },
  profileText: { color: colors.muted, marginTop: 5 },
});
