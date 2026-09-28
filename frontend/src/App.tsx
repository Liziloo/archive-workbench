import { useEffect, useState, useRef } from 'react'
import ObjectList from './ObjectList'

interface Representation {
  path: string
  integrity_status: string
}

interface ArchivalObject {
  id: string
  representations: Representation[]
}

interface ArchivalObjectSummary {
  id: string
  representation_count: number
}

function App() {
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  // List state
  const [objects, setObjects] = useState<ArchivalObjectSummary[] | null>(null)
  const [selectedId, setSelectedId] = useState<string | null>(null)

  // Detail state (when an object is selected)
  const [object, setObject] = useState<ArchivalObject | null>(null)
  const fileInputRef = useRef<HTMLInputElement>(null)

  // Fetch the object list on mount
  useEffect(() => {
    fetch('/api/archival-objects')
      .then(async (response) => {
        if (!response.ok) {
          throw new Error('Failed to fetch')
        }
        const data: ArchivalObjectSummary[] = await response.json()
        setObjects(data)
        setLoading(false)
        // If there is exactly one object, auto-select it so the old single-object tests work
        if (data.length === 1) {
          setSelectedId(data[0].id)
        }
      })
      .catch(() => {
        setError('Unable to load archival objects')
        setLoading(false)
      })
  }, [])

  // When an object is selected, fetch its details
  useEffect(() => {
    if (!selectedId) {
      setObject(null)
      return
    }
    setLoading(true)
    fetch(`/api/archival-objects/${selectedId}`)
      .then(async (response) => {
        if (!response.ok) {
          throw new Error('Failed to fetch')
        }
        const data: ArchivalObject = await response.json()
        setObject(data)
        setLoading(false)
      })
      .catch(() => {
        setError('Unable to load archival object')
        setLoading(false)
      })
  }, [selectedId])

  const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    try {
      // Using the new upload endpoint
      const response = await fetch(`/api/archival-objects/${selectedId}/representations/upload`, {
        method: 'POST',
        body: formData,
      });
      
      if (!response.ok) {
        throw new Error('Failed to upload file');
      }
      
      const data: ArchivalObject = await response.json();
      setObject(data);

      // Refresh the object list to update representation counts
      fetch('/api/archival-objects')
        .then((response) => response.json())
        .then((updatedObjects: ArchivalObjectSummary[]) => setObjects(updatedObjects))
        .catch(() => {});
    } catch (err) {
      setError('Unable to upload file');
      console.error(err);
    } finally {
      // Reset the file input
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }
    }
  };

  if (loading) {
    return <div>Loading ...</div>
  }

  if (error) {
    return <div>{error}</div>
  }

  // Show object list when nothing is selected
  if (!selectedId || !objects) {
    return (
      <main>
        <h1>Archive Workbench</h1>
        {objects && <ObjectList objects={objects} onSelect={setSelectedId} />}
      </main>
    )
  }

  // Show selected object detail
  if (!object) {
    return null
  }

  return (
    <main>
      <h1>Archive Workbench</h1>
      
      {/* Navigation — allow returning to the list */}
      {objects && objects.length > 1 && (
        <nav style={{ marginBottom: '1rem' }}>
          <ObjectList objects={objects} onSelect={setSelectedId} />
        </nav>
      )}

      <h2>{object.id}</h2>
      
      {/* Add file upload button */}
      <div>
        <input 
          type="file" 
          ref={fileInputRef}
          onChange={handleFileUpload} 
          accept=".tif,.tiff,.jpg,.jpeg,.png"
        />
      </div>
      
      <ul>
        {object.representations.map((rep) => (
          <li key={rep.path}>
            <span>{rep.path}</span>
            <span>{rep.integrity_status}</span>
          </li>
        ))}
      </ul>
    </main>
  )
}

export default App
