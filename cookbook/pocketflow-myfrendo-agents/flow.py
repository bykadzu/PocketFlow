"""
Main flow that orchestrates the Myfrendo AI Agent Team.
Connects the orchestrator with all personas.
"""
from pocketflow import Flow, BatchNode
from orchestrator import OrchestratorClassifier, OrchestratorSynthesizer, OrchestratorReporter
from personas import get_available_personas


class PersonaBatchExecutor(BatchNode):
    """
    Execute multiple personas in batch (parallel or sequential).
    """

    def __init__(self):
        super().__init__()
        self.personas = get_available_personas()

    def prep(self, shared):
        """
        Prepare the list of personas to execute based on orchestrator's decision.
        Returns a list where each item will be processed by exec.
        """
        personas_to_activate = shared.get("personas_to_activate", [])

        if not personas_to_activate:
            print("⚠️  No personas activated, using default set")
            personas_to_activate = ["graham", "hormozi"]

        print(f"\n🎭 Activating {len(personas_to_activate)} personas...")

        # Return list of persona names to execute
        return personas_to_activate

    def exec(self, persona_name):
        """
        Execute a single persona.
        This is called for each item in the list returned by prep.
        """
        if persona_name not in self.personas:
            print(f"⚠️  Persona '{persona_name}' not found, skipping")
            return None

        print(f"   🤖 Activating {persona_name}...")
        return persona_name  # Just return the name, actual execution in post

    def post(self, shared, prep_res, exec_res):
        """
        Execute all personas and collect their outputs.
        """
        personas_to_run = [name for name in exec_res if name]

        for persona_name in personas_to_run:
            if persona_name in self.personas:
                persona = self.personas[persona_name]
                # Run the persona
                persona.run(shared)


def create_myfrendo_flow():
    """
    Create the complete Myfrendo AI Agent Team flow.

    Flow structure:
    1. OrchestratorClassifier - Analyzes request and decides which personas to activate
    2. PersonaBatchExecutor - Executes selected personas in batch
    3. OrchestratorSynthesizer - Synthesizes all persona outputs
    4. OrchestratorReporter - Formats and displays final report
    """
    # Create nodes
    classifier = OrchestratorClassifier()
    persona_executor = PersonaBatchExecutor()
    synthesizer = OrchestratorSynthesizer()
    reporter = OrchestratorReporter()

    # Create flow and set start node
    flow = Flow(start=classifier)

    # Connect the flow
    classifier >> persona_executor >> synthesizer >> reporter

    return flow


if __name__ == "__main__":
    # Test the flow
    print("Testing Myfrendo AI Agent Team Flow...")
    print("="*80)

    # Create test question
    shared = {
        "question": "How should we get our first 5 real estate agency customers?"
    }

    # Create and run flow
    flow = create_myfrendo_flow()
    flow.run(shared)

    print("\n" + "="*80)
    print("Flow execution complete!")
    print("="*80)
