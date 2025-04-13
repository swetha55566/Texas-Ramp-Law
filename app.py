import streamlit as st
import requests
import fitz  # PyMuPDF


# ========== Settings ==========
LM_API_ENDPOINT = "http://127.0.0.1:1234/v1/chat/completions"
st.set_page_config(
    page_title="Ramp Compliance Chatbot",
    page_icon="🤖"
)


# ========== Title & Instructions ==========
st.title("🤖 Ramp Compliance Chatbot (LM Studio)")
st.markdown(
    "Upload a permit PDF or paste text, then ask if it's ADA/Texas compliant."
)


# ========== PDF Upload or Text Area ==========
pdf_file = st.file_uploader("📄 Upload permit PDF (optional)", type=["pdf"])
permit_text = ""

if pdf_file:
    with fitz.open(stream=pdf_file.read(), filetype="pdf") as doc:
        for page in doc:
            permit_text += page.get_text()
else:
    permit_text = st.text_area("Or paste permit text:")


# ========== Ask a Question ==========
question = st.text_input(
    "❓ Ask a question (e.g., Is this compliant?)"
)


# ========== Rule-Based Compliance Hints ==========
def rule_check(text):
    violations = []

    if "1:8" in text or "1 to 8" in text:
        violations.append("❌ Slope 1:8 (ADA requires max 1:12)")

    if "32 inches" in text or "width of 32" in text:
        violations.append("❌ Width below 36 inches (minimum)")

    if "no handrails" in text:
        violations.append(
            "❌ Missing handrails (required if rise exceeds 6 inches)"
        )

    if "no landings" in text:
        violations.append("❌ Missing landings (required for top and bottom)")

    return violations


# ========== Submit & Respond ==========
if st.button("🚀 Submit") and question and permit_text.strip():
    st.markdown("### 🔎 Preliminary Rule-Based Check")

    for issue in rule_check(permit_text.lower()):
        st.error(issue)

    prompt = f"{permit_text}\n\nQuestion: {question}"

    with st.spinner("Thinking..."):
        try:
            response = requests.post(
                LM_API_ENDPOINT,
                headers={"Content-Type": "application/json"},
                json={
                    "model": "local-model",
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.5
                }
            )

            if response.status_code == 200:
                result = response.json()["choices"][0]["message"]["content"]
                st.markdown("### 🤖 LLM Answer")
                st.success(result)
            else:
                st.error(
                    f"❌ API Error {response.status_code}: {response.text}"
                )

        except Exception as e:
            st.error(f"🚫 Failed to connect to LM Studio: {e}")
