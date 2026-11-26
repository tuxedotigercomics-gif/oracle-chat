# Decisions & constraints

## Model choices
- Do NOT adopt Qwen3.8 for the office work: user tests Qwen3.6 = 4/6 pass, Qwen3.8 = 0/6.
- Local Oracle model is qwen2.5:3b because it fits 8 GB and works offline. The 64 GB M1 Max is NOT the target machine.
- Cloud via bundled OpenCode CLI `opencode-cli`, not direct HTTP. Cloud sessions deny tools.

## Office work (frozen, under independent review)
- Office is READ-ONLY unless explicitly asked. One writer only. Phrase guidance to Grokbot as questions. Independent reviewer, not echoing suggestions.
- Live office frozen: no restart, no test requests, no tapping card `180e`, no rollback unless approved after review.
- Card `act-356ddba8180e` (`180e`) is pending, untouched, expires 4:38 PM. DO NOT TAP.
- Old card `d531` moved to `phone/superseded/` (not deleted).
- Approved fixes installed 1:14 PM MT: label regex `R\d{1,2}[a-z]?`, card cleanup, responder restarted PID 47461.
- Pass criteria: ["R1a"] passes and charges exactly one round; R1aa/Rx/R1A/bare "R1a" bounce with zero round; third refusal stops for review; guard catches Rowan's first patch; full suite shows the same 39 known failures and nothing new.
- Three real bugs found by Grokbot: string round marker "1.free1" causes int parse crash; leftover bounce entries logged against later refusals; phone/superseded/ symlink gap can redirect card moves.
- Staging evidence still incomplete: final pytest summary, 39-failure baseline comparison, explanation of 5 test_public_assets.py errors, tests for the three new bugs.

## Generated avatars
- 20 image-generation jobs all failed with `Invalid credential`. Do not retry image generation unless credentials are fixed. CSS pixel sprites are the working substitute.
