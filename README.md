# LangChain Chatbot

A simple and interactive chatbot built with LangChain, supporting both OpenAI (GPT-3.5, GPT-4, GPT-4 Turbo Preview) and Google Gemini (gemini-2.0-flash) models. This application provides a conversational interface with memory capabilities, multi-modal support (text and images, where supported by the model), and easy configuration options.

- 🤖 **Multi-provider:** Use either OpenAI or Google Gemini models
- 🖼️ **Multi-modal:** Supports text and (where available) image input/output with Gemini (gemini-2.0-flash) and future OpenAI models
- 🧠 **Conversation memory:** Remembers chat history for context-aware responses
- ⚙️ **Configurable:** Easily switch models and API keys in the sidebar
- 💬 **Modern UI:** Real-time chat with typing indicators and clear chat functionality

## Features

- 🤖 Interactive chat interface with Streamlit
- 🧠 Conversation memory using LangChain
- ⚙️ Configurable model selection (GPT-3.5, GPT-4, etc.)
- 🌡️ Adjustable temperature for response creativity
- 💬 Real-time chat with typing indicators
- 🗑️ Clear chat functionality
- 🔧 Easy configuration through sidebar

## Supported Models

- **OpenAI (GPT-3.5, GPT-4, GPT-4 Turbo Preview)**
- **Google Gemini (gemini-2.0-flash)**

## Prerequisites

- Python 3.8 or higher
- OpenAI API key

## Setup

1. **Clone or navigate to the project directory:**
   ```bash
   cd langchain-chatbot
   ```
2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Set up your environment variables:**
   - Copy `.env.example` to `.env`
   - Add your API keys:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here  # [Get your OpenAI API key here](https://platform.openai.com/api-keys)
   GEMINI_API_KEY=your_gemini_api_key_here  # [Get your Gemini API key here](https://aistudio.google.com/app/apikey)
   ```
   - Edit `.env` and replace the placeholders with your actual API keys

## Usage

1. **Start the application:**
   ```bash
   streamlit run app.py
   ```
2. **Open your browser:**
   - The application will automatically open in your default browser
   - Usually available at `http://localhost:8501`
3. **Configure the chatbot:**
   - Use the sidebar to select your preferred model (OpenAI or Gemini)
   - Enter the appropriate API key for the selected model
   - Adjust the temperature for response creativity
   - Check if your API key is properly configured (status is shown for both OpenAI and Gemini)
4. **Start chatting:**
   - Type your messages in the chat input at the bottom
   - The chatbot will respond with context-aware replies
   - Use the "Clear Chat" button to start a new conversation

## Notes
- You can use either OpenAI or Google Gemini (gemini-2.0-flash) models by selecting them in the sidebar.
- The sidebar will show the status of both API keys and allow you to enter or update them at any time.
- Debug information is shown in the sidebar and above each assistant response to help you verify which model and key are being used.

## Troubleshooting
- If you see a 401 error, double-check that the correct API key is entered for the selected model.
- For Gemini, your key should **not** start with `sk-` (that's an OpenAI key).
- For OpenAI, your key should start with `sk-`.

## Configuration Options

### Models Available
- **GPT-3.5 Turbo**: Fast and cost-effective (default)
- **GPT-4**: More capable but slower and more expensive
- **GPT-4 Turbo Preview**: Latest features and improvements

### Temperature Settings
- **0.0**: Very focused and deterministic responses
- **0.7**: Balanced creativity and consistency (default)
- **1.0**: Maximum creativity and variety

## Project Structure

```
langchain-chatbot/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variables template
├── README.md          # This file
└── venv/              # Virtual environment (created during setup)
```

## Key Components

### LangChain Integration
- **ChatOpenAI**: Connects to OpenAI's API
- **ConversationBufferMemory**: Maintains conversation history
- **ConversationChain**: Orchestrates the chat flow

### Streamlit Features
- **Session State**: Persists chat history across interactions
- **Chat Interface**: Modern chat UI with user/assistant messages
- **Sidebar Configuration**: Easy access to settings
- **Error Handling**: Graceful handling of API errors

## Customization

### Adding New Models
To add support for additional models, modify the model selection in `app.py`:

```python
model = st.selectbox(
    "Select Model",
    ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo-preview", "your-new-model"],
    index=0
)
```

### Custom Prompts
You can customize the system prompt by modifying the ConversationChain initialization in `app.py`.

### Styling
The application uses Streamlit's default styling, but you can customize it by adding custom CSS in the `st.markdown()` sections.

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve this chatbot!

## License

This project is open source and available under the MIT License. 