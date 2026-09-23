import React, { useEffect, useState } from "react";
import { Alert, Pressable, SafeAreaView, ScrollView, StyleSheet, Text, TextInput, View } from "react-native";
import { NativeStackScreenProps } from "@react-navigation/native-stack";
import { RootStackParamList } from "../../App";
import { discoverHospitals, discoverProviders, ProviderCard, HospitalCard } from "../api/client";
import { colors, radius, spacing } from "../theme";

type Props = NativeStackScreenProps<RootStackParamList, "CareDirectory">;

export default function CareDirectoryScreen({ navigation }: Props) {
  const [providers, setProviders] = useState<ProviderCard[]>([]);
  const [hospitals, setHospitals] = useState<HospitalCard[]>([]);
  const [search, setSearch] = useState("");
  const [busy, setBusy] = useState(true);

  async function load() {
    setBusy(true);
    try {
      const [p, h] = await Promise.all([discoverProviders(search || undefined), discoverHospitals(search || undefined)]);
      setProviders(p); setHospitals(h);
    } catch (e) { Alert.alert("CareLink", e instanceof Error ? e.message : "Unable to load care options."); }
    finally { setBusy(false); }
  }

  useEffect(() => { load(); }, []);

  return <SafeAreaView style={styles.safe}><ScrollView contentContainerStyle={styles.content}>
    <Pressable onPress={() => navigation.goBack()}><Text style={styles.back}>‹ Back</Text></Pressable>
    <Text style={styles.brand}>CareLink <Text style={styles.ai}>AI</Text></Text>
    <Text style={styles.title}>Find care</Text>
    <Text style={styles.subtitle}>Discover available healthcare professionals and hospitals.</Text>
    <TextInput style={styles.input} placeholder="Search by city" value={search} onChangeText={setSearch} onSubmitEditing={load} />
    <Pressable style={styles.search} onPress={load}><Text style={styles.searchText}>{busy ? "Searching..." : "Search"}</Text></Pressable>

    <Text style={styles.section}>Healthcare professionals</Text>
    {providers.map(p => <View key={p.id} style={styles.card}>
      <Text style={styles.name}>{p.full_name}</Text><Text style={styles.meta}>{p.provider_type} · {p.specialty || "General care"}</Text>
      <Text style={styles.meta}>{p.facility_name || "Independent provider"} · {p.city || "Location not set"}</Text>
      <Text style={styles.status}>{p.verification_status === "verified" ? "Verified provider" : "Verification pending"}</Text>
      <View style={styles.row}>
        <Pressable style={styles.primarySmall} onPress={() => navigation.navigate("Booking", { providerId: p.id, providerName: p.full_name })}><Text style={styles.primaryText}>Request appointment</Text></Pressable>
        <Pressable style={styles.secondarySmall} onPress={() => navigation.navigate("Messages", { providerId: p.id, providerName: p.full_name })}><Text style={styles.secondaryText}>Message</Text></Pressable>
      </View>
    </View>)}
    {!providers.length && !busy && <Text style={styles.empty}>No providers found yet.</Text>}

    <Text style={styles.section}>Hospitals & clinics</Text>
    {hospitals.map(h => <View key={h.id} style={styles.card}><Text style={styles.name}>{h.name}</Text><Text style={styles.meta}>{h.address}, {h.city}</Text><Text style={styles.meta}>{h.services || "Healthcare services"}</Text></View>)}
    {!hospitals.length && !busy && <Text style={styles.empty}>No hospitals found for this search.</Text>}
  </ScrollView></SafeAreaView>;
}
const styles=StyleSheet.create({
safe:{flex:1,backgroundColor:colors.background},content:{padding:spacing.lg},back:{color:colors.primaryDark,fontWeight:"800",marginBottom:spacing.lg},brand:{fontSize:21,fontWeight:"800",color:colors.text},ai:{color:colors.primary},title:{fontSize:30,fontWeight:"800",color:colors.text,marginTop:spacing.lg},subtitle:{color:colors.muted,lineHeight:22,marginTop:spacing.sm},input:{backgroundColor:colors.surface,borderWidth:1,borderColor:colors.border,borderRadius:radius.md,padding:15,marginTop:spacing.lg},search:{backgroundColor:colors.primary,borderRadius:radius.pill,paddingVertical:14,alignItems:"center",marginTop:spacing.sm},searchText:{color:"#fff",fontWeight:"800"},section:{fontSize:20,fontWeight:"800",color:colors.text,marginTop:spacing.xl,marginBottom:spacing.md},card:{backgroundColor:colors.surface,borderWidth:1,borderColor:colors.border,borderRadius:radius.lg,padding:spacing.md,marginBottom:spacing.sm},name:{fontSize:18,fontWeight:"800",color:colors.text},meta:{color:colors.muted,marginTop:5},status:{color:colors.primaryDark,fontWeight:"700",marginTop:8},row:{flexDirection:"row",gap:spacing.sm,marginTop:spacing.md},primarySmall:{flex:1,backgroundColor:colors.primary,borderRadius:radius.pill,paddingVertical:12,alignItems:"center"},primaryText:{color:"#fff",fontWeight:"800",fontSize:12},secondarySmall:{paddingHorizontal:14,justifyContent:"center",borderWidth:1,borderColor:colors.border,borderRadius:radius.pill},secondaryText:{color:colors.primaryDark,fontWeight:"800",fontSize:12},empty:{color:colors.muted}
});