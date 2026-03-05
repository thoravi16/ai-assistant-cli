import streamlit as st
from ai_cli.ai_engine import ask_ai, explain_code, generate_script, summarize_text
from ai_cli.file_utils import extract_content
from ai_cli.vault import save_recipe, search_recipe

st.set_page_config(page_title="AI Developer Assistant", layout="wide")
st.title("AI Assistant & Command Generator")

tab1, tab2, tab3, tab4 = st.tabs(
    ["Ask AI", "Generate Script", "Summarize File", "Command Vault"]
)

# Ask AI
with tab1:
    query = st.text_area("Ask a question")
    if st.button("Ask"):
        st.write(ask_ai(query))

# Generate Script
with tab2:
    task = st.text_area("Describe script to generate")
    if st.button("Generate"):
        st.code(generate_script(task), language="python")

# Summarize File
with tab3:
    uploaded_file = st.file_uploader("Upload file")
    if uploaded_file:
        with open(uploaded_file.name, "wb") as f:
            f.write(uploaded_file.read())
        content = extract_content(uploaded_file.name)
        st.write(summarize_text(content))

# Vault
with tab4:
    st.subheader("Save Command")
    name = st.text_input("Recipe Name")
    command = st.text_input("Command")
    tags = st.text_input("Tags (comma separated)")
    if st.button("Save"):
        save_recipe(name, command, tags.split(","))
        st.success("Saved")

    st.subheader("Search Recipes")
    keyword = st.text_input("Search")
    if st.button("Search"):
        results = search_recipe(keyword)
        for r in results:
            st.code(r["command"])
