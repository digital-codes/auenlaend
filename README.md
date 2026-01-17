# AUENLÄND Chatbot

A simple, conversational chatbot application written in Python.

## Features

- Interactive CLI-based chat interface
- Conversation history tracking
- Pattern-based response system
- Built-in commands (help, history, clear, exit)
- Friendly and responsive interactions

## Installation

This chatbot requires Python 3.6 or higher. No external dependencies are needed.

### Clone the repository

```bash
git clone https://github.com/digital-codes/auenlaend.git
cd auenlaend
```

### (Optional) Install dependencies

```bash
pip install -r requirements.txt
```

Note: Currently, no external dependencies are required.

## Usage

### Running the chatbot

```bash
python3 chatbot.py
```

or make it executable:

```bash
chmod +x chatbot.py
./chatbot.py
```

### Available Commands

Once the chatbot is running, you can use these commands:

- `help` - Display help information and available commands
- `history` - Show the conversation history
- `clear` - Clear the conversation history
- `exit` or `quit` - Exit the chatbot

### Example Interaction

```
==================================================
Welcome to AUENLÄND Bot!
==================================================
Type 'help' for available commands or 'exit' to quit.

You: hello
AUENLÄND Bot: Hi there! What would you like to talk about?

You: what can you do?
AUENLÄND Bot: I'm a chatbot designed to have conversations with you. I can respond to your messages, remember our conversation, and answer simple questions. Type 'help' to see available commands.

You: thanks
AUENLÄND Bot: You're welcome!

You: exit
AUENLÄND Bot: Goodbye! Have a great day!
```

## How It Works

The AUENLÄND chatbot uses pattern matching to recognize common phrases and questions, then provides appropriate responses. It maintains a conversation history that can be reviewed or cleared during the session.

### Key Features:

- **Greeting Recognition**: Responds to greetings like "hello", "hi", "hey"
- **Context Awareness**: Recognizes questions about itself and provides relevant information
- **History Management**: Tracks all interactions with timestamps
- **Random Response Variation**: Provides varied responses to keep conversations natural

## Development

### Project Structure

```
auenlaend/
├── chatbot.py           # Main chatbot application
├── requirements.txt     # Python dependencies (currently empty)
└── README.md           # This file
```

### Extending the Chatbot

To add new response patterns, edit the `responses` dictionary in the `AuenlaendChatbot` class within `chatbot.py`.

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.