# Archive Workbench — Decisions

This document records durable decisions about Archive Workbench. It is not a design diary or a list of possible approaches. Implementation details belong in the code unless they rise to the level of a durable project decision.

## 1. AW is a workbench, not the publication system

Archive Workbench prepares and processes archival material for publication. Omeka S remains the system responsible for the published collection, including its published resources and relationships.

**Consequence:** AW should integrate with Omeka S rather than attempting to replace or duplicate its publication model.

## 2. The archival object is distinct from its representations

A physical archival object, its digital representations, derivatives of those representations, and information about them are distinct things.

A representation does not replace the object it represents, and one representation does not replace another merely because it is newer, higher quality, or more convenient.

**Consequence:** AW must preserve these distinctions throughout processing and publication.

## 3. Host files remain external to AW

A digital representation may refer to an existing file on the archivist's host filesystem.

AW records the file's actual filesystem path and content identity (SHA-256).

AW does not copy the file into AW-managed storage as part of ordinary representation registration.

The local browser UI cannot obtain the host filesystem path through normal browser file-selection APIs.

AW therefore uses a local companion service to bridge the browser UI to narrowly scoped host filesystem capabilities.

The companion may open a native file picker and read the selected file to establish properties AW needs, such as SHA-256.

The companion is not archival storage and does not become responsible for preserving the selected file.

AW retains the resulting path and identity so that later integrity checking and reassociation can operate on the external file.

## 4. The local companion is a capability bridge, not archival storage

The local companion provides narrowly scoped host-filesystem capabilities that ordinary browser APIs cannot provide.

Its initial responsibility is to allow the archivist to select and examine an existing host-side file and return the information AW needs to associate that file with a digital representation.

The companion does not own archival records, define archival semantics, or become responsible for storing or preserving the files it accesses.

**Consequence:** The companion provides filesystem access for AW workflows while AW remains responsible for archival objects, representations, their identities, and associated archival state.

## 5. Archival evidence must not be silently destroyed or overwritten

AW must not silently discard, overwrite, or obscure archival evidence. Changes with consequential effects must be reversible.

This applies regardless of whether the proposed action originates with a human, deterministic automation, a heuristic, or AI.

**Consequence:** The safe path should be the normal path, and processing mistakes should be recoverable.

## 6. Reliable, low-risk work should be automated

If a computer can perform a task reliably without creating danger to the archive or its eventual publication, AW should perform that task rather than requiring the human archivist to do it manually.

This includes routine, repetitive, administrative, and data-management work wherever reliable automation is possible.

**Consequence:** Human attention should be reserved for work that actually requires human judgment.

## 7. AI is advisory and collaborative

AI may be used when it can meaningfully improve archival processing, but AI-assisted work is collaborative rather than autonomous.

AI may propose information, interpretations, relationships, classifications, or other actions. A human remains responsible for evaluating and approving consequential interpretive decisions.

**Consequence:** AI errors should result in incorrect proposals requiring correction, not irreversible changes to the archive.

## 8. Historical interpretation and consequential archival actions require human approval

Questions of historical interpretation, and actions that could have lasting consequences for physical archival artifacts, must be supervised and approved by a human.

This safeguard applies to automation generally, not only to AI.

**Consequence:** AW must not make consequential archival judgments on the assumption that an automated result is sufficiently probable.

## 9. AW is developed as usable vertical slices

Development proceeds through thin, end-to-end slices of real archival work. Each slice should produce something that can actually be used and tested against real material before the system is expanded horizontally.

Tests define intended behavior before implementation.

The development loop is:

> Define behavior → write the test → make it pass → refactor → repeat.

A theoretically complete system that cannot yet be used to process archival material does not fulfill AW's purpose.

**Consequence:** Development should prioritize early, usable capability over completing an abstract architecture before the application can do useful work.
