# Company D — Software QA Manager (2019–2023)

## Situation

Company D built its games with an overseas development team, so requirements had to be agreed in
writing across a time-zone gap. QA was on call for online bugs, and every release meant re-checking
bet correctness by hand across the whole game catalogue — the regression pass alone took 40 minutes
of clicking per run.

## Action

- Coordinated requirements with the overseas dev team and stayed on call for online bugs.
- Built the regression automation in this folder: recorded the flows in Selenium IDE, converted the
  recordings to Python 3, and ran them against every game product to validate bet correctness.
- Refactored the recorded scripts into reusable functions with an automatic HTML report, so a new
  game needed a test module rather than a new recording.
- Automated the betting checks against the game server with Postman and Python, on an hourly
  schedule.
- Wrote a Python availability monitor for the game-server API that writes a text log.
- Built JIRA on public cloud and administered it.

## Result

- Bet-correctness regression across all game products: **40 minutes → 20 minutes** per run.
- Scheduled game-server betting checks: **40 minutes → 5 minutes**, running hourly instead of
  on request.
- Online-bug response no longer depended on a manual sweep to confirm whether betting was correct.

## What is in this folder

The `selenium-autogame` suite — the regression automation described above. The browser tests run on
Selenium with `unittest` and report through a vendored `HTMLTestRunner`; the game-server checks go
straight at the API with `requests`; one spec is written in Cypress.

| File | What it is |
|---|---|
| `selenium-autogame/game_run.py` | Entry point: discovers every `gametest*.py` module, runs them as one suite and writes the HTML report. |
| `selenium-autogame/gamevariable.py` | Game catalogue config: game id list, game names in four languages, per-game total-bet limits and buy-free prices, plus the lookup helpers (`get_gamename`, `get_gametotalbet`, `get_gamebuyfree`) and the game-id to URL routing. |
| `selenium-autogame/urlvariable.py` | Environment config: the staging / demo / production site maps and the agent-to-URL table, with one lookup function. |
| `selenium-autogame/gametest_16.py` … `gametest_20.py`, `gametest_new.py` | Per-game-family test modules — the reusable functions the recordings were refactored into. Each drives a game, places bets and checks the result. |
| `selenium-autogame/test_16.py`, `test_16ff.py`, `test_17.py` … `test_20.py` | The `unittest` runners that pair with each game-family module (`test_16ff.py` is the Firefox variant). |
| `selenium-autogame/test_newmodule.py` | Runner for a newly added game family. |
| `selenium-autogame/test_demoallspin.py` | API sweep: posts a `spin` command straight to the game server for every game id in demo mode — the broad "does any game reject a bet" pass, without a browser. |
| `selenium-autogame/test_kostress.py` | Stress test against the game-server API: repeats spin requests with different bet payloads and currencies to look for failures under load. |
| `selenium-autogame/ko.js` | Cypress spec covering the same games in the browser — visits the game URL, clicks the canvas to bet and checks the bet record page. |
| `selenium-autogame/maintaincheck.py` | Multi-site maintenance / availability check: walks a list of agent sites and screenshots each one. |
| `selenium-autogame/newuat.py`, `uatnewgame.py`, `uatoldgame.py` | UAT runners — new-build acceptance, new-game acceptance, and the existing-game regression set. |
| `selenium-autogame/HTMLTestRunner.py`, `HTMLTestReport.py` | Vendored HTML report generators for `unittest` — the two variants the suite was run with. |
| `selenium-autogame/requirements.txt` | Minimal dependencies, derived from the imports in this folder. |

### `qa-process/` — the QA process documents from the same job

The written side of the same role: the test plans the automation above was built to replace, the
reports that came out of it, and the onboarding material used to bring new QA engineers up.

| File | What it is |
|---|---|
| `test-plans/demo 10 slot test plan.xlsx` | Test plan for a ten-game slot demo release — scope, per-game test items and the pass/fail grid. |
| `test-plans/10 demo bug list.xlsx` | The bug list that came out of that plan: one row per defect with environment, steps and state. |
| `test-plans/bet record test plan.xlsx` | Test plan for the bet-record screen — record accuracy, filtering and paging. |
| `test-plans/cdn test plan.xlsx` | Test plan for the CDN release path: asset pull, cache behaviour and per-region checks. |
| `test-reports/測試報告(總結).xlsx` | Release test summary report — result counts per project pulled from saved JIRA filters, with the outstanding-issue breakdown. |
| `test-scenarios/前後台操作情境.xlsx` | End-to-end operation scenarios spanning the player front end and the admin back end. |
| `test-scenarios/後台操作情境.xlsx` | Admin-only operation scenarios — account, wallet and configuration paths. |
| `qa-training/jira/Jira 工作流.pptx` | JIRA workflow training deck: which statuses QA may set, who opens which issue type, and how Regression is handled. |
| `qa-training/jira/Jira 操作介紹.pptx` | JIRA walkthrough deck for new QA engineers — dashboards, boards, creating an issue, searching and the personal-settings screens. |
| `qa-training/jira/Jira 常用功能.docx` | The everyday-JIRA guide that goes with it: saved filters, JQL by date range, column and view options, and exporting an issue list. |
| `qa-training/測試工作內容.xlsx` | What the QA job covers, broken down by activity — used for onboarding and for scoping. |
| `qa-training/工作項目清單.xlsx` | The QA work-item checklist worked through per release. |
| `qa-training/考試.docx` | The QA hiring exam written for this team — domain terms, test-design and bug-reporting questions. |
| `tools/api-collections/thunder-collection_上板包_CDN測試.json` | Thunder Client collection for the build-upload and CDN checks, one request per region and B2B / B2C class. |
| `tools/api-collections/thunder-collection_加解密工具.json` | Thunder Client collection for the request encrypt / decrypt helper endpoint. |
| `tools/api-collections/thunder-collection_查訂單.json` | Thunder Client collection for the order-comparison (reconciliation) endpoint. |
| `maintenance/維護確認清單 2023.xlsx` | Weekly maintenance confirmation checklist — per region and per surface, what is re-checked after each maintenance window. |

Two tool guides from this set — a Fiddler capture walkthrough and a CDN capture walkthrough — are
not published. They are almost entirely annotated screenshots of internal systems, and the detail
that would have to go runs through the whole frame rather than sitting in one strip, so they cannot
be anonymised without re-shooting them.

### Running it

```
pip install -r company-D/selenium-autogame/requirements.txt
cd company-D/selenium-autogame && python -c "import gamevariable, urlvariable"
```

The config modules load cleanly, which is what CI checks. The tests themselves drive a live game
platform that is not public, so they cannot run end-to-end from this repository.

## Notes on anonymisation

- The company, its games and its partner sites are referred to only as "Company D"; product, brand
  and vendor names were removed.
- `gamevariable.py`: the vendor game catalogue was replaced with placeholders — game names became
  `Game 01` … `Game 88` in all four languages, and the bet limits and buy-free prices became round
  numbers. The entry count, the four-language structure and every key and variable name were kept,
  so `import gamevariable` and all attribute lookups still resolve.
- `urlvariable.py` and `maintaincheck.py`: every host, site map entry and agent code was replaced
  with `example.internal` and placeholder agent ids. The dictionary structure and the lookup
  functions were kept for the same reason.
- Test accounts and passwords in the test modules were replaced with `<ACCOUNT>` and `<REDACTED>`.
- `qa-process/`: every employer host, test-site URL and JIRA tenant link was replaced with
  `example.internal`, in the visible cells **and** in the hyperlink targets inside the containers.
  The Thunder Client collections had their API keys replaced with `<REDACTED>` and their agent,
  master-agent and messaging ids with `<ACCOUNT>`; both the file and the request bodies inside it
  are still valid JSON. One agent code and one configured threshold value were replaced. Business
  terms that appear as test-item names (with no figure attached) were left as written — they are
  what the documents are about.
- `qa-training/jira/`: the two JIRA walkthrough documents are built from screenshots, so the
  anonymisation is painted onto the images. Every grey block is a redaction — the browser chrome
  strip (the JIRA tenant address and the bookmark bar), and, elsewhere in the frame, account names
  and avatars, project and issue keys, and two dashboard gadget titles named after a product id.
  The images keep their original pixel size so the pages lay out as they did; the tenant link in
  the document text and in the hyperlink targets became `example.internal`, and the document
  author field was cleared.
