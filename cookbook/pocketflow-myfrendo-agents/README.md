# Myfrendo AI Agent Team

A multi-agent AI system with 5 expert personas coordinated by an orchestrator, built with PocketFlow. Designed for Myfrendo - a bootstrap business automating real estate agencies with AI voice agents.

## Overview

This system implements a **20-persona architecture** (5 core personas now, 15+ to be added) where:

1. User asks a question
2. **Orchestrator** analyzes and routes to relevant personas
3. **Expert personas** analyze from their unique perspectives
4. **Orchestrator** synthesizes insights into actionable recommendations
5. User receives comprehensive, multi-perspective analysis

**Key Innovation**: Only the Orchestrator talks to the user. Personas communicate through the orchestrator, enabling true multi-agent collaboration.

## The 5 Core Personas

### 🧠 The Orchestrator
**Role**: Mission control, request router, synthesizer

**Responsibilities**:
- Parse and classify user requests
- Route to appropriate personas
- Synthesize diverse perspectives
- Generate final actionable reports

**Always active** for every request.

---

### 📚 Graham (Paul Graham)
**Archetype**: Y Combinator co-founder, startup philosopher

**Expertise**:
- Product-market fit and bootstrapping
- "Do things that don't scale" philosophy
- Growth rate focus
- Talking to users relentlessly
- Managing runway carefully

**Activated for**: Strategy, early-stage, PMF questions

**Example insight**: *"Before building automation for all of real estate, manually onboard 10 agencies. The insights will save you 6 months of building the wrong thing."*

---

### 💰 Hormozi (Alex Hormozi)
**Archetype**: Master of irresistible offers

**Expertise**:
- Offer crafting and value stacking
- Guarantee structures
- Pricing psychology
- LTV:CAC optimization
- Risk reversal strategies

**Activated for**: Pricing, sales, offer design questions

**Example insight**: *"Offer: We call 1,000 leads. Pay nothing upfront. 15% commission only on closed deals. If we don't book 50 appointments in month 1, month 2 is free. Zero risk."*

---

### 🤖 Karpathy (Andrej Karpathy)
**Archetype**: AI researcher, former Tesla AI Director

**Expertise**:
- Model selection (GPT-4 vs 4-mini vs fine-tuned)
- Inference cost optimization
- Latency reduction
- Prompt engineering
- LLM reliability and error handling

**Activated for**: Technical, AI/ML, implementation questions

**Example insight**: *"Use 2-stage pipeline: GPT-4o-mini for 90% of calls ($0.003/call), escalate complex to Claude Opus ($0.02/call). Saves 70% on inference with same quality."*

---

### 🏠 Real Estate Vet (20-year industry veteran)
**Archetype**: Seasoned real estate broker

**Expertise**:
- Agent pain points and workflows
- Industry terminology and credibility
- Compliance (TCPA, fair housing)
- Seasonal market dynamics
- What agents actually pay for

**Activated for**: Domain-specific, industry reality checks

**Example insight**: *"Agents don't care about 'AI innovation.' They care about closings. Your voice agent must sound like it's been in real estate for 10 years or you'll lose trust in 30 seconds."*

---

## Architecture

```
User Question
      ↓
┌─────────────────────────────────────┐
│   Orchestrator Classifier           │ ← Analyzes request type
│   (Routes to personas)              │
└─────────────────────────────────────┘
      ↓
┌─────────────────────────────────────┐
│   Persona Batch Executor            │ ← Runs selected personas
│   (Parallel execution)              │
│                                     │
│   • Graham                          │
│   • Hormozi                         │
│   • Karpathy                        │
│   • Real Estate Vet                 │
└─────────────────────────────────────┘
      ↓
┌─────────────────────────────────────┐
│   Orchestrator Synthesizer          │ ← Combines insights
│   (Identifies agreements/conflicts) │
└─────────────────────────────────────┘
      ↓
┌─────────────────────────────────────┐
│   Orchestrator Reporter             │ ← Formats final report
│   (Actionable recommendations)      │
└─────────────────────────────────────┘
      ↓
User Response
```

## Installation

1. **Clone and navigate**:
```bash
cd cookbook/pocketflow-myfrendo-agents
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Set up environment**:
```bash
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
export OPENAI_API_KEY='your-key-here'
```

## Usage

### Interactive Mode

Run the agent team in interactive CLI mode:

```bash
python main.py
```

Then ask questions naturally:
```
💬 Your question: How should we get our first customer?
```

The Orchestrator will automatically select relevant personas and synthesize their insights.

### Single Question Mode

Ask a single question and exit:

```bash
python main.py "How should we price our voice agent service?"
```

Or with `--` prefix:

```bash
python main.py --"What LLM should we use for real-time voice calls?"
```

### Example Questions

**Strategy**:
- "How should we get our first customer?"
- "Should we raise funding or stay bootstrapped?"
- "What's our competitive moat?"

**Pricing & Sales**:
- "How should we price our service?"
- "What guarantees should we offer?"
- "How do we make our offer irresistible?"

**Technical**:
- "Which LLM should we use for voice agents?"
- "How can we reduce latency below 400ms?"
- "What's the most cost-effective tech stack?"

**Domain**:
- "What are real estate agents' biggest pain points?"
- "How do we handle TCPA compliance?"
- "What conversion rate should we expect?"

## Output Example

```
================================================================================
MYFRENDO AI AGENT TEAM - ANALYSIS REPORT
================================================================================

📝 Question: How should we get our first customer?

🎯 EXECUTIVE SUMMARY
--------------------------------------------------------------------------------
Focus on manual, unscalable outreach to 10-15 target agencies (3-10 agents
each) with an irresistible risk-free offer. Learn intensively from these early
customers before automating anything.

💡 KEY INSIGHTS
--------------------------------------------------------------------------------
1. Do things that don't scale initially - manual onboarding teaches what matters
   Sources: Graham, Real Estate Vet | Confidence: 85%

2. Offer structure must eliminate all buyer risk with performance guarantees
   Sources: Hormozi, Real Estate Vet | Confidence: 90%

3. Target agencies with 3-10 agents (sweet spot for budget + decision speed)
   Sources: Real Estate Vet, Hormozi | Confidence: 80%

🚀 RECOMMENDED ACTIONS
--------------------------------------------------------------------------------
1. [HIGH] Build list of 50 target agencies, call top 15 personally
   Owner: Founder
   Why: Graham emphasizes learning from early users; Real Estate Vet confirms
        agencies this size have budget but move fast on decisions

2. [HIGH] Create risk-reversal offer: First month free, pay only on results
   Owner: Sales/Founder
   Why: Hormozi's value stacking eliminates friction; proven in service businesses

3. [MEDIUM] Set up minimal tracking for call metrics and conversion rates
   Owner: Technical team
   Why: Karpathy emphasizes measuring before optimizing; need baseline data

✅ IMMEDIATE NEXT STEPS
--------------------------------------------------------------------------------
1. Create Airtable with 50 target agencies (name, size, contact info)
2. Draft cold email with irresistible offer (use Hormozi framework)
3. Set up simple metrics dashboard (calls made, appointments booked, revenue)
4. Schedule 5 outreach calls per day for next 2 weeks

🛠️  TOOLS TO USE
--------------------------------------------------------------------------------
• Airtable (agency tracking)
• Simple spreadsheet (metrics)
• Calendar blocking (daily outreach time)

================================================================================
Analyzed by 4 expert personas
================================================================================
```

## File Structure

```
pocketflow-myfrendo-agents/
├── main.py              # Entry point (interactive or single-question mode)
├── flow.py              # Main PocketFlow orchestration
├── orchestrator.py      # Orchestrator nodes (classifier, synthesizer, reporter)
├── personas.py          # The 5 core persona implementations
├── tools.py             # Tool calling (N8N, Retell, Twilio, etc.)
├── utils.py             # LLM calling and helper functions
├── requirements.txt     # Dependencies
├── .env.example         # Environment variables template
└── README.md            # This file
```

## How It Works

### 1. Request Classification

The **OrchestratorClassifier** analyzes your question:
- Determines request type (strategy, sales, technical, domain, etc.)
- Selects which personas to activate
- Decides execution mode (parallel or sequential)

```python
class OrchestratorClassifier(Node):
    def exec(self, question):
        # Analyzes question and returns classification
        return {
            "request_type": "strategy",
            "personas_to_activate": ["graham", "real_estate_vet"],
            "execution_mode": "parallel"
        }
```

### 2. Persona Execution

**PersonaBatchExecutor** runs selected personas in parallel:

```python
class PersonaBatchExecutor(BatchNode):
    def prep(self, shared):
        return shared.get("personas_to_activate", [])

    def post(self, shared, prep_res, exec_res):
        for persona_name in exec_res:
            persona.run(shared)  # Each persona adds to shared["persona_outputs"]
```

### 3. Synthesis

**OrchestratorSynthesizer** combines all persona insights:
- Identifies agreements and disagreements
- Prioritizes by confidence and relevance
- Creates actionable recommendations

### 4. Reporting

**OrchestratorReporter** formats the final user-facing report with:
- Executive summary
- Key insights with sources
- Recommended actions
- Next steps

## Tool Calling

Personas can call tools when needed. Current tools:

- `n8n_trigger_workflow` - Trigger N8N automation workflows
- `retell_create_call` - Create AI voice calls via Retell
- `twilio_send_sms` - Send SMS messages
- `database_query` - Query business data
- `web_search` - Search the web for information
- `calculate_metrics` - Compute business metrics (CAC, LTV, etc.)

Example from a persona:

```python
def exec(self, inputs):
    # Persona determines it needs data
    result = tool_registry.call_tool(
        "calculate_metrics",
        metric_type="unit_economics",
        data={"total_marketing_spend": 1000, "new_customers": 10}
    )
    # Uses result in analysis
```

## Extending the System

### Add More Personas

See `docs/myfrendo_ai_team_personas.md` for the full 20-persona roadmap.

To add a new persona:

1. **Create persona class** in `personas.py`:
```python
class NewPersona(BasePersona):
    def __init__(self):
        super().__init__(
            name="Persona Name",
            archetype="Description"
        )

    def get_system_prompt(self) -> str:
        return """You are [persona]..."""
```

2. **Register in `get_available_personas()`**:
```python
def get_available_personas():
    return {
        "graham": GrahamPersona(),
        "new_persona": NewPersona(),  # Add here
        # ...
    }
```

3. **Update orchestrator routing** in `orchestrator.py` to include the new persona in relevant request types.

### Add New Tools

Add to `tools.py`:

```python
class ToolRegistry:
    def __init__(self):
        self.tools = {
            # ...
            "new_tool": self.new_tool,
        }

    def new_tool(self, param1: str) -> Dict[str, Any]:
        # Implementation
        return {"success": True, "data": result}
```

## Testing

**Test individual components**:

```bash
# Test utilities
python utils.py

# Test tools
python tools.py

# Test personas
python personas.py

# Test orchestrator
python orchestrator.py

# Test full flow
python flow.py
```

## Context: Myfrendo

This agent system is built for **Myfrendo** - a bootstrap business helping real estate agencies with AI automations.

**Business Model**:
- 0€ to 10K MRR bootstrap journey
- 85% gross margins (AI + automation, no salary costs)
- Commission-based pricing (% of results)
- Target: Small-to-medium real estate agencies (3-10 agents)

**Tech Stack**:
- N8N for workflow automation
- Retell AI for voice agents
- Twilio for telephony
- PocketFlow for agent orchestration

**Value Proposition**:
- Voice AI that calls/qualifies leads automatically
- Appointment booking without manual work
- CRM integration and reporting
- Pay only for results (commission model)

## Roadmap

- [x] 5 core personas (Orchestrator, Graham, Hormozi, Karpathy, Real Estate Vet)
- [ ] Add 15 more personas (Jobs, Ive, Thiel, Bezos, Carmack, Torvalds, DHH, Sales Psychologist, Data Scientist, Ops Manager, Compliance, Finance Pro, Copywriter, Customer Success)
- [ ] Inter-persona direct communication (personas can request input from specific other personas)
- [ ] Tool integration (actual N8N, Retell, Twilio API calls)
- [ ] Memory/context persistence across sessions
- [ ] Streaming output for real-time responses
- [ ] Web UI for non-CLI usage
- [ ] Fine-tuned models for specific personas

## License

MIT

## Credits

Built with [PocketFlow](https://github.com/The-Pocket/PocketFlow) - the 100-line minimalist LLM framework.

For Myfrendo - Business that boosts businesses 🚀
