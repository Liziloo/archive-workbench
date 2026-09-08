# Current Development State

Archive Workbench has completed its first substantive GUI behavioral slice and is beginning the next archivist-facing behavior.

## Completed Slice: Open an Archival Object

The GUI can:

* request an archival object from the FastAPI backend
* display the archival object's identity
* display all digital representations
* display the path/name of each representation
* display the integrity status of each representation
* display a loading state while the object is retrieved
* display an error state when retrieval fails

The behavior is tested at both the API and GUI boundaries.

The current implementation uses an in-memory backend fixture. Persistence and broader object-management behavior have not yet been introduced.

## Developer Environment

The frontend and backend can be developed together with a single command.

The development environment provides:

* Vite development server with frontend HMR
* FastAPI/Uvicorn development server with Python reload
* Vite proxying of `/api` requests to FastAPI
* a root `npm run dev` command that starts both servers

The development environment is functioning end-to-end.

## Architecture

```text
Archive Workbench
├── frontend/
│   └── React + TypeScript + Vite
│       ├── graphical user interface
│       └── frontend tests
│
└── backend/
    └── FastAPI / Python
        ├── API
        ├── services
        └── domain behavior
```

The frontend consumes backend behavior through the API rather than duplicating domain logic.

## Completed Backend Capability

The backend currently supports:

* archival objects
* multiple digital representations of an archival object
* content identity and duplicate detection
* explicit confirmation of duplicate representations
* representation integrity checking
* detection of modified or missing representations
* searching for and recovering missing representations
* explicit reassociation of representations
* optional explicit representation ordering

The backend representation tests pass.

### Known Unresolved Behavior

The semantics of `ordered_representations` when an object contains a mixture of ordered and unordered representations have not been defined.

## Frontend Infrastructure

The frontend includes:

* React + TypeScript + Vite
* Vitest
* React Testing Library
* jsdom
* ESLint
* TypeScript checking
* Vite development and production builds
* frontend acceptance tests

The frontend acceptance tests pass.

## Current Test State

* Backend: 26 tests passing
* Frontend: 5 tests passing
* Frontend build: passing
* Frontend lint: passing

## Next Slice: Add a Digital Representation

The next behavior is to allow an archivist to add a digital representation to an existing archival object.

The slice should exercise the existing backend/domain representation behavior through the API and GUI rather than duplicating that behavior in the frontend.

The exact acceptance criteria for this slice are to be defined before implementation.

## Out of Scope for the Current Work

* polished visual design
* full metadata editing
* Dublin Core / Omeka S integration
* publication workflows
* authentication
* preservation infrastructure
* database redesign unless required by an actual capability
* AI features
* bulk processing
* dashboards
* generalized workflow/state-machine architecture
* advanced search
* migration work
* premature frontend state-management or component frameworks
* desktop wrappers such as Tauri or Electron unless a demonstrated requirement warrants one

## Development Approach

New product behavior is developed test-first:

1. define the behavioral acceptance criteria
2. write the acceptance tests
3. implement the smallest behavior required to satisfy them
4. verify the complete behavior end-to-end

Developer ergonomics and other non-product scaffolding may be implemented directly when they do not change product behavior.

No additional architecture or framework should be introduced unless required by an actual capability.
