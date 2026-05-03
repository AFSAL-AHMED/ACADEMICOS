import React, { useEffect, useState, useCallback } from 'react';
import {
  View, Text, StyleSheet, ActivityIndicator,
  TouchableOpacity, ScrollView,
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { api } from '../services/api';

function StatCard({ emoji, label, value, color }) {
  return (
    <View style={[styles.statCard, { borderColor: color + '44' }]}>
      <Text style={styles.statEmoji}>{emoji}</Text>
      <Text style={[styles.statValue, { color }]}>{value}</Text>
      <Text style={styles.statLabel}>{label}</Text>
    </View>
  );
}

export default function DashboardScreen() {
  const [streak, setStreak]   = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError]     = useState(null);

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await api.getStreak();
      setStreak(data);
    } catch (e) {
      setError('Could not load stats. Is the backend running?');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { load(); }, []);

  const streakMsg = () => {
    if (!streak) return '';
    const s = streak.streak;
    if (s === 0) return "Start your streak today! 🚀";
    if (s < 3)   return "Great start! Keep going 💪";
    if (s < 7)   return "You're on fire! 🔥";
    if (s < 14)  return "Incredible consistency! ⚡";
    return "Legendary learner! 🏆";
  };

  return (
    <LinearGradient colors={['#0f0b1e', '#1a1035']} style={styles.bg}>
      <ScrollView contentContainerStyle={styles.container}>
        <View style={styles.header}>
          <Text style={styles.heading}>📊 Dashboard</Text>
          <Text style={styles.sub}>Your learning progress</Text>
        </View>

        {loading ? (
          <ActivityIndicator color="#a78bfa" size="large" style={{ marginTop: 60 }} />
        ) : error ? (
          <Text style={styles.error}>{error}</Text>
        ) : (
          <>
            {/* Streak Hero */}
            <LinearGradient
              colors={['#4f46e5', '#7c3aed']}
              style={styles.streakHero}
              start={{ x: 0, y: 0 }} end={{ x: 1, y: 1 }}
            >
              <Text style={styles.streakFire}>🔥</Text>
              <Text style={styles.streakNumber}>{streak?.streak ?? 0}</Text>
              <Text style={styles.streakDayLabel}>Day Streak</Text>
              <Text style={styles.streakMsg}>{streakMsg()}</Text>
            </LinearGradient>

            {/* Stats Row */}
            <View style={styles.statsRow}>
              <StatCard emoji="📓" label="Total Entries" value={streak?.total_entries ?? 0} color="#a78bfa" />
              <StatCard emoji="🔥" label="Current Streak" value={`${streak?.streak ?? 0}d`} color="#f97316" />
            </View>

            {/* Tips */}
            <View style={styles.tipsCard}>
              <Text style={styles.tipsTitle}>💡 Study Tips</Text>
              {[
                'Write even 3 lines daily to maintain your streak',
                'Tag your topics to see your focus areas',
                'Rate difficulty honestly — it tracks your growth',
                'Review past entries before exams for a quick recap',
              ].map((tip, i) => (
                <View key={i} style={styles.tip}>
                  <Text style={styles.tipDot}>•</Text>
                  <Text style={styles.tipText}>{tip}</Text>
                </View>
              ))}
            </View>

            {/* Refresh */}
            <TouchableOpacity style={styles.refreshBtn} onPress={load} activeOpacity={0.8}>
              <Text style={styles.refreshText}>↻  Refresh Stats</Text>
            </TouchableOpacity>
          </>
        )}
      </ScrollView>
    </LinearGradient>
  );
}

const styles = StyleSheet.create({
  bg:            { flex: 1 },
  container:     { padding: 20, paddingBottom: 50 },
  header:        { marginBottom: 20 },
  heading:       { fontSize: 26, fontWeight: '800', color: '#e2e0f0' },
  sub:           { fontSize: 13, color: '#7c6faa', marginTop: 2 },
  streakHero:    { borderRadius: 20, padding: 32, alignItems: 'center', marginBottom: 20 },
  streakFire:    { fontSize: 44, marginBottom: 4 },
  streakNumber:  { fontSize: 72, fontWeight: '900', color: '#fff', lineHeight: 80 },
  streakDayLabel:{ fontSize: 16, color: '#c4b5fd', fontWeight: '600', letterSpacing: 1 },
  streakMsg:     { fontSize: 14, color: '#ddd6fe', marginTop: 8, fontStyle: 'italic' },
  statsRow:      { flexDirection: 'row', gap: 12, marginBottom: 20 },
  statCard:      { flex: 1, backgroundColor: '#16102b', borderRadius: 16, padding: 18, alignItems: 'center', borderWidth: 1 },
  statEmoji:     { fontSize: 26, marginBottom: 6 },
  statValue:     { fontSize: 28, fontWeight: '800' },
  statLabel:     { fontSize: 12, color: '#7c6faa', marginTop: 4, fontWeight: '600' },
  tipsCard:      { backgroundColor: '#16102b', borderRadius: 16, padding: 18, borderWidth: 1, borderColor: '#2d2250', marginBottom: 20 },
  tipsTitle:     { color: '#a78bfa', fontWeight: '700', fontSize: 14, marginBottom: 12, textTransform: 'uppercase', letterSpacing: 0.8 },
  tip:           { flexDirection: 'row', marginBottom: 8 },
  tipDot:        { color: '#7c3aed', fontSize: 16, marginRight: 8, marginTop: -2 },
  tipText:       { color: '#9490b8', fontSize: 13, lineHeight: 20, flex: 1 },
  refreshBtn:    { backgroundColor: '#1e1533', borderRadius: 12, paddingVertical: 12, alignItems: 'center', borderWidth: 1, borderColor: '#3d3360' },
  refreshText:   { color: '#a78bfa', fontWeight: '700', fontSize: 14 },
  error:         { color: '#f87171', textAlign: 'center', marginTop: 60, fontSize: 14, paddingHorizontal: 30 },
});
