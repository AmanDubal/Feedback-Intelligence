'use client';

import { useRouter } from 'next/navigation';
import { Upload } from 'lucide-react';

export default function Home() {
  const router = useRouter();

  return (
    <div className="text-center py-12">
      <h1 className="text-4xl font-bold text-gray-900 mb-4">
        AI Product Feedback Intelligence
      </h1>
      <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
        Transform chaos into actionable priorities. Automatically cluster feedback,
        detect issues, and prioritize what matters most.
      </p>

      <div className="grid md:grid-cols-3 gap-6 max-w-4xl mx-auto mb-12">
        <div className="bg-white p-6 rounded-lg shadow">
          <div className="text-3xl mb-2">🎯</div>
          <h3 className="font-semibold mb-2">Smart Clustering</h3>
          <p className="text-sm text-gray-600">
            AI groups similar complaints automatically
          </p>
        </div>

        <div className="bg-white p-6 rounded-lg shadow">
          <div className="text-3xl mb-2">📊</div>
          <h3 className="font-semibold mb-2">Priority Ranking</h3>
          <p className="text-sm text-gray-600">
            Know exactly what to fix first
          </p>
        </div>

        <div className="bg-white p-6 rounded-lg shadow">
          <div className="text-3xl mb-2">🔥</div>
          <h3 className="font-semibold mb-2">Trend Detection</h3>
          <p className="text-sm text-gray-600">
            Catch issues before they explode
          </p>
        </div>
      </div>

      <div className="flex justify-center gap-4">
        <button
          onClick={() => router.push('/dashboard')}
          className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-medium"
        >
          View Dashboard
        </button>
        <button
          onClick={() => router.push('/analysis')}
          className="px-6 py-3 bg-white text-gray-700 border border-gray-300 rounded-lg hover:bg-gray-50 font-medium flex items-center gap-2"
        >
          <Upload size={20} />
          Upload Feedback
        </button>
      </div>
    </div>
  );
}