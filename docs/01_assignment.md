# Singtel Data Science Assessment
Technical Take-Home Test – Senior Data Scientist

Thanks for your interest in the role! This take-home assessment will allow you to demonstrate your skills in building AI-powered agent workflows, predictive modules and integrate software components using modern tools and frameworks.

## Submission Deadline
Please submit your completed assignment by **14th July 2025**. We will take stock of your submitted repository for evaluation at this point. After that, any further commits will not be part of the evaluation but can be considered as interview preparations.

## Reference Repository
Your tasks will be based on the following OpenAI CS Agents Demo repository: [OpenAI CS Agents Demo](https://github.com/openai/openai-cs-agents-demo)

Please fork this repository and use it as the foundation for completing the tasks. Feel free to swap framework or model providers as you see fit. (Ps: Our team uses Langchain/Langgraph and will be happy to review code written in these frameworks)

## Expected Deliverable Artifacts
Submit the following:

- Link to your GitHub fork. Do ensure that the repository is accessible! The repo should contain the following
- Artifacts for your completed tasks (code and documentation)
- Instructions to run your code – you are recommended to make the application easily deployable to a service such as Replit, so that we can easily spin up an instance to check out your application.
- PDF or Markdown document with your Integration Strategy write-up. 
- **Optional** Screenshots or access details for your bonus dashboard/logging solution.

## Further Notes

-	You are encouraged to use AI tools (e.g., ChatGPT, GitHub Copilot, Claude, Gemini) to help accelerate your delivery. Ensure you understand the generated code and document your reasoning clearly. Your grasp and thoughtful integration of AI-generated content will be evaluated.
-	This assessment is meant to be time-scoped, in respect of your busy schedules. As a guideline the tasks above should take no more than 10 hours of focused time.

All the best! We look forward to reviewing your submission.

## Tasks

| id | status | task |
| -- | -- | -- |
| 01 | open | Custom Agent and Tool |
| 02 | open | Retrieval-Augmented Generation (RAG) |
| 03 | open | Integration Strategy and Approach (Write-up) |
| 04 | open | Optional Bonus Task |

### (open) Task 1: Custom Agent and Tool
Implement a new custom agent and at least one custom tool suitable for a telecommunications use case. Possible examples include:

- Telco Products/Roaming plan recommendation engine (preferred, due to immediate relevance to JD)
- Billing dispute parsing and categorization (good to have)
- Data usage history check (good to have)

Mocked data is allowed to enable the tool’s demonstration. To keep within a time bound, please describe some of the approaches you have planned and would have utilised, if given sufficient time.

Clearly document:

- The specific business problem your custom tool addresses.
- Integration method between your tool and the agent.

### (open) Task 2: Retrieval-Augmented Generation (RAG)
Implement a basic RAG pipeline to ground your agent's responses. You may use:

- A small document collection
- Mocked/Generated telco knowledge base 
- Public web available data

Clearly indicate in your response logs when retrieved information is being utilized. Whilst there is limited opportunity to extensively fine-tune, do state some your proposed techniques/approaches to improve the RAG pipeline

### (open) Task 3: Integration Strategy and Approach (Write-up)
Provide a concise (~400 words) strategy document outlining:

- Possible deployment methods for your agent in an enterprise telco environment (e.g., WhatsApp, Microsoft Teams, web portal).
- Anticipated practical integration challenges (authentication, latency, UI design, scalability).
- Metrics to evaluate agent performance and value in a production environment.

### (open) Task 4: Optional Bonus Task
Create a simple usage dashboard or logging mechanism demonstrating:

- Total user queries handled
- Breakdown of tool usage frequency
- Retrieval hit/miss analytics

Feel free to use lightweight frameworks like Streamlit, Gradio, NiceGUI, Flask, or FastAPI.