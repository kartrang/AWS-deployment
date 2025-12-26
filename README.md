# 🤖 AI Voice Assistant - Quad Mode RAG, Chat, Vision & Process Flow System

A powerful AI assistant with voice capabilities that supports general chat (like ChatGPT), document-specific Q&A using Retrieval-Augmented Generation (RAG), image analysis with vision AI, and AI-powered process flow diagram generation. Built with Streamlit, OpenAI, and Qdrant.

## ✨ Features

### 🎯 **Four Operating Modes**
- **General Chat Mode**: Ask any question like ChatGPT with voice responses
- **RAG Mode**: Query your uploaded PDF documents with AI-powered answers
- **Image Chat Mode**: Upload or capture images and ask questions about them with AI vision analysis
- **Process Flow Creator**: Generate professional process flow diagrams from process descriptions with AI-powered content generation

### 🧠 **Multiple AI Models**
- OpenAI models: GPT-4o, GPT-4o-mini, GPT-4-turbo, GPT-3.5-turbo
- Open source models: Llama-3.1-70b, Mixtral-8x7b, Gemma-7b (via Groq - coming soon)

### 🎤 **Voice Features**
- Text-to-speech with 11 different voice options
- Downloadable MP3 audio responses
- Real-time audio playback (when available)

### 📄 **Document Processing**
- PDF upload and processing
- Intelligent document chunking
- Vector similarity search with Qdrant
- Source citation for answers

### 🎨 **Modern UI**
- Clean, responsive design
- Mode-based dynamic interface
- Progress tracking and status updates
- Custom styling for better UX

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/Shubhamsaboo/awesome-llm-apps.git
cd awesome-llm-apps/rag_tutorials/voice_rag_openaisdk
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure API Keys

The application requires API keys which you can enter directly in the sidebar:

**For General Chat Mode:**
- [OpenAI API Key](https://platform.openai.com/) - Required for AI responses and voice generation

**For RAG Mode (Document Q&A):**
- [OpenAI API Key](https://platform.openai.com/) - For AI processing and TTS
- [Qdrant URL](https://cloud.qdrant.io/) - Vector database endpoint
- Qdrant API Key - From your Qdrant cluster settings

**For Image Chat Mode:**
- [OpenAI API Key](https://platform.openai.com/) - Required for vision AI and voice generation

**For Presentation Generator:**
- [OpenAI API Key](https://platform.openai.com/) - Required for AI content generation

### 4. Run the Application
```bash
streamlit run rag_voice.py
```

### 5. Access the Interface
Open your browser and navigate to `http://localhost:5000` (or the URL shown in the console).

## 📖 How to Use

### General Chat Mode
1. Select "General Chat" from the sidebar
2. Choose your preferred AI model
3. Enter your OpenAI API key
4. Start asking questions!
5. Get text and voice responses

### RAG (Document Q&A) Mode
1. Select "RAG (Document Q&A)" from the sidebar
2. Configure Qdrant URL, Qdrant API Key, and OpenAI API Key
3. Upload PDF documents
4. Ask questions about your documents
5. Get AI answers with source citations

### Image Chat Mode
1. Select "Image Chat" from the sidebar
2. Enter your OpenAI API key
3. Upload an image file OR capture from camera
4. Ask questions about the image
5. Get AI visual analysis with voice responses
6. Continue the conversation about the image

### Process Flow Creator Mode
1. Select "Process Flow Creator" from the sidebar
2. Enter your OpenAI API key
3. Describe your process including:
   - **Roles/Departments**: Who is responsible for each step
   - **Activities and tasks**: What needs to be done
   - **Tools and systems used**: Systems, software, or equipment
   - **Decision points**: Yes/No conditions and branches
   - **Handoffs**: When work moves between roles
4. Generate swimlane diagram with AI analysis
5. Download the editable PowerPoint file

**Features**:
- **Swimlane Layout**: Horizontal lanes for each role/department
- **Auto-detection**: AI identifies roles, steps, tools, and decision points
- **Visual Process Maps**: Different shapes for different types (ovals, rectangles, diamonds)
- **Color-coded lanes**: Each role gets a distinct color
- **Cross-lane flows**: Shows handoffs between departments
- **Editable PowerPoint**: Fully customizable output

## 🏗️ Architecture

### Document Processing Pipeline
1. **Upload**: PDF files uploaded through Streamlit interface
2. **Chunking**: Documents split using RecursiveCharacterTextSplitter
3. **Embedding**: Text converted to vectors using FastEmbed
4. **Storage**: Vectors stored in Qdrant vector database

### Query Processing Flow
1. **Embedding**: User query converted to vector
2. **Search**: Similar documents retrieved from Qdrant
3. **Context**: Relevant document chunks assembled
4. **Generation**: AI agent generates response
5. **Voice**: Text-to-speech conversion with selected voice
6. **Delivery**: Response displayed with audio download option

### General Chat Flow
1. **Input**: User question received
2. **Context**: Chat history maintained for continuity
3. **Processing**: Selected AI model generates response
4. **Voice**: TTS conversion with voice options
5. **Output**: Text and audio response delivered

### Image Chat Flow
1. **Upload/Capture**: Image uploaded or captured from camera
2. **Encoding**: Image converted to base64 format
3. **Analysis**: OpenAI Vision API analyzes image with user query
4. **Response**: AI generates detailed visual description/answer
5. **Voice**: TTS conversion with selected voice
6. **Conversation**: Follow-up questions supported with context

### Presentation Generator Flow
1. **Document Upload (Optional)**: PDF, Word, or PowerPoint files uploaded for content extraction
2. **Content Extraction**: Text extracted from uploaded documents (if provided)
3. **Template Processing (Optional)**: Template PPT loaded for styling
4. **Topic Input**: User specifies presentation topic and requirements
5. **AI Generation**: OpenAI generates structured presentation content from topic or documents
6. **PPT Creation**: python-pptx creates editable PowerPoint file with proper alignment
7. **Download**: User downloads professionally formatted presentation with centered titles and aligned content

**Key Features**:
- Works with or without source documents
- Proper text alignment (centered titles, left-aligned bullets)
- No blank bullet points
- Professional formatting

## 🛠️ Technology Stack

- **Frontend**: Streamlit
- **AI Framework**: OpenAI Agents SDK, OpenAI Vision API
- **Vector Database**: Qdrant
- **Embeddings**: FastEmbed
- **Document Processing**: LangChain, PyPDF, python-docx, python-pptx
- **Image Processing**: Pillow (PIL)
- **Presentation Generation**: python-pptx
- **Text-to-Speech**: OpenAI TTS API
- **Audio**: sounddevice, PortAudio

## 📋 Requirements

See `requirements.txt` for full list. Key dependencies:
- streamlit
- openai-agents
- qdrant-client
- fastembed
- langchain
- langchain-community
- openai
- python-dotenv
- pypdf
- python-docx
- python-pptx
- Pillow

## 🎙️ Voice Options

Choose from 11 different voices:
- alloy, ash, ballad, coral, echo
- fable, onyx, nova, sage, shimmer, verse

## 🔒 Security

- API keys entered via secure password fields
- No credentials stored in code
- SSL verification enabled for Qdrant
- Environment variable support for deployment

## 🌐 Deployment

The application is configured for deployment on Replit and other cloud platforms:
- Port 5000 configured for web access
- Autoscale deployment settings
- Production-ready error handling

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is part of the awesome-llm-apps repository.

## 🙏 Acknowledgments

- OpenAI for the AI models and TTS capabilities
- Qdrant for vector database
- Streamlit for the web framework
- LangChain for document processing tools

## 📧 Support

For issues and questions, please open an issue on GitHub.

---

**Made with ❤️ using OpenAI, Streamlit, and Qdrant**
