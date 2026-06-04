'use client';

import { useState } from 'react';
import type { Cluster } from '@/types';

interface Props {
  clusters: Cluster[];
}

export default function IssueCluster({ clusters }: Props) {
  const [expandedCluster, setExpandedCluster] = useState<string | null>(null);

  if (!clusters || clusters.length === 0) {
    return (
      <div className="bg-white p-6 rounded-lg shadow">
        <h2 className="text-xl font-semibold mb-4">Issue Clusters</h2>
        <p className="text-gray-500 text-center py-12">
          No clusters found. Upload feedback and run clustering analysis.
        </p>
      </div>
    );
  }

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'critical':
        return 'bg-red-100 text-red-800 border-red-300';
      case 'major':
        return 'bg-orange-100 text-orange-800 border-orange-300';
      case 'minor':
        return 'bg-yellow-100 text-yellow-800 border-yellow-300';
      default:
        return 'bg-gray-100 text-gray-800 border-gray-300';
    }
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow">
      <h2 className="text-xl font-semibold mb-6">AI-Detected Issue Clusters</h2>
      <div className="space-y-4">
        {clusters.map((cluster) => (
          <div
            key={cluster.id}
            className="border rounded-lg overflow-hidden hover:shadow-md transition-shadow"
          >
            <button
              onClick={() =>
                setExpandedCluster(
                  expandedCluster === cluster.id ? null : cluster.id
                )
              }
              className="w-full p-4 bg-gray-50 hover:bg-gray-100 flex justify-between items-start text-left"
            >
              <div className="flex-1">
                <div className="flex items-center gap-3 mb-2">
                  <h3 className="font-semibold text-lg">{cluster.name}</h3>
                  <span
                    className={`px-3 py-1 rounded-full text-sm font-medium border ${getSeverityColor(
                      cluster.severity
                    )}`}
                  >
                    {cluster.severity}
                  </span>
                </div>
                <p className="text-sm text-gray-600">
                  {cluster.issue_count} complaint{cluster.issue_count !== 1 ? 's' : ''} in this cluster
                </p>
              </div>
              <div className="text-gray-400 text-xl">
                {expandedCluster === cluster.id ? '−' : '+'}
              </div>
            </button>

            {expandedCluster === cluster.id && (
              <div className="p-4 border-t bg-white">
                <div className="mb-4">
                  <h4 className="text-sm font-semibold text-gray-700 mb-2">
                    Key Keywords
                  </h4>
                  <div className="flex flex-wrap gap-2">
                    {cluster.main_keywords.map((keyword, idx) => (
                      <span
                        key={idx}
                        className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm"
                      >
                        {keyword}
                      </span>
                    ))}
                  </div>
                </div>

                <div className="mb-4">
                  <h4 className="text-sm font-semibold text-gray-700 mb-2">
                    Sample Complaints
                  </h4>
                  <div className="space-y-2">
                    {cluster.sample_feedback.slice(0, 3).map((feedback, idx) => (
                      <div
                        key={idx}
                        className="p-3 bg-gray-50 rounded border-l-2 border-blue-500"
                      >
                        <p className="text-sm text-gray-700">
                          "{feedback.content}"
                        </p>
                        <div className="flex gap-2 mt-1 text-xs text-gray-500">
                          <span className="px-2 py-0.5 bg-gray-200 rounded">
                            {feedback.source}
                          </span>
                          {feedback.platform && (
                            <span className="px-2 py-0.5 bg-gray-200 rounded">
                              {feedback.platform}
                            </span>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                <div className="flex gap-2">
                  <button className="flex-1 px-3 py-2 bg-blue-600 text-white text-sm rounded hover:bg-blue-700 transition">
                    Create Jira Ticket
                  </button>
                  <button className="flex-1 px-3 py-2 bg-gray-200 text-gray-800 text-sm rounded hover:bg-gray-300 transition">
                    View All Complaints
                  </button>
                </div>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}