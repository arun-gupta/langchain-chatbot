import os
import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_vertexai import ChatVertexAI
from langchain_anthropic import ChatAnthropic
from langchain.schema import HumanMessage, AIMessage
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain_ollama import ChatOllama

# Load environment variables
load_dotenv()

# Helper function to mask API keys
def mask_key(key):
    if not key:
        return "[not set]"
    if len(key) <= 8:
        return key
    return key[:4] + "..." + key[-4:]

# Page configuration
st.set_page_config(
    page_title="LangChain Chatbot",
    page_icon="🤖",
    layout="wide"
)

# Initialize session state for chat history and API keys
if "messages" not in st.session_state:
    st.session_state.messages = []

if "conversation" not in st.session_state or "llm_model" not in st.session_state:
    st.session_state.llm_model = os.getenv("LLM_MODEL", "gpt-3.5-turbo")
    st.session_state.temperature = float(os.getenv("LLM_TEMPERATURE", 0.7))
    st.session_state.conversation = None

# Initialize API keys from environment variables
if "openai_api_key" not in st.session_state:
    st.session_state.openai_api_key = os.getenv("OPENAI_API_KEY", "")
if "gemini_api_key" not in st.session_state:
    st.session_state.gemini_api_key = os.getenv("GEMINI_API_KEY", "")
if "anthropic_api_key" not in st.session_state:
    st.session_state.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY", "")
if "claude_model" not in st.session_state:
    st.session_state.claude_model = os.getenv("CLAUDE_MODEL", "claude-3-haiku-20240307")
if "vertexai_project" not in st.session_state:
    st.session_state.vertexai_project = os.getenv("VERTEXAI_PROJECT_ID", "")
if "vertexai_region" not in st.session_state:
    st.session_state.vertexai_region = os.getenv("VERTEXAI_REGION", "us-central1")
if "vertexai_model" not in st.session_state:
    st.session_state.vertexai_model = os.getenv("VERTEXAI_MODEL", "chat-bison")
if "ollama_model" not in st.session_state:
    st.session_state.ollama_model = os.getenv("OLLAMA_MODEL", "llama3")
if "ollama_temperature" not in st.session_state:
    st.session_state.ollama_temperature = float(os.getenv("OLLAMA_TEMPERATURE", 0.7))
# GOOGLE_APPLICATION_CREDENTIALS check
if "google_application_credentials" not in st.session_state:
    st.session_state.google_application_credentials = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "")
if "gac_set" not in st.session_state:
    st.session_state.gac_set = bool(st.session_state.google_application_credentials)
if "gac_exists" not in st.session_state:
    st.session_state.gac_exists = os.path.isfile(st.session_state.google_application_credentials) if st.session_state.gac_set else False


# Sidebar for API keys and model selection
with st.sidebar:
    st.title("🔑 API & Model Configuration")

    # Model provider selection
    model_provider = st.selectbox(
        "Select Model Provider",
        ["OpenAI", "Google Gemini", "Anthropic Claude", "Google Vertex AI", "Ollama (Llama3)"],
        index=0,
    )
    if model_provider == "OpenAI":
        openai_api_key = st.text_input("OpenAI API Key", type="password", value=st.session_state.get("openai_api_key", ""))
        if openai_api_key:
            st.session_state["openai_api_key"] = openai_api_key
    elif model_provider == "Google Gemini":
        gemini_api_key = st.text_input("Gemini API Key", type="password", value=st.session_state.get("gemini_api_key", ""))
        if gemini_api_key:
            st.session_state["gemini_api_key"] = gemini_api_key
    elif model_provider == "Anthropic Claude":
        anthropic_api_key = st.text_input("Anthropic API Key", type="password", value=st.session_state.get("anthropic_api_key", ""))
        if anthropic_api_key:
            st.session_state["anthropic_api_key"] = anthropic_api_key
        st.session_state.claude_model = st.text_input(
            "Claude Model",
            value=st.session_state.get("claude_model", "claude-3-haiku-20240307")
        )
    elif model_provider == "Google Vertex AI":
        vertexai_project = st.text_input("Vertex AI Project ID", value=st.session_state.get("vertexai_project", ""))
        vertexai_region = st.text_input("Vertex AI Region", value=st.session_state.get("vertexai_region", "us-central1"))
        if vertexai_project:
            st.session_state["vertexai_project"] = vertexai_project
        if vertexai_region:
            st.session_state["vertexai_region"] = vertexai_region
        st.session_state.vertexai_model = st.text_input(
            "Vertex AI Model",
            value=st.session_state.get("vertexai_model", "chat-bison")
        )
    elif model_provider == "Ollama (Llama3)":
        ollama_model = st.text_input("Ollama Model", value=st.session_state.get("ollama_model", "llama3"))
        if ollama_model:
            st.session_state["ollama_model"] = ollama_model
        st.session_state.ollama_temperature = st.slider(
            "Ollama Temperature",
            min_value=0.0,
            max_value=1.0,
            value=st.session_state.get("ollama_temperature", 0.7),
            step=0.05,
        )
    
    st.markdown("---")
    st.subheader("🔑 API Key Status")
    st.write(f"**Current Provider:** {model_provider}")
    st.write(f"**OpenAI Key:** {'✅' if st.session_state.get('openai_api_key') else '❌'}")
    st.write(f"**Gemini Key:** {'✅' if st.session_state.get('gemini_api_key') else '❌'}")
    st.write(f"**Anthropic Key:** {'✅' if st.session_state.get('anthropic_api_key') else '❌'}")
    st.write(f"**Vertex Project:** {'✅' if st.session_state.get('vertexai_project') else '❌'}")
    st.write(f"**Vertex Region:** {'✅' if st.session_state.get('vertexai_region') else '❌'}")
    if st.session_state.gac_set and st.session_state.gac_exists:
        st.write(f"**Google Vertex AI Key:** ✅")
        st.write(f"**Google Vertex AI Key File Exists:** ✅")
    st.write(f"**Ollama Model:** {'✅' if st.session_state.get('ollama_model') else '❌'}")
    
    # Show masked keys for debugging
    st.markdown("---")
    st.subheader("🔍 Debug Info")
    st.write(f"**OpenAI:** `{mask_key(st.session_state.get('openai_api_key', ''))}`")
    st.write(f"**Gemini:** `{mask_key(st.session_state.get('gemini_api_key', ''))}`")
    st.write(f"**Anthropic:** `{mask_key(st.session_state.get('anthropic_api_key', ''))}`")
    st.write(f"**Vertex Project:** `{st.session_state.get('vertexai_project', '[not set]')}`")
    st.write(f"**Vertex Region:** `{st.session_state.get('vertexai_region', '[not set]')}`")
    if st.session_state.gac_set and st.session_state.gac_exists:
        st.write(f"**Google Vertex AI:** `{st.session_state.google_application_credentials or '[not set]'}`")
        st.write(f"**Google Vertex AI File Exists:** {'✅' if st.session_state.gac_exists else '❌'}")
    st.write(f"**Ollama Model:** `{st.session_state.get('ollama_model', '[not set]')}`")

    # Clear chat button
    if st.button("Clear Chat"):
        st.session_state.messages = []
        if st.session_state.conversation:
            st.session_state.conversation.memory.clear()
        st.rerun()

# LLM selection logic
if model_provider == "OpenAI":
    llm = ChatOpenAI(
        openai_api_key=st.session_state.get("openai_api_key"),
        model="gpt-3.5-turbo",
        temperature=0.7,
    )
elif model_provider == "Google Gemini":
    llm = ChatGoogleGenerativeAI(
        google_api_key=st.session_state.get("gemini_api_key"),
        model="gemini-2.0-flash",
        temperature=0.7,
    )
elif model_provider == "Anthropic Claude":
    llm = ChatAnthropic(
        anthropic_api_key=st.session_state.get("anthropic_api_key"),
        model=st.session_state.get("claude_model", "claude-3-haiku-20240307"),
        temperature=0.7,
    )
elif model_provider == "Google Vertex AI":
    llm = ChatVertexAI(
        project=st.session_state.get("vertexai_project"),
        location=st.session_state.get("vertexai_region", "us-central1"),
        model=st.session_state.get("vertexai_model", "chat-bison"),
        temperature=0.7,
    )
elif model_provider == "Ollama (Llama3)":
    llm = ChatOllama(
        model=st.session_state.get("ollama_model", "llama3"),
        temperature=st.session_state.get("ollama_temperature", 0.7),
    )
else:
    st.error("No valid model provider selected.")
    st.stop()

# After model_provider selection in the sidebar
if "active_provider" not in st.session_state:
    st.session_state.active_provider = model_provider

# Initialize the conversation chain if needed
if (
    st.session_state.conversation is None
    or st.session_state.llm_model != st.session_state.get("active_model")
    or st.session_state.temperature != st.session_state.get("active_temperature")
    or model_provider != st.session_state.get("active_provider")
):
    try:
        memory = ConversationBufferMemory()
        st.session_state.conversation = ConversationChain(
            llm=llm,
            memory=memory,
            verbose=False
        )
        st.session_state.active_model = st.session_state.llm_model
        st.session_state.active_temperature = st.session_state.temperature
        st.session_state.active_provider = model_provider
    except Exception as e:
        st.error(f"Error initializing chatbot: {e}")
        st.session_state.conversation = None

# Header
st.title("🤖 LangChain Chatbot")
st.markdown("A simple chatbot built with LangChain, supporting OpenAI (🔵), Google Gemini (🟣), Anthropic Claude (🟡), Google Vertex AI (🟢), Ollama  with Llama3 (🟠), and Streamlit.")

# Main chat interface
st.markdown("---")

# Define avatar icons for each provider (same shape, different color)
PROVIDER_AVATARS = {
    "OpenAI": "🔵",           # Blue circle
    "Google Gemini": "🟣",    # Purple circle
    "Anthropic Claude": "🟡", # Yellow circle
    "Google Vertex AI": "🟢", # Green circle
    "Ollama (Llama3)": "🟠", # Orange circle
}

# Display chat messages
for message in st.session_state.messages:
    if message["role"] == "assistant":
        # Use the avatar for the provider that generated this message
        provider = message.get("provider", st.session_state.get("active_provider", "OpenAI"))
        avatar = PROVIDER_AVATARS.get(provider, "🤖")
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])
    else:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("What would you like to ask?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get bot response
    avatar = PROVIDER_AVATARS.get(model_provider, "🤖")
    with st.chat_message("assistant", avatar=avatar):
        message_placeholder = st.empty()
        if st.session_state.conversation:
            try:
                with st.spinner("Thinking..."):
                    response = st.session_state.conversation.predict(input=prompt)
                message_placeholder.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response, "provider": model_provider})
            except Exception as e:
                error_message = f"Error: {str(e)}"
                message_placeholder.error(error_message)
                st.session_state.messages.append({"role": "assistant", "content": error_message, "provider": model_provider})
        else:
            error_message = "Chatbot not initialized. Please check your API key configuration."
            message_placeholder.error(error_message)
            st.session_state.messages.append({"role": "assistant", "content": error_message, "provider": model_provider})

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
        Built with ❤️ using LangChain, OpenAI, Gemini, Claude, Vertex AI, Ollama (Llama3), and Streamlit
    </div>
    """,
    unsafe_allow_html=True
) 
