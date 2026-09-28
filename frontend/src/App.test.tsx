/// <reference types="vitest/globals" />
import { render, screen, fireEvent } from '@testing-library/react'
import App from './App'

const archivalObject = {
  id: 'example-object',
  representations: [
    {
      path: 'letter-front.tif',
      integrity_status: 'intact',
    },
    {
      path: 'letter-back.tif',
      integrity_status: 'modified',
    },
  ],
}

const objectList = [
  { id: 'example-object', representation_count: 2 },
  { id: 'new-object-1', representation_count: 0 },
]

describe('App — archival object navigation', () => {
  afterEach(() => {
    vi.restoreAllMocks()
  })

  it('shows the object list when no object is selected', async () => {
    vi.spyOn(globalThis, 'fetch')
      .mockResolvedValueOnce(
        new Response(JSON.stringify(objectList), {
          status: 200,
          headers: { 'Content-Type': 'application/json' },
        }),
      )
      .mockResolvedValue(
        new Response(JSON.stringify(archivalObject), {
          status: 200,
          headers: { 'Content-Type': 'application/json' },
        }),
      )

    render(<App />)

    expect(await screen.findByText('example-object')).toBeInTheDocument()
    expect(screen.getByText('new-object-1')).toBeInTheDocument()
  })

  it('shows a loading state while the object list is being retrieved', async () => {
    vi.spyOn(globalThis, 'fetch').mockReturnValue(new Promise(() => {}))

    render(<App />)

    expect(screen.getByText(/loading/i)).toBeInTheDocument()
  })

  it('displays the selected object after clicking an item in the list', async () => {
    vi.spyOn(globalThis, 'fetch')
      .mockResolvedValueOnce(
        new Response(JSON.stringify(objectList), {
          status: 200,
          headers: { 'Content-Type': 'application/json' },
        }),
      )
      .mockResolvedValueOnce(
        new Response(JSON.stringify(archivalObject), {
          status: 200,
          headers: { 'Content-Type': 'application/json' },
        }),
      )

    render(<App />)

    // Object list should be visible with clickable items
    await screen.findByText('example-object')

    const listItem = screen.getByText('example-object')

    fireEvent.click(listItem)

    // After clicking, the detail view should appear (heading or representation)
    expect(
      await screen.findByRole('heading', { name: /example-object/i }),
    ).toBeInTheDocument()
  })

  it('displays representations after selecting an object', async () => {
    vi.spyOn(globalThis, 'fetch')
      .mockResolvedValueOnce(
        new Response(JSON.stringify(objectList), {
          status: 200,
          headers: { 'Content-Type': 'application/json' },
        }),
      )
      .mockResolvedValueOnce(
        new Response(JSON.stringify(archivalObject), {
          status: 200,
          headers: { 'Content-Type': 'application/json' },
        }),
      )

    render(<App />)

    await screen.findByText('example-object')

    const listItem = screen.getByText('example-object')
    fireEvent.click(listItem)

    expect(await screen.findByText('letter-front.tif')).toBeInTheDocument()
    expect(screen.getByText('letter-back.tif')).toBeInTheDocument()
  })

  it('shows all available archival objects in the list', async () => {
    vi.spyOn(globalThis, 'fetch')
      .mockResolvedValueOnce(
        new Response(JSON.stringify(objectList), {
          status: 200,
          headers: { 'Content-Type': 'application/json' },
        }),
      )
      .mockResolvedValue(
        new Response(JSON.stringify(archivalObject), {
          status: 200,
          headers: { 'Content-Type': 'application/json' },
        }),
      )

    render(<App />)

    expect(await screen.findByText('example-object')).toBeInTheDocument()
    expect(screen.getByText('new-object-1')).toBeInTheDocument()
  })

  it('displays an error when the object list cannot be retrieved', async () => {
    vi.spyOn(globalThis, 'fetch').mockResolvedValue(
      new Response(null, {
        status: 500,
      }),
    )

    render(<App />)

    expect(
      await screen.findByText(/unable to load archival objects/i),
    ).toBeInTheDocument()
  })
})
