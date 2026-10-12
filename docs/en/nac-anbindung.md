# NaC as a consumer

This repository owns schema/ontology artifacts and the roadmap. NaC retains its existing notarial usecases, BPMN/process contracts, access gates and integration adapters.

## Planned consumption

- NaC binds an approved release version and immutable commit/artifact hash.
- An integration manifest identifies repository, version, hash and compatible NaC adapter version.
- Production execution must not resolve a moving main branch.
- No manually maintained copy of domain schemas or this roadmap in NaC.
- Downloaded artifacts may use an explicitly derived, reproducible cache; ontologie8/schema remains authoritative.
- Updates require reviewable dependency changes plus compatibility/migration tests.
- No per-request ontology network lookup; approved artifacts are bound beforehand.
- SharePoint remains NaC storage, not ontology content. Private data requires NaC's approved operating boundary.

## Ownership

| ontologie8/schema | NaC |
| --- | --- |
| Terms, stable IDs, field/relationship definitions | Workflow binding and matter roles |
| JSON/RDF mapping, SHACL and validation contracts | Adapters, CLI/office UI and workflow gates |
| Synthetic reference cases and benchmark definitions | Approved tenant tests and production storage |
| Versions and breaking-change notices | Dependency binding and update approval |

No release, package or schema is implemented yet. P0 defines packaging, namespaces, leading representation and the exact version contract.
