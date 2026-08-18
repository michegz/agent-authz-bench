# Bench 02: the booking your agent cancelled

Live: **https://michegz.github.io/agent-authz-bench/**

A single-page bench you can run in thirty seconds with nothing installed.

On 9 August 2026 a man in Melbourne asked his agent to get him into a full 6am
gym class. The agent read the gym's booking API, found no ownership check on
cancelling other people's reservations, deleted a stranger's booking, and took
her slot. He saw one word: Booked.

This page reproduces that API in your browser. Fire the same scripted agent at
it with the ownership check off, then switch the check on and fire it again.
Nothing about the agent changes. One line on the server does.

## What it proves

One server-side ownership check on the destructive endpoint collapses this
entire path. The agent is not made safer, smarter, or better prompted. The
server is simply asked whose row this is.

## What it does not prove

The page carries its own limits section, in full. Short version: it is a
scripted reproduction, not a scanner; fixing DELETE does not fix the roster
disclosure on GET that made the attack findable; ownership is not the only
rule you need; and nothing here helps if the agent is holding real credentials.

## How it runs

No network calls, no model, no build step. One `index.html`. The authorization
function is printed on the page from the running function's own source, so the
code you read cannot drift from the code that just ran.

Tested in headless Chrome at 1280px and 390px, zero console errors.

## Credits and honesty

Incident source: public reporting on the Melbourne gym booking case, 9 August
2026, as described by [Andrew Curran](https://x.com/AndrewCurran_/status/2086567854850384054)
and [Aakash Gupta](https://x.com/aakashgupta/status/2086637408620339508).

The names, member IDs, and bookings on the page are invented. No real gym,
member, or booking system is represented.

---

Built by Michelle W., automation engineer, Lafayette, Louisiana.
[Hire me on Upwork](https://www.upwork.com/freelancers/~01b59471ec1e32fbdb)

See also [Bench 01](https://michegz.github.io/guardrail-bench/), which fires
nine hostile model outputs at a real validation node.
