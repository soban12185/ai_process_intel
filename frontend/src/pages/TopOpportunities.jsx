import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { api } from '../services/api';

export default function TopOpportunities() {
  const [processes, setProcesses] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.getTopProcesses(10)
      .then(setProcesses)
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="text-center py-12 text-gray-500">Loading top opportunities...</div>;

  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-bold text-gray-800">Top 10 AI Opportunities</h1>
      <p className="text-gray-500 text-sm">Processes ranked by AI opportunity score (dynamically calculated)</p>

      <div className="space-y-3">
        {processes.map((p) => (
          <Link
            key={p.process_id}
            to={`/processes/${p.process_id}`}
            className="block bg-white rounded-lg p-4 shadow hover:shadow-md transition-shadow"
          >
            <div className="flex items-center gap-4">
              <div className="w-10 h-10 rounded-full bg-nova-600 text-white flex items-center justify-center font-bold text-sm">
                {p.rank}
              </div>
              <div className="flex-1">
                <h3 className="font-semibold text-gray-800">{p.process_name}</h3>
                <p className="text-xs text-gray-500">{p.business_function}</p>
              </div>
              <div className="text-right">
                <div className="text-2xl font-bold text-nova-600">{p.total_score}</div>
                <span className={`px-2 py-0.5 rounded text-xs font-medium ${getPriorityColor(p.priority)}`}>
                  {p.priority}
                </span>
              </div>
            </div>
            <div className="flex gap-4 mt-2 text-xs text-gray-500">
              <span>Automation: {p.automation_potential}</span>
              <span>Benefit: {p.business_benefit}</span>
              <span>Risk: {p.risk_factor}</span>
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
}

function getPriorityColor(p) {
  switch (p) {
    case 'Very High': return 'bg-red-100 text-red-800';
    case 'High': return 'bg-orange-100 text-orange-800';
    case 'Medium': return 'bg-yellow-100 text-yellow-800';
    case 'Low': return 'bg-green-100 text-green-800';
    default: return 'bg-gray-100 text-gray-800';
  }
}
