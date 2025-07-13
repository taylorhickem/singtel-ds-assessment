# Custom Agent and Tool
Implement a new custom agent and at least one custom tool suitable for a telecommunications use case. Possible examples include:

- Telco Products/Roaming plan recommendation engine (preferred, due to immediate relevance to JD)
- Billing dispute parsing and categorization (good to have)
- Data usage history check (good to have)

Mocked data is allowed to enable the tool’s demonstration. To keep within a time bound, please describe some of the approaches you have planned and would have utilised, if given sufficient time.

Clearly document:

- The specific business problem your custom tool addresses.
- Integration method between your tool and the agent.

## Proposed Design

The custom agent will be built with **LangChain** using the `AgentExecutor` API. A conversational
LLM (OpenAI `gpt-3.5-turbo`) will drive the agent. The key custom tool is a
**Roaming Plan Recommendation** utility that looks up a mock catalogue of plans
and selects the most appropriate option for the user based on destination,
expected usage and budget. Additional lightweight tools can be added (such as a
billing dispute classifier) but the focus is on demonstrating one complete
example.

### Tool implementation

- Mock data stored in a small CSV is loaded with **pandas**.
- Business logic is implemented as a Python function that accepts structured
  input (destination, data usage, travel duration) and returns a recommended
  plan with reasoning.
- The function is wrapped as a `StructuredTool` in LangChain so the agent can
  invoke it when required.

### Agent flow

1. **Prompt & Memory** – the agent uses a conversation chain with minimal
   memory to maintain context.
2. **Tool Calls** – when the user asks for roaming advice the agent calls the
   recommendation tool, passing the parsed parameters.
3. **Response** – the result is combined with natural language guidance from the
   LLM.

This design keeps the tool logic separate from the agent so that more telco
utilities can be added easily. Mock data keeps the implementation simple while
showing how a real data source would be integrated.
