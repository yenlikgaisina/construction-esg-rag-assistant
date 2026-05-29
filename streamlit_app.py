import streamlit as st
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain_community.embeddings import OpenAIEmbeddings

from ensemble import ensemble_retriever_from_docs
from full_chain import create_full_chain, ask_question
from local_loader import load_txt_files
from prompts import GENERATORS
from utils.report_generator import build_markdown_report

st.set_page_config(
    page_title="BuildLens AI",
    page_icon="🏗",
    layout="wide"
)

st.title("🏗 BuildLens AI")
st.caption(
    "Turn construction ESG documents into source-backed decisions. "
    "Analyse sustainability reports, carbon plans, tender documents, and circular economy strategies."
)

# --- Homepage value cards ---
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("#### 🔎 Understand")
    st.write("Ask plain-English questions and get answers grounded in your ESG knowledge base.")
with col2:
    st.markdown("#### 📊 Assess")
    st.write("See where projects stand across embodied carbon, circular economy and climate resilience.")
with col3:
    st.markdown("#### 📝 Communicate")
    st.write("Generate summaries, briefings and checklists you can share with clients and boards.")

st.divider()


def show_ui(qa, prompt_to_user="How may I help you?"):
    if "messages" not in st.session_state.keys():
        st.session_state.messages = [{"role": "assistant", "content": prompt_to_user}]

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # User-provided prompt
    if prompt := st.chat_input():
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

    # Generate a new response if last message is not from assistant
    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = ask_question(qa, prompt)
                st.markdown(response.content)
        message = {"role": "assistant", "content": response.content}
        st.session_state.messages.append(message)


@st.cache_resource
def get_retriever(openai_api_key=None):
    docs = load_txt_files()
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key, model="text-embedding-3-small")
    return ensemble_retriever_from_docs(docs, embeddings=embeddings)


def get_chain(openai_api_key=None, huggingfacehub_api_token=None):
    ensemble_retriever = get_retriever(openai_api_key=openai_api_key)
    chain = create_full_chain(ensemble_retriever,
                              openai_api_key=openai_api_key,
                              chat_memory=StreamlitChatMessageHistory(key="langchain_messages"))
    return chain


def get_secret_or_input(secret_key, secret_name, info_link=None):
    if secret_key in st.secrets:
        st.write("Found %s secret" % secret_key)
        secret_value = st.secrets[secret_key]
    else:
        st.write(f"Please provide your {secret_name}")
        secret_value = st.text_input(secret_name, key=f"input_{secret_key}", type="password")
    if secret_value:
        st.session_state[secret_key] = secret_value
    if info_link:
        st.markdown(f"[Get an {secret_name}]({info_link})")
    return secret_value


def ask_tab(chain):
    st.subheader("Ask questions about ESG, circular economy, embodied carbon, and construction sustainability")
    st.markdown("##### Try asking:")
    example_questions = [
        "What are the most important ESG topics in construction?",
        "Explain embodied carbon in simple terms.",
        "How can UK homes reduce overheating risk?",
        "What is circular economy in construction?",
        "What practical steps can a construction company take to improve ESG performance?",
    ]
    for question in example_questions:
        st.markdown(f"- {question}")
    show_ui(chain, "What would you like to know about ESG and sustainable construction?")


def generate_tab(chain):
    st.subheader("Generate a ready-to-share document")
    st.write("Pick a document type and BuildLens AI will draft it using the knowledge base.")

    choice = st.selectbox("Document type", list(GENERATORS.keys()))
    topic = st.text_input("Focus or project name (optional)",
                          placeholder="e.g. a mid-rise residential development")

    if st.button("Generate"):
        instruction = GENERATORS[choice]
        query = instruction
        if topic:
            query += f"\n\nFocus the response on: {topic}"
        with st.spinner("Drafting..."):
            response = ask_question(chain, query)
        st.session_state["last_generated_title"] = choice
        st.session_state["last_generated_text"] = response.content
        st.markdown(response.content)
        st.caption("⚠️ AI-generated draft. Please review before sharing.")


def download_tab():
    st.subheader("Download your report")
    title = st.session_state.get("last_generated_title")
    text = st.session_state.get("last_generated_text")
    if not text:
        st.info("Generate a document in the Generate tab first, then come back here to download it.")
        return
    report = build_markdown_report(title, text)
    st.markdown(f"**Ready to download:** {title}")
    st.download_button(
        label="Download Markdown report",
        data=report,
        file_name="buildlens_report.md",
        mime="text/markdown",
    )


def run():
    ready = True

    openai_api_key = st.session_state.get("OPENAI_API_KEY")
    huggingfacehub_api_token = st.session_state.get("HUGGINGFACEHUB_API_TOKEN")

    with st.sidebar:
        st.header("Setup")
        if not openai_api_key:
            openai_api_key = get_secret_or_input('OPENAI_API_KEY', "OpenAI API key",
                                                 info_link="https://platform.openai.com/account/api-keys")
        if not huggingfacehub_api_token:
            huggingfacehub_api_token = get_secret_or_input('HUGGINGFACEHUB_API_TOKEN', "HuggingFace Hub API Token",
                                                           info_link="https://huggingface.co/docs/huggingface_hub/main/en/quick-start#authentication")

    if not openai_api_key:
        st.warning("Missing OPENAI_API_KEY")
        ready = False
    if not huggingfacehub_api_token:
        st.warning("Missing HUGGINGFACEHUB_API_TOKEN")
        ready = False

    if not ready:
        st.stop()

    chain = get_chain(openai_api_key=openai_api_key, huggingfacehub_api_token=huggingfacehub_api_token)

    ask, generate, download = st.tabs(["Ask", "Generate", "Download"])
    with ask:
        ask_tab(chain)
    with generate:
        generate_tab(chain)
    with download:
        download_tab()


run()
