#!/usr/bin/env python3
"""
AUENLÄND Chatbot - A simple conversational chatbot
"""

import sys
import random
from datetime import datetime


class AuenlaendChatbot:
    """A simple chatbot with conversational capabilities."""
    
    def __init__(self):
        self.name = "AUENLÄND Bot"
        self.conversation_history = []
        self.responses = {
            "greetings": [
                "Hello! How can I help you today?",
                "Hi there! What would you like to talk about?",
                "Greetings! I'm here to chat with you.",
            ],
            "farewell": [
                "Goodbye! Have a great day!",
                "See you later! Take care!",
                "Farewell! It was nice chatting with you!",
            ],
            "thanks": [
                "You're welcome!",
                "My pleasure!",
                "Happy to help!",
            ],
            "help": [
                "I'm AUENLÄND Bot, here to chat with you!\n"
                "You can ask me questions, have a conversation, or use these commands:\n"
                "  - 'help' - Show this help message\n"
                "  - 'history' - Show conversation history\n"
                "  - 'clear' - Clear conversation history\n"
                "  - 'exit' or 'quit' - End the conversation"
            ],
            "default": [
                "That's interesting! Tell me more.",
                "I see. What else would you like to discuss?",
                "Thanks for sharing that with me!",
                "Fascinating! Can you elaborate?",
            ]
        }
        
    def add_to_history(self, user_input, bot_response):
        """Add an interaction to conversation history."""
        self.conversation_history.append({
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "user": user_input,
            "bot": bot_response
        })
    
    def get_response(self, user_input):
        """Generate a response based on user input."""
        user_input_lower = user_input.lower().strip()
        
        # Command handling
        if user_input_lower in ["exit", "quit", "bye", "goodbye"]:
            return random.choice(self.responses["farewell"]), True
        
        if user_input_lower in ["help", "?", "help me"]:
            return self.responses["help"][0], False
        
        if user_input_lower == "history":
            if not self.conversation_history:
                return "No conversation history yet.", False
            history_text = "\n--- Conversation History ---\n"
            for entry in self.conversation_history:
                history_text += f"[{entry['timestamp']}]\n"
                history_text += f"You: {entry['user']}\n"
                history_text += f"Bot: {entry['bot']}\n\n"
            return history_text, False
        
        if user_input_lower == "clear":
            self.conversation_history = []
            return "Conversation history cleared.", False
        
        # Pattern-based responses
        if any(word in user_input_lower for word in ["hello", "hi", "hey", "greetings"]):
            return random.choice(self.responses["greetings"]), False
        
        if any(word in user_input_lower for word in ["thank", "thanks", "thx"]):
            return random.choice(self.responses["thanks"]), False
        
        if "name" in user_input_lower and ("your" in user_input_lower or "you" in user_input_lower):
            return f"My name is {self.name}. What's yours?", False
        
        if "how are you" in user_input_lower:
            return "I'm doing great, thank you for asking! How are you?", False
        
        if "what can you do" in user_input_lower or "what do you do" in user_input_lower:
            return "I'm a chatbot designed to have conversations with you. I can respond to your messages, remember our conversation, and answer simple questions. Type 'help' to see available commands.", False
        
        # Default response
        return random.choice(self.responses["default"]), False
    
    def run(self):
        """Main chatbot loop."""
        print("=" * 50)
        print(f"Welcome to {self.name}!")
        print("=" * 50)
        print("Type 'help' for available commands or 'exit' to quit.\n")
        
        while True:
            try:
                user_input = input("You: ").strip()
                
                if not user_input:
                    continue
                
                response, should_exit = self.get_response(user_input)
                print(f"{self.name}: {response}\n")
                
                if not should_exit:
                    self.add_to_history(user_input, response)
                
                if should_exit:
                    break
                    
            except KeyboardInterrupt:
                print(f"\n\n{self.name}: Goodbye!")
                break
            except EOFError:
                print(f"\n\n{self.name}: Goodbye!")
                break


def main():
    """Entry point for the chatbot."""
    chatbot = AuenlaendChatbot()
    chatbot.run()


if __name__ == "__main__":
    main()
