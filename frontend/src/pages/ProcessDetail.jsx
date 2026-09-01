import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { api } from '../services/api';

export default function ProcessDetail() {
  const { id } = useParams();
  const [process, setProcess] = useState(null);
  const [analysis, setAnalysis] = useState(null);
  const [score, setScore] = useState(null);
  const [evidence, setEvidence] = useState(null);
  const [loading, setLoading] = useState(true);
  const [analyzing, setAnalyzing] = useState(false);

  useEffect(() => {
    setLoading(true);
    Promise.all([api.getProcess(id), api.getAnalysis(id)])
      .then(([p, a]) => {
        setProcess(p);
        if (a.length > 0) {
          setAnalysis(a[0]);
          if (a[0].score) setScore(a[0].score);
        }
      })
      .catch(console.error)
      .finally(() => setLoading(false));

    api.getEvidence(id).then(setEvidence).catch(() => {});
  }, [id]);

  const handleAnalyze = async () => {
    setAnalyzing(true);
    try {
      await api.analyzeProcess(id);
      const [a, e] = await Promise.all([api.getAnalysis(id), api.getEvidence(id)]);
      if (a.length > 0) {
        setAnalysis(a[0]);
        if (a[0].score) setScore(a[0].score);
      }
      setEvidence(e);
    } catch (err) {
      alert('Analysis failed: ' + err.message);
    } finally {
      setAnalyzing(false);
    }
  };

  if (loading) return <div className="text-center py-12 text-gray-500">Loading...</div>;
  if (!process) return <div className="text-center py-12 text-red-500">Process not found</div>;

  return (
    <div className="space-y-6 max-w-5xl">
      <div className="flex justify-between items-start">
        <div>
          <h1 className="text-2xl font-bold text-gray-800">{process.name}</h1>
          <p className="text-gray-500 text-sm mt-1">{process.business_function} | ID: {process.id}</p>
        </div>
        <button
          onClick={handleAnalyze}
          disabled={analyzing}
          className="bg-nova-600 text-white px-4 py-2 rounded text-sm hover:bg-nova-700 disabled:opacity-50"
        >
          {analyzing ? 'Analyzing...' : analysis ? 'Re-analyze' : 'Analyze Process'}
        </button>
      </div>

      <div className="bg-white rounded-lg p-5 shadow">
        <h3 className="font-semibold text-gray-700 mb-2">Description</h3>
        <p className="text-gray-600 text-sm">{process.description}</p>
      </div>

      {process.activities?.length > 0 && (
        <div className="bg-white rounded-lg p-5 shadow">
          <h3 className="font-semibold text-gray-700 mb-2">Activities</h3>
          <ol className="list-decimal list-inside text-sm text-gray-600 space-y-1">
            {process.activities.map((a, i) => <li key={i}>{a.name}</li>)}
          </ol>
        </div>
      )}

      {analysis ? (
        <>
          <div className="bg-white rounded-lg p-5 shadow">
            <h3 className="font-semibold text-gray-700 mb-3">Business Purpose</h3>
            <p className="text-gray-600 text-sm">{analysis.business_purpose}</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <InfoCard title="Key Activities" items={analysis.key_activities} color="blue" />
            <InfoCard title="Current Challenges" items={analysis.current_challenges} color="red" />
            <InfoCard title="AI Opportunities" items={analysis.ai_opportunities} color="green" />
            <InfoCard title="Technologies" items={analysis.technologies} color="purple" />
            <InfoCard title="Business Benefits" items={analysis.business_benefits} color="emerald" />
            <InfoCard title="Risks" items={analysis.risks} color="amber" />
            <InfoCard title="Human Involvement" items={analysis.human_involvement} color="slate" />
          </div>

          {score && (
            <div className="bg-white rounded-lg p-5 shadow">
              <h3 className="font-semibold text-gray-700 mb-3">AI Opportunity Score: {score.total_score} / 100</h3>
              <div className="flex items-center gap-3 mb-4">
                <span className={`px-3 py-1 rounded-full text-sm font-semibold ${getPriorityColor(score.priority)}`}>
                  {score.priority} Priority
                </span>
                <span className="text-sm text-gray-500">Automation Potential: {analysis.automation_potential}</span>
              </div>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                <ScoreDim label="Automation" value={score.automation_potential} />
                <ScoreDim label="Business Benefit" value={score.business_benefit} />
                <ScoreDim label="Data Availability" value={score.data_availability} />
                <ScoreDim label="AI Feasibility" value={score.ai_feasibility} />
                <ScoreDim label="Process Repetition" value={score.process_repetition} />
                <ScoreDim label="Risk Factor" value={score.risk_factor} neg />
                <ScoreDim label="Regulatory" value={score.regulatory_sensitivity} neg />
              </div>
              <div className="mt-4 p-3 bg-slate-50 rounded text-xs text-gray-600 font-mono">
                <strong>Formula:</strong> {score.scoring_formula}
              </div>
            </div>
          )}

          <div className="bg-white rounded-lg p-5 shadow">
            <h3 className="font-semibold text-gray-700 mb-2">AI Reasoning</h3>
            <p className="text-gray-600 text-sm whitespace-pre-wrap">{analysis.reasoning}</p>
            <p className="text-xs text-gray-400 mt-2">Confidence: {(analysis.confidence * 100).toFixed(0)}%</p>
          </div>
        </>
      ) : (
        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-5 text-center">
          <p className="text-yellow-700">No analysis yet. Click "Analyze Process" to generate AI intelligence.</p>
        </div>
      )}

      {evidence && evidence.evidence?.length > 0 && (
        <div className="bg-white rounded-lg p-5 shadow">
          <h3 className="font-semibold text-gray-700 mb-3">Research Evidence ({evidence.total_sources} sources)</h3>
          <div className="space-y-3">
            {evidence.evidence.map((e, i) => (
              <div key={i} className="border-l-4 border-nova-400 pl-3">
                <p className="text-sm font-medium text-gray-700">{e.title}</p>
                <p className="text-xs text-gray-500">{e.publisher} | {e.source_type}</p>
                <p className="text-xs text-gray-600 mt-1">{e.finding_summary}</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

function InfoCard({ title, items, color }) {
  const colorMap = { blue: 'bg-blue-50 border-blue-200', red: 'bg-red-50 border-red-200', green: 'bg-green-50 border-green-200', purple: 'bg-purple-50 border-purple-200', emerald: 'bg-emerald-50 border-emerald-200', amber: 'bg-amber-50 border-amber-200', slate: 'bg-slate-50 border-slate-200' };
  return (
    <div className={`rounded-lg p-4 border ${colorMap[color]}`}>
      <h4 className="font-semibold text-sm text-gray-700 mb-2">{title}</h4>
      <ul className="text-xs text-gray-600 space-y-1">
        {(items || []).map((item, i) => <li key={i} className="flex gap-1"><span className="text-gray-400">•</span>{item}</li>)}
      </ul>
    </div>
  );
}

function ScoreDim({ label, value, neg }) {
  const pct = (value / 10) * 100;
  const barColor = neg
    ? (value >= 7 ? 'bg-red-500' : value >= 4 ? 'bg-yellow-500' : 'bg-green-500')
    : (value >= 7 ? 'bg-green-500' : value >= 4 ? 'bg-yellow-500' : 'bg-red-500');
  return (
    <div>
      <div className="flex justify-between text-xs mb-1">
        <span className="text-gray-600">{label}</span>
        <span className="font-medium">{value}/10</span>
      </div>
      <div className="h-2 bg-gray-200 rounded-full overflow-hidden">
        <div className={`h-full ${barColor} rounded-full`} style={{ width: `${pct}%` }} />
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
