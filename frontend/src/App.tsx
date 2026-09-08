import { useEffect, useState } from 'react'

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
