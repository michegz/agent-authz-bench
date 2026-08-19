# Bench 02: two endpoints checked, one did not

Live: **https://michegz.github.io/agent-authz-bench/**

A single-page bench you can run in thirty seconds with nothing installed.

A class waitlist exposes three endpoints. `createReservation` and `joinWaitlist`
both refuse to act on behalf of another user. `cancelReservation` never asks.
Run the agent and watch which endpoint it ends up using, then switch the missing
check on and run the identical agent again.

## What it proves

One ownership check, applied consistently to the call that destroys something,
closes the path. The agent is not made safer, smarter, or better prompted.

The demo half of the page proves itself by running: no network calls, no model,
every number computed live in your browser.

## What it does not prove

The page carries its own limits section in full. Short version: it is a
hand-written model, not a scanner; fixing cancel does not fix an API that hands
a full waitlist with user IDs to any caller; ownership is not the only rule;
and nothing here helps if the agent holds real credentials.

## Sourcing

The page was prompted by a reported incident in Australia. Every sentence about
that incident is quarantined in a clearly marked box on the page, and each line
carries its own source link ([The Next Web](https://thenextweb.com/news/openclaw-ai-agent-gym-booking-api-flaw-australia),
[The Register](https://www.theregister.com/ai-and-ml/2026/08/10/gym-rat-asks-ai-agent-to-book-him-a-class-it-hacks-a-waitlist-api-to-bump-him-up-the-list/5285591)).
Where the sources disagree, the page says so rather than picking the better story.

**Correction, 2026-08-19 00:08 UTC** (commit `0bd2380`, 44 minutes after first
publication at 2026-08-18 23:24 UTC). The first published version of this page said the
class was full, that the agent took the cancelled member's seat, that the member
was a woman, and that the incident happened on 9 August. None of that is in the
reporting. He was fourth on a waitlist and moved to third; the cancelled member
appears only as a user ID; no source gives an incident date. Every one of those
four errors made the story more compelling than the truth, which is the direction
error runs when you write the narrative before checking the sources.

## How it runs

No network calls, no model, no build step. One `index.html`. The authorization
function is printed on the page from the running function's own source, so the
code you read cannot drift from the code that just ran.

Tested in headless Chrome at 1280px and 390px, zero console errors.

---

Built by Michelle W., automation engineer, Lafayette, Louisiana.
[Hire me on Upwork](https://www.upwork.com/freelancers/~01b59471ec1e32fbdb)

See also [Bench 01](https://michegz.github.io/guardrail-bench/), which fires
nine hostile model outputs at a real validation node.
