import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { api } from '../services/api';

export default function ProcessList() {
  const [processes, setProcesses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [functionFilter, setFunctionFilter] = useState('');
  const [sortField, setSortField] = useState('name');
  const [sortDir, setSortDir] = useState('asc');

  useEffect(() => {
    api.getProcesses()
      .then(setProcesses)
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  const functions = [...new Set(processes.map(p => p.business_function))].sort();

  const filtered = processes
    .filter(p => !search || p.name.toLowerCase().includes(search.toLowerCase()) || p.description.toLowerCase().includes(search.toLowerCase()))
    .filter(p => !functionFilter || p.business_function === functionFilter)
    .sort((a, b) => {
      const mul = sortDir === 'asc' ? 1 : -1;
      return a[sortField] > b[sortField] ? mul : -mul;
    });

  const toggleSort = (field) => {
    if (sortField === field) setSortDir(d => d === 'asc' ? 'desc' : 'asc');
    else { setSortField(field); setSortDir('asc'); }
  };

  if (loading) return <div className="text-center py-12 text-gray-500">Loading processes...</div>;

  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-bold text-gray-800">Business Processes</h1>
      <p className="text-gray-500 text-sm">{filtered.length} processes</p>

      <div className="flex gap-4 flex-wrap">
        <input
          type="text"
          placeholder="Search processes..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="border rounded px-3 py-2 text-sm flex-1 min-w-[200px]"
        />
        <select
          value={functionFilter}
          onChange={(e) => setFunctionFilter(e.target.value)}
          className="border rounded px-3 py-2 text-sm"
        >
          <option value="">All Functions</option>
          {functions.map(f => <option key={f} value={f}>{f}</option>)}
        </select>
      </div>

      <div className="bg-white rounded-lg shadow overflow-hidden">
        <table className="w-full text-sm">
          <thead>
            <tr className="bg-slate-50 border-b text-left">
              <th className="py-3 px-3 cursor-pointer hover:text-nova-600" onClick={() => toggleSort('name')}>
                Name {sortField === 'name' ? (sortDir === 'asc' ? '↑' : '↓') : ''}
              </th>
              <th className="py-3 px-3 cursor-pointer hover:text-nova-600" onClick={() => toggleSort('business_function')}>
                Function {sortField === 'business_function' ? (sortDir === 'asc' ? '↑' : '↓') : ''}
              </th>
              <th className="py-3 px-3">Status</th>
              <th className="py-3 px-3">Actions</th>
            </tr>
          </thead>
          <tbody>
            {filtered.map(p => (
              <tr key={p.id} className="border-b hover:bg-slate-50">
                <td className="py-2 px-3">
                  <Link to={`/processes/${p.id}`} className="text-nova-600 hover:underline font-medium">{p.name}</Link>
                </td>
                <td className="py-2 px-3 text-gray-500">{p.business_function}</td>
                <td className="py-2 px-3">
                  <span className={`px-2 py-0.5 rounded text-xs ${p.status === 'seeded' ? 'bg-slate-100 text-slate-600' : 'bg-green-100 text-green-700'}`}>
                    {p.status}
                  </span>
                </td>
                <td className="py-2 px-3">
                  <Link to={`/processes/${p.id}`} className="text-nova-600 text-xs hover:underline">View</Link>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        {filtered.length === 0 && (
          <p className="text-center py-8 text-gray-400">No processes match your search.</p>
        )}
      </div>
    </div>
  );
}
