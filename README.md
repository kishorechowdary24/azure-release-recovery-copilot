\# Azure Release Recovery Copilot



An AI copilot that helps investigate Azure web app deployment incidents by comparing the reported problem with lessons saved from past incidents.



\## What it does



1\. Accepts a deployment error and optional details about a recent change.

2\. Searches Hindsight for related past incidents when memory is enabled.

3\. Uses Groq to generate a likely explanation, suggested checks, and a confidence level.

4\. Lets the user record the actual cause and fix so the outcome can help with future incidents.



This is a hackathon prototype. It accepts incident details manually; it does not connect directly to Azure DevOps or make changes to Azure resources.



\## Built with



\- Python

\- Streamlit

\- Hindsight for incident memory

\- Groq for AI generated investigation advice



\## Run locally



1\. Create a `.env` file in the project folder with these variables:



&#x20;  ```text

&#x20;  HINDSIGHT\_BASE\_URL=your\_hindsight\_endpoint

&#x20;  HINDSIGHT\_API\_KEY=your\_hindsight\_api\_key

&#x20;  HINDSIGHT\_BANK\_ID=your\_bank\_id

&#x20;  GROQ\_API\_KEY=your\_groq\_api\_key

