const API_BASE = import.meta.env.VITE_API_URL || '';

async function fetchJson(url, options = {}) {
  const baseUrl = API_BASE || '';
  const response = await fetch(`${baseUrl}${url}`, {
    headers: { 'Content-Type': 'application/json', ...options.headers },
    ...options,
  });
  if (!response.ok) {
    const err = await response.json().catch(() => ({ detail: response.statusText }));
    throw new Error(err.detail || 'API request failed');
  }
  return response.json();
}

export const api = {
  getProcesses: (function_) => fetchJson(`/api/processes${function_ ? `?business_function=${encodeURIComponent(function_)}` : ''}`),
  getProcess: (id) => fetchJson(`/api/processes/${id}`),
  createProcess: (data) => fetchJson('/api/processes', { method: 'POST', body: JSON.stringify(data) }),
  analyzeProcess: (id) => fetchJson(`/api/processes/${id}/analyze`, { method: 'POST' }),
  getAnalysis: (id) => fetchJson(`/api/processes/${id}/analysis`),
  getEvidence: (id) => fetchJson(`/api/processes/${id}/evidence`),
  getTopProcesses: (limit = 10) => fetchJson(`/api/processes/top?limit=${limit}`),
  getHumanLed: () => fetchJson('/api/processes/human-led'),
  getStats: () => fetchJson('/api/processes/stats'),
  analyzeNew: (data) => fetchJson('/api/processes/analyze-new', { method: 'POST', body: JSON.stringify(data) }),
  query: (question) => fetchJson('/api/query', { method: 'POST', body: JSON.stringify({ question }) }),
};
