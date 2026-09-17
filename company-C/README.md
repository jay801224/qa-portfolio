# Company C — Software QA Manager (2019)

## Situation

Company C ran lottery, chess and live-casino products. There was no issue tracker of its own, no
written QA onboarding, and new QA engineers learned the products by asking whoever was free.

## Action

- Built JIRA from scratch on Linux, and separated it into products, platforms and on-call projects
  so that live incidents did not sit in the same queue as feature work.
- Wrote the QA onboarding SOP — the must-read test documents a new QA engineer works through — and
  trained new QA engineers against it.
- Recorded product demo videos so the same walkthrough did not have to be given repeatedly.
- Ran the delivery process: scrum with a weekly release.

## Result

- New QA engineers had a written path from day one instead of shadowing; the onboarding sheet in
  this folder is that path.
- Live-incident work and project work were separable in JIRA, so on-call load became visible.

## What is in this folder

| File | What it is |
|---|---|
| `qa-onboarding/測試必讀文檔.md` | The same document as Markdown, so it renders on GitHub without downloading anything. Two tables: the JIRA field-by-field filing guide, and the on-boarding / junior course list (lesson 1–20). |
| `qa-onboarding/測試必讀文檔.pdf` | The original must-read onboarding document for new QA engineers. Covers how to file a JIRA ticket with a worked example, the five priority levels and what qualifies for each (from "company reputation or money loss" down to "unimportant text error"), what to record for environment, how to use labels for later filtering, and what to attach — screenshots for static problems, video for dynamic ones. |

GitHub does not render `.pdf` inline, so read the `.md` — it carries the same content.

## Notes on anonymisation

- The company and its products are referred to only as "Company C"; the filename previously carried
  a company alias and was renamed.
- Three product and project names appeared in the document's label guidance. They were replaced with
  `<PRODUCT>` in the Markdown version and blacked out of the PDF with true redaction — the text is
  removed from the content stream, not covered over. Both files now extract clean.
- Document metadata was stripped.
