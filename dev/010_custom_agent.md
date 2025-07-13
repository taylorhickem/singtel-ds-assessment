# Custom Agent
This release covers Task 01: Custom agent and tool `docs/tasks/0301_custom_agent.md`

## Session logs

session logs are timestamped to Singapore timezone in reverse chronological order, with latest entries at the top, and earlier entries at the bottom.

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


