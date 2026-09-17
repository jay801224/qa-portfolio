# Security practice — personal, not employer work

> Everything in this folder is my own practice on **public** TryHackMe rooms and CTF boxes. No
> employer system, data or account appears anywhere in it.

## Situation

Testing money-handling flows means knowing how they get attacked. I work through public
TryHackMe rooms and CTF boxes in my own time to keep that side sharp, and I write each one up the
way I would write up a test run at work: plan first, then what I actually did, then the findings.

## Action

- Worked a public TryHackMe room end to end: recon, web enumeration, SQL injection to bypass
  authentication, file-upload to a web shell, then local privilege escalation.
- Wrote it up in three parts — the plan before starting, the operation log during, and the answers
  afterwards — rather than only keeping the final flag.
- Wrote a separate walkthrough for a CTF box covering the same ground, including the dead ends worth
  not repeating.
- Ran the exercise as an AI-driven run: the agent worked the phases without asking for instructions,
  and the operation log records where that held up and where it did not.

## Result

- Completed the room (completion screenshot in this folder).
- The write-ups are reusable: the plan-then-log-then-findings structure is the same one I use for a
  test run, so they double as a worked example of how I record an investigation.

## What is in this folder

| File | What it is |
|---|---|
| `tryhackme/01_plan.md` | The plan written before starting: scope, what to enumerate first, and what to try in what order. |
| `tryhackme/02_operation.md` | The operation log: what was run, what came back, and how each step led to the next — SQL injection for auth bypass, config file read, web shell, then privilege escalation. |
| `tryhackme/03_answers.md` | The room's questions and my answers, with how each one was obtained. Flags and hashes are redacted (see below). |
| `tryhackme/nmap_scan.txt` | Raw port-scan output from the recon step. |
| `tryhackme/thm_room_completed.png` | Screenshot of the completed room. |
| `ctf_walkthroughs/thm_gallery666.md` | Walkthrough of the same box written as a guide — the working path, plus the approaches that waste time and why. |

## Notes on anonymisation

- Nothing here is employer work, so there is no company, product or account to anonymise.
- Room flags (`THM{...}`) are replaced with `THM{<redacted>}`, hash values with `<hash>`, and the
  practice box's own throwaway credentials with `<practice-box-password>`. Those values belong to a
  public practice machine, not to any real system, but publishing them spoils the room for other
  learners and trips secret scanners, so they are redacted.
- Target IP addresses are replaced with `10.0.0.1`.
- One screenshot showing the full answer key was withheld for the same reason.
- Image metadata was stripped.
