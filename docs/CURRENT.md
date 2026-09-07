# Current Development State

Archive Workbench is transitioning from tested backend domain behavior to its first usable graphical interface.

## Current Slice: Frontend Scaffolding

The backend currently contains the tested domain behavior for working with archival objects and their digital representations. The next step is to establish the GUI infrastructure needed to exercise that behavior through an actual user interface.

The GUI will be a **React + TypeScript application using Vite**, communicating with the existing FastAPI backend.

This is an infrastructure/scaffolding step, not yet a user-facing behavioral slice.

### Immediate goals

* Create the `frontend/` React + TypeScript + Vite application.
* Establish frontend development and test infrastructure.
* Establish the boundary between the React frontend and FastAPI backend.
* Make the frontend runnable alongside the backend.
* Establish the smallest appropriate application smoke test.
* Avoid introducing additional frameworks or architectural machinery until a real requirement calls for them.

### After scaffolding

Once the frontend infrastructure exists, development returns to the normal test-first workflow.

The first GUI behavioral slice should establish that an archivist can perform a meaningful operation through the GUI—for example, creating or opening an archival object—rather than merely testing that a GUI application exists.

## Architecture

```text
Archive Workbench
├── frontend/
│   └── React + TypeScript + Vite
│       └── graphical user interface
│
└── backend/
    └── FastAPI / Python
        ├── API
        ├── services
        └── domain behavior
```

The GUI should consume backend behavior through the API boundary rather than duplicating domain logic in the frontend.

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

The backend representation tests currently pass.

### Known unresolved behavior

The semantics of `ordered_representations` when an object contains a mixture of ordered and unordered representations have not yet been defined. No behavior should be invented for this case without an explicit requirement and test.

## Development Workflow

Continue using the established test-first workflow:

1. Define the intended behavior.
2. Write the test.
3. Have Aider implement the behavior.
4. Run the tests.
5. Inspect and refactor.
6. Repeat.

For the frontend transition, the GUI framework and test infrastructure may be established before the first user-facing GUI acceptance test. This scaffolding does not itself constitute a product behavior.

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

## Success Condition

The scaffolding work is complete when the React/TypeScript frontend can be developed and tested as part of Archive Workbench and can communicate with the existing FastAPI application.

The next success condition is a tested, usable GUI behavior—not merely proof that the frontend exists.
