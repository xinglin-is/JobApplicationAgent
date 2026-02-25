import os
import json
from dotenv import load_dotenv

from src.agent.graph import build_graph

def main():
    load_dotenv()
    print("Job Application Agent Pipeline Initialization")
    
    if not os.getenv("OPENAI_API_KEY"):
        print("OPENAI_API_KEY not found in environment. Skipping LLM execution.")
        return

    # Sample data
    sample_url = "https://example.com"
    
    # We will try to read a sample CV from test_cv.txt
    try:
        with open("test_cv.txt", "r", encoding="utf-8") as f:
            sample_cv = f.read()
    except FileNotFoundError:
        print("test_cv.txt not found. Creating a dummy one for testing...")
        sample_cv = "Software Engineer with 5 years of experience in Python, building web applications and data pipelines."
        with open("test_cv.txt", "w", encoding="utf-8") as f:
            f.write(sample_cv)

    print(f"\nStarting Job Application Agent for URL: {sample_url}")
    
    # Build and run the graph
    app = build_graph()
    
    initial_state = {
        "url": sample_url,
        "raw_cv": sample_cv
    }
    
    try:
        final_state = app.invoke(initial_state)
        print("\n\n--- Pipeline execution finished successfully ---")
        
        print("\n--- Initial Evaluation ---")
        init_eval = final_state.get("initial_evaluation", {})
        print(f"Score: {init_eval.get('score', 'N/A')}/100")
        print(f"Reasoning: {init_eval.get('reasoning', 'N/A')}")
        print(f"Missing Skills: {', '.join(init_eval.get('missing_skills', []))}")
        
        print("\n--- Final Evaluation ---")
        final_eval = final_state.get("final_evaluation", {})
        print(f"Score: {final_eval.get('score', 'N/A')}/100")
        print(f"Reasoning: {final_eval.get('reasoning', 'N/A')}")
        print(f"Missing Skills: {', '.join(final_eval.get('missing_skills', []))}")
        
    except Exception as e:
        print(f"\nError during Pipeline execution: {e}")

if __name__ == "__main__":
    main()
