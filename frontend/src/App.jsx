import React from 'react';
import { BrowserRouter, Routes, Route, NavLink } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import ProcessList from './pages/ProcessList';
import ProcessDetail from './pages/ProcessDetail';
import TopOpportunities from './pages/TopOpportunities';
import HumanLed from './pages/HumanLed';
import Query from './pages/Query';
import AddProcess from './pages/AddProcess';

const navItems = [
  { to: '/', label: 'Dashboard' },
  { to: '/processes', label: 'Processes' },
  { to: '/top-opportunities', label: 'Top 10' },
  { to: '/human-led', label: 'Human-Led' },
  { to: '/query', label: 'Ask AI' },
  { to: '/add-process', label: '+ Add Process' },
];

function Sidebar() {
  return (
    <aside className="w-64 bg-nova-900 text-white min-h-screen p-4">
      <div className="mb-8">
        <h1 className="text-xl font-bold">NovaBank</h1>
        <p className="text-nova-300 text-xs mt-1">AI Process Intelligence</p>
      </div>
      <nav className="space-y-1">
        {navItems.map((item) => (
          <NavLink
            key={item.to}
            to={item.to}
            end={item.to === '/'}
            className={({ isActive }) =>
              `block px-3 py-2 rounded text-sm transition-colors ${
                isActive ? 'bg-nova-700 text-white' : 'text-nova-200 hover:bg-nova-800'
              }`
            }
          >
            {item.label}
          </NavLink>
        ))}
      </nav>
    </aside>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <div className="flex min-h-screen bg-slate-100">
        <Sidebar />
        <main className="flex-1 p-6 overflow-auto">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/processes" element={<ProcessList />} />
            <Route path="/processes/:id" element={<ProcessDetail />} />
            <Route path="/top-opportunities" element={<TopOpportunities />} />
            <Route path="/human-led" element={<HumanLed />} />
            <Route path="/query" element={<Query />} />
            <Route path="/add-process" element={<AddProcess />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}
