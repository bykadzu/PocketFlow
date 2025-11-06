"""
Main entry point for the Myfrendo AI Agent Team.
Run this to interact with the agent team.
"""
import os
import sys
from flow import create_myfrendo_flow
from tools import tool_registry


def print_welcome():
    """Print welcome message."""
    print("""
╔════════════════════════════════════════════════════════════════════════════╗
║                  MYFRENDO AI AGENT TEAM                                    ║
║                  Business that boosts businesses                           ║
╚════════════════════════════════════════════════════════════════════════════╝

Your 5-person expert team:
  🧠 Orchestrator   - Mission control & synthesis
  📚 Graham         - Startup philosophy & bootstrapping
  💰 Hormozi        - Offer crafting & value stacking
  🤖 Karpathy       - AI/ML engineering
  🏠 Real Estate Vet - Industry domain expertise

The Orchestrator will automatically select the right personas for your question.
Type 'help' for example questions, 'quit' to exit.
""")


def print_help():
    """Print example questions."""
    print("""
Example questions you can ask:

STRATEGY:
• How should we get our first customer?
• Should we raise funding or stay bootstrapped?
• What's our competitive moat in real estate AI?

PRODUCT & PRICING:
• How should we price our voice agent service?
• What guarantees should we offer to reduce risk?
• How do we make our offer irresistible?

TECHNICAL:
• Which LLM should we use for voice agents?
• How can we reduce voice latency below 400ms?
• What's the most cost-effective tech stack?

DOMAIN-SPECIFIC:
• What are the biggest pain points for real estate agents?
• How do we handle TCPA compliance for cold calling?
• What conversion rate should we expect?

OPERATIONS:
• How do we scale from 10 to 100 customers?
• What metrics should we track daily?
• How do we onboard new agency customers?

Just ask naturally - the Orchestrator will route to the right experts!
""")


def run_interactive_mode():
    """Run in interactive CLI mode."""
    print_welcome()

    # Create the flow once
    flow = create_myfrendo_flow()

    while True:
        print("\n" + "─"*80)
        user_input = input("\n💬 Your question: ").strip()

        if not user_input:
            continue

        if user_input.lower() in ['quit', 'exit', 'q']:
            print("\n👋 Thanks for using Myfrendo AI Agent Team!")
            break

        if user_input.lower() == 'help':
            print_help()
            continue

        # Run the agent team
        print("\n" + "="*80)
        shared = {"question": user_input}

        try:
            flow.run(shared)
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("Please try again or type 'help' for examples.")


def run_single_question(question: str):
    """Run a single question and exit."""
    print_welcome()
    print(f"\n💬 Question: {question}")
    print("\n" + "="*80)

    shared = {"question": question}
    flow = create_myfrendo_flow()

    try:
        flow.run(shared)
        print("\n✅ Analysis complete!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


def main():
    """Main entry point."""
    # Check for OpenAI API key
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY environment variable not set")
        print("Please set it with: export OPENAI_API_KEY='your-key-here'")
        sys.exit(1)

    # Parse command line arguments
    if len(sys.argv) > 1:
        # Single question mode
        question = " ".join(sys.argv[1:])
        if question.startswith("--"):
            question = question[2:]  # Remove -- prefix
        run_single_question(question)
    else:
        # Interactive mode
        run_interactive_mode()


if __name__ == "__main__":
    main()
