#!/usr/bin/env python3
"""Command Line Interface for interacting with Roaming Plan Agent
"""
# dependencies ---------------------------------------------------
from recommend_agent.chat_agent import DialogueManager


# entry point ---------------------------------------------------
def run():
    DialogueManager().run()


if __name__ == "__main__":
    run()