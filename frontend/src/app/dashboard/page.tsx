'use client';

import { useEffect, useState } from 'react';
import { analysisAPI } from '@/lib/api';
import type { DashboardData } from '@/types';
import TopPainPoints from '@/components/Dashboard/TopPainPoints';
import TrendChart from '@/components/Dashboard/TrendChart';
import SeverityBreakdown from '@/components/Dashboard/SeverityBreakdown';
import UserMood from '@/components/Dashboard/UserMood';

export default function DashboardPage() {
  const [data, setData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDashboard();
  }, []);

  const loadDashboard = async () => {
    try {
      const result = await analysisAPI.getDashboard();
      setData(result);
    } catch (error) {
      console.error('Error loading dashboard:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="text-center py-12">Loading dashboard...</div>;
  }

  if (!data) {
    return <div className="text-center py-12">No data available</div>;
  }

  return (
    <div>
      <h1 className="text-3xl font-bold mb-8">Dashboard</h1>

      {/* Overview Stats */}
      <div className="grid md:grid-cols-3 gap-6 mb-8">
        <div className="bg-white p-6 rounded-lg shadow">
          <div className="text-sm text-gray-600 mb-1">Total Feedbacks</div>
          <div className="text-3xl font-bold">{data.overview.total_feedbacks}</div>
        </div>
        <div className="bg-white p-6 rounded-lg shadow">
          <div className="text-sm text-gray-600 mb-1">Active Issues</div>
          <div className="text-3xl font-bold">{data.overview.active_issues}</div>
        </div>
        <div className="bg-white p-6 rounded-lg shadow">
          <div className="text-sm text-gray-600 mb-1">Critical Issues</div>
          <div className="text-3xl font-bold text-red-600">
            {data.overview.critical_issues}
          </div>
        </div>
      </div>

      {/* Top Pain Points */}
      <div className="mb-8">
        <TopPainPoints painPoints={data.top_pain_points} />
      </div>

      {/* Charts Row */}
      <div className="grid md:grid-cols-2 gap-6 mb-8">
        <SeverityBreakdown data={data.severity_breakdown} />
        <UserMood data={data.sentiment_breakdown} />
      </div>

      {/* Trending Issues */}
      {data.trending_issues.length > 0 && (
        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-xl font-semibold mb-4">🔥 Trending Issues</h2>
          <div className="space-y-3">
            {data.trending_issues.map((issue, idx) => (
              <div key={idx} className="flex justify-between items-center p-3 bg-red-50 rounded">
                <span className="font-medium">{issue.title}</span>
                <span className="text-red-600 text-sm">
                  ↑ {issue.change_percentage}%
                </span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}