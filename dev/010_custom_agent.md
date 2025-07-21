# Custom Agent
This release covers Task 01: Custom agent and tool `docs/tasks/0301_custom_agent.md`

## Session logs


session logs are timestamped to Singapore timezone in reverse chronological order, with latest entries at the top, and earlier entries at the bottom.

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
