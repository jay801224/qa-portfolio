# Company A — Senior QA Lead (2015–2017)

## Situation

Company A ran an online betting platform. I joined as Senior QA Lead and owned manual QA for the
product: there was no automation practice in place and no shared training material for new testers.

## Action

- Led manual QA for the platform: functional, stress, compatibility, UX and integration testing.
- Wrote the test plans and test reports, and estimated testing cost for planned work.
- Ran QA training for the team, and wrote the training material myself (Selenium + Python, 2014–2017).
- Used Fiddler 4 to inspect and replay backend traffic during testing of the money-handling flows.

## Result

- The Fiddler work located critical backend bugs in the betting, deposit and withdrawal flows.
  Company-estimated impact avoided: more than 1M per year.
- The Selenium + Python material in this folder became the in-house QA training course.

## What is in this folder

| File | What it is |
|---|---|
| `selenium-training/selenium.pptx` | Slide deck used in the QA training session: how to install Python, Selenium, pip, how to pick a browser driver, and how to record and replay a first script. |
| `selenium-training/Python-Selenium自動化測試.docx` | Written tutorial for the same course — environment setup, browser drivers (geckodriver / chromedriver), JDK, and worked Selenium examples in Python. |
| `selenium-training/自動化相關教學1.pdf` | Step-by-step install walkthrough handed out in class: Selenium IDE, Python 2.7, pip, Selenium 3.41, geckodriver, and adding Python to the PATH. |

These three are employer-era training documents and are kept in their original form. GitHub does not
render `.pptx` / `.docx` / `.pdf` inline, so the summaries above describe what each one contains.

## Notes on anonymisation

- The company and its products are referred to only as "Company A"; product and brand names were
  removed.
- Every hyperlink target inside the `.docx` that was not a third-party public documentation host was
  replaced with `example.internal`.
- Document metadata (author, company, revision history, thumbnails) was stripped from the containers.
- The embedded screenshots in the Python/Selenium document were reviewed one by one. Five were
  removed outright and replaced with a grey "screenshot removed" placeholder of the same size,
  because they showed a colleague's real email address, a plaintext mail password, or a live
  betting-site login. Nine more had a single line blacked out (an email address, a Windows user
  name, or a product name) and are otherwise intact. The rest were left untouched.
- The PDF text still contains the author's own personal domain and local Windows paths from 2015.
  PDF text cannot be edited without re-rendering the file, and these are the author's own, not the
  employer's, so they were left as they are.
- One file from this folder was withheld from the public repository because it was corrupt and its
  contents could not be verified.
