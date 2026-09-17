# Company E — Senior Game Analysis QA (2023–2025)

> **Case study only — there is no code in this folder.** The automation described below was written
> inside the employer's repository and is not mine to publish. This page records what was built and
> what it changed; nothing from it was copied here.

## Situation

Company E built reel-based games. Every game shipped with its own hand-written test cases, so a
change to a shared parameter meant editing each game's cases one by one, and reel data was checked
against the mathematical RTP model by hand.

## Action

- Built the regression suite in Python with Robot Framework: a set of public keywords shared across
  games, plus per-game test cases layered on top. The test cases were modularised so that a
  parameter change was made once and picked up by every game that used it.
- Wrote autopilot scripts for the base game and for the feature regression pass, so a build could be
  run through both without a tester driving it.
- Automated reel-data validation against the mathematical RTP models through the API, replacing the
  manual spreadsheet comparison.
- Surveyed AI testing tools and promoted the ones that held up — test-case generation AI, Jira AI,
  and LLM assistants — into the team's workflow.
- Ran the manual side too: sprint planning and functional test cases.

## Result

- A shared-keyword layer meant a parameter change was made once rather than per game.
- Base-game and feature regression became unattended runs instead of manual passes.
- Reel data was checked against the RTP model automatically rather than by eye.

## What is in this folder

Nothing but this page. See the note at the top: the work is described, not published.

For automation code I can show, see `company-F/` and `company-D/`.

## Notes on anonymisation

- The company and its games are referred to only as "Company E"; no product, game or brand name
  appears here.
- No file, script or document from this employer is included.
