export interface Feedback {
  id: number;
  platform: string;
  content: string;
  title?: string;
  rating?: number;
  sentiment?: 'positive' | 'neutral' | 'negative';
  created_at: string;
}

export interface Issue {
  id: number;
  title: string;
  category: string;
  severity: 'critical' | 'major' | 'minor';
  priority: 'immediate' | 'next_sprint' | 'low';
  trend: 'increasing' | 'stable' | 'decreasing' | 'resolved';
  complaint_count: number;
  complaint_percentage: number;
  affected_users?: number;
  affected_platforms?: string[];
  affected_versions?: string[];
  keywords?: string[];
  priority_score?: number;
}

export interface DashboardData {
  overview: {
    total_feedbacks: number;
    active_issues: number;
    critical_issues: number;
  };
  top_pain_points: Array<{
    title: string;
    complaints: number;
    percentage: number;
    severity: string;
    trend: string;
  }>;
  severity_breakdown: Record<string, number>;
  sentiment_breakdown: Record<string, number>;
  trending_issues: Array<{
    title: string;
    trend: string;
    change_percentage: number;
  }>;
}

export interface PrioritiesData {
  priorities: {
    immediate: Issue[];
    next_sprint: Issue[];
    low: Issue[];
  };
  total_issues: number;
}