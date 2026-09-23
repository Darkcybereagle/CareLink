import React from "react";
import { ActivityIndicator, View } from "react-native";
import { NavigationContainer, DefaultTheme } from "@react-navigation/native";
import { createNativeStackNavigator } from "@react-navigation/native-stack";
import { StatusBar } from "expo-status-bar";
import { AuthProvider, useAuth } from "./src/auth/AuthContext";
import { colors } from "./src/theme";
import WelcomeScreen from "./src/screens/WelcomeScreen";
import LoginScreen from "./src/screens/LoginScreen";
import RegisterScreen from "./src/screens/RegisterScreen";
import OnboardingScreen from "./src/screens/OnboardingScreen";
import HomeScreen from "./src/screens/HomeScreen";
import AIIntakeScreen from "./src/screens/AIIntakeScreen";
import CareDirectoryScreen from "./src/screens/CareDirectoryScreen";
import BookingScreen from "./src/screens/BookingScreen";
import HomeVisitScreen from "./src/screens/HomeVisitScreen";
import AppointmentsScreen from "./src/screens/AppointmentsScreen";
import ActivityScreen from "./src/screens/ActivityScreen";
import MessagesScreen from "./src/screens/MessagesScreen";
import ProviderSetupScreen from "./src/screens/ProviderSetupScreen";
import ProviderHomeScreen from "./src/screens/ProviderHomeScreen";
import ProviderAppointmentsScreen from "./src/screens/ProviderAppointmentsScreen";
import ProviderHomeVisitsScreen from "./src/screens/ProviderHomeVisitsScreen";
import ProviderSummariesScreen from "./src/screens/ProviderSummariesScreen";
import ProviderProfileScreen from "./src/screens/ProviderProfileScreen";
import ProviderMessagesScreen from "./src/screens/ProviderMessagesScreen";

export type RootStackParamList = {
  Welcome: undefined;
  Login: undefined;
  Register: undefined;
  Onboarding: undefined;
  Home: undefined;
  AIIntake: undefined;
  CareDirectory: undefined;
  Booking: { providerId: number; providerName: string };
  HomeVisit: undefined;
  Appointments: undefined;
  Activity: undefined;
  Messages: { providerId: number; providerName: string };
  ProviderSetup: undefined;
  ProviderHome: undefined;
  ProviderAppointments: undefined;
  ProviderHomeVisits: undefined;
  ProviderSummaries: undefined;
  ProviderProfile: undefined;
  ProviderMessages: undefined;
};

const Stack = createNativeStackNavigator<RootStackParamList>();

function AppNavigator() {
  const { user, profile, providerProfile, loading } = useAuth();

  if (loading) return <View style={{flex:1,alignItems:"center",justifyContent:"center",backgroundColor:colors.background}}><ActivityIndicator size="large" color={colors.primary}/></View>;

  return <Stack.Navigator screenOptions={{headerShown:false}}>
    {!user ? <>
      <Stack.Screen name="Welcome" component={WelcomeScreen}/>
      <Stack.Screen name="Login" component={LoginScreen}/>
      <Stack.Screen name="Register" component={RegisterScreen}/>
    </> : user.role === "patient" ? !profile ? <Stack.Screen name="Onboarding" component={OnboardingScreen}/> : <>
      <Stack.Screen name="Home" component={HomeScreen}/>
      <Stack.Screen name="AIIntake" component={AIIntakeScreen}/>
      <Stack.Screen name="CareDirectory" component={CareDirectoryScreen}/>
      <Stack.Screen name="Booking" component={BookingScreen}/>
      <Stack.Screen name="HomeVisit" component={HomeVisitScreen}/>
      <Stack.Screen name="Appointments" component={AppointmentsScreen}/>
      <Stack.Screen name="Activity" component={ActivityScreen}/>
      <Stack.Screen name="Messages" component={MessagesScreen}/>
    </> : !providerProfile ? <Stack.Screen name="ProviderSetup" component={ProviderSetupScreen}/> : <>
      <Stack.Screen name="ProviderHome" component={ProviderHomeScreen}/>
      <Stack.Screen name="ProviderAppointments" component={ProviderAppointmentsScreen}/>
      <Stack.Screen name="ProviderHomeVisits" component={ProviderHomeVisitsScreen}/>
      <Stack.Screen name="ProviderSummaries" component={ProviderSummariesScreen}/>
      <Stack.Screen name="ProviderProfile" component={ProviderProfileScreen}/>
      <Stack.Screen name="ProviderMessages" component={ProviderMessagesScreen}/>
    </>}
  </Stack.Navigator>;
}

export default function App() {
  return <AuthProvider><NavigationContainer theme={{...DefaultTheme,colors:{...DefaultTheme.colors,background:colors.background}}}><StatusBar style="dark"/><AppNavigator/></NavigationContainer></AuthProvider>;
}
