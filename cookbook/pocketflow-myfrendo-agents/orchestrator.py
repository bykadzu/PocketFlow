"""
The Orchestrator - Master coordinator that routes requests to personas
and synthesizes their outputs into coherent recommendations.
"""
from pocketflow import Node
from utils import call_llm, extract_yaml_from_response
import yaml
import json


class OrchestratorClassifier(Node):
    """
    First step: Classify the user's request to determine which personas to activate.
    """

    def prep(self, shared):
        """Get the user's question."""
        return shared.get("question", "")

    def exec(self, question):
        """Classify the request type and determine which personas to activate."""
        print(f"🎯 Orchestrator analyzing request...")

        prompt = f"""You are the Orchestrator AI for Myfrendo, coordinating a team of expert personas.

Your team:
1. Graham - Startup philosophy, bootstrapping, product-market fit, doing things that don't scale
2. Hormozi - Offer crafting, value stacking, pricing, guarantees, sales psychology
3. Karpathy - AI/ML engineering, model selection, technical implementation, cost optimization
4. Real Estate Vet - Industry expertise, agent workflows, compliance, practical reality checks

## USER QUESTION
{question}

## YOUR TASK
Analyze this question and determine:
1. What type of request is this? (strategy, product, sales, technical, domain-specific, or general)
2. Which personas should analyze this question?
3. What's the priority/sequence? (parallel or sequential)

Respond in this format:
```yaml
request_type: <strategy|product|sales|technical|domain|general>
reasoning: |
  <Why you classified it this way>
personas_to_activate:
  - <persona_name>
  - <persona_name>
execution_mode: <parallel|sequential>
context_needed:
  <any key-value pairs of context you need>
```

Guidelines:
- Strategy questions → Graham, Real Estate Vet
- Sales/Pricing questions → Hormozi, Real Estate Vet
- Technical/AI questions → Karpathy, possibly Graham for feasibility
- Product questions → All personas for comprehensive view
- Industry-specific → Real Estate Vet essential, plus others as needed
- General → Start with 2-3 most relevant personas
"""

        response = call_llm(prompt, model="gpt-4o")
        yaml_str = extract_yaml_from_response(response)
        classification = yaml.safe_load(yaml_str)

        print(f"   Type: {classification.get('request_type')}")
        print(f"   Activating: {', '.join(classification.get('personas_to_activate', []))}")

        return classification

    def post(self, shared, prep_res, exec_res):
        """Save classification results."""
        shared["request_type"] = exec_res.get("request_type", "general")
        shared["personas_to_activate"] = exec_res.get("personas_to_activate", [])
        shared["execution_mode"] = exec_res.get("execution_mode", "parallel")
        shared["context"] = exec_res.get("context_needed", {})
        shared["classification_reasoning"] = exec_res.get("reasoning", "")


class OrchestratorSynthesizer(Node):
    """
    Final step: Synthesize all persona outputs into a coherent, actionable response.
    """

    def prep(self, shared):
        """Get all persona outputs and the original question."""
        return {
            "question": shared.get("question", ""),
            "request_type": shared.get("request_type", ""),
            "persona_outputs": shared.get("persona_outputs", []),
            "classification_reasoning": shared.get("classification_reasoning", "")
        }

    def exec(self, inputs):
        """Synthesize persona insights into final recommendation."""
        question = inputs["question"]
        request_type = inputs["request_type"]
        persona_outputs = inputs["persona_outputs"]

        print(f"\n🧠 Orchestrator synthesizing {len(persona_outputs)} persona insights...")

        # Format persona outputs for the synthesizer
        persona_summaries = []
        for output in persona_outputs:
            persona_summaries.append({
                "persona": output["persona"],
                "key_insights": output.get("key_insights", []),
                "recommendation": output["output"],
                "confidence": output.get("confidence", 50)
            })

        prompt = f"""You are the Orchestrator AI for Myfrendo. You've gathered insights from expert personas.

## ORIGINAL QUESTION
{question}

## REQUEST TYPE
{request_type}

## PERSONA INSIGHTS
{json.dumps(persona_summaries, indent=2)}

## YOUR TASK
Synthesize these diverse perspectives into a coherent, actionable response for the user.

Your synthesis should:
1. Identify common themes and agreements across personas
2. Highlight valuable disagreements or different perspectives
3. Prioritize insights by relevance and confidence
4. Provide clear, actionable recommendations
5. Note any tools/actions needed
6. Be concise but comprehensive

Respond in this format:
```yaml
executive_summary: |
  <2-3 sentence summary of the recommendation>

key_insights:
  - insight: <Insight 1>
    sources: [<persona names who agree>]
    confidence: <average confidence>
  - insight: <Insight 2>
    sources: [<persona names>]
    confidence: <confidence>

recommended_actions:
  - action: <Specific action to take>
    priority: <high|medium|low>
    owner: <who should do this>
    rationale: <why this action based on persona insights>

areas_of_agreement:
  - <What all/most personas agreed on>

areas_of_disagreement:
  - <Where personas had different views, if any>

next_steps:
  - <Immediate next step 1>
  - <Immediate next step 2>

tools_to_use:
  - <Any tools mentioned by personas>
```
"""

        response = call_llm(prompt, model="gpt-4o")
        yaml_str = extract_yaml_from_response(response)
        synthesis = yaml.safe_load(yaml_str)

        return synthesis

    def post(self, shared, prep_res, exec_res):
        """Save the final synthesis."""
        shared["final_synthesis"] = exec_res
        print(f"✅ Orchestrator synthesis complete")


class OrchestratorReporter(Node):
    """
    Format the final response for the user in a clean, readable format.
    """

    def prep(self, shared):
        """Get the synthesis and question."""
        return {
            "question": shared.get("question", ""),
            "synthesis": shared.get("final_synthesis", {}),
            "persona_outputs": shared.get("persona_outputs", [])
        }

    def exec(self, inputs):
        """Format the final report."""
        synthesis = inputs["synthesis"]
        question = inputs["question"]

        # Build formatted output
        report = []
        report.append("="*80)
        report.append("MYFRENDO AI AGENT TEAM - ANALYSIS REPORT")
        report.append("="*80)
        report.append(f"\n📝 Question: {question}\n")

        # Executive Summary
        report.append("🎯 EXECUTIVE SUMMARY")
        report.append("-" * 80)
        report.append(synthesis.get("executive_summary", "No summary available"))
        report.append("")

        # Key Insights
        report.append("💡 KEY INSIGHTS")
        report.append("-" * 80)
        for i, insight in enumerate(synthesis.get("key_insights", []), 1):
            sources = ", ".join(insight.get("sources", []))
            confidence = insight.get("confidence", "N/A")
            report.append(f"{i}. {insight.get('insight', '')}")
            report.append(f"   Sources: {sources} | Confidence: {confidence}%")
            report.append("")

        # Recommended Actions
        report.append("🚀 RECOMMENDED ACTIONS")
        report.append("-" * 80)
        for i, action in enumerate(synthesis.get("recommended_actions", []), 1):
            priority = action.get("priority", "medium").upper()
            report.append(f"{i}. [{priority}] {action.get('action', '')}")
            report.append(f"   Owner: {action.get('owner', 'N/A')}")
            report.append(f"   Why: {action.get('rationale', '')}")
            report.append("")

        # Next Steps
        report.append("✅ IMMEDIATE NEXT STEPS")
        report.append("-" * 80)
        for i, step in enumerate(synthesis.get("next_steps", []), 1):
            report.append(f"{i}. {step}")
        report.append("")

        # Agreement/Disagreement
        if synthesis.get("areas_of_agreement"):
            report.append("🤝 TEAM CONSENSUS")
            report.append("-" * 80)
            for item in synthesis["areas_of_agreement"]:
                report.append(f"• {item}")
            report.append("")

        if synthesis.get("areas_of_disagreement"):
            report.append("🔀 DIFFERING PERSPECTIVES")
            report.append("-" * 80)
            for item in synthesis["areas_of_disagreement"]:
                report.append(f"• {item}")
            report.append("")

        # Tools
        if synthesis.get("tools_to_use"):
            report.append("🛠️  TOOLS TO USE")
            report.append("-" * 80)
            for tool in synthesis["tools_to_use"]:
                report.append(f"• {tool}")
            report.append("")

        report.append("="*80)
        report.append(f"Analyzed by {len(inputs['persona_outputs'])} expert personas")
        report.append("="*80)

        return "\n".join(report)

    def post(self, shared, prep_res, exec_res):
        """Save and print the final report."""
        shared["final_report"] = exec_res
        print("\n" + exec_res)


if __name__ == "__main__":
    # Test the orchestrator classifier
    print("Testing Orchestrator Classifier...")

    shared = {
        "question": "How should we price our voice agent service for real estate agencies?"
    }

    classifier = OrchestratorClassifier()
    classifier.run(shared)

    print(f"\nClassification result:")
    print(f"Request type: {shared.get('request_type')}")
    print(f"Personas to activate: {shared.get('personas_to_activate')}")
    print(f"Execution mode: {shared.get('execution_mode')}")
