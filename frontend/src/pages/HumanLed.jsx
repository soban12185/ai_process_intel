import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { api } from '../services/api';

export default function HumanLed() {
  const [processes, setProcesses] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.getHumanLed()
      .then(setProcesses)
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="text-center py-12 text-gray-500">Loading...</div>;

  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-bold text-gray-800">Human-Led Processes</h1>
      <p className="text-gray-500 text-sm">Processes that should remain predominantly human-operated due to regulatory sensitivity, high risk, or low automation feasibility</p>

      {processes.length === 0 ? (
        <div className="bg-white rounded-lg p-8 text-center text-gray-400">
          No processes currently classified as human-led. Analyze processes first.
        </div>
      ) : (
        <div className="space-y-3">
          {processes.map((p) => (
            <Link
              key={p.process_id}
              to={`/processes/${p.process_id}`}
              className="block bg-white rounded-lg p-4 shadow hover:shadow-md transition-shadow border-l-4 border-amber-400"
            >
              <div className="flex justify-between items-start">
                <div>
                  <h3 className="font-semibold text-gray-800">{p.process_name}</h3>
                  <p className="text-xs text-gray-500">{p.business_function}</p>
                </div>
                <div className="flex gap-2 text-xs">
                  <span className="px-2 py-0.5 bg-amber-100 text-amber-800 rounded">Regulatory: {p.regulatory_sensitivity}</span>
                  <span className="px-2 py-0.5 bg-red-100 text-red-800 rounded">Risk: {p.risk_factor}</span>
                  <span className="px-2 py-0.5 bg-slate-100 text-slate-700 rounded">Auto: {p.automation_potential}</span>
                </div>
              </div>
              {p.reasons?.length > 0 && (
                <div className="mt-2 flex flex-wrap gap-2">
                  {p.reasons.map((r, i) => (
                    <span key={i} className="text-xs text-amber-700 bg-amber-50 px-2 py-0.5 rounded">{r}</span>
                  ))}
                </div>
              )}
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
