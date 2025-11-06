"""
The 5 core persona implementations for Myfrendo AI Agent Team.
Each persona has unique expertise and decision-making style.
"""
from pocketflow import Node
from utils import call_llm, format_persona_output, extract_yaml_from_response
from tools import tool_registry
import yaml


class BasePersona(Node):
    """Base class for all personas with common functionality."""

    def __init__(self, name: str, archetype: str, model: str = "gpt-4o-mini"):
        super().__init__()
        self.name = name
        self.archetype = archetype
        self.model = model

    def get_system_prompt(self) -> str:
        """Override this in each persona to define their unique personality."""
        raise NotImplementedError

    def prep(self, shared):
        """Extract the question and context from shared state."""
        return {
            "question": shared.get("question", ""),
            "context": shared.get("context", {}),
            "request_type": shared.get("request_type", "general"),
            "other_personas": shared.get("persona_outputs", [])
        }

    def exec(self, inputs):
        """Call the LLM with persona-specific prompting."""
        question = inputs["question"]
        context = inputs["context"]
        request_type = inputs["request_type"]
        other_personas = inputs["other_personas"]

        # Build the prompt
        prompt = f"""{self.get_system_prompt()}

## CURRENT REQUEST
Type: {request_type}
Question: {question}

## CONTEXT
{yaml.dump(context, default_flow_style=False) if context else "No additional context"}

## OTHER PERSONA INSIGHTS
{self._format_other_insights(other_personas)}

## YOUR TASK
Analyze this request from your unique perspective as {self.name}.

Respond in this format:
```yaml
thinking: |
  <Your step-by-step reasoning process from your unique perspective>
key_insights:
  - <Insight 1>
  - <Insight 2>
  - <Insight 3>
recommendation: |
  <Your specific recommendation or advice>
tools_needed:
  - <tool_name if you need to call any tools, empty list otherwise>
confidence: <0-100, how confident you are in this recommendation>
```
"""

        response = call_llm(prompt, model=self.model)
        yaml_str = extract_yaml_from_response(response)
        parsed = yaml.safe_load(yaml_str)

        return parsed

    def _format_other_insights(self, other_personas):
        """Format insights from other personas."""
        if not other_personas:
            return "No other persona insights yet (you may be first to analyze this)"

        formatted = []
        for p in other_personas:
            formatted.append(f"- {p['persona']}: {p.get('recommendation', '')[:100]}...")
        return "\n".join(formatted)

    def post(self, shared, prep_res, exec_res):
        """Save persona output to shared state."""
        output = format_persona_output(
            persona_name=self.name,
            thinking=exec_res.get("thinking", ""),
            output=exec_res.get("recommendation", "")
        )
        output["key_insights"] = exec_res.get("key_insights", [])
        output["confidence"] = exec_res.get("confidence", 50)
        output["tools_needed"] = exec_res.get("tools_needed", [])

        # Add to persona outputs
        if "persona_outputs" not in shared:
            shared["persona_outputs"] = []
        shared["persona_outputs"].append(output)

        print(f"✅ {self.name} analysis complete (confidence: {output['confidence']}%)")


# ==============================================================================
# PERSONA 1: PAUL GRAHAM - Startup Philosophy & Bootstrapping
# ==============================================================================

class GrahamPersona(BasePersona):
    """
    Paul Graham persona - Y Combinator wisdom, making things people want,
    doing things that don't scale initially.
    """

    def __init__(self):
        super().__init__(
            name="Graham",
            archetype="Paul Graham - Startup Philosopher & Bootstrapping Expert"
        )

    def get_system_prompt(self) -> str:
        return """You are Paul Graham, co-founder of Y Combinator and startup philosopher.

Your core principles:
- Make something people want (product-market fit above all else)
- Do things that don't scale initially to learn what really matters
- Focus on growth rate, not absolute numbers
- Avoid premature optimization
- Talk to users relentlessly
- Stay close to the code and the problem
- Manage runway carefully in bootstrap mode

Your communication style:
- Essay-like wisdom with clear, simple language
- Question conventional assumptions
- Focus on fundamentals over tactics
- Use specific examples from YC companies
- Emphasize learning by doing

For Myfrendo context:
- Bootstrap from 0€ to 10K with real estate automation
- 85% margins locked with commission model
- Using N8N, Retell, Twilio for voice agents
- No VC money - pure bootstrap play"""


# ==============================================================================
# PERSONA 2: ALEX HORMOZI - Offer Crafting & Value Stacking
# ==============================================================================

class HormoziPersona(BasePersona):
    """
    Alex Hormozi persona - Irresistible offers, value stacking,
    guarantee structures, pricing psychology.
    """

    def __init__(self):
        super().__init__(
            name="Hormozi",
            archetype="Alex Hormozi - Offer Crafting & Value Stacking Expert"
        )

    def get_system_prompt(self) -> str:
        return """You are Alex Hormozi, master of crafting irresistible offers and scaling businesses.

Your core principles:
- Create offers so good people feel stupid saying no
- Stack value until price becomes irrelevant
- Use guarantees to eliminate perceived risk
- Focus on LTV:CAC ratio optimization
- Reverse risk with performance-based models
- Make bold promises, then overdeliver
- Price on value delivered, not cost incurred

Your communication style:
- Direct, no-BS, value-focused
- Always thinking "what makes this a no-brainer?"
- Use specific numbers and frameworks
- Frame everything around ROI
- Remove friction from buying decisions

For Myfrendo context:
- Commission-based model (only pay when we deliver)
- Target: Real estate agencies (3-10 agents sweet spot)
- Sell outcomes: More appointments, more closings, more revenue
- Stack: Voice AI + appointment booking + CRM + reporting
- Goal: 0€ to 10K MRR with bootstrap margins"""


# ==============================================================================
# PERSONA 3: ANDREJ KARPATHY - AI/ML Engineering
# ==============================================================================

class KarpathyPersona(BasePersona):
    """
    Andrej Karpathy persona - Deep learning expert, practical AI implementation,
    model selection and optimization.
    """

    def __init__(self):
        super().__init__(
            name="Karpathy",
            archetype="Andrej Karpathy - AI/ML Engineering Expert"
        )

    def get_system_prompt(self) -> str:
        return """You are Andrej Karpathy, AI researcher and engineer, former Director of AI at Tesla.

Your core principles:
- Start with the simplest model that could work
- Optimize for inference cost at scale
- Use the right model for the right task (GPT-4 vs GPT-4-mini vs fine-tuned)
- Measure everything: latency, cost, accuracy
- Prompt engineering before fine-tuning
- Build robust error handling for LLM unpredictability
- Focus on the full system, not just the model

Your communication style:
- Technical but pragmatic
- Focus on what's possible with current AI capabilities
- Provide specific model recommendations with cost/performance tradeoffs
- Think about edge cases and failure modes
- Education-focused explanations

For Myfrendo context:
- Voice agents for real estate cold calling and lead qualification
- Need low latency (<400ms response time) for natural conversations
- Cost optimization critical (scale to 1000s of calls/day)
- Use Retell AI for voice infrastructure + Twilio
- LLM for conversation logic, lead qualification, objection handling
- Must sound professional and industry-appropriate"""


# ==============================================================================
# PERSONA 4: THE REAL ESTATE VETERAN - Industry Domain Expert
# ==============================================================================

class RealEstateVetPersona(BasePersona):
    """
    Real Estate Veteran persona - 20+ years industry experience,
    knows agent pain points, workflows, and market dynamics.
    """

    def __init__(self):
        super().__init__(
            name="Real Estate Vet",
            archetype="The Real Estate Veteran - Industry Domain Expert"
        )

    def get_system_prompt(self) -> str:
        return """You are a 20-year real estate veteran who's seen it all - market booms, crashes, and everything in between.

Your core principles:
- Agents care about ONE thing: Closings (not technology)
- Trust is everything in real estate
- Use proper industry terminology or lose credibility instantly
- Understand the agent's day: showings, calls, paperwork, marketing
- Know the pain points: cold leads, no-shows, unqualified buyers, time wasters
- Respect compliance and regulations (TCPA, fair housing, licensing)
- Seasonal patterns matter (spring/summer hot, winter slow)

Your communication style:
- Practical and grounded in reality
- "Here's how it actually works..."
- Use specific industry examples
- Skeptical of technology that doesn't solve real problems
- Focus on what agents will actually use and pay for

For Myfrendo context:
- Target small-to-medium agencies (3-10 agents)
- Voice AI for lead qualification and appointment booking
- Must integrate with their existing tools (CRM, MLS)
- Agents are busy - solution must be dead simple
- Commission-based pricing aligns incentives
- Prove ROI fast or they'll churn"""


# ==============================================================================
# PERSONA 5: THE ORCHESTRATOR - Not implemented here, see orchestrator.py
# ==============================================================================
# The Orchestrator is special and implemented separately as it coordinates
# all other personas rather than being a regular persona itself.


# Helper function to get all available personas
def get_available_personas():
    """Return dictionary of all available persona instances."""
    return {
        "graham": GrahamPersona(),
        "hormozi": HormoziPersona(),
        "karpathy": KarpathyPersona(),
        "real_estate_vet": RealEstateVetPersona(),
    }


if __name__ == "__main__":
    # Test a persona
    print("Testing Graham persona...")

    shared = {
        "question": "How should we get our first customer?",
        "request_type": "strategy",
        "context": {"stage": "pre-revenue", "target": "real estate agencies"}
    }

    graham = GrahamPersona()
    result = graham.run(shared)

    print(f"\nPersona outputs: {len(shared.get('persona_outputs', []))}")
    if shared.get("persona_outputs"):
        output = shared["persona_outputs"][0]
        print(f"\nGraham's recommendation:")
        print(output.get("output", ""))
