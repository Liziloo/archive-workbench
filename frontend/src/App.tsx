import { useEffect, useState, useRef } from 'react'

interface Representation {
  path: string
  integrity_status: string
}

interface ArchivalObject {
  id: string
  representations: Representation[]
}

function App() {
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [object, setObject] = useState<ArchivalObject | null>(null)
  const fileInputRef = useRef<HTMLInputElement>(null)

  useEffect(() => {
    fetch('/api/archival-objects/example-object')
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
  }, [])

  const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    try {
      // Using the new upload endpoint
      const response = await fetch('/api/archival-objects/example-object/representations/upload', {
        method: 'POST',
        body: formData,
      });
      
      if (!response.ok) {
        throw new Error('Failed to upload file');
      }
      
      const data: ArchivalObject = await response.json();
      setObject(data);
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

  if (!object) {
    return null
  }

  return (
    <main>
      <h1>Archive Workbench</h1>
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
