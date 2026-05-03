import React, { useEffect, useState, useCallback } from 'react';
import {
  View, Text, FlatList, TouchableOpacity,
  StyleSheet, ActivityIndicator, RefreshControl,
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { useNavigation } from '@react-navigation/native';
import { api } from '../services/api';

function EntryCard({ item, onPress }) {
  return (
    <TouchableOpacity style={styles.card} onPress={onPress} activeOpacity={0.82}>
      <View style={styles.cardTop}>
        <Text style={styles.cardTitle} numberOfLines={1}>{item.title || 'Untitled Entry'}</Text>
        <Text style={styles.cardDate}>{item.date || ''}</Text>
      </View>
      <Text style={styles.cardPreview} numberOfLines={2}>{item.entry}</Text>
      <View style={styles.cardBottom}>
        {item.topics?.slice(0, 3).map((t) => (
          <View key={t} style={styles.chip}><Text style={styles.chipText}>{t}</Text></View>
        ))}
        {item.difficulty ? (
          <View style={styles.diffChip}><Text style={styles.diffText}>{item.difficulty}</Text></View>
        ) : null}
      </View>
    </TouchableOpacity>
  );
}

export default function HistoryScreen() {
  const navigation = useNavigation();
  const [entries, setEntries]     = useState([]);
  const [loading, setLoading]     = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [error, setError]         = useState(null);

  const load = useCallback(async (isRefresh = false) => {
    if (isRefresh) setRefreshing(true);
    else setLoading(true);
    setError(null);
    try {
      const data = await api.getEntries();
      setEntries(data);
    } catch (e) {
      setError('Could not load entries. Is the backend running?');
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  }, []);

  useEffect(() => { load(); }, []);

  return (
    <LinearGradient colors={['#0f0b1e', '#1a1035']} style={styles.bg}>
      <View style={styles.header}>
        <Text style={styles.heading}>📖 Past Entries</Text>
        <Text style={styles.sub}>{entries.length} entries synced from Notion</Text>
      </View>

      {loading ? (
        <ActivityIndicator color="#a78bfa" size="large" style={{ marginTop: 60 }} />
      ) : error ? (
        <Text style={styles.error}>{error}</Text>
      ) : entries.length === 0 ? (
        <Text style={styles.empty}>No entries yet. Start your first journal! ✍️</Text>
      ) : (
        <FlatList
          data={entries}
          keyExtractor={(item) => item.id}
          renderItem={({ item }) => (
            <EntryCard
              item={item}
              onPress={() => navigation.navigate('EntryDetail', { entry: item })}
            />
          )}
          contentContainerStyle={{ padding: 16, paddingBottom: 40 }}
          refreshControl={
            <RefreshControl refreshing={refreshing} onRefresh={() => load(true)} tintColor="#a78bfa" />
          }
        />
      )}
    </LinearGradient>
  );
}

const styles = StyleSheet.create({
  bg:          { flex: 1 },
  header:      { paddingHorizontal: 20, paddingTop: 16, paddingBottom: 8 },
  heading:     { fontSize: 24, fontWeight: '800', color: '#e2e0f0' },
  sub:         { fontSize: 13, color: '#7c6faa', marginTop: 2 },
  card:        { backgroundColor: '#16102b', borderRadius: 16, padding: 16, marginBottom: 12, borderWidth: 1, borderColor: '#2d2250' },
  cardTop:     { flexDirection: 'row', justifyContent: 'space-between', marginBottom: 6 },
  cardTitle:   { flex: 1, color: '#e2e0f0', fontWeight: '700', fontSize: 15, marginRight: 8 },
  cardDate:    { color: '#7c6faa', fontSize: 12, alignSelf: 'flex-start' },
  cardPreview: { color: '#9490b8', fontSize: 13, lineHeight: 19, marginBottom: 10 },
  cardBottom:  { flexDirection: 'row', flexWrap: 'wrap', gap: 6 },
  chip:        { backgroundColor: '#2d1b6e', borderRadius: 20, paddingHorizontal: 10, paddingVertical: 3 },
  chipText:    { color: '#a78bfa', fontSize: 11, fontWeight: '600' },
  diffChip:    { backgroundColor: '#1e1035', borderRadius: 20, paddingHorizontal: 10, paddingVertical: 3, borderWidth: 1, borderColor: '#4f46e5' },
  diffText:    { color: '#818cf8', fontSize: 11 },
  error:       { color: '#f87171', textAlign: 'center', marginTop: 60, fontSize: 14, paddingHorizontal: 30 },
  empty:       { color: '#7c6faa', textAlign: 'center', marginTop: 80, fontSize: 15 },
});
