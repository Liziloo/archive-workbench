interface ArchivalObjectSummary {
  id: string
  representation_count: number
}

interface ObjectListProps {
  objects: ArchivalObjectSummary[]
  onSelect: (id: string) => void
}

function ObjectList({ objects, onSelect }: ObjectListProps) {
  return (
    <section>
      <h2>Archival Objects</h2>
      <ul data-testid="object-list">
        {objects.map((obj) => (
          <li
            key={obj.id}
            data-testid={`object-item-${obj.id}`}
            onClick={() => onSelect(obj.id)}
            style={{ cursor: 'pointer', paddingLeft: '0.5rem' }}
          >
            <strong>{obj.id}</strong>
            {' ('}
            {obj.representation_count}
            {' representations)'}
          </li>
        ))}
      </ul>
    </section>
  )
}

export default ObjectList
