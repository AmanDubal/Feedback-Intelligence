interface PainPoint {
  title: string;
  complaints: number;
  percentage: number;
  severity: string;
  trend: string;
}

interface Props {
  painPoints: PainPoint[];
}

const severityColors = {
  critical: 'bg-red-100 text-red-800',
  major: 'bg-orange-100 text-orange-800',
  minor: 'bg-yellow-100 text-yellow-800',
};

const trendIcons = {
  increasing: '↑',
  stable: '→',
  decreasing: '↓',
  resolved: '✓',
};

export default function TopPainPoints({ painPoints }: Props) {
  return (
    <div className="bg-white p-6 rounded-lg shadow">
      <h2 className="text-xl font-semibold mb-4">Top Pain Points</h2>
      <div className="space-y-4">
        {painPoints.map((point, idx) => (
          <div key={idx} className="border-l-4 border-blue-500 pl-4">
            <div className="flex justify-between items-start mb-2">
              <h3 className="font-semibold text-lg">{point.title}</h3>
              <span className={`px-2 py-1 rounded text-xs font-medium ${
                severityColors[point.severity as keyof typeof severityColors]
              }`}>
                {point.severity}
              </span>
            </div>
            <div className="flex items-center gap-4 text-sm text-gray-600">
              <span>{point.complaints} complaints</span>
              <span>{point.percentage}% of total</span>
              <span className="flex items-center gap-1">
                {trendIcons[point.trend as keyof typeof trendIcons]}
                {point.trend}
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}