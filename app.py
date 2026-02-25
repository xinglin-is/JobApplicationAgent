import streamlit as st
import os
from dotenv import load_dotenv

from src.agent.graph import build_graph

# Load environment variables
load_dotenv()

# Set page config
st.set_page_config(page_title="Job Application Agent", layout="wide")

st.title("💼 Job Application Agent")
st.markdown("Tailor your CV to a specific job posting intelligently.")

# Sidebar for inputs
with st.sidebar:
    st.header("Inputs")
    url_input = st.text_input("Job Posting URL", placeholder="https://example.com/job/123")
    cv_input = st.text_area("Your Raw CV", height=300, placeholder="Paste your current CV text here...")
    
    run_btn = st.button("Analyze & Rewrite", type="primary", use_container_width=True)

if run_btn:
    if not os.getenv("OPENAI_API_KEY"):
        st.error("Please set OPENAI_API_KEY in your .env file.")
        st.stop()
        
    if not url_input or not cv_input.strip():
        st.warning("Please provide both a Job Posting URL and your Raw CV.")
        st.stop()
        
    with st.spinner("Processing... This may take a couple of minutes."):
        try:
            # Build the graph
            app = build_graph()
            
            initial_state = {
                "url": url_input,
                "raw_cv": cv_input
            }
            
            # Invoke the LangGraph pipeline
            final_state = app.invoke(initial_state)
            
            st.success("Pipeline execution finished successfully!")
            
            # Layout for evaluations
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📉 Initial Evaluation")
                init_eval = final_state.get("initial_evaluation", {})
                score = init_eval.get('score', 0)
                st.metric("Match Score", f"{score}/100")
                st.write("**Reasoning:**")
                st.write(init_eval.get('reasoning', 'N/A'))
                st.write("**Missing Skills:**")
                missing_skills = init_eval.get('missing_skills', [])
                if missing_skills:
                    for skill in missing_skills:
                        st.markdown(f"- {skill}")
                else:
                    st.write("None")
                
            with col2:
                st.subheader("📈 Final Evaluation")
                final_eval = final_state.get("final_evaluation", {})
                score = final_eval.get('score', 0)
                st.metric("Match Score", f"{score}/100")
                st.write("**Reasoning:**")
                st.write(final_eval.get('reasoning', 'N/A'))
                st.write("**Missing Skills:**")
                missing_skills = final_eval.get('missing_skills', [])
                if missing_skills:
                    for skill in missing_skills:
                        st.markdown(f"- {skill}")
                else:
                    st.write("None")
                
            st.divider()
            st.subheader("✨ Rewritten CV")
            st.markdown(final_state.get("rewritten_cv", "No rewritten CV found."))
            
        except Exception as e:
            st.error(f"Error during pipeline execution: {e}")
