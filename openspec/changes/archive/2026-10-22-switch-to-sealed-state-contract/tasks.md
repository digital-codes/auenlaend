# Tasks

## 1. Response rendering under the sealed-token layout

- [x] 1.1 In `ChatPane.vue` `formatBotMessage`: replace the `message.context` gate with `message.state` + `message.message`, and read options from `message.options` instead of `message.context.options`; verify in the browser: a bot answer against the updated backend renders its text bubble (no empty bubbles, no console TypeError)
- [x] 1.2 Verify media rendering is unchanged: an answer with image/audio/link (e.g. the Reh answer) shows the image, audio player, and link as before

## 2. Request echo of the state token

- [x] 2.1 In `ChatPane.vue` `appendChatMessage`: build follow-up requests by echoing `state`/`session` from the previous response, incrementing `sequence`, setting `message` and `lang`, and removing all `postMsg.context` reading/mutation (including the `last_intent`/`last_input` block); verify in the browser: a multi-turn conversation (e.g. "was macht das reh" → "und wie groß ist sie?") works with the state token echoed and no TypeError in the console
- [x] 2.2 Remove `context: {}` from the first-request literal and from the dummy post in `App.vue`; verify the first message still starts a conversation (backend assigns session and returns the first token)

## 3. Option buttons and error resilience

- [x] 3.1 Verify option buttons render from `message.options` end-to-end: "gibt es da frösche" shows the five species buttons, clicking one sends it as the user message and completes the flow with content; also verify the feature-fallback prompt (e.g. "wie groß ist das reh" → pick "Reh") offers ≤ 3 feature buttons and picking one answers
- [x] 3.2 Implement the error bubble in `appendChatMessage` (design D3): on `null`-data responses (sanitization 400 or network failure) append an error bubble, reset `loading`, and keep the input usable; verify in the browser: an input with `&` or `<script>` shows the error bubble and the next message works normally

## 4. End-to-end regression walk

- [x] 4.1 Walk the full happy path in the browser against the updated backend: reh answer → size follow-up (focus) → frosch options → pick → content → breakout after three gibberish inputs (invitation bubble renders, next question starts fresh)

## Workflow follow-up

- Archive the change after the review requirements are satisfied.
- Deploy frontend and backend in lockstep (the backend's `options` field and the frontend switch are one contract).
