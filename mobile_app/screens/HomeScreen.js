import React, { useState } from 'react';
import {
  View, Text, TextInput, TouchableOpacity,
  ScrollView, StyleSheet, Alert, ActivityIndicator, KeyboardAvoidingView, Platform,
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import StarRating from '../components/StarRating';
import TagSelector from '../components/TagSelector';
import { api } from '../services/api';

export default function HomeScreen() {
  const today = new Date().toLocaleDateString('en-IN', {
    weekday: 'long', year: 'numeric', month: 'long', day: 'numeric',
  });

  const [title, setTitle]         = useState('');
  const [entry, setEntry]         = useState('');
  const [topics, setTopics]       = useState([]);
  const [difficulty, setDifficulty] = useState(3);
  const [loading, setLoading]     = useState(false);

  const handleSubmit = async () => {
    if (!title.trim() || !entry.trim()) {
      Alert.alert('Missing Fields', 'Please fill in the title and your journal entry.');
      return;
    }
    setLoading(true);
    try {
      await api.createEntry({ title, entry, topics, difficulty });
      Alert.alert('✅ Synced to Notion!', 'Your learning journal entry has been saved.');
      setTitle('');
      setEntry('');
      setTopics([]);
      setDifficulty(3);
    } catch (e) {
      Alert.alert('Error', 'Could not save entry. Is the backend running?\n\n' + e.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <KeyboardAvoidingView style={{ flex: 1 }} behavior={Platform.OS === 'ios' ? 'padding' : undefined}>
      <LinearGradient colors={['#0f0b1e', '#1a1035']} style={styles.bg}>
        <ScrollView contentContainerStyle={styles.container} keyboardShouldPersistTaps="handled">
          {/* Header */}
          <View style={styles.header}>
            <Text style={styles.emoji}>✍️</Text>
            <Text style={styles.heading}>Today's Journal</Text>
            <Text style={styles.date}>{today}</Text>
          </View>

          {/* Title */}
          <View style={styles.card}>
            <Text style={styles.label}>What's today's main topic?</Text>
            <TextInput
              style={styles.input}
              placeholder="e.g. Binary Search Trees"
              placeholderTextColor="#5b4f8a"
              value={title}
              onChangeText={setTitle}
            />
          </View>

          {/* Journal Entry */}
          <View style={styles.card}>
            <Text style={styles.label}>What did you learn today?</Text>
            <TextInput
              style={[styles.input, styles.textarea]}
              placeholder="Write your thoughts, key concepts, examples..."
              placeholderTextColor="#5b4f8a"
              value={entry}
              onChangeText={setEntry}
              multiline
              numberOfLines={6}
              textAlignVertical="top"
            />
          </View>

          {/* Tags */}
          <View style={styles.card}>
            <Text style={styles.label}>Topics Covered</Text>
            <TagSelector selected={topics} onChange={setTopics} />
          </View>

          {/* Difficulty */}
          <View style={styles.card}>
            <Text style={styles.label}>How difficult was it?</Text>
            <StarRating value={difficulty} onChange={setDifficulty} />
          </View>

          {/* Submit */}
          <TouchableOpacity
            style={[styles.submitBtn, loading && { opacity: 0.7 }]}
            onPress={handleSubmit}
            disabled={loading}
            activeOpacity={0.85}
          >
            <LinearGradient colors={['#7c3aed', '#4f46e5']} style={styles.submitGradient} start={{ x: 0, y: 0 }} end={{ x: 1, y: 0 }}>
              {loading ? (
                <ActivityIndicator color="#fff" />
              ) : (
                <Text style={styles.submitText}>📓  Save & Sync to Notion</Text>
              )}
            </LinearGradient>
          </TouchableOpacity>
        </ScrollView>
      </LinearGradient>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  bg:           { flex: 1 },
  container:    { padding: 20, paddingBottom: 40 },
  header:       { alignItems: 'center', marginBottom: 24, marginTop: 10 },
  emoji:        { fontSize: 40, marginBottom: 6 },
  heading:      { fontSize: 26, fontWeight: '800', color: '#e2e0f0', letterSpacing: 0.5 },
  date:         { fontSize: 13, color: '#7c6faa', marginTop: 4 },
  card:         { backgroundColor: '#16102b', borderRadius: 16, padding: 16, marginBottom: 14, borderWidth: 1, borderColor: '#2d2250' },
  label:        { color: '#a78bfa', fontWeight: '700', fontSize: 13, marginBottom: 10, textTransform: 'uppercase', letterSpacing: 0.8 },
  input:        { backgroundColor: '#1e1533', borderRadius: 10, padding: 12, color: '#e2e0f0', fontSize: 15, borderWidth: 1, borderColor: '#3d3360' },
  textarea:     { height: 130, lineHeight: 22 },
  submitBtn:    { borderRadius: 14, overflow: 'hidden', marginTop: 6 },
  submitGradient:{ paddingVertical: 16, alignItems: 'center', justifyContent: 'center' },
  submitText:   { color: '#fff', fontWeight: '800', fontSize: 16, letterSpacing: 0.4 },
});
