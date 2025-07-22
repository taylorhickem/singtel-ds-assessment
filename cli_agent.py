#!/usr/bin/env python3
"""Command Line Interface for interacting with Roaming Plan Agent
"""
# dependencies --------------------------------------------------------------
from dotenv import load_dotenv
from recommend_agent.chat_agent import RoamingPlanAgent


# entry point --------------------------------------------------------------
def main():
    load_dotenv()
    print("📱 Welcome to the Roaming Plan Assistant CLI")
    print("Type 'exit' or 'quit' to leave the session.")
    print("--------------------------------------------------")

    agent = RoamingPlanAgent()
    
    while True:
        user_input = input("👤 You: ").strip()
        if user_input.lower() in ("exit", "quit"):
            print("👋 Goodbye!")
            break
        
        result = agent.step(user_input)

        # Handle response based on type
        if "prompt" in result:
            print("🤖 Agent:", result["prompt"])
        elif "confirmation" in result:
            print("🚀", result["confirmation"])
            print("📦 Purchase payload:", result["plan_payload"])
        elif "selected_plan" in result:
            print("✅ You selected:")
            print(result["selected_plan"])
            print("Type 'confirm' to proceed or 'cancel' to choose again.")
        elif "response" in result:
            print("🤖 Agent:", result["response"])
        elif "plans" in result and result["plans"]:
            print("📦 Recommended Plans:")
            for idx, plan in enumerate(result["plans"], 1):
                print(f"  Option {idx}: {plan}")
            print("Reply with 'option 1', 'option 2', etc. to select a plan.")
        elif "selected_plan" in result:
            print("✅ You selected:")
            print(result["selected_plan"])
        elif "error" in result:
            print("❌ Error:", result["error"])
        else:
            print("🤖 (No response)")


if __name__ == "__main__":
    main()
