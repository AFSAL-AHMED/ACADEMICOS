import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { Ionicons } from '@expo/vector-icons';
import { StatusBar } from 'expo-status-bar';

import HomeScreen        from './screens/HomeScreen';
import HistoryScreen     from './screens/HistoryScreen';
import DashboardScreen   from './screens/DashboardScreen';
import EntryDetailScreen from './screens/EntryDetailScreen';

const Tab   = createBottomTabNavigator();
const Stack = createNativeStackNavigator();

// Stack wrapping History so EntryDetail can slide in
function HistoryStack() {
  return (
    <Stack.Navigator
      screenOptions={{
        headerStyle:   { backgroundColor: '#16102b' },
        headerTintColor: '#a78bfa',
        headerTitleStyle: { fontWeight: '700', color: '#e2e0f0' },
      }}
    >
      <Stack.Screen name="History"     component={HistoryScreen}     options={{ title: 'Past Entries' }} />
      <Stack.Screen name="EntryDetail" component={EntryDetailScreen} options={{ title: 'Entry' }} />
    </Stack.Navigator>
  );
}

export default function App() {
  return (
    <NavigationContainer>
      <StatusBar style="light" />
      <Tab.Navigator
        screenOptions={({ route }) => ({
          tabBarIcon: ({ focused, color, size }) => {
            const icons = {
              Journal:   focused ? 'book'          : 'book-outline',
              History:   focused ? 'time'          : 'time-outline',
              Dashboard: focused ? 'stats-chart'   : 'stats-chart-outline',
            };
            return <Ionicons name={icons[route.name]} size={size} color={color} />;
          },
          tabBarActiveTintColor:   '#a78bfa',
          tabBarInactiveTintColor: '#5b4f8a',
          tabBarStyle: {
            backgroundColor: '#0f0b1e',
            borderTopColor:  '#1e1533',
            borderTopWidth:  1,
            paddingBottom:   6,
            height:          60,
          },
          tabBarLabelStyle:   { fontSize: 11, fontWeight: '600' },
          headerStyle:        { backgroundColor: '#0f0b1e' },
          headerTitleStyle:   { color: '#e2e0f0', fontWeight: '800' },
          headerTintColor:    '#a78bfa',
          headerShadowVisible: false,
        })}
      >
        <Tab.Screen
          name="Journal"
          component={HomeScreen}
          options={{ title: "Today's Journal", headerTitle: '🎓 ACADEMICOS' }}
        />
        <Tab.Screen
          name="History"
          component={HistoryStack}
          options={{ headerShown: false }}
        />
        <Tab.Screen
          name="Dashboard"
          component={DashboardScreen}
          options={{ title: 'Dashboard' }}
        />
      </Tab.Navigator>
    </NavigationContainer>
  );
}
