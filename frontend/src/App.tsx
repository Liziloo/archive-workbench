import { useEffect, useState } from 'react'

interface Project {
  id: string;
  name: string;
  description: string;
}

interface ProjectStats {
  name: string;
  item_count: number;
}

function App() {
  const [projects, setProjects] = useState<Project[]>([]);
  const [selectedProject, setSelectedProject] = useState<ProjectStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [view, setView] = useState<'dashboard' | 'matches'>('dashboard');
  const [pendingMatches, setPendingMatches] = useState<any[]>([]);

  // Fetch pending matches if in match view
  useEffect(() => {
    if (view === 'matches') {
      fetch("http://localhost:8000/api/v1/matches/pending")
        .then(res => res.json())
        .then(data => setPendingMatches(data));
    }
  }, [view]);

  const handleMatch = (id: string, action: 'confirm' | 'reject') => {
    fetch(`http://localhost:8000/api/v1/matches/${id}/${action}`, { method: 'POST' })
      .then(() => setPendingMatches(prev => prev.filter(m => m.id !== id)));
  };

  useEffect(() => {
    fetch("http://localhost:8000/api/v1/projects/")
      .then(res => res.json())
      .then(data => {
        setProjects(data);
        setLoading(false);
      });
  }, []);

  const selectProject = (id: string) => {
    fetch(`http://localhost:8000/api/v1/projects/${id}/stats`)
      .then(res => res.json())
      .then(data => setSelectedProject(data));
  };

  if (loading) return <div className="bg-black min-h-screen text-white p-10 font-mono">Initializing Workbench...</div>;

  if (!selectedProject) {
    return (
      <div className="min-h-screen bg-black text-white p-12 font-sans">
        <h1 className="text-4xl font-bold mb-4">Archive <span className="text-purple-500">Workbench</span></h1>
        <p className="text-gray-400 mb-12 text-lg">Select a project to begin curation.</p>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 max-w-4xl">
          {projects.map(p => (
            <button
              key={p.id}
              onClick={() => selectProject(p.id)}
              className="bg-gray-900 border border-gray-800 p-8 text-left rounded-xl hover:border-purple-500 transition-all group"
            >
              <h2 className="text-2xl font-bold group-hover:text-purple-400 transition-colors">{p.name}</h2>
              <p className="text-gray-500 mt-2">{p.description}</p>
              <div className="mt-6 text-xs font-mono text-purple-600 uppercase tracking-widest">Open Project →</div>
            </button>
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-black text-white p-8">
      <nav className="flex gap-8 mb-12 border-b border-gray-800 pb-4">
        <button onClick={() => setView('dashboard')} className={`text-sm font-bold uppercase tracking-widest ${view === 'dashboard' ? 'text-purple-500' : 'text-gray-500'}`}>Dashboard</button>
        <button onClick={() => setView('matches')} className={`text-sm font-bold uppercase tracking-widest ${view === 'matches' ? 'text-purple-500' : 'text-gray-500'}`}>Match Review ({pendingMatches.length})</button>
      </nav>

      {view === 'dashboard' ? (
        <div>
          <h1 className="text-4xl font-bold mb-2">{selectedProject.name}</h1>
          <p className="text-green-400 font-mono">Items: {selectedProject.item_count}</p>
        </div>
      ) : (
        <div className="space-y-12">
          {pendingMatches.map(m => (
            <div key={m.id} className="bg-gray-900 rounded-xl overflow-hidden border border-gray-800">
              <div className="bg-gray-800 p-4 flex justify-between items-center">
                <span className="text-purple-400 font-bold">{m.score}% Visual Match</span>
                <div className="flex gap-4">
                  <button onClick={() => handleMatch(m.id, 'reject')} className="px-4 py-2 bg-red-900/20 text-red-400 rounded hover:bg-red-900/40 transition-all">Reject</button>
                  <button onClick={() => handleMatch(m.id, 'confirm')} className="px-6 py-2 bg-purple-600 text-white rounded hover:bg-purple-500 transition-all">Confirm & Merge</button>
                </div>
              </div>
              <div className="grid grid-cols-2 gap-1 p-1 bg-black">
                <div className="relative">
                  <img src={`http://localhost:8000/api/v1/assets/${m.asset_a.sha256}/image`} className="w-full h-96 object-contain bg-gray-900" />
                  <div className="absolute bottom-2 left-2 bg-black/60 px-2 py-1 text-xs text-gray-300">Carl's Scan: {m.asset_a.filename}</div>
                </div>
                <div className="relative">
                  <img src={`http://localhost:8000/api/v1/assets/${m.asset_b.sha256}/image`} className="w-full h-96 object-contain bg-gray-900" />
                  <div className="absolute bottom-2 left-2 bg-black/60 px-2 py-1 text-xs text-gray-300">Your Scan: {m.asset_b.filename}</div>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default App;