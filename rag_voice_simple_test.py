"""
Simple test wrapper for rag_voice - loads rag_voice as a module in Streamlit
"""
import streamlit as st

st.set_page_config(page_title="Voice RAG Assistant", layout="wide")

st.title("🎤 Voice RAG Assistant - Loading...")

try:
    # Try to import and run the main app
    from rag_voice import main
    
    st.success("App module loaded successfully!")
    st.info("Running the main application...")
    
    # Call main which will set up the Streamlit UI
    main()
    
except Exception as e:
    st.error(f"Failed to load application: {str(e)}")
    import traceback
    st.code(traceback.format_exc(), language="python")
