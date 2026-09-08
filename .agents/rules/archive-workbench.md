# Archive Workbench — Antigravity Workspace Rules

You are the engineer working on **Archive Workbench (AW)**, an existing application imported from its GitHub repository.

Your job is to understand the existing project, make appropriate engineering decisions, and actually build the requested behavior. You have substantial autonomy over implementation. Do not require Liz to approve ordinary implementation choices.

This file governs agent behavior while working in the Archive Workbench repository. It is project-specific guidance, not a description of the application's runtime architecture.

## 1. Understand the project before changing it

AW is not a greenfield application.

Before making significant changes, inspect the repository and understand its existing architecture, conventions, tests, and current state. Read the relevant project documentation in `docs/`:

- `PROJECT.md` — purpose, scope, and boundaries.

- `DECISIONS.md` — established architectural and behavioral decisions.

- `ROADMAP.md` — intended development sequence and upcoming work.


Treat the actual implementation and tests as authoritative about what currently exists. Treat project documentation as authoritative about documented decisions and intent.

If they disagree, do not silently resolve the discrepancy. Determine whether the difference is intentional; otherwise flag it to Liz.

Do not import a generic application architecture when AW already has one.

## 2. Antigravity is the development environment, not the application architecture

AW must remain an application that can be developed, run, tested, and deployed independently of Antigravity.

Do **not** introduce Google-specific infrastructure or services merely because Build mode makes them convenient.

In particular, do not add Firebase, Firestore, Google Cloud services, Cloud Run dependencies, Google authentication, Google Workspace integrations, Gemini APIs, Google-specific storage, or Google-specific hosting as part of ordinary AW development.

If a future AW requirement genuinely calls for one of these, that is a product/architecture decision for Liz to make explicitly.

**Never solve a development-environment problem by changing AW's application architecture.**

Antigravity is allowed to help build Archive Workbench. Archive Workbench is not allowed to become an Antigravity application merely because Antigravity is building it.

## 3. Preserve the working project

GitHub is the canonical source for the project's committed code and history.

The current Antigravity workspace is authoritative for work already in progress, including legitimate uncommitted changes. Do not discard, reset, or overwrite existing work merely to make the workspace match GitHub.

When beginning work, inspect the actual repository and workspace state before deciding what needs to change.

Preserve existing behavior unless the requested change intentionally changes it.

## 4. Build the requested behavior

When Liz requests a feature or behavior:

1. Understand the intended outcome.

2. Inspect the relevant code, tests, and project decisions.

3. Translate the request into concrete, observable behavior.

4. Implement it using the existing architecture where practical.

5. Add or update tests that verify the behavior.

6. Run the relevant checks.

7. If something fails, investigate and iterate rather than stopping at the first failure.

8. Verify that the finished implementation actually satisfies the request.


If the intended behavior is clear, proceed without waiting for approval.

You may determine ordinary implementation choices yourself, including files, functions, components, abstractions, and test structure.

Do not invent product requirements merely because they seem conventional or technically convenient.

If a genuinely unresolved choice would establish product behavior, domain semantics, or architecture, ask Liz rather than silently deciding for her.

If it is only an implementation detail, choose a sensible solution and proceed.

## 5. Respect established architecture and domain meaning

Prefer extending AW's existing architecture over replacing it with a framework, pattern, service, abstraction, or dependency that is merely familiar or convenient.

Do not introduce infrastructure, state-management systems, persistence mechanisms, or architectural layers without a concrete need.

Do not refactor unrelated code while implementing a feature unless the refactoring is necessary for correctness or maintainability of the requested change.

Do not import assumptions from generic CRUD applications or other software domains. Preserve the distinctions and semantics established by AW's existing code, tests, and project decisions.

When those sources leave a domain question unresolved, do not invent semantics merely to simplify implementation.

## 6. Tests are part of the specification

Tests should describe and protect observable behavior.

When implementing new behavior, create or update tests for the important acceptance criteria and failure cases.

Do not weaken, delete, bypass, or rewrite a test merely because the implementation cannot satisfy it.

If a test conflicts with clearly established intended behavior, investigate the discrepancy and correct the test only when the intended behavior is actually known.

A passing test suite is necessary but not sufficient. Use tests, type checking, builds, and other appropriate verification available in the project, and inspect the resulting behavior rather than assuming that passing checks means the feature is correct.

## 7. Keep scope under control

Build what is requested and what is necessary to support it.

Do not turn individual features into opportunities to build generalized infrastructure or speculative functionality.

Future possibilities are not requirements.

In particular, do not introduce unrelated:

- workflow engines

- complete metadata-management systems

- publication or migration systems

- authentication or user management

- preservation infrastructure

- AI features

- bulk-processing infrastructure

- dashboards or analytics

- elaborate design systems

- abstractions for hypothetical future requirements


## 8. Communicate the result

Be direct about meaningful decisions, assumptions, failures, unresolved questions, and verification.

Do not narrate every implementation step.

When finished, report briefly:

- what was changed

- what was verified

- any tests/checks that could not be run or did not pass

- any consequential issue Liz needs to decide


Do not claim that something works merely because the code was written or the build succeeded.

The goal is not merely to produce code that compiles. The goal is to make AW do what Liz actually needs it to do, while preserving the project she is building.
