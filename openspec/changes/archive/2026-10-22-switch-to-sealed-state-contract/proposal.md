# Proposal

## Why

The backend (`auenBot/botCtl`) replaced the plaintext `context`
round-trip with an opaque sealed `state` token, moved conversation
state server-side (focus, last input/intent), and now exposes
user-facing option lists as a plaintext `options` field next to the
token. The frontend is hard-broken against that contract: every bot
reply renders empty (`formatBotMessage` gates on `message.context`),
the second message onward crashes with a TypeError (the request
builder mutates `postMsg.context`, which no longer exists), option
buttons never render (options were read from the gone `context`), and
backend 400s (input sanitization) or network errors crash the chat
loop on `null` data. Deploying the backend without this change leaves
the chat unusable.

## What Changes

- **Response gate**: `formatBotMessage` in `ChatPane.vue` accepts a
  response when it carries the sealed `state` token and a `message`;
  the `context` gate is removed. Rendering of
  `message.text/image/audio/link` is unchanged.
- **Options rendering**: option buttons read the new plaintext
  `message.options` field (title dicts from the backend's
  `expose-response-options` change) instead of
  `message.context.options`.
- **Request echo**: the next request is built from the previous
  response by echoing `state`, `session`, and `sequence + 1` with a
  new `message` and the selected `lang`; all `context` reading and
  mutation (`last_intent`, `last_input`) is removed — that state is
  server-side now. The first request carries no `state`.
- **Error resilience**: backend 400 responses (input sanitization) and
  network failures no longer crash `appendChatMessage`; the user sees
  an error bubble in the chat and the loading state resets.
- Cleanup: `context: {}` removed from the first request and from the
  backend-check dummy post in `App.vue`.

## Capabilities

### New Capabilities

- `sealed-state-contract`: The frontend side of the sealed-token API
  contract — echoing the opaque state token, rendering responses and
  options under the new field layout, and degrading gracefully on
  backend errors.

### Modified Capabilities

(none)

## Impact

- **Code**: `src/components/ChatPane.vue` (gate, echo, error
  handling), `src/App.vue` (dummy post cleanup). No new dependencies,
  no routing or component-structure changes; `BotResponse.vue` option
  rendering is unchanged (title-based options work as-is).
- **Backend dependency**: requires the `expose-response-options`
  backend change (options field) and the sealed-token backend
  (`add-encrypted-state-tokens`); deploy in lockstep.
- **Security**: the frontend never sees the sealing secret — it can
  neither read nor forge conversation state; it only echoes opaque
  tokens.
- **Not affected**: i18n, layout, `BotResponse.vue` display logic,
  autobot demo mode, backend comms service structure.
