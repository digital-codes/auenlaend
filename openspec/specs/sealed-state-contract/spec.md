# sealed-state-contract Specification

## Purpose

Implements the frontend side of the sealed-token API contract: echo
the opaque state token between requests, render bot responses and
option lists under the new field layout, and degrade gracefully when
the backend rejects or cannot be reached.

## Requirements

### Requirement: Requests echo the opaque state token

The first request of a conversation SHALL carry no `state` value. Every
subsequent request SHALL echo the `state` token from the most recent
bot response, together with that response's `session` id, an
incremented `sequence`, a new `message`, and the selected language.
The frontend SHALL NOT read, modify, or reconstruct conversation state
— no `context` object SHALL be sent.

#### Scenario: First request starts a conversation

- **WHEN** the user sends the first message with no prior bot response
- **THEN** the request carries the message, an empty session, sequence
  1, the language, and no `state` field and no `context` field

#### Scenario: Follow-up requests echo the token

- **WHEN** a bot response carried a `state` token and the user sends
  the next message
- **THEN** the request echoes that `state` token and `session`, with
  `sequence` incremented and the new message text

#### Scenario: Conversation state is not reconstructed client-side

- **WHEN** a follow-up request is built
- **THEN** no `context` field is sent and no intent, entity, or
  feature values are read from previous responses

### Requirement: Bot responses render under the sealed-token layout

A bot response SHALL be rendered when it carries a `state` token and a
`message`; the response's `message.text`, `message.image`,
`message.audio`, and `message.link` SHALL be displayed as before. A
response without a `state` token SHALL NOT render as a chat message.

#### Scenario: Sealed response renders its message content

- **WHEN** the backend responds with a `state` token and a message
  containing text (and optionally image, audio, or link)
- **THEN** the bot bubble displays that content

#### Scenario: Responses without a token do not render

- **WHEN** a payload without a `state` token arrives
- **THEN** no empty bot bubble is appended to the chat

### Requirement: Option lists render from the plaintext options field

When a bot response carries an `options` field, the frontend SHALL
render its entries as selectable option buttons (title-based, as
before). Selecting an option SHALL send the option title as the next
user message. The `options` field SHALL be read from the response
root, not from any context object.

#### Scenario: Option prompt renders buttons

- **WHEN** the backend offers choices (e.g. the five frosch species)
  and the response carries the plaintext `options` list
- **THEN** the bot bubble shows the option buttons with their titles

#### Scenario: Selected option is sent as user input

- **WHEN** the user clicks an option button
- **THEN** the option title is sent as the next user message, echoing
  the current state token

#### Scenario: Responses without options show no buttons

- **WHEN** a bot response carries no `options` field
- **THEN** no option buttons are rendered

### Requirement: Backend errors degrade gracefully in the chat

When the backend responds with an error status (e.g. HTTP 400 for
sanitization-rejected input) or is unreachable, the frontend SHALL
append a visible error bubble to the chat, reset the loading state,
and keep the conversation usable. The error SHALL NOT crash the
message flow or leave the input permanently disabled.

#### Scenario: Sanitization rejection is shown to the user

- **WHEN** the backend rejects an input with HTTP 400 (e.g. HTML tags
  or injection-prone characters in the message)
- **THEN** an error bubble appears in the chat, the loading spinner
  stops, and the user can send a new message

#### Scenario: Network failure is shown to the user

- **WHEN** the backend is unreachable or the request fails
- **THEN** an error bubble appears in the chat and the conversation
  remains usable
