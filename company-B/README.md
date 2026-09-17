# Company B — Project Manager Lead (2018–2019)

## Situation

Company B ran lottery, chess and sports products on one online platform. Each product team had its
own issue workflow in JIRA, so tickets could not be compared or reported across projects, and the
planned chat service had no written specification.

## Action

- Wrote the product specification for the chat service in Axure RP, covering both the customer and
  admin sides, on PC and mobile.
- Set up JIRA: permissions, issue types and schemes, then migrated every online project onto a
  single unified workflow.
- Used Google Analytics for behaviour analysis on the live products.
- Ran the delivery process: scrum with a weekly release.

## Result

- All online projects ended up on one JIRA workflow, so ticket state meant the same thing in every
  project and cross-project reporting became possible.
- The chat service shipped against a written spec (mind maps and sequence diagram in this folder)
  rather than verbal requirements.

## What is in this folder

| File | What it is |
|---|---|
| `automation-acceptance-deck/自動化驗收測試.pptx` | Acceptance-testing deck for the mobile automation setup: how the QA lab was put together, the Robot Framework / Appium / Macaca toolchain, the install steps for Android Studio, the SDK, Node and Gradle, and the keyword-by-keyword walkthrough of the acceptance flows (click, swipe, swipe-by-percent, XPath location). |
| `automation-acceptance-deck/自動化驗收測試-slides.pdf` | The same deck rendered to PDF, 38 pages, so it can be read in the browser without downloading the `.pptx`. |
| `chatroom-spec/聊天室脑图.xmind` | Mind map of the chat room front end: entry points (from a game lobby, from the mobile app), room types, message types, and the user actions available in each state. |
| `chatroom-spec/控端脑图.png` | Mind map of the chat admin console — moderation, broadcast and account controls. Exported as an image. |
| `chatroom-spec/循序图.pptx` | Sequence diagram deck for the chat service: client, chat server and platform backend, and the message flow between them. |
| `jira-process/JIRA流程(後來的).pptx` | The later, unified workflow deck — the single scheme every online project was migrated onto. |
| `test-plan/ABOUT QA.pptx` | "About QA" deck used to explain to the product and dev teams what QA does, what it needs as input, and what it hands back. |
| `test-plan/test plan_case_data.xlsx` | Workbook with three sheets — `Test plan`, `Test case`, `Test data` — showing the plan-to-case-to-data structure used on the lottery products. |

GitHub does not render `.pptx` / `.xlsx` / `.xmind` / `.pdf` inline, so the summaries above describe
what each one contains.

## Notes on anonymisation

- The company and its products are referred to only as "Company B"; product, brand and vendor names
  were removed.
- Shared-document links to the employer's Google Sheets were replaced with `example.internal`, both
  in the hyperlink targets and in the visible slide text.
- Two business figures in the workbook were replaced with `<per spec>`.
- Document metadata (author, company, revision history, thumbnails) and hidden sheets were stripped
  from the containers.
- The automation acceptance deck described a QA lab that no longer exists. Its lab credentials
  (the vSphere and remote-desktop accounts and passwords in the environment table), the LAN IP
  addresses, the internal file-share path and the employer's APK download hostname were redacted in
  **both** formats — replaced in the `.pptx` slide text and hyperlink targets, and blacked out with
  true PDF redaction (text removed from the content stream, not just covered) in the rendered PDF.
  A local Windows install path was replaced with `C:\<path>`. All 38 pages are still there.
- The deck's 21 embedded screenshots were then reviewed one by one. Eleven were removed outright and
  replaced with a grey "screenshot removed" placeholder of the same size, because they showed a live
  betting site with a real login, an account balance and bet records, a colleague's Windows user
  name, or a test device's serial number. Six more had the identifying strip blacked out and are
  otherwise intact; four were already clean. The same decisions were applied page by page to the
  rendered PDF, so the two formats match.
- A Jira ticketing-convention PDF that used to sit in `jira-process/` was dropped from this folder
  altogether. Its label table listed the employer's internal product lines and departments by their
  real internal names, and that table was most of the document, so there was nothing worth keeping
  once it was redacted. The workflow deck next to it covers the same process.
- The acceptance deck's last slide assigned each lottery game to a named colleague. Those names were
  replaced with `<colleague>` in both the `.pptx` slide text and the rendered PDF.
