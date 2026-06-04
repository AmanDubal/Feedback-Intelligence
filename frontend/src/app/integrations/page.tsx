'use client';

import { useState } from 'react';
import { AlertCircle, CheckCircle, ChevronDown } from 'lucide-react';

interface Integration {
  id: string;
  name: string;
  description: string;
  icon: string;
  connected: boolean;
  lastSync?: string;
  category: 'data_source' | 'alert' | 'ticketing';
}

export default function IntegrationsPage() {
  const [integrations, setIntegrations] = useState<Integration[]>([
    {
      id: 'csv',
      name: 'CSV Upload',
      description: 'Upload feedback data from CSV files',
      icon: '📊',
      connected: true,
      lastSync: new Date().toISOString(),
      category: 'data_source',
    },
    {
      id: 'json_api',
      name: 'JSON API',
      description: 'Programmatic feedback submission via API',
      icon: '🔌',
      connected: true,
      lastSync: new Date().toISOString(),
      category: 'data_source',
    },
    {
      id: 'email',
      name: 'Email',
      description: 'Collect feedback from email submissions',
      icon: '📧',
      connected: false,
      category: 'data_source',
    },
    {
      id: 'webhook',
      name: 'Webhooks',
      description: 'Real-time feedback via webhook endpoints',
      icon: '🔗',
      connected: true,
      lastSync: new Date().toISOString(),
      category: 'data_source',
    },
    {
      id: 'slack',
      name: 'Slack',
      description: 'Receive alerts about critical issues on Slack',
      icon: '💬',
      connected: false,
      category: 'alert',
    },
    {
      id: 'discord',
      name: 'Discord',
      description: 'Send notifications to Discord channels',
      icon: '🎵',
      connected: false,
      category: 'alert',
    },
    {
      id: 'jira',
      name: 'Jira',
      description: 'Auto-create tickets for detected issues',
      icon: '🎯',
      connected: false,
      category: 'ticketing',
    },
    {
      id: 'github',
      name: 'GitHub',
      description: 'Create GitHub issues automatically',
      icon: '🐙',
      connected: false,
      category: 'ticketing',
    },
  ]);

  const [expandedId, setExpandedId] = useState<string | null>(null);
  const [selectedCategory, setSelectedCategory] = useState<string>('all');

  const categories = [
    { value: 'all', label: 'All Integrations' },
    { value: 'data_source', label: 'Data Sources' },
    { value: 'alert', label: 'Alerts' },
    { value: 'ticketing', label: 'Ticketing' },
  ];

  const filteredIntegrations =
    selectedCategory === 'all'
      ? integrations
      : integrations.filter((i) => i.category === selectedCategory);

  const handleConnect = (id: string) => {
    setIntegrations((prev) =>
      prev.map((i) =>
        i.id === id
          ? {
              ...i,
              connected: !i.connected,
              lastSync: !i.connected ? new Date().toISOString() : undefined,
            }
          : i
      )
    );
  };

  return (
    <div className="max-w-6xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-2">Integrations</h1>
        <p className="text-gray-600">
          Connect your feedback sources, alerting systems, and project management tools
        </p>
      </div>

      {/* Category Filter */}
      <div className="flex flex-wrap gap-2 mb-8">
        {categories.map((cat) => (
          <button
            key={cat.value}
            onClick={() => setSelectedCategory(cat.value)}
            className={`px-4 py-2 rounded-lg font-medium transition ${
              selectedCategory === cat.value
                ? 'bg-blue-600 text-white'
                : 'bg-gray-200 text-gray-800 hover:bg-gray-300'
            }`}
          >
            {cat.label}
          </button>
        ))}
      </div>

      {/* Stats */}
      <div className="grid md:grid-cols-3 gap-4 mb-8">
        <div className="bg-white p-6 rounded-lg shadow">
          <div className="text-gray-600 text-sm">Total Integrations</div>
          <div className="text-3xl font-bold text-gray-900">
            {filteredIntegrations.length}
          </div>
        </div>
        <div className="bg-white p-6 rounded-lg shadow">
          <div className="text-gray-600 text-sm">Connected</div>
          <div className="text-3xl font-bold text-green-600">
            {filteredIntegrations.filter((i) => i.connected).length}
          </div>
        </div>
        <div className="bg-white p-6 rounded-lg shadow">
          <div className="text-gray-600 text-sm">Not Connected</div>
          <div className="text-3xl font-bold text-orange-600">
            {filteredIntegrations.filter((i) => !i.connected).length}
          </div>
        </div>
      </div>

      {/* Integrations List */}
      <div className="space-y-4">
        {filteredIntegrations.map((integration) => (
          <div
            key={integration.id}
            className="bg-white rounded-lg shadow overflow-hidden"
          >
            <button
              onClick={() =>
                setExpandedId(expandedId === integration.id ? null : integration.id)
              }
              className="w-full p-6 flex items-start justify-between hover:bg-gray-50 transition"
            >
              <div className="flex items-start gap-4 flex-1 text-left">
                <div className="text-4xl">{integration.icon}</div>
                <div className="flex-1">
                  <h3 className="font-semibold text-lg mb-1">{integration.name}</h3>
                  <p className="text-gray-600 text-sm">{integration.description}</p>
                  {integration.connected && integration.lastSync && (
                    <div className="mt-2 text-xs text-gray-500">
                      Last synced:{' '}
                      {new Date(integration.lastSync).toLocaleDateString()}
                    </div>
                  )}
                </div>
              </div>

              <div className="flex items-center gap-3">
                <div className="flex flex-col items-end gap-1">
                  {integration.connected ? (
                    <div className="flex items-center gap-1 text-green-600">
                      <CheckCircle size={20} />
                      <span className="text-sm font-medium">Connected</span>
                    </div>
                  ) : (
                    <div className="flex items-center gap-1 text-gray-400">
                      <AlertCircle size={20} />
                      <span className="text-sm font-medium">Not Connected</span>
                    </div>
                  )}
                </div>
                <ChevronDown
                  size={20}
                  className={`text-gray-400 transition ${
                    expandedId === integration.id ? 'rotate-180' : ''
                  }`}
                />
              </div>
            </button>

            {expandedId === integration.id && (
              <div className="p-6 border-t bg-gray-50">
                {integration.category === 'data_source' && (
                  <div className="space-y-4">
                    {integration.id === 'playstore' && (
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          Package Name
                        </label>
                        <input
                          type="text"
                          placeholder="com.example.app"
                          className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        />
                        <label className="block text-sm font-medium text-gray-700 mt-4 mb-2">
                          Service Account JSON
                        </label>
                        <input
                          type="file"
                          accept=".json"
                          className="w-full px-4 py-2 border rounded-lg"
                        />
                      </div>
                    )}
                    {integration.id === 'appstore' && (
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          App ID
                        </label>
                        <input
                          type="text"
                          placeholder="123456789"
                          className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        />
                        <p className="text-xs text-gray-500 mt-2">
                          You'll need API credentials from App Store Connect
                        </p>
                      </div>
                    )}
                  </div>
                )}

                {integration.category === 'alert' && (
                  <div className="space-y-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        {integration.id === 'slack' ? 'Slack Webhook URL' : 'Discord Webhook URL'}
                      </label>
                      <input
                        type="text"
                        placeholder="https://..."
                        className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Alert Threshold (# of complaints)
                      </label>
                      <input
                        type="number"
                        defaultValue="5"
                        className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      />
                    </div>
                  </div>
                )}

                {integration.category === 'ticketing' && (
                  <div className="space-y-4">
                    {integration.id === 'jira' && (
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          Jira URL
                        </label>
                        <input
                          type="text"
                          placeholder="https://your-domain.atlassian.net"
                          className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        />
                        <label className="block text-sm font-medium text-gray-700 mt-4 mb-2">
                          API Token
                        </label>
                        <input
                          type="password"
                          className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        />
                      </div>
                    )}
                    {integration.id === 'github' && (
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          Repository (owner/repo)
                        </label>
                        <input
                          type="text"
                          placeholder="myorg/myrepo"
                          className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        />
                        <label className="block text-sm font-medium text-gray-700 mt-4 mb-2">
                          Personal Access Token
                        </label>
                        <input
                          type="password"
                          className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        />
                      </div>
                    )}
                  </div>
                )}

                <div className="mt-6 flex gap-3">
                  <button
                    onClick={() => handleConnect(integration.id)}
                    className={`flex-1 py-2 px-4 rounded-lg font-medium transition ${
                      integration.connected
                        ? 'bg-red-600 text-white hover:bg-red-700'
                        : 'bg-blue-600 text-white hover:bg-blue-700'
                    }`}
                  >
                    {integration.connected ? 'Disconnect' : 'Connect'}
                  </button>
                  <button className="flex-1 py-2 px-4 bg-gray-200 text-gray-800 rounded-lg font-medium hover:bg-gray-300 transition">
                    Test Connection
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