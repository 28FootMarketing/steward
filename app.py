import os, requests, streamlit as st

API=os.getenv("STEWARD_API","http://localhost:8080/ask")
TOKEN=os.getenv("API_TOKEN","")

st.set_page_config(page_title="AI Union Steward", layout="centered")
st.title("AI Union Steward")

q = st.text_area("Ask a question:", height=140, placeholder="Example: What article covers overtime?")
verbatim = st.checkbox("Return exact text and citation only")

if st.button("Get Answer") and q.strip():
    headers = {"Authorization": f"Bearer {TOKEN}"} if TOKEN else {}
    try:
        r = requests.post(API, json={"question": q, "verbatim": verbatim}, headers=headers, timeout=180)
        if r.ok:
            data=r.json()
            st.write(data.get("answer","(no answer)"))
            if data.get("citations"):
                with st.expander("Citations"):
                    st.write("\n".join(data["citations"]))
        else:
            st.error(f"Service error: {r.status_code}")
    except Exception as e:
        st.error(f"Request failed: {e}")
