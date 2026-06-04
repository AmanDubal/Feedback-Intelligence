'use client';

import { useState } from 'react';
import { feedbackAPI } from '@/lib/api';
import { Upload } from 'lucide-react';

interface Props {
  onUploadComplete: () => void;
}

export default function CSVUpload({ onUploadComplete }: Props) {
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  const handleFileSelect = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    if (!file.name.endsWith('.csv')) {
      setError('Please upload a CSV file');
      return;
    }

    setUploading(true);
    setError(null);
    setSuccess(null);

    try {
      const result = await feedbackAPI.uploadCSV(file);
      setSuccess(result.message);
      setTimeout(() => {
        onUploadComplete();
      }, 1000);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Upload failed');
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow">
      <h2 className="text-xl font-semibold mb-4">Upload Feedback</h2>
      
      <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center">
        <Upload className="mx-auto h-12 w-12 text-gray-400 mb-4" />
        
        <label className="cursor-pointer">
          <span className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 inline-block">
            Choose CSV File
          </span>
          <input
            type="file"
            accept=".csv"
            onChange={handleFileSelect}
            disabled={uploading}
            className="hidden"
          />
        </label>

        <p className="text-sm text-gray-500 mt-4">
          CSV should contain: content, title (optional), rating (optional)
        </p>
      </div>

      {uploading && (
        <div className="mt-4 text-center text-blue-600">
          Uploading and processing...
        </div>
      )}

      {error && (
        <div className="mt-4 p-3 bg-red-50 text-red-800 rounded">
          {error}
        </div>
      )}

      {success && (
        <div className="mt-4 p-3 bg-green-50 text-green-800 rounded">
          {success}
        </div>
      )}
    </div>
  );
}