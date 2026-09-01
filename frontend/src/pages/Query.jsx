import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { api } from '../services/api';

const EXAMPLE_QUESTIONS = [
  "What should we automate first?",
  "Which processes have the highest AI potential?",
  "Which processes should remain predominantly human-led?",
  "Why is fraud detection ranked highly?",
  "Show me the research supporting Process 7.",
  "What are the biggest AI risks across our processes?",
];

export default function Query() {
  const [question, setQuestion] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleQuery = async (q) => {
    const query = q || question;
    if (!query.trim()) return;
    setLoading(true);
    try {
      const res = await api.query(query);
      setResult(res);
    } catch (err) {
      setResult({ answer: 'Error: ' + err.message, processes: [], evidence: [] });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-4 max-w-4xl">
      <h1 className="text-2xl font-bold text-gray-800">Ask the Process Intelligence Engine</h1>
      <p className="text-gray-500 text-sm">Natural language queries over NovaBank's process intelligence data</p>

      <div className="flex gap-2">
        <input
          type="text"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleQuery()}
          placeholder="Ask a question about processes, AI opportunities, risks..."
          className="flex-1 border rounded px-4 py-2 text-sm"
        />
        <button
          onClick={() => handleQuery()}
          disabled={loading}
          className="bg-nova-600 text-white px-6 py-2 rounded text-sm hover:bg-nova-700 disabled:opacity-50"
        >
          {loading ? 'Thinking...' : 'Ask'}
        </button>
      </div>

      <div className="flex flex-wrap gap-2">
        {EXAMPLE_QUESTIONS.map((q, i) => (
          <button
            key={i}
            onClick={() => { setQuestion(q); handleQuery(q); }}
            className="text-xs bg-slate-100 hover:bg-slate-200 text-slate-700 px-3 py-1.5 rounded-full transition-colors"
          >
            {q}
          </button>
        ))}
      </div>

      {result && (
        <div className="bg-white rounded-lg p-5 shadow space-y-4">
          <div>
            <h3 className="font-semibold text-gray-700 mb-2">Answer</h3>
            <p className="text-gray-600 text-sm whitespace-pre-wrap">{result.answer}</p>
          </div>

          {result.processes?.length > 0 && (
            <div>
              <h4 className="font-semibold text-sm text-gray-700 mb-2">Referenced Processes</h4>
              <div className="space-y-1">
                {result.processes.map((p) => (
                  <Link
                    key={p.id}
                    to={`/processes/${p.id}`}
                    className="flex items-center gap-2 text-sm text-nova-600 hover:underline"
                  >
                    <span className="font-medium">{p.name}</span>
                    {p.ai_score && <span className="text-gray-400">Score: {p.ai_score}</span>}
                    {p.priority && <span className="text-gray-400">({p.priority})</span>}
                  </Link>
                ))}
              </div>
            </div>
          )}

          {result.evidence?.length > 0 && (
            <div>
              <h4 className="font-semibold text-sm text-gray-700 mb-2">Evidence Sources</h4>
              <ul className="text-xs text-gray-600 space-y-1">
                {result.evidence.map((e, i) => <li key={i}>• {e}</li>)}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
