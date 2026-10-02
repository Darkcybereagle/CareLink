import React, { useEffect, useState } from "react";
import { Alert, Pressable, SafeAreaView, ScrollView, StyleSheet, Text, TextInput, View } from "react-native";
import { NativeStackScreenProps } from "@react-navigation/native-stack";
import { RootStackParamList } from "../../App";
import { discoverHospitals, discoverProviders, ProviderCard, HospitalCard } from "../api/client";
import { colors, radius, spacing } from "../theme";

type Props = NativeStackScreenProps<RootStackParamList, "CareDirectory">;
type ProviderType = "doctor" | "nurse";

export default function CareDirectoryScreen({ navigation, route }: Props) {
  const initialType = route.params?.initialProviderType;
  const [providerType, setProviderType] = useState<ProviderType | undefined>(initialType);
  const [providers, setProviders] = useState<ProviderCard[]>([]);
  const [hospitals, setHospitals] = useState<HospitalCard[]>([]);
  const [search, setSearch] = useState("");
  const [busy, setBusy] = useState(true);

  async function load(type: ProviderType | undefined = providerType) {
    setBusy(true);
    try {
      const [p, h] = await Promise.all([
        discoverProviders(search || undefined, undefined, type),
        discoverHospitals(search || undefined),
      ]);
      setProviders(p);
      setHospitals(h);
    } catch (e) {
      Alert.alert("CareLink", e instanceof Error ? e.message : "Unable to load care options.");
    } finally {
      setBusy(false);
    }
  }

  function chooseType(type: ProviderType | undefined) {
    setProviderType(type);
    void load(type);
  }

  useEffect(() => { void load(initialType); }, []);

  return <SafeAreaView style={styles.safe}><ScrollView contentContainerStyle={styles.content}>
    <Pressable onPress={() => navigation.goBack()}><Text style={styles.back}>‹ Back</Text></Pressable>
    <Text style={styles.brand}>CareLink <Text style={styles.ai}>AI</Text></Text>
    <Text style={styles.title}>{providerType === "nurse" ? "Find a nurse" : providerType === "doctor" ? "Find a doctor" : "Find care"}</Text>
    <Text style={styles.subtitle}>Discover verified healthcare professionals and facilities. Nurse care and home-care support are first-class CareLink services.</Text>

    <View style={styles.filters}>
      <Pressable style={[styles.filter, !providerType && styles.filterActive]} onPress={() => chooseType(undefined)}><Text style={styles.filterText}>All</Text></Pressable>
      <Pressable style={[styles.filter, providerType === "nurse" && styles.filterActive]} onPress={() => chooseType("nurse")}><Text style={styles.filterText}>Nurses</Text></Pressable>
      <Pressable style={[styles.filter, providerType === "doctor" && styles.filterActive]} onPress={() => chooseType("doctor")}><Text style={styles.filterText}>Doctors</Text></Pressable>
    </View>

    <TextInput style={styles.input} placeholder="Search by city, e.g. Abuja" value={search} onChangeText={setSearch} onSubmitEditing={() => load()} />
    <Pressable style={styles.search} onPress={() => load()} disabled={busy}><Text style={styles.searchText}>{busy ? "Searching..." : "Search"}</Text></Pressable>

    <Text style={styles.section}>{providerType === "nurse" ? "Verified nurses" : providerType === "doctor" ? "Verified doctors" : "Healthcare professionals"}</Text>
    {providers.map(p => <View key={p.id} style={styles.card}>
      <Text style={styles.name}>{p.full_name}</Text>
      <Text style={styles.meta}>{p.provider_type} · {p.specialty || "General care"}</Text>
      <Text style={styles.meta}>{p.facility_name || "Independent provider"} · {p.city || "Location not set"}</Text>
      <Text style={styles.status}>✓ Verified provider</Text>
      {p.provider_type === "nurse" && p.offers_home_visits && <Text style={styles.homeCare}>Home-care visits available</Text>}
      <Text style={styles.meta}>★ {p.average_rating ?? "New"} · {p.review_count} reviews · {p.cases_completed} completed cases</Text>
      <View style={styles.row}>
        <Pressable style={styles.primarySmall} onPress={() => navigation.navigate("ProviderDetails", { provider: p })}><Text style={styles.primaryText}>View profile</Text></Pressable>
        <Pressable style={styles.secondarySmall} onPress={() => navigation.navigate("Messages", { providerId: p.id, providerName: p.full_name })}><Text style={styles.secondaryText}>Message</Text></Pressable>
      </View>
    </View>)}
    {!providers.length && !busy && <Text style={styles.empty}>No verified {providerType ? providerType + "s" : "providers"} are available for this search yet.</Text>}

    <Text style={styles.section}>Hospitals & clinics</Text>
    {hospitals.map(h => <View key={h.id} style={styles.card}><Text style={styles.name}>{h.name}</Text><Text style={styles.meta}>{h.address}, {h.city}</Text><Text style={styles.meta}>{h.services || "Healthcare services"}</Text></View>)}
    {!hospitals.length && !busy && <Text style={styles.empty}>No hospitals or clinics found for this search.</Text>}
  </ScrollView></SafeAreaView>;
}

const styles=StyleSheet.create({
safe:{flex:1,backgroundColor:colors.background},content:{padding:spacing.lg},back:{color:colors.primaryDark,fontWeight:"800",marginBottom:spacing.lg},brand:{fontSize:21,fontWeight:"800",color:colors.text},ai:{color:colors.primary},title:{fontSize:30,fontWeight:"800",color:colors.text,marginTop:spacing.lg},subtitle:{color:colors.muted,lineHeight:22,marginTop:spacing.sm},filters:{flexDirection:"row",gap:spacing.sm,marginTop:spacing.lg},filter:{flex:1,borderWidth:1,borderColor:colors.border,borderRadius:radius.pill,paddingVertical:10,alignItems:"center"},filterActive:{backgroundColor:colors.blueSoft,borderColor:colors.primary},filterText:{fontWeight:"800",color:colors.primaryDark},input:{backgroundColor:colors.surface,borderWidth:1,borderColor:colors.border,borderRadius:radius.md,padding:15,marginTop:spacing.lg},search:{backgroundColor:colors.primary,borderRadius:radius.pill,paddingVertical:14,alignItems:"center",marginTop:spacing.sm},searchText:{color:"#fff",fontWeight:"800"},section:{fontSize:20,fontWeight:"800",color:colors.text,marginTop:spacing.xl,marginBottom:spacing.md},card:{backgroundColor:colors.surface,borderWidth:1,borderColor:colors.border,borderRadius:radius.lg,padding:spacing.md,marginBottom:spacing.sm},name:{fontSize:18,fontWeight:"800",color:colors.text},meta:{color:colors.muted,marginTop:5},status:{color:colors.primaryDark,fontWeight:"700",marginTop:8},homeCare:{color:colors.primaryDark,fontWeight:"700",marginTop:5},row:{flexDirection:"row",gap:spacing.sm,marginTop:spacing.md},primarySmall:{flex:1,backgroundColor:colors.primary,borderRadius:radius.pill,paddingVertical:12,alignItems:"center"},primaryText:{color:"#fff",fontWeight:"800",fontSize:12},secondarySmall:{paddingHorizontal:14,justifyContent:"center",borderWidth:1,borderColor:colors.border,borderRadius:radius.pill},secondaryText:{color:colors.primaryDark,fontWeight:"800",fontSize:12},empty:{color:colors.muted}
});
