import React, { useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, PieChart, Pie, Cell, Treemap } from 'recharts';
import { api } from '../services/api';

const COLORS = ['#ef4444', '#f97316', '#eab308', '#22c55e', '#3b82f6', '#8b5cf6'];

function StatCard({ label, value, color = 'bg-white' }) {
  return (
    <div className={`${color} rounded-lg p-4 shadow`}>
      <p className="text-xs text-gray-500 uppercase tracking-wide">{label}</p>
      <p className="text-2xl font-bold mt-1">{value}</p>
    </div>
  );
}

export default function Dashboard() {
  const [stats, setStats] = useState(null);
  const [topProcesses, setTopProcesses] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([api.getStats(), api.getTopProcesses(10)])
      .then(([s, t]) => { setStats(s); setTopProcesses(t); })
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="text-center py-12 text-gray-500">Loading dashboard...</div>;
  if (!stats) return <div className="text-center py-12 text-red-500">Failed to load stats</div>;

  const priorityData = [
    { name: 'Very High', value: stats.very_high_count },
    { name: 'High', value: stats.high_count },
    { name: 'Medium', value: stats.medium_count },
    { name: 'Low', value: stats.low_count },
  ].filter(d => d.value > 0);

  const topChartData = topProcesses.slice(0, 10).map(p => ({
    name: p.process_name.length > 25 ? p.process_name.slice(0, 25) + '...' : p.process_name,
    score: p.total_score,
  }));

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-800">NovaBank Process Intelligence Dashboard</h1>
        <p className="text-gray-500 text-sm mt-1">AI opportunity analysis across {stats.total_processes} banking processes</p>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <StatCard label="Total Processes" value={stats.total_processes} />
        <StatCard label="Very High Opportunity" value={stats.very_high_count} color="bg-red-50" />
        <StatCard label="High Opportunity" value={stats.high_count} color="bg-orange-50" />
        <StatCard label="Avg AI Score" value={stats.avg_score} color="bg-blue-50" />
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <StatCard label="Medium Opportunity" value={stats.medium_count} color="bg-yellow-50" />
        <StatCard label="Low Opportunity" value={stats.low_count} color="bg-green-50" />
        <StatCard label="High Automation" value={stats.high_automation_count} color="bg-purple-50" />
        <StatCard label="Analyzed" value={stats.analyzed_processes} color="bg-slate-50" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-lg p-4 shadow">
          <h3 className="text-sm font-semibold text-gray-700 mb-3">Priority Distribution</h3>
          <ResponsiveContainer width="100%" height={250}>
            <PieChart>
              <Pie data={priorityData} cx="50%" cy="50%" outerRadius={80} dataKey="value" label={({ name, value }) => `${name}: ${value}`}>
                {priorityData.map((_, i) => <Cell key={i} fill={['#ef4444', '#f97316', '#eab308', '#22c55e'][i]} />)}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>

        <div className="bg-white rounded-lg p-4 shadow">
          <h3 className="text-sm font-semibold text-gray-700 mb-3">Top 10 AI Opportunities</h3>
          <ResponsiveContainer width="100%" height={250}>
            <BarChart data={topChartData} layout="vertical" margin={{ left: 10 }}>
              <XAxis type="number" domain={[0, 100]} />
              <YAxis type="category" dataKey="name" width={130} tick={{ fontSize: 11 }} />
              <Tooltip />
              <Bar dataKey="score" fill="#3b82f6" radius={[0, 4, 4, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="bg-white rounded-lg p-4 shadow">
        <h3 className="text-sm font-semibold text-gray-700 mb-3">Top Processes</h3>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b text-left text-gray-500">
                <th className="py-2 px-3">#</th>
                <th className="py-2 px-3">Process</th>
                <th className="py-2 px-3">Function</th>
                <th className="py-2 px-3">Score</th>
                <th className="py-2 px-3">Priority</th>
                <th className="py-2 px-3">Automation</th>
              </tr>
            </thead>
            <tbody>
              {topProcesses.map((p) => (
                <tr key={p.process_id} className="border-b hover:bg-slate-50">
                  <td className="py-2 px-3 text-gray-400">{p.rank}</td>
                  <td className="py-2 px-3 font-medium">{p.process_name}</td>
                  <td className="py-2 px-3 text-gray-500">{p.business_function}</td>
                  <td className="py-2 px-3"><span className="font-bold text-nova-600">{p.total_score}</span></td>
                  <td className="py-2 px-3">
                    <span className={`px-2 py-0.5 rounded text-xs font-medium ${getPriorityColor(p.priority)}`}>
                      {p.priority}
                    </span>
                  </td>
                  <td className="py-2 px-3 text-gray-500">{p.automation_potential}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
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
