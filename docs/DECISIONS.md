# Archive Workbench — Decisions

This document records durable decisions about Archive Workbench. It is not a design diary or a list of possible approaches. Provisional ideas belong in `CURRENT.md`; implementation details belong in the code unless they rise to the level of a durable project decision.

## 1. AW is a workbench, not the publication system

Archive Workbench prepares and processes archival material for publication. Omeka S remains the system responsible for the published collection, including its published resources and relationships.

**Consequence:** AW should integrate with Omeka S rather than attempting to replace or duplicate its publication model.

## 2. The archival object is distinct from its representations

A physical archival object, its digital representations, derivatives of those representations, and information about them are distinct things.

A representation does not replace the object it represents, and one representation does not replace another merely because it is newer, higher quality, or more convenient.

**Consequence:** AW must preserve these distinctions throughout processing and publication.

## 3. Archival evidence must not be silently destroyed or overwritten

AW must not silently discard, overwrite, or obscure archival evidence. Changes with consequential effects must be reversible.

This applies regardless of whether the proposed action originates with a human, deterministic automation, a heuristic, or AI.

**Consequence:** The safe path should be the normal path, and processing mistakes should be recoverable.

## 4. Reliable, low-risk work should be automated

If a computer can perform a task reliably without creating danger to the archive or its eventual publication, AW should perform that task rather than requiring the human archivist to do it manually.

This includes routine, repetitive, administrative, and data-management work wherever reliable automation is possible.

**Consequence:** Human attention should be reserved for work that actually requires human judgment.

## 5. AI is advisory and collaborative

AI may be used when it can meaningfully improve archival processing, but AI-assisted work is collaborative rather than autonomous.

AI may propose information, interpretations, relationships, classifications, or other actions. A human remains responsible for evaluating and approving consequential interpretive decisions.

**Consequence:** AI errors should result in incorrect proposals requiring correction, not irreversible changes to the archive.

## 6. Historical interpretation and consequential archival actions require human approval

Questions of historical interpretation, and actions that could have lasting consequences for physical archival artifacts, must be supervised and approved by a human.

This safeguard applies to automation generally, not only to AI.

**Consequence:** AW must not make consequential archival judgments on the assumption that an automated result is sufficiently probable.

## 7. AW is developed as usable vertical slices

Development proceeds through thin, end-to-end slices of real archival work. Each slice should produce something that can actually be used and tested against real material before the system is expanded horizontally.

Tests define intended behavior before implementation.

The development loop is:

> Define behavior → write the test → make it pass → refactor → repeat.

A theoretically complete system that cannot yet be used to process archival material does not fulfill AW's purpose.

**Consequence:** Development should prioritize early, usable capability over completing an abstract architecture before the application can do useful work.
