'use client';

import { useState, useEffect } from 'react';
import { analysisAPI, feedbackAPI } from '@/lib/api';
import type { PrioritiesData } from '@/types';
import CSVUpload from '@/components/Upload/CSVUpload';
import PriorityList from '@/components/Analysis/PriorityList';

export default function AnalysisPage() {
  const [priorities, setPriorities] = useState<PrioritiesData | null>(null);
  const [loading, setLoading] = useState(false);
  const [clustering, setClustering] = useState(false);

  useEffect(() => {
    loadPriorities();
  }, []);

  const loadPriorities = async () => {
    try {
      setLoading(true);
      const result = await analysisAPI.getPriorities();
      setPriorities(result);
    } catch (error) {
      console.error('Error loading priorities:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleUploadComplete = async () => {
    // After upload, trigger clustering
    setClustering(true);
    try {
      await analysisAPI.cluster(7);
      await loadPriorities();
    } catch (error) {
      console.error('Error clustering:', error);
    } finally {
      setClustering(false);
    }
  };

  return (
    <div>
      <h1 className="text-3xl font-bold mb-8">Feedback Analysis</h1>

      {/* Upload Section */}
      <div className="mb-8">
        <CSVUpload onUploadComplete={handleUploadComplete} />
      </div>

      {/* Clustering Status */}
      {clustering && (
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
          <div className="flex items-center gap-2">
            <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600"></div>
            <span className="text-blue-800">
              Analyzing feedback and clustering issues...
            </span>
          </div>
        </div>
      )}

      {/* Priority Lists */}
      {loading ? (
        <div className="text-center py-12">Loading priorities...</div>
      ) : priorities ? (
        <PriorityList priorities={priorities} />
      ) : (
        <div className="text-center py-12 text-gray-500">
          Upload feedback to see analysis
        </div>
      )}
    </div>
  );
}