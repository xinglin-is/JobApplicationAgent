# Job Application Agent - Planning

## Project Overview
**"An agent that tailors your CV to any job posting"**

## Core Features
- **Information Gathering:** Agent reads a target job posting (using a URL tool) and ingests your current CV.
- **Content Tailoring:** Rewrites the bullet points in your CV to match the specific language, keywords, and tone of the job posting.
- **Evaluation (Eval):** Scores the match between your CV and the job description both *before* and *after* the rewrite to quantify the improvement.

## Technical Scope (What this covers)
- **Agents:** Building autonomous agents capable of making decisions and calling tools.
- **Tools:** Creating tools for the agent to use (e.g., web scraping/URL reading tools).
- **Streaming:** Implementing streaming responses so the user can see the rewrite happen in real-time.
- **Evaluation:** Using LLMs as judges to evaluate the quality of the generated CV against the job requirements.
- **Prompt Engineering:** Crafting robust prompts for extraction, rewriting, and evaluation.

## Proposed Phases (Draft)

### Phase 1: Core Parsing & Tools
- Set up project structure.
- Build the URL scraping tool to extract text from job posting links.
- Write base prompts for extracting key requirements from job descriptions.

### Phase 2: The Rewriter Agent
- Implement the agent that takes the parsed job description and the raw CV.
- Implement streaming for the agent's output.
- Prompt engineer the rewriting process to ensure the resume doesn't hallucinate but just reframes existing experience.

### Phase 3: Evaluation Engine
- Build the scoring logic (evaluator).
- Test the CV against the job posting before and after the agent's changes.
- Output a detailed score breakdown.

### Phase 4: UI / CLI Refinement
- Tie it all together into a clean interface (CLI or Web UI).
