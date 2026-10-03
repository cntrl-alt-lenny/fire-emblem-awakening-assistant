# Framework feedback: successor brief makes inherited reports appear stale

Project: `cntrl-alt-lenny/fire-emblem-awakening-assistant`
Observed commit: `7904a62964f97f1cfd4eab727a91dfb5a8562fe5`
Framework release: 3.1.0

## What happened

Under owner-approves, Brain accepted the exact audit delivery but did not merge
without approval. The owner also requested the next round's prompts. Brain
created and pushed `brain/002-combat-gate` from the delivered Verifier branch,
adding only the next brief/prompts and a review attachment. The original Worker
and Verifier branch tips and reports did not move. Status then identified both
round 001 reports as stale, apparently considering the successor branch that
carries those reports rather than the original delivered branch.

## Reproduction commands

Commands used in this project (exit 0):

```sh
python3 tools/fw.py delivery --round 001-foundation-audit
git switch -c brain/002-combat-gate origin/verifier/001-foundation-audit
# Add the next brief/prompts and prior-round review attachment, then:
git add docs/rounds/001-foundation-audit/attachments/brain-review.md docs/rounds/002-combat-gate
git commit -m 'Review foundation audit and brief strict combat gate round'
git push -u origin brain/002-combat-gate
python3 tools/fw.py status
```

Original delivered tip:
`3da1cd4408fd51d28606058ae74b956d587c72eb`.

## Expected result

Recognize round 001's unchanged named delivery as reported, and round 002 as
briefed/not started. Adding a successor brief should not require either seat to
rewrite a report for an unchanged exact delivery. If this branching pattern is
unsupported, diagnose that restriction rather than saying the seat moved its
branch. It is useful to prepare independent follow-up work while an accepted
audit awaits owner approval.

## Actual result

```text
in flight: 001-foundation-audit (Tier 2)
  worker: stale -- its report no longer describes its branch
  verifier: stale -- its report no longer describes its branch
in flight: 002-combat-gate (Tier 2)
  worker: not started
  verifier: not started
next: ask Brain what to send the Worker of round 001-foundation-audit: its report is out of date
```

Brain checked the PR head remains exactly the accepted delivery, with successful
CI. No framework modification, force push, report restamp or merge was performed
to suppress the warning. The exact-commit acceptance record and required merge
approval remain authoritative; the new round is independently briefed.
