import type { PrioritiesData, Issue } from '@/types';

interface Props {
  priorities: PrioritiesData;
}

const priorityConfig = {
  immediate: {
    title: '🚨 Fix Immediately',
    color: 'border-red-500 bg-red-50',
    badge: 'bg-red-100 text-red-800',
  },
  next_sprint: {
    title: '📅 Next Sprint',
    color: 'border-orange-500 bg-orange-50',
    badge: 'bg-orange-100 text-orange-800',
  },
  low: {
    title: '📝 Low Priority',
    color: 'border-yellow-500 bg-yellow-50',
    badge: 'bg-yellow-100 text-yellow-800',
  },
};

function IssueCard({ issue }: { issue: Issue }) {
  return (
    <div className="bg-white p-4 rounded-lg border-l-4 border-blue-500 shadow-sm hover:shadow-md transition-shadow">
      <div className="flex justify-between items-start mb-2">
        <h3 className="font-semibold text-lg">{issue.title}</h3>
        <span className={`px-2 py-1 rounded text-xs font-medium ${
          issue.severity === 'critical' ? 'bg-red-100 text-red-800' :
          issue.severity === 'major' ? 'bg-orange-100 text-orange-800' :
          'bg-yellow-100 text-yellow-800'
        }`}>
          {issue.severity}
        </span>
      </div>

      <div className="text-sm text-gray-600 mb-3">
        Category: {issue.category}
      </div>

      <div className="flex flex-wrap gap-3 text-sm">
        <div className="flex items-center gap-1">
          <span className="font-medium">{issue.complaint_count}</span>
          <span className="text-gray-600">complaints</span>
        </div>
        <div className="flex items-center gap-1">
          <span className="font-medium">{issue.complaint_percentage}%</span>
          <span className="text-gray-600">of total</span>
        </div>
        <div className={`px-2 py-1 rounded text-xs ${
          issue.trend === 'increasing' ? 'bg-red-100 text-red-800' :
          issue.trend === 'decreasing' ? 'bg-green-100 text-green-800' :
          'bg-gray-100 text-gray-800'
        }`}>
          {issue.trend === 'increasing' ? '↑' : issue.trend === 'decreasing' ? '↓' : '→'} {issue.trend}
        </div>
      </div>

      {issue.keywords && issue.keywords.length > 0 && (
        <div className="mt-3 flex flex-wrap gap-2">
          {issue.keywords.slice(0, 5).map((keyword, idx) => (
            <span key={idx} className="px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded">
              {keyword}
            </span>
          ))}
        </div>
      )}

      {issue.affected_platforms && issue.affected_platforms.length > 0 && (
        <div className="mt-2 text-xs text-gray-500">
          Affects: {issue.affected_platforms.join(', ')}
        </div>
      )}
    </div>
  );
}

export default function PriorityList({ priorities }: Props) {
  return (
    <div className="space-y-8">
      {Object.entries(priorityConfig).map(([key, config]) => {
        const issues = priorities.priorities[key as keyof typeof priorities.priorities];
        if (issues.length === 0) return null;

        return (
          <div key={key} className={`p-6 rounded-lg border-2 ${config.color}`}>
            <h2 className="text-2xl font-bold mb-4">{config.title}</h2>
            <div className="space-y-4">
              {issues.map((issue) => (
                <IssueCard key={issue.id} issue={issue} />
              ))}
            </div>
          </div>
        );
      })}

      {priorities.total_issues === 0 && (
        <div className="text-center py-12 text-gray-500">
          No issues found. Upload feedback to see analysis.
        </div>
      )}
    </div>
  );
}