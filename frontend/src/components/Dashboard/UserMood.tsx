'use client';

import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

interface Props {
  data: Record<string, number>;
}

const moodEmojis = {
  positive: '😊',
  neutral: '😐',
  negative: '😠',
};

export default function UserMood({ data }: Props) {
  const chartData = Object.entries(data).map(([name, value]) => ({
    mood: name.charAt(0).toUpperCase() + name.slice(1),
    count: value,
    emoji: moodEmojis[name as keyof typeof moodEmojis],
  }));

  return (
    <div className="bg-white p-6 rounded-lg shadow">
      <h2 className="text-xl font-semibold mb-4">User Mood</h2>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="mood" />
          <YAxis />
          <Tooltip />
          <Bar dataKey="count" fill="#3B82F6" />
        </BarChart>
      </ResponsiveContainer>
      <div className="flex justify-around mt-4">
        {chartData.map((item) => (
          <div key={item.mood} className="text-center">
            <div className="text-3xl mb-1">{item.emoji}</div>
            <div className="text-sm text-gray-600">{item.mood}</div>
          </div>
        ))}
      </div>
    </div>
  );
}