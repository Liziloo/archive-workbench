/// <reference types="vitest/globals" />
import { render, screen } from '@testing-library/react'
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

describe('Archival Object view', () => {
  afterEach(() => {
    vi.restoreAllMocks()
  })

  it('opens an existing archival object and displays its identity', async () => {
    vi.spyOn(globalThis, 'fetch').mockResolvedValue(
      new Response(JSON.stringify(archivalObject), {
        status: 200,
        headers: { 'Content-Type': 'application/json' },
      }),
    )

    render(<App />)

    expect(
      await screen.findByRole('heading', { name: /example-object/i }),
    ).toBeInTheDocument()
  })

  it('displays all digital representations', async () => {
    vi.spyOn(globalThis, 'fetch').mockResolvedValue(
      new Response(JSON.stringify(archivalObject), {
        status: 200,
        headers: { 'Content-Type': 'application/json' },
      }),
    )

    render(<App />)

    expect(await screen.findByText('letter-front.tif')).toBeInTheDocument()
    expect(screen.getByText('letter-back.tif')).toBeInTheDocument()
  })

  it('displays the integrity status of each representation', async () => {
    vi.spyOn(globalThis, 'fetch').mockResolvedValue(
      new Response(JSON.stringify(archivalObject), {
        status: 200,
        headers: { 'Content-Type': 'application/json' },
      }),
    )

    render(<App />)

    await screen.findByText('letter-front.tif')

    expect(screen.getByText('intact')).toBeInTheDocument()
    expect(screen.getByText('modified')).toBeInTheDocument()
  })

  it('displays a loading state while the object is being retrieved', () => {
    vi.spyOn(globalThis, 'fetch').mockReturnValue(new Promise(() => {}))

    render(<App />)

    expect(screen.getByText(/loading/i)).toBeInTheDocument()
  })

  it('displays an error when the object cannot be retrieved', async () => {
    vi.spyOn(globalThis, 'fetch').mockResolvedValue(
      new Response(null, {
        status: 500,
      }),
    )

    render(<App />)

    expect(
      await screen.findByText(/unable to load archival object/i),
    ).toBeInTheDocument()
  })
})