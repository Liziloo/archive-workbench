import { useEffect, useState } from 'react'

interface SystemStatus {
  project: string;
  database: string;
  redis: string;
  gpu: { active: boolean; device: string; vram: string };
}

function App() {
  const [status, setStatus] = useState<SystemStatus | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetch("http://localhost:8000/api/v1/system/status")
      .then(res => {
        if (!res.ok) throw new Error("Backend is not responding");
        return res.json();
      })
      .then(data => setStatus(data))
      .catch(err => setError(err.message));
  }, []);

  if (error) return <div className="p-10 text-red-500 font-bold">Error: {error}</div>;
  if (!status) return <div className="p-10 text-white">Connecting to GPU-Monster...</div>;

  return (
    <div className="min-h-screen bg-black text-gray-100 p-8 font-sans">
      <header className="mb-12">
        <h1 className="text-4xl font-extrabold tracking-tight text-white">
          {status.project} <span className="text-purple-500">Workbench</span>
        </h1>
        <p className="text-gray-400 mt-2">Infrastructure Control Panel</p>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        <StatusCard title="Database (OMV)" value={status.database} color="text-green-400" />
        <StatusCard title="Redis (OMV)" value={status.redis} color={status.redis === 'Online' ? 'text-green-400' : 'text-red-400'} />
        <div className="bg-gray-900 p-6 rounded-xl border border-gray-800 shadow-2xl">
          <h2 className="text-xs font-bold text-gray-500 uppercase tracking-widest mb-4">GPU Acceleration (Local)</h2>
          <p className="text-xl font-mono text-purple-400">{status.gpu.device}</p>
          <p className="text-sm text-gray-500 mt-1">{status.gpu.vram} VRAM Available</p>
        </div>
      </div>
    </div>
  )
}

function StatusCard({ title, value, color }: { title: string, value: string, color: string }) {
  return (
    <div className="bg-gray-900 p-6 rounded-xl border border-gray-800 shadow-2xl">
      <h2 className="text-xs font-bold text-gray-500 uppercase tracking-widest mb-4">{title}</h2>
      <p className={`text-3xl font-mono ${color}`}>{value}</p>
    </div>
  )
}

export default App