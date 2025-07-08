# LangChain Chatbot

A simple and interactive chatbot built with LangChain, supporting OpenAI (GPT-3.5 Turbo), Google Gemini (gemini-2.0-flash), and Google Vertex AI (chat-bison) models. This application provides a conversational interface with memory capabilities, multi-modal support (text and images, where supported by the model), and easy configuration options.

- 🤖 **Multi-provider:** Use OpenAI, Google Gemini, or Google Vertex AI models
- 🖼️ **Multi-modal:** Supports text and (where available) image input/output with Gemini, Vertex AI, and future OpenAI models
- 🧠 **Conversation memory:** Remembers chat history for context-aware responses
- ⚙️ **Configurable:** Easily switch models and API keys in the sidebar
- 💬 **Modern UI:** Real-time chat with typing indicators and clear chat functionality

## Features

- 🤖 Interactive chat interface with Streamlit
- 🧠 Conversation memory using LangChain
- ⚙️ Configurable model selection (OpenAI, Gemini, Vertex AI)
- 🌡️ Adjustable temperature for response creativity
- 💬 Real-time chat with typing indicators
- 🗑️ Clear chat functionality
- 🔧 Easy configuration through sidebar

## Supported Models

- **OpenAI (GPT-3.5 Turbo)**
- **Google Gemini (gemini-2.0-flash)**
- **Google Vertex AI (chat-bison)**

## Prerequisites

- Python 3.8 or higher
- API keys for your chosen provider(s):
  - OpenAI API key (for GPT-3.5 Turbo)
  - Google Gemini API key (for gemini-2.0-flash)
  - Google Cloud service account key + project ID (for Vertex AI)

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

### Environment Variables
Copy `.env.example` to `.env` and fill in the required keys:

```
OPENAI_API_KEY=your-openai-api-key
GEMINI_API_KEY=your-gemini-api-key
VERTEXAI_PROJECT_ID=your-gcp-project-id
VERTEXAI_REGION=us-central1
```

- For Vertex AI, you must also set up a Google Cloud service account and download the JSON key (see Vertex AI Setup above).

### .gitignore
- The `.gitignore` file ensures that `venv/`, `.env`, `.env.example`, and Google Cloud service account keys are not committed to the repository.

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
- You can use OpenAI, Google Gemini (gemini-2.0-flash), or Google Vertex AI (chat-bison) models by selecting them in the sidebar.
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

## How to Find Your Google Cloud Project ID

Your **Google Cloud Project ID** is a unique identifier for your project in Google Cloud. Here’s how you can find it:

### Method 1: Google Cloud Console (Web UI)
1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. At the top left, click the project dropdown (it may show your current project name).
3. In the list, you’ll see all your projects.  
   - The **Project ID** is shown in the “ID” column (not the “Name” column).
   - It usually looks like: `my-sample-project-123456`

### Method 2: Command Line (gcloud CLI)
If you have the Google Cloud SDK installed, run:
```sh
gcloud projects list
```
This will show a table with your project names, IDs, and numbers.

### Method 3: Billing or API Dashboard
- When you enable billing or APIs, the project ID is often shown in the dashboard or URL.

**Note:**
- The Project ID is globally unique and is used in API calls and configuration.
- Do not confuse it with the Project Name (which is just a label and can be changed). 

## How to Get Google Vertex AI Credentials

To use Vertex AI, you need a Google Cloud service account key (JSON file) with the right permissions. Here’s how to get it:

1. **Create a Google Cloud Project**
   - Go to the [Google Cloud Console](https://console.cloud.google.com/).
   - Click the project dropdown at the top and select “New Project”.

2. **Enable Vertex AI API**
   - In your project, go to “APIs & Services” > “Enable APIs and Services”.
   - Search for “Vertex AI API” and enable it.

3. **Create a Service Account**
   - Go to “IAM & Admin” > “Service Accounts”.
   - Click “Create Service Account”.
   - Give it a name (e.g., `vertex-ai-sa`).
   - Click “Create and Continue”.

4. **Grant Vertex AI Permissions**
   - Assign the role: `Vertex AI User` (or `Vertex AI Admin` for full access).
   - Click “Continue” and then “Done”.

5. **Create and Download a Service Account Key**
   - Click on your new service account in the list.
   - Go to the “Keys” tab.
   - Click “Add Key” > “Create new key”.
   - Choose “JSON” and click “Create”.
   - Download the JSON file and keep it safe (this is your “API key” for Vertex AI).

6. **Set the Environment Variable**
   - Set the environment variable in your shell or `.env` file:
     ```
     GOOGLE_APPLICATION_CREDENTIALS=/path/to/your/service-account-file.json
     ```
     Replace `/path/to/your/service-account-file.json` with the actual path to your downloaded JSON key.

7. **Set Project and Region**
   - In your `.env` or via the app sidebar, set:
     ```
     VERTEXAI_PROJECT_ID=your-gcp-project-id
     VERTEXAI_REGION=us-central1
     ```

**References:**
- [Google Cloud: Creating and managing service account keys](https://cloud.google.com/iam/docs/creating-managing-service-account-keys)
- [Vertex AI Python Client Authentication](https://cloud.google.com/vertex-ai/docs/start/client-auth) 

