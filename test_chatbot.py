#!/usr/bin/env python3
"""
Unit tests for AUENLÄND Chatbot
"""

import unittest
from chatbot import AuenlaendChatbot


class TestAuenlaendChatbot(unittest.TestCase):
    """Test cases for the AuenlaendChatbot class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.chatbot = AuenlaendChatbot()
    
    def test_initialization(self):
        """Test chatbot initialization."""
        self.assertEqual(self.chatbot.name, "AUENLÄND Bot")
        self.assertEqual(len(self.chatbot.conversation_history), 0)
    
    def test_greeting_response(self):
        """Test greeting recognition."""
        response, should_exit = self.chatbot.get_response("hello")
        self.assertFalse(should_exit)
        self.assertIsInstance(response, str)
        self.assertGreater(len(response), 0)
    
    def test_exit_command(self):
        """Test exit command."""
        response, should_exit = self.chatbot.get_response("exit")
        self.assertTrue(should_exit)
        self.assertGreater(len(response), 0)
    
    def test_help_command(self):
        """Test help command."""
        response, should_exit = self.chatbot.get_response("help")
        self.assertFalse(should_exit)
        self.assertIn("help", response.lower())
        self.assertIn("history", response.lower())
    
    def test_history_tracking(self):
        """Test conversation history tracking."""
        self.chatbot.get_response("hello")
        self.chatbot.add_to_history("hello", "Hi there!")
        self.assertEqual(len(self.chatbot.conversation_history), 1)
        self.assertEqual(self.chatbot.conversation_history[0]["user"], "hello")
    
    def test_clear_history(self):
        """Test clearing conversation history."""
        self.chatbot.add_to_history("test", "response")
        response, should_exit = self.chatbot.get_response("clear")
        self.assertFalse(should_exit)
        self.assertEqual(len(self.chatbot.conversation_history), 0)
    
    def test_thanks_response(self):
        """Test thanks recognition."""
        response, should_exit = self.chatbot.get_response("thanks")
        self.assertFalse(should_exit)
        self.assertGreater(len(response), 0)
    
    def test_name_question(self):
        """Test name question response."""
        response, should_exit = self.chatbot.get_response("what is your name")
        self.assertFalse(should_exit)
        self.assertIn("AUENLÄND Bot", response)


if __name__ == "__main__":
    unittest.main()
