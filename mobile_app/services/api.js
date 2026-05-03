import { API_BASE_URL } from '../config';

export const api = {
  async createEntry(data) {
    const res = await fetch(`${API_BASE_URL}/journal/entry`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  },

  async getEntries() {
    const res = await fetch(`${API_BASE_URL}/journal/entries`);
    if (!res.ok) throw new Error(await res.text());
    const data = await res.json();
    return data.entries;
  },

  async getStreak() {
    const res = await fetch(`${API_BASE_URL}/journal/streak`);
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  },
};
