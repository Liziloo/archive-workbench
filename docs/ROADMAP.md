# Archive Workbench — Development Roadmap

This roadmap describes the intended progression of Archive Workbench from its current vertical-slice foundation toward a usable archival workbench.

It is a development roadmap, not a complete requirements specification. Later slices intentionally contain unresolved questions that should be answered from actual archival workflows rather than decided prematurely. The sequence may change if real use exposes a better order.

## 0. Foundation

**Status: Complete**

Establish the project foundation and the test-first vertical-slice development approach.

The project should have:

* clear purpose and boundaries;
* durable architectural and domain decisions;
* a working development environment;
* a domain model grounded in archival objects and their representations;
* automated tests defining established behavior;
* a minimal end-to-end GUI/API path.

---

## 1. Local Companion Foundation

**Status: Next**

Establish the minimal local companion service required for AW to access existing host-side files from the browser-based workbench.

The companion should:

* run locally alongside AW;

* provide a narrowly scoped native file-selection capability;

* allow the archivist to select an existing host-side file;

* return the selected file's actual host filesystem path;

* provide the file information AW needs to register the file, including its SHA-256 identity;

* handle cancellation and relevant filesystem failures.

The companion is a capability bridge. It does not own archival records, define archival semantics, or become responsible for storing or preserving the files it accesses.

This slice does **not** include:

* archival object management;

* representation management;

* copying files into AW-managed storage;

* persistent storage;

* generalized filesystem access;

* generalized import infrastructure.

**Success criterion:** AW can invoke the companion and receive a usable host-side file reference and the information needed to examine that file for registration.

---

## 2. Add a Digital Representation

**Status: Next**

Allow an archivist to add an existing digital file as a representation of an open archival object.

The intended interaction is:

1. Open an archival object.
2. Choose **Add Digital Representation**.
3. Use the local companion service's native file picker to select an existing host-side file.
4. The companion provides AW with the selected file's actual host filesystem path and the file information AW needs.
5. AW creates and associates a representation.
6. The new representation immediately appears in the object view.

This slice should establish end-to-end behavior for:

* selecting an existing file through the GUI;
* getting the selected file's actual host filesystem path and required file information to the backend;
* creating a domain `Representation`;
* computing its SHA-256 identity;
* detecting duplicate content;
* requiring explicit confirmation when adding a duplicate;
* handling selection, filesystem access, validation, and other relevant failures;
* showing the resulting representation immediately.

The slice does **not** include:

* persistent storage;
* copying files into AW-managed storage;
* a preservation-storage system;
* representation metadata management;
* representation ordering UI;
* generalized import infrastructure.

AW should associate an existing host-side digital file rather than import it into AW-managed storage. The local companion provides the filesystem access needed to select and examine the file; it does not become responsible for storing or preserving it.

---

## 3. Create and Manage Archival Objects

Move beyond the hard-coded example object.

Establish the ability to:

* create archival objects;
* identify objects;
* list objects;
* open a selected object;
* return to the object list;
* maintain multiple distinct objects simultaneously.

Persistence is not required yet; an in-memory implementation is sufficient while the domain and workflow are still being established.

---

## 4. Multiple Archives

Establish the architectural boundary between distinct archives before object-management functionality grows too far.

An AW installation must be able to contain multiple distinct archives without conflating their contents.

This slice should establish enough behavior to:

* define archive ownership of archival objects;
* ensure representations remain associated through their objects;
* select or switch between archives;
* keep archival records from different archives distinct.

The precise model for defining, organizing, and selecting archives is intentionally deferred until the workflow makes the appropriate model clear.

---

## 5. Physical Archival Object Information

Add the ability to describe and edit basic information about the physical archival object.

Fields and behavior should emerge from actual archival processing rather than from a generalized metadata schema designed in advance.

This slice should establish the domain meaning and workflow for information that describes the physical object itself, distinct from its digital representations.

---

## 6. Representation Management

Provide useful management and inspection of an object's digital representations.

Potential behavior includes:

* inspecting representations;
* showing intact, modified, and missing status;
* showing representation identity;
* showing the last known file path;
* managing ordering where ordering is meaningful;
* distinguishing representations from derivatives;
* determining whether representations can or should be detached or removed.

The semantics of mixed ordered and unordered representations remain intentionally unresolved until the workflow establishes what ordering means.

---

## 7. File Recovery and Reassociation

Allow an archivist to recover a representation whose associated file is missing or displaced.

The intended workflow is:

1. AW identifies a representation requiring attention.
2. The archivist selects a possible replacement file.
3. AW verifies the replacement against the representation's known identity.
4. A matching file can be reassociated.
5. A nonmatching file is rejected.

Reassociation must preserve the representation's identity. AW must not silently treat a different file as the same representation.

---

## 8. Archival Processing and Workbench Tasks

Build the processing workflow around real archival work rather than around a generalized workflow engine.

Use the Haushalter and Casler material to determine what the workbench actually needs to help an archivist do.

The workbench should:

* represent processing state where it is genuinely useful;
* surface missing or incomplete information;
* support a useful sequence of archival tasks;
* make routine administrative work fast;
* preserve human control over consequential decisions.

Do not build a generalized workflow engine merely to support hypothetical future workflows.

---

## 9. Descriptive and Administrative Metadata

Add the metadata actually required by the archival workflow.

Likely areas include:

* dates;
* locations;
* people;
* physical description;
* provenance and context;
* archival location;
* date received;
* date imaged;
* other information demonstrated to be necessary through real processing.

The goal is not to create a comprehensive metadata-management system in advance. Metadata behavior should emerge from actual use.

---

## 10. Derivatives and Processing Outputs

Distinguish original digital representations from working and publication derivatives.

Establish:

* relationships between source representations and derivatives;
* provenance of processing outputs;
* clear identification of originals versus derivatives;
* appropriate handling of derivative files.

AW should track and support these relationships, but it is not intended to become an image editor or general-purpose media-processing application.

---

## 11. Review and Quality Control

Provide a way to surface material problems requiring attention.

Potential attention states include:

* missing files;
* modified files;
* incomplete information;
* questionable results;
* unresolved archival decisions.

The workbench should make problems visible and support human review. It should not silently "fix" historical interpretation or other consequential decisions.

---

## 12. Search, Retrieval, and Navigation

Once enough archival data exists to make retrieval useful, support efficient navigation across it.

Potential capabilities include:

* searching and filtering archival objects;
* filtering by archive;
* searching by people, dates, and locations;
* finding objects requiring attention;
* navigating between objects and representations;
* other retrieval patterns demonstrated by actual use.

Search should be driven by the information archivists actually need to retrieve, not by a generic search system built in advance.

---

## 13. Omeka S Preparation and Export

Prepare archival information and files for publication through Omeka S.

AW remains the workbench; Omeka S remains the publication system.

Capabilities should emerge from actual publication needs and may include:

* mapping AW information to Omeka S properties;
* preparing files and metadata for publication;
* export or packaging;
* validation;
* interaction with the Omeka S API where useful.

AW should not become a replacement for Omeka S.

---

## 14. Persistence

Introduce durable persistence only after the domain and workflow have earned stable requirements.

Persistence should support the structures that have emerged through earlier slices, potentially including:

* multiple archives;
* archival objects;
* digital representations;
* metadata;
* relationships;
* processing state;
* representation identity and integrity information.

The persistence model should preserve the architectural boundary between distinct archives and should reflect the established domain rather than dictate it prematurely.

---

## 15. Operationalization and Real Archive Use

Exercise AW against real archival material and real working conditions.

Use material such as the Haushalter and Casler archives to test:

* multiple archival objects;
* multiple representations;
* multiple distinct archives;
* real filesystem behavior;
* interruptions and incomplete processing;
* missing and changed files;
* real metadata;
* actual archival decisions;
* recovery from ordinary problems encountered during use.

Fix problems exposed by real work.

The goal is not merely to demonstrate that the software works in a controlled development environment, but to determine whether it actually makes archival processing easier, safer, and more reliable for the archivist using it.
