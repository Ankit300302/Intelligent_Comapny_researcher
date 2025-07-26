# app.py
import streamlit as st
from agent import CompanyAgent
import json

st.set_page_config(page_title="Company Research Agent", layout="centered")

st.title("🧠 Lightweight Company Intelligence Agent")

with st.form("company_form"):
    company_name = st.text_input("Enter company name", placeholder="e.g., OpenAI")
    submitted = st.form_submit_button("Search")

if submitted and company_name:
    with st.spinner("🔍 Gathering insights..."):
        agent = LightweightCompanyAgent()
        result = agent.research_company(company_name)

    st.subheader(f"📋 Summary for {result['company_name']}")
    st.markdown(f"**🌐 Website**: {result['website'] or 'Not found'}")
    st.markdown(f"**🧠 Summary**: {result['summary']}")
    st.markdown(f"**👥 Key People**: {result['key_people']}")
    st.markdown(f"**📦 Products/Services**: {result['products_services']}")
    st.markdown(f"**🌍 Locations**: {result['locations']}")

    st.markdown("**📰 Recent News Headlines**")
    if result['recent_news']:
        for headline in result['recent_news']:
            st.write(f"- {headline}")
    else:
        st.write("No news found.")

    # JSON Download Button
    json_data = json.dumps(result, indent=2)
    file_name = f"{result['company_name'].replace(' ', '_')}_report.json"
    st.download_button(
        label="📥 Download JSON Report",
        data=json_data,
        file_name=file_name,
        mime="application/json"
    )
