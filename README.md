![CI](https://github.com/jay801224/qa-portfolio/actions/workflows/ci.yml/badge.svg)

# QA Portfolio — Jay Su

ISTQB Foundation certified, 10+ years of manual QA and 4+ years of test automation, all of it in the
online lottery / live-casino / iGaming domain. I have worked as QA lead, QA manager and project
manager, which means I have both written the test plan and owned the release it gated. This
repository is the work itself: automation suites that run, the test plans and process documents I
wrote, and — where the code belongs to an employer and cannot be published — a case study saying so
plainly. Every company is referred to as Company A–F; see the anonymisation policy at the bottom.

## Pinned projects

| Project | Stack | Result | Link |
|---|---|---|---|
| API contract, security and load testing | pytest, requests, k6 | API contract and security regression runs from one command with an HTML + JSON report; load tests judged against p95/p99 and error-rate thresholds instead of by eye | [`company-F/api-tests`](company-F/api-tests) · [`company-F/load-test-k6`](company-F/load-test-k6) |
| AI-assisted card verification | Playwright, Gemini Vision, OpenCV/OCR | Gave a machine-readable oracle to a check that had none — the cards a player sees in the video stream are verified against the round data, and cross-checked across three displays by round id | [`company-F/ai-assisted-testing`](company-F/ai-assisted-testing) |
| Game regression automation | Selenium, unittest, requests | Bet-correctness regression across the whole game catalogue cut from 40 minutes to 20; scheduled game-server betting checks from 40 minutes to 5, running hourly | [`company-D/selenium-autogame`](company-D/selenium-autogame) |

## Run it

Three commands, from the repository root, in a fresh virtual environment:

```
pip install -r company-F/api-tests/requirements.txt && pytest company-F/api-tests --collect-only -q
pip install -r company-D/selenium-autogame/requirements.txt && cd company-D/selenium-autogame && python -c "import gamevariable, urlvariable"
node --check company-F/load-test-k6/http_load.js
```

The first collects the API suite, the second loads the game and environment config modules, the
third checks the k6 script parses. CI runs all three on every push, plus a real `k6 run` against a
public echo service and a secret scan. The suites themselves target systems that are not public, so
they collect and load but do not execute end to end from here.

## Timeline

| Years | Company | Role |
|---|---|---|
| 2015–2017 | Company A | Senior QA Lead |
| 2018–2019 | Company B | Project Manager Lead |
| 2019 | Company C | Software QA Manager |
| 2019–2023 | Company D | Software QA Manager |
| 2023–2025 | Company E | Senior Game Analysis QA |
| 2025–present | Company F | QA, live-casino games |

## Repository map

| Folder | What is in it |
|---|---|
| [`company-A/`](company-A) | Self-written Selenium + Python QA training material. |
| [`company-B/`](company-B) | Chat-service specification (mind maps, sequence diagram), the JIRA workflow and ticket-filing rules, a test plan / case / data workbook. |
| [`company-C/`](company-C) | The QA onboarding document new engineers were trained against. |
| [`company-D/`](company-D) | The Selenium game regression suite — 26 files, config-driven, with HTML reporting. |
| [`company-E/`](company-E) | Case study only — no code. The work belongs to the employer; the page says what was built and what it changed. |
| [`company-F/`](company-F) | Current work: API contract and security tests, k6 load testing, AI-assisted card verification, browser performance runner, universal TC runner and test plans, Jira automation. |
| [`security-practice/`](security-practice) | Personal TryHackMe and CTF write-ups. Not employer work. |

Earlier training code lives in a separate public repository:
[jay801224/practice](https://github.com/jay801224/practice) — 2022 Selenium / Robot Framework /
Appium practice, kept there rather than copied here.

## Anonymisation policy

Every artifact in this repository has been through a desensitisation pass before publication:

- **Company, product, brand and vendor names** are removed. Companies are Company A–F; products are
  referred to by genre (lottery, live casino, slots) or by public game name only.
- **Hosts, URLs and IP addresses** are replaced with `example.internal` and `10.0.0.1`. The only
  hosts left intact are third-party public documentation and tooling sites on a signed allowlist.
  Shared-document links to employer systems are always replaced, never allowlisted.
- **Accounts, agent codes, passwords and tokens** are replaced with `<ACCOUNT>`, `USER01` / `PID01`
  and `<REDACTED>`.
- **Ticket and page identifiers** from the employers' issue trackers and wikis are removed.
- **Commercial figures** — RTP percentages, payout ratios, odds, table limits, bet limits and
  buy-free prices — are replaced with `<per spec>` or with round placeholder numbers. Where a
  configuration file was mostly such data, the values were placeholdered while the keys, the entry
  count and the structure were kept, so the module still imports and the design is still readable.
- **Document metadata** — author, company, revision history, thumbnails, hidden sheets and image
  EXIF — is stripped from every Office document, PDF and image.

Beyond those replacements the artifacts are kept in their original form; nothing was rewritten to
look better than it was. Documents produced during employment are shown here for portfolio
demonstration purposes only — see [`LICENSE`](LICENSE) for what that covers.
