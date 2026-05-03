import React from 'react';
import { View, Text, ScrollView, StyleSheet } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';

export default function EntryDetailScreen({ route }) {
  const { entry } = route.params;

  return (
    <LinearGradient colors={['#0f0b1e', '#1a1035']} style={styles.bg}>
      <ScrollView contentContainerStyle={styles.container}>
        {/* Title & Date */}
        <Text style={styles.title}>{entry.title || 'Untitled Entry'}</Text>
        <Text style={styles.date}>{entry.date || ''}</Text>

        {/* Tags */}
        {entry.topics?.length > 0 && (
          <View style={styles.tagsRow}>
            {entry.topics.map((t) => (
              <View key={t} style={styles.chip}>
                <Text style={styles.chipText}>{t}</Text>
              </View>
            ))}
          </View>
        )}

        {/* Difficulty */}
        {entry.difficulty ? (
          <View style={styles.diffRow}>
            <Text style={styles.diffLabel}>Difficulty: </Text>
            <Text style={styles.diffValue}>{entry.difficulty}</Text>
          </View>
        ) : null}

        {/* Divider */}
        <View style={styles.divider} />

        {/* Entry text */}
        <Text style={styles.entryText}>{entry.entry}</Text>
      </ScrollView>
    </LinearGradient>
  );
}

const styles = StyleSheet.create({
  bg:         { flex: 1 },
  container:  { padding: 24, paddingBottom: 60 },
  title:      { fontSize: 24, fontWeight: '800', color: '#e2e0f0', marginBottom: 6 },
  date:       { fontSize: 13, color: '#7c6faa', marginBottom: 14 },
  tagsRow:    { flexDirection: 'row', flexWrap: 'wrap', gap: 8, marginBottom: 12 },
  chip:       { backgroundColor: '#2d1b6e', borderRadius: 20, paddingHorizontal: 12, paddingVertical: 4 },
  chipText:   { color: '#a78bfa', fontSize: 12, fontWeight: '600' },
  diffRow:    { flexDirection: 'row', marginBottom: 10 },
  diffLabel:  { color: '#7c6faa', fontSize: 13 },
  diffValue:  { color: '#818cf8', fontSize: 13, fontWeight: '600' },
  divider:    { height: 1, backgroundColor: '#2d2250', marginVertical: 18 },
  entryText:  { color: '#c4b5fd', fontSize: 15, lineHeight: 26 },
});
