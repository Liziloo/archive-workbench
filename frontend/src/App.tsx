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
    <div className="min-h-screen bg-black text-white p-12 font-sans">
      <button
        onClick={() => setSelectedProject(null)}
        className="text-gray-500 hover:text-white mb-8 transition-colors"
      >
        ← Back to Projects
      </button>

      <header className="mb-12">
        <h1 className="text-4xl font-bold">{selectedProject.name}</h1>
        <p className="text-gray-400 mt-2">Project Dashboard</p>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        <div className="bg-gray-900 p-8 rounded-xl border border-gray-800">
          <h2 className="text-gray-500 text-xs font-bold uppercase tracking-widest mb-4">Total Items</h2>
          <p className="text-5xl font-mono text-green-400">{selectedProject.item_count}</p>
        </div>

        {/* Placeholder for future stats */}
        <div className="bg-gray-900 p-8 rounded-xl border border-gray-800 opacity-50">
          <h2 className="text-gray-500 text-xs font-bold uppercase tracking-widest mb-4">Unverified Evidence</h2>
          <p className="text-5xl font-mono text-yellow-600">--</p>
        </div>
      </div>
    </div>
  );
}

export default App;