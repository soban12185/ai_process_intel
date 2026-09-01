import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { api } from '../services/api';

const FUNCTIONS = [
  'Customer Onboarding', 'KYC', 'AML', 'Compliance', 'Fraud', 'Cards',
  'Lending', 'Mortgage', 'Credit', 'Collections', 'Payments', 'Treasury',
  'Finance', 'Operations', 'HR', 'Procurement', 'IT', 'Cybersecurity',
  'Data Management', 'Risk', 'Retail Banking', 'Corporate Banking',
  'Wealth Management', 'Customer Service', 'Security', 'General',
];

export default function AddProcess() {
  const navigate = useNavigate();
  const [form, setForm] = useState({ name: '', description: '', business_purpose: '', business_function: 'General', activities: '' });
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (analyze = false) => {
    if (!form.name.trim()) return alert('Process name is required');
    setLoading(true);
    try {
      const data = {
        name: form.name,
        description: form.description,
        business_purpose: form.business_purpose,
        business_function: form.business_function,
        activities: form.activities.split('\n').filter(l => l.trim()).map((name, i) => ({ name: name.trim(), sequence_order: i + 1 })),
      };

      if (analyze) {
        const result = await api.analyzeNew(data);
        navigate(`/processes/${result.process_id}`);
      } else {
        const proc = await api.createProcess(data);
        navigate(`/processes/${proc.id}`);
      }
    } catch (err) {
      alert('Error: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl space-y-4">
      <h1 className="text-2xl font-bold text-gray-800">Add New Process (Process 101+)</h1>
      <p className="text-gray-500 text-sm">Add a new business process. It will use the same AI analysis pipeline as the existing 120 processes.</p>

      <div className="bg-white rounded-lg p-5 shadow space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Process Name *</label>
          <input
            type="text"
            value={form.name}
            onChange={(e) => setForm({ ...form, name: e.target.value })}
            placeholder="e.g. Insurance Claim Processing"
            className="w-full border rounded px-3 py-2 text-sm"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Description</label>
          <textarea
            value={form.description}
            onChange={(e) => setForm({ ...form, description: e.target.value })}
            placeholder="Describe what this process does..."
            rows={3}
            className="w-full border rounded px-3 py-2 text-sm"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Business Purpose</label>
          <input
            type="text"
            value={form.business_purpose}
            onChange={(e) => setForm({ ...form, business_purpose: e.target.value })}
            placeholder="Why does this process exist?"
            className="w-full border rounded px-3 py-2 text-sm"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Business Function</label>
          <select
            value={form.business_function}
            onChange={(e) => setForm({ ...form, business_function: e.target.value })}
            className="w-full border rounded px-3 py-2 text-sm"
          >
            {FUNCTIONS.map(f => <option key={f} value={f}>{f}</option>)}
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Activities (one per line)</label>
          <textarea
            value={form.activities}
            onChange={(e) => setForm({ ...form, activities: e.target.value })}
            placeholder={"Receive claim\nVerify policy\nAssess damage\nProcess payment\nClose claim"}
            rows={5}
            className="w-full border rounded px-3 py-2 text-sm font-mono"
          />
        </div>

        <div className="flex gap-3">
          <button
            onClick={() => handleSubmit(false)}
            disabled={loading}
            className="bg-slate-600 text-white px-4 py-2 rounded text-sm hover:bg-slate-700 disabled:opacity-50"
          >
            {loading ? 'Saving...' : 'Save Without Analyzing'}
          </button>
          <button
            onClick={() => handleSubmit(true)}
            disabled={loading}
            className="bg-nova-600 text-white px-4 py-2 rounded text-sm hover:bg-nova-700 disabled:opacity-50"
          >
            {loading ? 'Analyzing...' : 'Save & Analyze with AI'}
          </button>
        </div>
      </div>
    </div>
  );
}
