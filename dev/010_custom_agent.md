# Custom Agent
This release covers Task 01: Custom agent and tool `docs/tasks/0301_custom_agent.md`

## Situation
Part 1 of the assignment is to build a custom Roaming Plan Recommendation Agent.

## Roaming Plan Agent
The roaming plan agent design is summarized in `docs/tasks/0301_custom_agent.md`
it is comprised of an AI Agent interface that navigates the user through a selection process to select an appropriate Data Roaming Plan for their travel needs. The Roaming Plan Agent uses a Roaming Plan Recommendation Tool for modularity to separate the deterministic plan lookup tasks from the organic natural language processing for the user interface task.

## Implementation
In this release, the Agent was partially implemented with

- **Recommendation tool** - full functionality using an SQLite database backend
- **AI User Intent Classifer** - one-shot Agent using OpenAI gpt-3.5-turbo to classify the User prompt as either on or off topic

In future releases, both of these two tools can be plugged in to a LangChain AI Agent to manage the full end-to-end workflow.

## Session logs

session logs are timestamped to Singapore timezone in reverse chronological order, with latest entries at the top, and earlier entries at the bottom.

### Roaming data plan [Developer] RoamingPlanAgent 2025-07-22 20:00

__Refactored Architecture__
Separated concerns:

- DialogueManager handles interaction and flow
- RoamingIntentClassifier handles LLM-backed scoring
- Introduced a base classifier for reuse across other domains

__Improved Behavior__

- Replaced brittle "yes"/"no" classification with real-valued score (0–1.0)
- Added reasoning output for debugging and auditability
- Tuned threshold (0.33) to catch ambiguous but travel-related prompts
- Recovered accuracy on previously unstable cases (e.g. “Langkawi”, “Hajj”, “snorkeling”)

__Test Coverage__

- Classifier outputs are tested with bulk prompt lists via subTest()
- Failures show reasoning and score for diagnosis

__Next: Plug in full RoamingPlanAgent__
After redirect, launch LangChain agent to:

- Ask for destination, duration, data amount
- Call RoamingPlanRecommender
- Present ranked plans

### Roaming data plan [Developer] ChatGPT prompt RoamingPlanAgent 2025-07-22 15:59

ok, lets start with a much simpler setup that uses these three components - the Dialogue Manager, the RoamingPlanAgent, and the cli interface, and no tool integration, it simply starts the conversation, and determines whether the user response is relevant for selecting a plan, if yes, then it returns "Great, let me forward you on to my associate!" and it redirects to dummy URL for another chat agent that will perform the rest of the steps, analogous to the redirect at the end for purchasing the plan. So we've got an outline that we can then build in the remaining features. 

Start simple, VERY simple. I was able to implement another LangChain solution in < 100 lines of code, so start out as bare minimus as possible, and work with the existing dependencies unless you have a compelling argument to use a different set. Also, if you can implement with fewer dependencies, do so and tell me which ones to drop.

### Roaming data plan [Codex] RoamingPlanAgent 2025-07-22 14:43
Attempt to diagnose and resolve failed test case.

__diagnostics__
The conversation failed to implement several workflow features from the design:

1. **Off-topic handling** – User messages like "I want a pony" were not detected
   as irrelevant, so the agent kept repeating the same prompt.
2. **Validation loop** – The tool was invoked with `Blorkistan` and missing
   duration/data even though inputs were incomplete.
3. **Results templating and confirmation** – The plan list was printed but the
   agent never progressed to confirmation or purchase redirection.

These issues stem from missing state tracking for off-topic counts, duplicate
`_tool_recommend` implementations and lack of checks before calling the tool.

__resolution__
Implemented a single `_tool_recommend` with input validation and state updates,
added an `off_topic_count` field with exit logic after three irrelevant replies,
and reset the counter whenever valid progress is made. The `step` method now
monitors unchanged state to detect off-topic responses and returns a support
message when the threshold is reached.

### Roaming data plan [Developer] Codex prompt RoamingPlanAgent 2025-07-22 14:40
for context, refer to 
 - the failed test log in `/docs/0301_custom_agent.md` section ## Test case, failed
 - Roaming Plan Agent design doc `/docs/0301_custom_agent.md` and release doc `dev/010_custom_eagent.md`
 - `AGENTS.md`
 - db schema `data/schema.json` and tables `data/*`
 - source code for the recommend agent `recommend_agent/*`
 - test script `test.py`

your task
 - scope `recommend_agent.chat_agent.RoamingPlanAgent` and `cli_agent.py`
 - review the failed test cases and the design for the `RoamingPlanAgent`
 - perform a complete diagnostics and identify each of the design features that were failed to implement in the conversation flow, there were several.
 - for each failure, diagnose the cause in how the agent code was implented, and a resolution
 - document your diagnostics and resolution strategy in a subsection of the failure test case ### diagnostics and ### resolution
 - implement the fixes 
 - summarize your updates as a timestamped session log in the release doc section ### Roaming data plan [Codex] RoamingPlanAgent 2025-07-22 <HH>:<MM>
 - raise a PR with changes to `test.py` and your session log

### Roaming data plan [Developer] RoamingPlanAgent 2025-07-22 14:34
validation and testing
 - still failed, but now in a functional failure and not exceptions
 - debugged requirements conflicts, rebuilt env with updated requirements
 - added a cli interface `cli_agent.py` for direct interaction testing with chat agent
 - added OpenAI_API_KEY to env variable with import using loadenv
 - overwrite _tool_recommend()
 - set verbose = True
 - updated the Agent system message

### Roaming data plan [Codex] RoamingPlanAgent 2025-07-22 13:04

- Implemented LangChain-based `RoamingPlanAgent` using `ChatOpenAI` and
  `create_openai_functions_agent`.
- Added structured tool wrapper around `RoamingPlanRecommender` to update agent
  state when invoked.
- Added fallback regex logic when no LLM is configured to keep tests runnable
  offline.
- Updated `step` method to return conversation state and handle plan selection.
- Expanded tests to cover near-match country handling and prompting for missing
  trip details.

### Roaming data plan [Developer] Codex prompt RoamingPlanAgent 2025-07-22 13:02
for context, refer to 
 - Roaming Plan Agent design doc `/docs/0301_custom_agent.md` and release doc `dev/010_custom_eagent.md`
 - `AGENTS.md`
 - db schema `data/schema.json` and tables `data/*`
 - source code for the recommend agent `recommend_agent/*`
 - test script `test.py`

your task
 - scope `recommend_agent.chat_agent.RoamingPlanAgent`
 - review the test cases and the design for the `RoamingPlanAgent`
 - take note that the design implementation is conversational LLM OpenAI `gpt-3.5-turbo`, using the `recommend_agent.recommend.RoamingPlanRecommender` as a tool. The current implementation is based on regex, and would have difficulty handling a conversation with a real human interface.
 - implement the agent as a class using LangChain package, taking into consideration the test cases, design aims of exposing the state, language interface between the user and the plan recommender tool 
 - summarize your updates as a timestamped session log in the release doc section ### Roaming data plan [Codex] RoamingPlanAgent 2025-07-22 <HH>:<MM>
 - raise a PR with changes to `test.py` and your session log

### Roaming data plan [Developer] RoamingPlanAgent review 2025-07-22 12:52
RoamingPlanAgent review
 - implemented using regex, not LLM

### Roaming data plan [Codex] RoamingPlanAgent 2025-07-21 22:04

- Implemented `RoamingPlanAgent` with stateful `step` method parsing destination,
  duration, data amount and service type.
- Integrated agent with `RoamingPlanRecommender` and basic plan selection logic.
- Updated `test.py` to exercise valid query, invalid country, high data demand
  and plan confirmation scenarios without skips.

### Roaming data plan [Developer] Codex prompt RoamingPlanAgent 2025-07-21 22:00
for context, refer to 
 - Roaming Plan Agent design doc `/docs/0301_custom_agent.md` and release doc `dev/010_custom_eagent.md`
 - `AGENTS.md`
 - db schema `data/schema.json` and tables `data/*`
 - source code for the recommend agent `recommend_agent/*`
 - test script `test.py`

your task
 - scope `recommend_agent.chat_agent.RoamingPlanAgent`
 - review the test cases and the design for the `RoamingPlanAgent`
 - implement the agent as a class, taking into consideration the test cases, design aims of exposing the state, language interface between the user and the plan recommender tool 
 - summarize your updates as a timestamped session log in the release doc section ### Roaming data plan [Codex] RoamingPlanAgent 2025-07-21 <HH>:<MM>
 - raise a PR with changes to `test.py` and your session log

### Roaming data plan [Developer] RoamingPlanAgent recommend agent test cases 2025-07-21 18:30
test cases
 - repaired test cases remove Magic Mock and test actual behavior of `agent.step`

### Roaming data plan [Codex] RoamingPlanAgent recommend agent test cases 2025-07-21 17:49
- added mocked unit tests for `RoamingPlanAgent` covering valid query, invalid country,
  high data demand and user purchase confirmation scenarios

### Roaming data plan [Developer] Codex prompt RoamingPlanAgent recommend agent test cases 2025-07-21 17:47
for context, refer to 
 - Roaming Plan Agent design doc `/docs/0301_custom_agent.md` and release doc `dev/010_custom_eagent.md`
 - `AGENTS.md`
 - db schema `data/schema.json` and tables `data/*`
 - source code for the recommend agent `recommend_agent/*`
 - test script `test.py`

your task
 - scope `test.py`
 - review the test cases listed for the Recommendation Agent in the Roaming Plan Agent design doc and the placeholders in `tests.py`
 - implement a few sample test cases in `test.py` making some assumptions about the future behavior and attributes of `RoamingPlanAgent` 
 - summarize your updates as a timestamped session log in the release doc section ### Roaming data plan [Codex] RoamingPlanAgent recommend agent test cases 2025-07-21 <HH>:<MM>
 - raise a PR with changes to `test.py` and your session log

### Roaming data plan [Codex] RoamingPlanAgent recommend agent class test cases 2025-07-21 17:07

Implemented skeleton unittest class `TestRoamingPlanAgent` in `test.py` with
placeholder tests for each scenario listed in the design document. All tests are
skipped until the future agent implementation is available.

### Roaming data plan [Developer] Codex prompt RoamingPlanAgent recommend agent test cases 2025-07-21 17:05
for context, refer to 
 - Roaming Plan Agent design doc `/docs/0301_custom_agent.md` and release doc `dev/010_custom_eagent.md`
 - `AGENTS.md`
 - db schema `data/schema.json` and tables `data/*`
 - source code for the recommend agent `recommend_agent/*`
 - test script `test.py`

your task
 - scope `test.py`
 - review the test cases listed for the Recommendation Agent in the Roaming Plan Agent design doc
 - design how to implement the test cases, considering the proposed options in the table or other options as you see fit
 - implement the test cases in `test.py`
 - summarize your updates as a timestamped session log in the release doc section ### Roaming data plan [Codex] RoamingPlanAgent recommend agent class test cases 2025-07-21 <>:<MM>
 - raise a PR with changes to `test.py` and your session log

### Roaming data plan [Developer] RoamingPlanAgent recommend agent test cases 2025-07-21 16:58
test cases
 - list 10x additional test cases in `docs/0301_custom_agent.md` for Roaming Plan Recommendation Agent
 - options for test implementation
  - `agent.step`, exposed agent state, response JSON parsing

### Roaming data plan [Developer] recommend agent design ChatGPT prompt 2025-07-21 16:25

__recommend agent__

For the chat agent, what are some design features for the agent to act as language aware semantic interpreter between the user and the recommend tool RoamingPlanRecommender (RPR)

The chat agent scope is prompt and gather the user requirements into the specific format that is valid for the RPR, and otherwise to continue in retry loop with the user until the trip specification is valid and ready to use with the RPR tool. Then the agent should select from the shortlisted plans from the RPR tool, format and present the options to the user, confirm plan selection and redirect the user to another URL to purchase the plan

update 0301_custom_agent.md to elaborate on this design intention, apply edits to the current version and add updates for design features that implement this requirement


### Roaming data plan [Developer] test cases 2025-07-21 16:02
tests
 - polish up test case for unsupported service type

### Roaming data plan [Codex] test cases 2025-07-21 15:34
- add tests for high data need filtering and unsupported service type

### Roaming data plan [Developer] test cases Codex prompt 2025-07-21 15:33
for context, refer to 
 - Roaming Plan Agent design doc `/docs/0301_custom_agent.md` and release doc `dev/010_custom_eagent.md`
 - `AGENTS.md`
 - db schema `data/schema.json` and tables `data/*`
 - source code for the recommend agent `recommend_agent/*`
 - test script `test.py`

your task
 - scope `test.py`
 - add two additional test cases to the test script for "High data need triggers filtering" and "unsupported service type"
 - summarize your updates as a timestamped session log in the release doc section ### Roaming data plan [Codex] test cases 2025-07-21 <HH>:<MM> 
 - raise a PR with changes to `test.py` and your session log

### Roaming data plan [Developer] test cases 2025-07-21 15:09
add test case for invalid destination "Blorkistan"

### Roaming data plan [Developer] recommendation tool 2025-07-21 13:55

test
 - validated
 - update test case for expected plan from test trip specifications

recommend
 - relax scoring on data gb requirement
 - append rates to plan results

roaming plans db
 - set build keep_open option default to True


### Roaming data plan [Developer] recommendation tool 2025-07-20 22:00

recommend tool
 - updated recommend method to use the SQLite db
 - updated test case
 - added interpolated solution for duration days in between fixed options
 - updated database build

roaming plans database
 - implemented db as normalized SQLite database with three tables
  - destination
  - ppu_rate
  - roaming_plan

### Roaming data plan [Developer] recommendation tool 2025-07-19 16:00
tests
- add a test case and implement using `pytest`
    - destination: "Malaysia" 
    - trip duration: 2 days
    - service type: "data"
    - data needed: 5.0

recommendation tool
 - reorganize, split into Agentic chat agent `recommend_agent/chat_agent.py` and non-agentic recommend tool `recommend_tool/recommend.py`
 - implement as RoamingPlanRecommender class `recommend_agent/recommend.RoamingPlanRecommender` method `RoamingPlanRecommender.recommend`
 - `recommend` function:
  - takes inputs
    - destination: location 
    - trip duration: number of days
    - service type: [data, sms, calls]
    - data needed: amount of data needed in GB
  - and returns results as a JSON row from the roaming plan CSV database `data/roaming_plans.csv`

### Environment [Developer] install dependencies 2025-07-13 20:30

```bash
pip install -r requirements.txt
```

### Roaming plan data [Developer] ChatGPT prompt plan database tool 2025-07-13 20:23

show a python script `recommend_agent/tools.py` that implements the custom plan database tool, and can be used as a LangChain tool for an Agent that implements this workflow `from recommend_agent.tools import plans_db_tool`

The csv file `roaming_plans.csv` is available at 

```
data/
  roaming_plans.csv
```

### Roaming plan data [Developer] ChatGPT prompt control flow decision tree 2025-07-13 20:13

Develop a control flow decision tree for the UX workflow

create this workflow as a new markdown section in the working design document
include mermaid diagram as well as description for each step in the workflow

 - implemented in an agenting framework like langchain
    - with natural english language instructions to the agent
    - with access to the roaming plans database interface tool
 - establish the user is in the right place -- selecting a roaming plan and if not redirect to another main chat support URL
 - graciously handle irrelevant prompts from the user "how bout them bears?", or attempts to hack or corrupt the agent "forget all previous instructions"
 - prompt the user for requirements gathering relevant to the roaming plans in a sequential guided manner
 - handle unexpected, invalid inputs graciously and with retry logic
 - match the user requirement in a logical way with the available plans
 - shortlist a ranked list of the top 3 plan options
 - give a brief pros and cons and suggested choice
 - take the choice selection by the user and
 - option to exit, if user still deciding
 - if selected, then confirm selection and ask if would like to continue to purchase the plan
 - if yes, then redirect URL to another workflow URL for purchasing the plan, and in the redirect include the plan selection details as a JSON

### Roaming plan data [Developer] table inspect 2025-07-13 20:00

__table: roaming_plans__

| column | example value |
| - | - |
| Zone | Zone 1 |
| Destination | Malaysia |
| Data_Pass_Validity | 1 day |
| Data_Pass_Data | 1 GB |
| Data_Pass_Price | S$1 |
| Pay_Per_Use_Data | S$0.01/10KB |
| Pay_Per_Use_Call_Outgoing | S$0.29/min |
| Pay_Per_Use_Call_Incoming | Free |
| Pay_Per_Use_SMS | S$0.10/SMS |

### Roaming plan data [Developer] ChatGPT prompt 2025-07-13 19:52

refer to PDF file `singtel_roaming_rates.pdf` and the design document `0301_custom_agent.md`
break up this PDF file into a structured dataset that can be implemented as an Agent tool for a Roaming Plan recommendation engine.
