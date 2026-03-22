# Atlas Haven Personas And Use Cases

- Status: Current + Planned
- Audience: Product owners, designers, maintainers, operators
- Source of truth: User and workflow reference for feature justification
- Related modules/features: Easy Setup, App Dock, Atlas Maps, AI Chat, Field Guide, Control Room

## 1. Primary Personas

### Local Operator

This user installs and maintains Atlas Haven on a personal workstation, mini PC,
or local server. They care about reliability, clarity, and the ability to manage
apps and data without deep container knowledge.

Core needs:

- bootstrap the stack quickly
- install the right apps and content for their use case
- understand system status and storage impact
- recover from failed updates or broken apps

### Knowledge User

This user primarily consumes library content, maps, and AI workflows. They may
not be the person who manages the stack, but they depend on the platform being
discoverable and consistent.

Core needs:

- access offline reference material
- search and browse library content
- use private AI chat with local files
- navigate maps without internet dependence

### Maintainer

This user evolves the Atlas Haven codebase, preserves parity with the legacy
product, and ships new modules.

Core needs:

- understand architecture boundaries
- track current versus planned behavior
- verify quality gates for each module
- keep docs synchronized with implementation

### App Author

This user adds new apps through the manifest-driven framework.

Core needs:

- understand the manifest schema
- declare runtime, mounts, ports, dependencies, and hooks
- avoid core orchestration edits when adding a normal app
- write smoke tests and docs for the new package

## 2. Secondary Personas

### Educator

Needs Kolibri, Wikipedia, curated educational references, and simple operator
flows for offline classroom or lab use.

### Researcher

Needs a persistent local library, AI-assisted search, and knowledge ingestion for
reference work without cloud dependence.

### Field Or Preparedness User

Needs maps, curated references, stable local tools, and minimal reliance on
network connectivity during active use.

## 3. Jobs To Be Done

### Job: Bring Up A Useful Local System Quickly

When I first deploy Atlas Haven, I want a guided setup and a working local stack
so that I can start using maps, library content, and apps without building the
system manually.

Relevant features:

- Easy Setup
- App Dock
- bundled manifests
- bundled demo Wikipedia

### Job: Install The Right Apps Without Docker Expertise

When I need new capability, I want to install apps from the UI so that I do not
have to memorize container images, ports, or mount paths.

Relevant features:

- App Dock
- manifest catalog
- dependency-aware orchestration

### Job: Access Offline Knowledge

When connectivity is unavailable, I want the library to remain useful so that I
can browse encyclopedic, educational, and reference content locally.

Relevant features:

- Kiwix
- ZIM workflows
- Library Explorer
- Library Shelf

### Job: Use Local AI Safely And Privately

When I need summarization or question answering, I want local model execution and
optional local file context so that my workflow does not depend on cloud tools.

Relevant features:

- Ollama runtime
- AI Chat
- Knowledge Base
- Qdrant dependency support

### Job: Maintain The Platform Without Guesswork

When something is outdated or unhealthy, I want one place to inspect, repair,
update, and relaunch services so that I can keep the system operational.

Relevant features:

- Control Room
- App Dock
- downloads and jobs visibility
- release and version awareness

### Job: Extend The Platform Cleanly

When I want a new app in the platform, I want to add it as a package with a
clear contract so that I do not have to rewrite core services.

Relevant features:

- manifest-and-app framework
- app docs
- smoke tests
- developer guides

## 4. Detailed Use Cases

### Use Case: First-Time Setup For A Research Laptop

The operator selects AI, library, and map capabilities in Easy Setup, chooses the
bundled demo Wikipedia option, installs Ollama and Qdrant, and later uploads
local PDFs into the Knowledge Base for AI-assisted retrieval.

### Use Case: Offline Education Deployment

The operator installs Kolibri and Kiwix, manages curated educational content,
uses the library for offline reference, and maintains the stack through the
Control Room without CLI intervention.

### Use Case: Local Notes And Data Tools Workspace

The operator installs FlatNotes for personal capture and CyberChef for data
transformation, then launches both from the App Dock as part of a self-contained
local workspace.

### Use Case: Maintenance And Recovery

The operator opens Control Room, checks pending app updates, reviews active
downloads, restarts a stopped service, and force reinstalls a problematic app.

### Use Case: Add A New App Package

The maintainer or app author creates a new app manifest, defines the runtime,
ports, mounts, and docs slug, adds optional hooks and smoke tests, and expects
the platform to detect the new app through catalog sync.

## 5. Persona Constraints And Expectations

- Operators need plain-language system explanations.
- Maintainers need exact contracts, boundaries, and module references.
- App authors need deterministic framework rules more than design prose.
- Knowledge users need consistency of terminology and navigation.

These constraints directly justify the split between PRD, features, user guides,
and developer documentation.
