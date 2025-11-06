# Myfrendo AI Agent Team - Design Document

## Problem Statement

Building a successful bootstrap business requires expertise across multiple domains: startup strategy, sales, technical implementation, industry knowledge, and more. Solo founders or small teams often lack deep expertise in all these areas.

**The Challenge**: How can we give Myfrendo (and similar startups) access to world-class expertise across all critical business dimensions without hiring a full team?

**The Solution**: A multi-agent AI system with specialized "persona" agents, each embodying deep expertise in a specific domain, coordinated by an orchestrator that synthesizes their diverse perspectives into actionable recommendations.

## Design Goals

1. **Multi-perspective analysis**: Every question analyzed from multiple expert viewpoints
2. **Specialization**: Each persona has deep, focused expertise in their domain
3. **Coherent synthesis**: Diverse insights combined into actionable recommendations
4. **Single source of truth**: Only the Orchestrator communicates with users
5. **Scalable**: Easy to add more personas as needed
6. **Tool-enabled**: Personas can call tools (APIs, databases, etc.) for real-world actions
7. **Bootstrap-friendly**: Optimize for cost-effectiveness and practical execution

## Architecture

### High-Level Flow

```
User Question
      ↓
[1] Orchestrator Classifier
      ↓
[2] Persona Batch Executor (Parallel)
      ↓
[3] Orchestrator Synthesizer
      ↓
[4] Orchestrator Reporter
      ↓
User Response
```

### Component Details

#### 1. Orchestrator Classifier (Node)

**Purpose**: Analyze user questions and route to appropriate personas

**Input**: User question
**Output**: Classification (request type, personas to activate, execution mode)

**Key Logic**:
- Classify request type (strategy, product, sales, technical, domain, general)
- Select 2-5 relevant personas based on question type
- Determine execution mode (parallel for most, sequential if dependencies exist)

**Example**:
```yaml
request_type: sales
personas_to_activate: [hormozi, real_estate_vet, graham]
execution_mode: parallel
```

#### 2. Persona Batch Executor (BatchNode)

**Purpose**: Execute selected personas in parallel

**Input**: List of persona names from classifier
**Output**: Each persona adds insights to `shared["persona_outputs"]`

**Key Logic**:
- Iterate through selected personas
- Each persona receives: question, context, other persona insights (if sequential)
- Each persona returns: thinking, key_insights, recommendation, confidence, tools_needed

**Design Pattern**: Uses PocketFlow's `BatchNode` for parallel execution

#### 3. Orchestrator Synthesizer (Node)

**Purpose**: Combine all persona insights into coherent analysis

**Input**: All persona outputs
**Output**: Synthesized insights with:
- Executive summary
- Key insights (with sources and confidence scores)
- Recommended actions (prioritized)
- Areas of agreement/disagreement
- Next steps

**Key Logic**:
- Identify common themes across personas
- Highlight valuable disagreements
- Prioritize by relevance and confidence
- Generate specific, actionable recommendations

#### 4. Orchestrator Reporter (Node)

**Purpose**: Format final analysis for user consumption

**Input**: Synthesis results
**Output**: Formatted report (CLI-friendly)

**Key Logic**:
- Structure report with clear sections
- Make actionable (not just insights, but specific next steps)
- Cite sources (which personas contributed each insight)
- Clean, scannable format

## Persona Design

### Base Persona Architecture

All personas inherit from `BasePersona` which provides:

```python
class BasePersona(Node):
    - get_system_prompt() -> str  # Unique personality and expertise
    - prep() -> dict                # Extract question and context
    - exec() -> dict                # LLM call with persona-specific prompt
    - post() -> None                # Save output to shared state
```

### The 5 Core Personas

#### 1. Orchestrator
- **Not a regular persona** - special coordinator role
- Implemented as separate nodes (Classifier, Synthesizer, Reporter)
- Has access to all tools and can orchestrate complex workflows

#### 2. Graham (Paul Graham)
- **Expertise**: Startup philosophy, bootstrapping, PMF
- **When activated**: Strategy, early-stage, growth questions
- **Perspective**: Do things that don't scale, talk to users, focus on growth rate
- **Example output**: "Manually onboard 10 agencies before automating anything"

#### 3. Hormozi (Alex Hormozi)
- **Expertise**: Offer design, value stacking, pricing, guarantees
- **When activated**: Sales, pricing, revenue questions
- **Perspective**: Create irresistible offers, reverse risk, focus on LTV:CAC
- **Example output**: "Offer: Pay nothing upfront, 15% commission only on closed deals, money-back guarantee"

#### 4. Karpathy (Andrej Karpathy)
- **Expertise**: AI/ML, model selection, cost optimization
- **When activated**: Technical, AI implementation questions
- **Perspective**: Right model for right task, measure latency/cost, pragmatic ML
- **Example output**: "Use GPT-4o-mini for 90% of calls to save 70% on inference costs"

#### 5. Real Estate Vet
- **Expertise**: Real estate industry, agent workflows, compliance
- **When activated**: Domain-specific, reality checks, all questions (grounding)
- **Perspective**: Agents care about closings not tech, trust is everything, compliance matters
- **Example output**: "Voice agent must sound like a 10-year veteran or lose trust instantly"

### Persona Interaction Pattern

**Parallel Mode** (default):
```
Question → All personas analyze simultaneously → Orchestrator synthesizes
```

**Sequential Mode** (when needed):
```
Question → Persona 1 → Persona 2 (sees P1's output) → ... → Orchestrator
```

**Current Implementation**: Parallel only (faster, simpler)

**Future Enhancement**: Support for direct inter-persona communication
- "Hormozi asks Karpathy: What's the cost per call at scale?"
- Enables more dynamic collaboration

## PocketFlow Patterns Used

### 1. Node Pattern
Each persona is a `Node` with `prep`, `exec`, `post` lifecycle:

```python
class GrahamPersona(BasePersona):
    def prep(self, shared):
        return shared.get("question"), shared.get("context")

    def exec(self, inputs):
        return call_llm(self.get_system_prompt() + inputs)

    def post(self, shared, prep_res, exec_res):
        shared["persona_outputs"].append(exec_res)
```

### 2. Flow Pattern
Orchestrator uses `Flow` to chain nodes:

```python
flow = Flow(start=classifier)
classifier >> executor >> synthesizer >> reporter
```

### 3. Batch Pattern
`PersonaBatchExecutor` uses `BatchNode` to run multiple personas:

```python
class PersonaBatchExecutor(BatchNode):
    def prep(self, shared):
        return ["graham", "hormozi", "karpathy"]  # List of personas

    def exec(self, persona_name):
        return persona_name  # Process each

    def post(self, shared, prep_res, exec_res):
        for name in exec_res:
            self.personas[name].run(shared)
```

### 4. Shared State Pattern
All nodes communicate via `shared` dictionary:

```python
shared = {
    "question": "...",
    "request_type": "strategy",
    "persona_outputs": [],
    "final_synthesis": {...}
}
```

## Tool Calling Design

### Tool Registry Pattern

Centralized registry of available tools:

```python
class ToolRegistry:
    def __init__(self):
        self.tools = {
            "n8n_trigger_workflow": self.n8n_trigger_workflow,
            "retell_create_call": self.retell_create_call,
            # ...
        }

    def call_tool(self, tool_name: str, **kwargs):
        return self.tools[tool_name](**kwargs)
```

### Tool Access Matrix

Different personas have access to different tools:

| Persona | N8N | Retell | Twilio | Database | Web Search |
|---------|-----|--------|--------|----------|------------|
| Orchestrator | ✅ | ✅ | ✅ | ✅ | ✅ |
| Graham | ❌ | ❌ | ❌ | ✅ | ✅ |
| Hormozi | ❌ | ❌ | ❌ | ✅ | ✅ |
| Karpathy | ❌ | ✅ | ❌ | ✅ | ❌ |
| Real Estate Vet | ❌ | ❌ | ❌ | ✅ | ✅ |

**Design Decision**: Start with open access, restrict as needed for safety/cost

### Current Implementation

Tools are **mocked** (return fake data) to enable development without API keys.

To enable real tools, replace mock implementations with actual API calls:

```python
def retell_create_call(self, phone_number, agent_config):
    # Replace this mock:
    return {"success": True, "call_id": "mock_123"}

    # With real API call:
    response = requests.post(
        "https://api.retellai.com/v1/calls",
        headers={"Authorization": f"Bearer {RETELL_API_KEY}"},
        json={"phone_number": phone_number, **agent_config}
    )
    return response.json()
```

## Myfrendo Context

This system is tailored for **Myfrendo**, a bootstrap business automating real estate agencies.

### Key Context Embedded in Personas

**Business Model**:
- 0€ → 10K MRR bootstrap
- 85% margins (AI + automation, no salaries)
- Commission-based pricing
- Early-stage team (co-founders)

**Target Customer**:
- Real estate agencies
- 3-10 agents (sweet spot)
- Need lead generation and qualification
- Time-poor, results-focused

**Tech Stack**:
- N8N (workflow automation)
- Retell AI (voice agents)
- Twilio (telephony)
- OpenAI/Anthropic (LLMs)

**Value Proposition**:
- AI voice agents that call and qualify leads
- Appointment booking automation
- Pay only on results (commission model)

This context is **baked into persona system prompts**, ensuring every recommendation is grounded in Myfrendo's reality.

## Design Decisions

### 1. Why Only 5 Personas Initially?

**Decision**: Start with 5 core personas, not all 20

**Rationale**:
- Faster iteration and testing
- Lower cost (fewer LLM calls)
- Cover 80% of question types
- Can add more as needs emerge

**Future**: Add remaining 15 personas (Jobs, Ive, Thiel, Bezos, etc.) based on actual usage patterns

### 2. Why Parallel Execution?

**Decision**: Run personas in parallel by default

**Rationale**:
- Much faster (5 personas in ~3-5 seconds vs 15-25 seconds sequential)
- Most questions don't require personas to see each other's outputs first
- Orchestrator synthesizes at the end anyway

**Tradeoff**: Lose potential for personas to build on each other's ideas in real-time

**Future**: Support sequential mode for specific question types

### 3. Why Structured YAML Output?

**Decision**: Personas return structured YAML, not freeform text

**Rationale**:
- Easier to parse and synthesize programmatically
- Enforces consistent output format
- Enables confidence scoring and source attribution
- Makes tool calling explicit

**Example**:
```yaml
thinking: |
  <reasoning process>
key_insights:
  - <insight 1>
  - <insight 2>
recommendation: |
  <specific recommendation>
confidence: 85
tools_needed:
  - calculate_metrics
```

### 4. Why Single Model (GPT-4o-mini)?

**Decision**: Use GPT-4o-mini for most personas, GPT-4o for orchestrator

**Rationale**:
- Cost optimization (mini is 10x cheaper)
- Personas don't need maximum reasoning (just domain expertise via prompting)
- Orchestrator needs stronger synthesis (use GPT-4o)

**Future**: Test persona-specific models (e.g., Claude for Graham's philosophical insights)

### 5. Why CLI First?

**Decision**: Build CLI interface before web UI

**Rationale**:
- Faster development
- Focus on core logic, not UI
- Easy testing and iteration
- Myfrendo's founder is technical (CLI-comfortable)

**Future**: Add web UI, API endpoints, Slack/Discord bots

## Scalability Considerations

### Adding More Personas

**Process**:
1. Define persona in `personas.py` (inherit from `BasePersona`)
2. Implement `get_system_prompt()` with unique expertise
3. Add to `get_available_personas()` registry
4. Update orchestrator routing logic

**Effort**: ~30 minutes per persona

### Inter-Persona Communication

**Current**: Personas only see other personas' outputs via orchestrator synthesis

**Future Enhancement**:
```python
# Hormozi wants to ask Karpathy something
shared["inter_persona_requests"].append({
    "from": "hormozi",
    "to": "karpathy",
    "question": "What's the inference cost at 10K calls/day?"
})
# Orchestrator routes this request
```

**Complexity**: Requires message routing and potential cycles/deadlocks

### Memory/Context Persistence

**Current**: Each question is independent (stateless)

**Future Enhancement**:
- Save conversation history
- Personas remember previous analyses
- Build long-term context about Myfrendo's progress

**Implementation**: Add vector database for semantic memory

## Testing Strategy

### Unit Tests
- Test each persona in isolation
- Mock LLM responses for deterministic testing
- Verify output format (YAML structure)

### Integration Tests
- Test full flow with real questions
- Verify orchestrator routing logic
- Check synthesis quality

### Evaluation Metrics
- **Response Quality**: Human eval of recommendations (1-5 scale)
- **Routing Accuracy**: Are the right personas activated?
- **Synthesis Coherence**: Does final report make sense?
- **Actionability**: Can user immediately act on recommendations?

### Example Test Cases

```python
def test_graham_activated_for_strategy():
    shared = {"question": "How do we get our first customer?"}
    classifier = OrchestratorClassifier()
    classifier.run(shared)
    assert "graham" in shared["personas_to_activate"]

def test_all_personas_produce_valid_yaml():
    for persona in get_available_personas().values():
        shared = {"question": "Test question"}
        persona.run(shared)
        output = shared["persona_outputs"][-1]
        assert "thinking" in output
        assert "recommendation" in output
        assert isinstance(output["confidence"], int)
```

## Future Enhancements

### Phase 2: More Personas
- Add Jobs, Ive, Thiel, Bezos (strategic expansion)
- Add Carmack, Torvalds, DHH (technical depth)
- Add Sales Psychologist, Data Scientist, Ops Manager (operational)
- Add Compliance Officer, Finance Pro (risk/finance)
- Add Copywriter, Customer Success (GTM)

### Phase 3: Advanced Capabilities
- **Streaming responses**: Show persona analyses in real-time
- **Tool execution**: Actually trigger N8N, Retell, Twilio
- **Memory**: Persist context across sessions
- **Fine-tuning**: Train persona-specific models
- **Multi-turn**: Ask follow-up questions
- **Proactive**: Orchestrator suggests questions to ask

### Phase 4: Productization
- **Web UI**: Beautiful interface for non-technical users
- **API**: Programmatic access for integrations
- **Slack/Discord bots**: Use in team chat
- **Plugins**: Add custom personas for specific companies
- **Marketplace**: Share/sell persona templates

## Conclusion

This design provides:

✅ **Multi-expert analysis** for better decision-making
✅ **Modular architecture** for easy expansion
✅ **PocketFlow patterns** for maintainable code
✅ **Myfrendo context** embedded throughout
✅ **Tool calling** for real-world actions
✅ **Scalable foundation** for future enhancements

The system transforms a solo founder into a founder with a world-class advisory board, available 24/7, at the cost of a few LLM API calls.

**Next Steps**: Test with real Myfrendo questions, iterate on persona prompts, add remaining 15 personas as needed.
