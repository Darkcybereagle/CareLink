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
        <Pressable style={styles.action} onPress={() => navigation.navigate("CareDirectory")}>
          <Text style={styles.actionTitle}>Find a doctor or hospital</Text>
          <Text style={styles.actionText}>Discover care options near you.</Text>
        </Pressable>
        <View style={styles.grid}>
          <Pressable style={styles.option} onPress={() => navigation.navigate("HomeVisit")}>
            <Text style={styles.icon}>⌂</Text><Text style={styles.optionTitle}>Request home care</Text><Text style={styles.optionText}>Ask for professional care at home.</Text>
          </Pressable>
          <Pressable style={styles.option} onPress={() => navigation.navigate("Appointments")}>
            <Text style={styles.icon}>◷</Text><Text style={styles.optionTitle}>Appointments</Text><Text style={styles.optionText}>View your appointment requests.</Text>
          </Pressable>
          <Pressable style={styles.option} onPress={() => navigation.navigate("Activity")}>
            <Text style={styles.icon}>●</Text><Text style={styles.optionTitle}>Care activity</Text><Text style={styles.optionText}>Notifications, home visits and follow-ups.</Text>
          </Pressable>
        </View>


