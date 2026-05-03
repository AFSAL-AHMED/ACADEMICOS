import React from 'react';
import { View, Text, TouchableOpacity, StyleSheet } from 'react-native';

export default function StarRating({ value, onChange }) {
  return (
    <View style={styles.row}>
      {[1, 2, 3, 4, 5].map((star) => (
        <TouchableOpacity key={star} onPress={() => onChange(star)} activeOpacity={0.7}>
          <Text style={[styles.star, star <= value && styles.starActive]}>★</Text>
        </TouchableOpacity>
      ))}
      <Text style={styles.label}>
        {value === 1 ? 'Easy' : value === 2 ? 'Medium' : value === 3 ? 'Hard' : value === 4 ? 'Tough' : 'Extreme'}
      </Text>
    </View>
  );
}

const styles = StyleSheet.create({
  row:       { flexDirection: 'row', alignItems: 'center', gap: 4 },
  star:      { fontSize: 28, color: '#3d3360' },
  starActive:{ color: '#a78bfa' },
  label:     { marginLeft: 8, color: '#a78bfa', fontWeight: '600', fontSize: 13 },
});
