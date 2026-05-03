import React, { useState } from 'react';
import { View, Text, TouchableOpacity, StyleSheet, TextInput } from 'react-native';

const PRESET_TAGS = ['DSA', 'Math', 'AI/ML', 'Web Dev', 'OS', 'DBMS', 'Networks', 'Python', 'Other'];

export default function TagSelector({ selected, onChange }) {
  const [custom, setCustom] = useState('');

  const toggle = (tag) => {
    if (selected.includes(tag)) {
      onChange(selected.filter((t) => t !== tag));
    } else {
      onChange([...selected, tag]);
    }
  };

  const addCustom = () => {
    const t = custom.trim();
    if (t && !selected.includes(t)) {
      onChange([...selected, t]);
    }
    setCustom('');
  };

  return (
    <View>
      <View style={styles.tags}>
        {PRESET_TAGS.map((tag) => (
          <TouchableOpacity
            key={tag}
            style={[styles.tag, selected.includes(tag) && styles.tagActive]}
            onPress={() => toggle(tag)}
            activeOpacity={0.75}
          >
            <Text style={[styles.tagText, selected.includes(tag) && styles.tagTextActive]}>
              {tag}
            </Text>
          </TouchableOpacity>
        ))}
      </View>
      <View style={styles.customRow}>
        <TextInput
          style={styles.customInput}
          placeholder="Add custom tag..."
          placeholderTextColor="#5b4f8a"
          value={custom}
          onChangeText={setCustom}
          onSubmitEditing={addCustom}
          returnKeyType="done"
        />
        <TouchableOpacity style={styles.addBtn} onPress={addCustom}>
          <Text style={styles.addBtnText}>+ Add</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  tags:          { flexDirection: 'row', flexWrap: 'wrap', gap: 8 },
  tag:           { backgroundColor: '#1e1533', borderRadius: 20, paddingHorizontal: 14, paddingVertical: 6, borderWidth: 1, borderColor: '#3d3360' },
  tagActive:     { backgroundColor: '#7c3aed', borderColor: '#a78bfa' },
  tagText:       { color: '#7c6faa', fontSize: 13, fontWeight: '500' },
  tagTextActive: { color: '#fff' },
  customRow:     { flexDirection: 'row', marginTop: 10, gap: 8 },
  customInput:   { flex: 1, backgroundColor: '#1e1533', borderRadius: 10, paddingHorizontal: 14, paddingVertical: 8, color: '#e2e0f0', borderWidth: 1, borderColor: '#3d3360', fontSize: 13 },
  addBtn:        { backgroundColor: '#7c3aed', borderRadius: 10, paddingHorizontal: 14, justifyContent: 'center' },
  addBtnText:    { color: '#fff', fontWeight: '700', fontSize: 13 },
});
