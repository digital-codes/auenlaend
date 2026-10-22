# Design

## Context

The frontend contracts were mapped in the exploration: `ChatPane.vue`
gates rendering on `message.context`, builds follow-up requests by
spreading the previous response and mutating `postMsg.context` (a
TypeError since the backend stopped sending `context`), reads options
from `message.context.options`, and crashes on `null` data from the
axios error wrapper (`backendComms.ts` returns `data: null` for
non-200/network). The backend now returns
`{state, message, session, sequence, options?}` and expects the token
echoed back; conversation state (intent, entity, feature, focus,
last input/intent) lives server-side inside the token.

## Goals / Non-Goals

**Goals:**

- Restore a working chat against the sealed-token backend: responses
  render, follow-ups echo the token, option buttons work again.
- Surface backend errors (sanitization 400s, network failures) in the
  chat instead of crashing.

**Non-Goals:**

- Decrypting or inspecting the state token (no secret client-side, by
  design).
- Restructuring components (`BotResponse.vue` option rendering is
  unchanged and title-based options work).
- Autobot demo mode (`formatAutobotMessage`) — it never touches the
  backend.
- Backend changes (owned by the `expose-response-options` /
  sealed-token changes in `auenBot/botCtl`).

## Decisions

### D1: Echo by spreading the previous response, minus `context`

Keep the existing spread pattern (`postMsg = { ...lastMsg.backendData }`)
— it already carries `state`, `session`, and the odd `"<lang>":
"<lang>"` key (ignored by the backend schema) — then overwrite
`message`, increment `sequence`, set `lang`, and `delete postMsg.context`
(harmless on new responses, defensive for stale chats). All
`postMsg.context.*` mutation lines are deleted: `last_input`/
`last_intent` are server-side now. Rationale: minimal diff; the spread
already implements the echo contract correctly.

### D2: Rendering gate = `state` + `message`

`formatBotMessage` returns a rendered bubble only when the payload has
a `state` token and a `message` object. Options are read from
`message.options` (the plaintext field added by the backend's
`expose-response-options` change). Rationale: the gate mirrors the
backend's actual response shape; anything else (400 wrappers, health
checks) must not produce bubbles.

### D3: Error bubbles instead of crashes

`backendComms.handleBackendResponse` keeps returning the null-data
wrapper on errors; `ChatPane.appendChatMessage` checks for it and
appends a user-language-agnostic error bubble (e.g. "Ich konnte deine
Nachricht leider nicht verarbeiten. Bitte versuche es erneut.") with
`type: "error"` (rendered like a bot bubble), resetting `loading`.
Rationale: sanitization 400s are now ordinary user outcomes; a stuck
spinner is worse than an honest error message. No toast/global state
needed for v1.

### D4: Cleanup of dead contract code

Remove `context: {}` from the first-request literal and from
`App.vue`'s dummy post. Rationale: the schema ignores unknown fields,
but keeping them invites future confusion about which contract is live.

## Risks / Trade-offs

- [Stale chats after backend redeploy] → A token sealed with an old
  secret becomes invalid (backend rejects with 400) → error bubble
  (D3) and the user starts a new conversation. Acceptable; the
  frontend does not persist tokens across reloads (in-memory only).
- [Autobot mode still demo-only] → Unchanged; real conversations
  require `backendReady`, as before.
- [Error bubble styling] → Reuses the bot bubble component; a distinct
  style is cosmetic polish, deferred.

## Migration Plan

1. Rework `ChatPane.vue` (D1–D3) and clean `App.vue` (D4).
2. Run the dev server against the updated backend
   (`STATE_TOKEN_SECRET` set) and manually walk the contract: first
   message → token echo → frosch options with buttons → pick →
   content; gibberish ×3 → breakout invitation renders.
3. Rollback: revert the branch; the backend's additive `options` field
   harms nothing on the old frontend except the already-broken
   `context` gate.

## Open Questions

(none)
