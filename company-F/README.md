# Company F — QA, live-casino games (2025–present)

## Situation

Company F builds live-casino games — blackjack and sic bo among them. Three things could not be
checked by hand at the rate the product shipped: whether the API contract still held, whether the
client stayed fast enough on the browsers players actually use, and whether the cards a player saw
on screen matched what the system had dealt. The last one is the hard case: the evidence is a video
stream and a canvas, so there is nothing in the DOM to assert against.

## Action

- **API contract and security tests** (`api-tests/`) — pytest suites over the login, Jira and public
  stream APIs, with an HTML + JSON report generator. The security suite covers SQL injection, XSS,
  path traversal, header injection, CORS and security headers.
- **Load testing** (`load-test-k6/`) — k6 HTTP and WebSocket scripts with pass/fail thresholds
  (p95/p99 latency, error rate) held in a config file, plus a Python reporter that turns the k6
  summary into HTML and JSON.
- **AI-assisted testing** (`ai-assisted-testing/`) — Gemini-vision screenshot validation and diff,
  and OCR card verification that reads the dealt cards off the video stream and checks them against
  the round's data, so the on-screen result can be asserted rather than eyeballed.
- **Browser performance** (`frontend-perf/`) — a runner built as two orthogonal axes: a *tier*
  decides which metrics to collect (Web Vitals, long tasks, DOM and resource counts, memory), an
  *adapter* decides how to get to the page under test. Adding an engine means adding an adapter, not
  forking the collector. There are also helpers that file the resulting performance findings into
  Jira as an epic with sub-tasks and attached evidence.
- **Test cases and plans** (`tc-framework/`) — a universal TC runner of site-agnostic checks where a
  failure is a bug regardless of spec, plus the written test plans for the live blackjack and live
  sic bo games.
- **Jira automation** (`jira-automation/`) — bots for creating, batching and verifying tickets.

## Result

- API contract and security regression runs from the command line and emits a report, instead of
  being a manual round of Postman calls.
- Load testing has thresholds, so a run gives a pass or a fail rather than a chart someone has to
  interpret.
- Card verification is automated against the video stream — the check that previously had no
  machine-readable oracle at all.
- The performance runner separates "what to measure" from "how to reach the page", so a new game
  engine costs one adapter file.

## What is in this folder

| Path | What it is |
|---|---|
| `api-tests/conftest.py` | pytest fixtures: base URL, auth headers, shared session. |
| `api-tests/test_login.py` | Login API: endpoint reachable, returns a game URL with a session token, responds under 5s. |
| `api-tests/test_jira.py` | Jira API: server reachable, credentials valid, query API works. |
| `api-tests/test_stream.py` | Public stream API contract tests; environment selected by `STREAM_ENV`. |
| `api-tests/test_stream_security.py` | Security suite for the same API — SQL injection, XSS, path traversal, header injection, security headers, CORS. |
| `api-tests/api_report.py` | Runs the suite and writes the HTML + JSON report. |
| `api-tests/requirements.txt` | Minimal dependencies, derived from the imports in this folder. |
| `load-test-k6/http_load.js` | k6 HTTP load script: login, then load the returned game page, with custom login-duration and login-error metrics. |
| `load-test-k6/ws_load.js` | k6 WebSocket load script: connect, join room, receive game events. |
| `load-test-k6/config/thresholds.json` | The pass/fail thresholds both scripts are judged against. |
| `load-test-k6/k6_report.py` | Turns a k6 summary export into an HTML + JSON report; can also run k6 itself. |
| `load-test-k6/README.md` | Notes for this sub-project. |
| `ai-assisted-testing/ai/gemini_vision.py` | Gemini API wrapper: screenshot or video in, structured description or generated test-case definitions out. |
| `ai-assisted-testing/ai/screenshot_analyzer.py` | Analyses a failing test's screenshot and returns a structured description, to help decide real bug vs broken script. |
| `ai-assisted-testing/ai/screenshot_diff.py` | Pixel diff of before/after screenshots with a difference percentage and a diff image. |
| `ai-assisted-testing/ai/screenshot_validator.py` | Catches screenshots that are identical when they should differ — a zero-API-cost check on the evidence itself. |
| `ai-assisted-testing/OCR/bac_card_verify.py` | Main card-verification run: enter the room, burst-capture each round, recognise the cards, write a JSON + HTML report. |
| `ai-assisted-testing/OCR/bac_4source_verify.py` | Cross-checks the dealt cards across the result animation, the video stream and the bet record, matched by round id, so a mismatch between displays is caught. |
| `ai-assisted-testing/OCR/bac_frame_analyzer.py` | Reads room / round / game / version from the page and picks the sharpest frame out of a burst. |
| `ai-assisted-testing/OCR/card_test_plans.py` | Card sequences that cover all 52 cards in three passes, to catch front-end/back-end card-id mismatches. |
| `ai-assisted-testing/OCR/bac_card_verify_poc.py` | The proof of concept the main runner grew out of. |
| `ai-assisted-testing/OCR/diag_bac_js_inject.py`, `diag_bac_methods.py` | Diagnostics used while building the above: does the injection work, and which of four ways of feeding a known card sequence actually records the right values. |
| `ai-assisted-testing/OCR/dom_dump_bet_record.py` | One-shot helper that dumps the bet-record panel's DOM so a broken selector can be replaced. |
| `frontend-perf/perf_runner.py` | The runner — picks one tier and one adapter and executes the combination. |
| `frontend-perf/perf_tiers/` | `basic` (Web Vitals, long tasks, DOM/resource counts, memory), `upgrade`, `advanced`, plus the shared base. |
| `frontend-perf/perf_adapters/` | `generic-url`, `product-react`, `product-egret`, plus the adapter base class. Adapters own page lifecycle only; metrics belong to the tier. |
| `frontend-perf/performance_baseline_collector.py`, `_egret.py`, `performance_baseline_shared.py` | The earlier two collectors the runner replaced, and the engine-agnostic helpers extracted from them. Kept because they show the refactor. |
| `frontend-perf/jira_ticket_perf_*.py` | The performance findings as Jira content — epic plus sub-task descriptions for the React stage, the Egret stage, and the design candidates. |
| `jira-automation/jira_bot.py` | Interactive CLI plus SDK for creating and verifying tickets. |
| `jira-automation/jira_batch.py`, `jira_create.py` | Batch creation with evidence attachment and duplicate checking. |
| `jira-automation/README.md` | Notes for this sub-project. |
| `tc-framework/universal_tc.py` | 41 site-agnostic test cases where a failure is a bug regardless of spec; runs against any URL. |
| `tc-framework/test-plan/live_blackjack_test_plan.md` | Written test plan for the live blackjack game. |
| `tc-framework/test-plan/live_sicbo_test_plan.md` | Written test plan for the live sic bo game. |
| `requirements.full.txt` | The full dependency list of the original work tree, kept for reference. The two runnable projects in this repository pin their own minimal `requirements.txt`. |

### Running it

```
pip install -r company-F/api-tests/requirements.txt
pytest company-F/api-tests --collect-only -q
node --check company-F/load-test-k6/http_load.js
```

Collection is what CI checks: the suites target APIs that are not public, so they cannot execute
end-to-end from this repository. The k6 script does run in CI against a public echo service to prove
it is valid and executable.

## Notes on anonymisation

- The company and its products are referred to only as "Company F"; product code names in filenames
  and class names were replaced with neutral ones (for example the per-engine adapters are now
  `product-react` and `product-egret`), and the import graph and CLI choices were updated to match.
- Every employer host, staging URL and internal endpoint was replaced with `example.internal`; IP
  addresses with `10.0.0.1`.
- Test accounts, agent codes and passwords were replaced with `<ACCOUNT>`, `USER01` / `PID01` and
  `<REDACTED>`.
- Jira ticket ids and Confluence page ids were removed.
- Commercial figures in the test plans — RTP percentages, payout ratios, table limits — were
  replaced with `<per spec>`.
- `load-test-k6/http_load.js` now defaults to a public echo service and takes its target from
  `TARGET_URL`, so the script can be run by anyone reading this repository.
- Two documents from this folder were withheld from the public repository because they carried
  payout tables and an internal specification link that could not be edited out of a PDF.
