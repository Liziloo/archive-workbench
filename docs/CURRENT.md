# Current Development State

Archive Workbench is transitioning from the completed backend representation work to its first usable graphical interface.

## Current Slice: First GUI Behavioral Slice

The React + TypeScript + Vite frontend and its testing infrastructure are established.

The frontend currently includes:

* React + TypeScript + Vite
* Vitest
* React Testing Library
* jsdom
* ESLint
* TypeScript checking
* Vite development and production builds
* a minimal application smoke test

The next slice is the first substantive GUI behavior, together with the API boundary required to support it.

### Immediate Goals

* Define the first meaningful archivist-facing GUI operation.
* Establish the smallest API surface required for that operation.
* Implement the operation through the GUI using the existing FastAPI backend.
* Keep archival domain behavior in the backend.

A likely starting point is creating or opening an archival object and displaying it in the GUI, but the exact behavior remains to be defined.

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

## Completed Frontend Infrastructure

The frontend can currently be developed and tested independently of product behavior.

The existing smoke test verifies that the application renders; it is infrastructure validation rather than a substantive product requirement.

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

## Current Success Condition

The frontend infrastructure is complete.

The next milestone is a tested, usable GUI behavior that exercises real Archive Workbench functionality through the FastAPI backend.
