import React,{useEffect,useState}from"react";
import{Alert,Pressable,SafeAreaView,ScrollView,StyleSheet,Text,View}from"react-native";
import{NativeStackScreenProps}from"@react-navigation/native-stack";
import{RootStackParamList}from"../../App";
import{getPatientAppointments}from"../api/client";
import{colors,radius,spacing}from"../theme";
type Props=NativeStackScreenProps<RootStackParamList,"Appointments">;
export default function AppointmentsScreen({navigation}:Props){const[data,setData]=useState<any[]>([]);useEffect(()=>{getPatientAppointments().then(setData).catch(e=>Alert.alert("CareLink",e.message));},[]);return <SafeAreaView style={styles.safe}><ScrollView contentContainerStyle={styles.content}><Text style={styles.back}onPress={()=>navigation.goBack()}>‹ Back</Text><Text style={styles.title}>Appointments</Text>{data.map(x=><View style={styles.card}key={x.id}><Text style={styles.name}>{new Date(x.scheduled_at).toLocaleString()}</Text><Text style={styles.meta}>{x.reason}</Text><Text style={styles.status}>{x.status}</Text></View>)}{!data.length&&<Text style={styles.empty}>No appointments yet.</Text>}</ScrollView></SafeAreaView>}
const styles=StyleSheet.create({safe:{flex:1,backgroundColor:colors.background},content:{padding:spacing.lg},back:{color:colors.primaryDark,fontWeight:"800"},title:{fontSize:30,fontWeight:"800",color:colors.text,marginTop:spacing.xl,marginBottom:spacing.lg},card:{backgroundColor:colors.surface,borderWidth:1,borderColor:colors.border,borderRadius:radius.lg,padding:spacing.md,marginBottom:spacing.sm},name:{fontWeight:"800",fontSize:17,color:colors.text},meta:{color:colors.muted,marginTop:5},status:{color:colors.primaryDark,fontWeight:"800",marginTop:8},empty:{color:colors.muted}});
