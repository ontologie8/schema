# Project: ontology and schemas

Updated: 2026-10-12. Independent project in [ontologie8/schema](https://github.com/ontologie8/schema); NaC is a future consumer.

## Request and project status

The project covers: people/family, organizations/directors, holdings/assets, events, gifts/wills, time and scenarios plus JSON Schema, RDF/Turtle, SHACL, SPARQL, NetworkX and an optional graph database. See the [full roadmap](../../roadmap/en/personen-nachlass-roadmap.md) and [NaC integration](nac-anbindung.md).

Working method: Kanban, weekly review, short sync as needed; maintainer funktion8 / ofunk. This schedules no meetings or reminders. P0–P6 remain backlog.

## Version-controlled project board

| Work package | Scope | Status | Dependency |
| --- | --- | --- | --- |
| P0 | Design, model boundaries and NaC consumer contract | Backlog | — |
| P1 | People, family, organizations and temporal roles | Backlog | P0 |
| P2 | JSON reference dataset, SharePoint mapping and 10,000-person benchmark | Backlog | P1 |
| P3 | Genogram projection and export contract | Backlog | P2 |
| P4 | Assets, holdings, obligations and transfers | Backlog | P1/P2 |
| P5 | Temporal scenarios and reviewed succession rules | Backlog | P3/P4 |
| P6 | Consumer integration, views and backend benchmark | Backlog | P1–P5 |

Track work packages in this board. [Acceptance criteria](akzeptanz.md) define the domain validation goals.

## Next step

Start P0: prepare a design spec comparing JSON-first and RDF-first, defining model boundaries and a small synthetic pilot.
