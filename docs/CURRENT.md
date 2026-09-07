# Archive Workbench — Current

## Current Slice

**A minimal usable interface for working with an archival object and its digital representations.**

The previous slice established the underlying behavior for representing one physical archival object with multiple digital representations, including:

- multiple representations per archival object
- content identity and duplicate detection
- explicit confirmation for adding duplicates
- integrity status
- detection of modified or missing representations
- searching for matching files
- human verification and reassociation
- optional explicit ordering of representations

That slice is complete.

The current slice moves from domain behavior to actual use: an archivist must be able to interact with this functionality through a minimal user interface rather than only through Python code and tests.

## Goal

Create the smallest end-to-end interface that allows an archivist to work with an archival object and its digital representations.

The interface does not need to be attractive, polished, or feature-complete.

It needs to make the established representation behavior usable.

This slice establishes the first usable interface to the existing domain behavior.

## Behavioral Scope

The intended behavioral scope of this slice is:

- create or open an archival object
- see the object's digital representations
- add a digital representation
- receive the existing duplicate warning/confirmation behavior
- see representation integrity status
- see which representations need attention
- use the existing recovery behavior when a representation needs attention

The interface should expose existing behavior rather than introduce new archival behavior.

## Principles

- The interface is a means of exercising existing archival behavior, not a reason to redesign that behavior.
- Prefer the smallest usable interface over premature visual or architectural polish.
- Preserve the distinction between the physical archival object and its digital representations.
- Do not invent archival interpretation or metadata requirements merely because a UI needs fields.
- Do not silently perform consequential actions.
- Existing human-confirmation requirements remain human-confirmation requirements in the UI.
- If a computer can perform an established routine operation reliably and safely, the interface should not require unnecessary manual repetition.
- Do not add functionality merely because it would eventually be useful.

## Explicitly Out of Scope

This slice does **not** include:

- final UI/UX design
- visual polish or branding
- complete archival metadata
- Dublin Core or Omeka S integration
- publication workflows
- authentication or multi-user support
- preservation-system design
- database/schema redesign unless required by an established behavior
- AI integration
- bulk processing
- dashboards
- advanced search
- migration of existing data
- generalized workflow/state-machine design

## Success Criteria

This slice is complete when an archivist can use the minimal interface to exercise the core representation workflow established by the previous slice without needing to interact directly with Python code.

The interface may be crude.

It must be real.