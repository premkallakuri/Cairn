# Data Model And Storage

- Status: Current + Planned
- Audience: Maintainers, operators, app authors
- Source of truth: Persistence and storage reference
- Related modules/features: platform DB, app storage, library, maps, AI

## Platform Persistence Layers

Atlas Haven uses multiple persistence layers:

- MySQL for durable platform state in runtime deployments
- Redis for worker-oriented infrastructure
- host-backed storage directories for app and content data

## Current Durable Data Domains

- service catalog records
- easy setup drafts
- chat sessions and messages
- download jobs
- knowledge base file and chunk state
- ZIM-related selection and file state

## Host Storage Roots

- `../storage/zim`
- `../storage/maps`
- `../storage/ollama`
- `../storage/qdrant`
- `../storage/flatnotes`
- `../storage/kolibri`
- `../storage/rag`
- `../storage/logs`

## Volume-Backed Infrastructure Data

- `../.docker/mysql`
- `../.docker/redis`

## Storage Rules For App Authors

- every manifest must declare required storage paths
- mounts should point to host-backed directories under the Atlas Haven storage root
- app docs must explain where user data lives

## Planned Evolution

- explicit settings persistence for operator-configurable behaviors
- backup/restore runbooks and validation tooling
- clearer storage accounting surfaced in Control Room
