# AI Voice Assistant - Replit Environment

## Project Overview
A six-mode AI assistant with advanced voice and diagram capabilities:
- **General Chat Mode**: ChatGPT-like conversations with voice responses
- **RAG Mode**: Document Q&A with PDF uploads and voice synthesis
- **Image Chat Mode**: Image analysis and visual Q&A with camera/upload support
- **Process Flow Creator**: AI-powered process flow diagram generation in PowerPoint and Excel formats
- **Voice Cloning**: Clone any voice and convert text to speech with professional quality controls
- **BPMN Diagram Generator**: Generate standard BPMN 2.0 XML diagrams from process descriptions

# Technology Stack
- **Frontend**: Streamlit web application
- **AI Models**: OpenAI (GPT-4o, GPT-4o-mini, GPT-4-turbo, GPT-3.5-turbo) with Vision API
- **Vector Database**: Qdrant for document embeddings
- **Document Processing**: LangChain with FastEmbed, PyPDF
- **Image Processing**: Pillow (PIL) for image handling
- **Flowchart Generation**: python-pptx (PowerPoint) and openpyxl (Excel) for swimlane diagram creation
- **Voice**: OpenAI TTS with 11 voice options + ElevenLabs voice cloning with advanced quality controls

## Recent Updates
- **October 21, 2025**: BPMN Diagram Generator Mode Added
  - Added BPMN Diagram Generator as 6th mode using OpenAI
  - AI-powered business process analysis and BPMN structuring
  - Generates standard BPMN 2.0 XML format
  - Supports BPMN elements: Start/End Events, Tasks (User, Service, etc.), Gateways (Exclusive, Parallel, Inclusive)
  - Comprehensive process-to-BPMN conversion with proper element linking
  - XML preview and download functionality (.bpmn files)
  - Compatible with Camunda Modeler, bpmn.io, Signavio, Bizagi, and all BPMN 2.0 tools
  - Detailed usage instructions for importing into BPMN tools
  - Clean UI with example process descriptions
  
  **Technical Implementation**: Uses OpenAI GPT-4o to analyze process descriptions and extract BPMN elements, then generates standards-compliant BPMN XML using Python's xml.etree.ElementTree with proper namespace declarations and element relationships.

- **October 20, 2025**: Voice Cloning Mode Added
  - Added Voice Cloning mode using ElevenLabs API
  - Upload voice samples (mp3, wav, m4a, flac) for cloning
  - Advanced voice quality controls:
    - Stability slider (consistency vs expressiveness)
    - Similarity Boost (match closeness to original voice)
    - Style Exaggeration (amplify speaking style)
    - Speaker Boost (clarity enhancement)
  - Text-to-speech generation with cloned voices
  - In-browser audio playback
  - MP3 download functionality
  - Comprehensive tips and guidance for optimal results
  - Session state management for voice cloning parameters
  - Clean UI with step-by-step workflow

- **October 13, 2025**: Excel Export for Swimlane Diagrams
  - Added Excel (.xlsx) export option alongside PowerPoint
  - Implemented professional Excel swimlane formatting with openpyxl
  - Features: removed gridlines, color-coded lanes, bordered step boxes, arrow indicators
  - Global step sequencing ensures cross-lane flows maintain correct horizontal order
  - Both PowerPoint and Excel generated from same AI-analyzed flow data
  - Side-by-side download buttons for dual format export

- **October 10, 2025**: Process Flow Creator Mode - SWIMLANE Diagrams
  - Replaced Presentation Generator with Process Flow Creator (Swimlane Diagram Generator)
  - Implemented AI-powered process analysis to extract roles, steps, and handoffs
  - Built swimlane diagram generation with horizontal lanes for roles/departments
  - Color-coded lanes with labeled headers for each role
  - Position steps within their assigned lanes showing responsibility
  - Added cross-lane connectors showing handoffs between roles
  - Shape types: ovals (start/end), rectangles (processes), diamonds (decisions)
  - Enhanced AI prompt to extract role assignments and lane information
  - Created comprehensive UI guidance with swimlane examples
  - Updated documentation for swimlane diagram functionality
  - Removed python-docx dependency (no longer needed)
  
  **Technical Implementation**: Uses python-pptx for PowerPoint and openpyxl for Excel to draw rectangle backgrounds for lanes, positions flowchart shapes within lanes based on role assignments, and connects steps with straight connectors/arrows that can cross lanes.

- **October 9, 2025**: Image Chat Mode Added
  - Added Image Chat mode with upload and camera capture
  - Integrated OpenAI Vision API for image analysis
  - Implemented follow-up conversation support for images
  - Added Pillow for image processing
  - Updated UI to support three modes
  - Enhanced documentation for Image Chat feature

- **October 8, 2025**: Major feature updates
  - Added General Chat mode for ChatGPT-like conversations
  - Implemented model selection (OpenAI + open source placeholders)
  - Improved UI design with custom CSS styling
  - Fixed LSP type errors for embedding conversions
  - Updated README with comprehensive documentation
  - Cleaned up requirements.txt
  - Added graceful audio fallback for cloud environments

- **September 23, 2025**: Initial Replit setup
  - Imported from GitHub and configured for Replit
  - Fixed Qdrant connection errors
  - Resolved embedding serialization bugs
  - Configured Streamlit for Replit proxy (0.0.0.0:5000)
  - Added PortAudio system dependency
  - Implemented graceful audio playback handling

## Project Structure
- `rag_voice.py`: Main Streamlit application
- `requirements.txt`: Python dependencies
- `.streamlit/config.toml`: Streamlit configuration
- `README.md`: Comprehensive documentation

## Features
### General Chat Mode
- No document upload required
- Multiple AI model selection
- Chat history tracking
- Voice responses with TTS

### RAG Mode
- PDF document upload and processing
- Vector similarity search
- Source citation
- Voice-enabled responses

### Image Chat Mode
- Image upload from device
- Camera capture support
- OpenAI Vision API integration
- Follow-up conversation about images
- Voice-enabled visual analysis

### Process Flow Creator Mode - Swimlane Diagrams
- Chat-based process description input
- AI-powered process analysis and structuring
- Automatic extraction of:
  - Roles and departments (creates swimlanes)
  - Process steps with role assignments
  - Tools and systems involved
  - Decision points (Yes/No conditions)
  - Cross-role handoffs
- Visual swimlane diagram generation with:
  - Horizontal lanes for each role/department
  - Color-coded lane headers
  - Ovals for start/end points (green)
  - Rectangles for process steps (light blue)
  - Diamonds for decision points (yellow)
- Connector arrows showing flow including cross-lane handoffs
- Dual format export: Editable PowerPoint (.pptx) and Excel (.xlsx) downloads with professional layout

### Voice Cloning Mode
- Upload voice samples (mp3, wav, m4a, flac) to clone any voice
- Advanced voice quality controls:
  - Stability slider (0-1): Balance between consistency and expressiveness
  - Similarity Boost (0-1): Control how closely to match the original voice
  - Style Exaggeration (0-1): Amplify the speaking style of the voice
  - Speaker Boost: Enhance clarity and quality
- Text-to-speech generation with cloned voices
- In-browser audio playback
- MP3 download functionality
- Comprehensive tips for optimal voice cloning results
- Recommended: 30+ seconds of clear audio for best cloning quality

### BPMN Diagram Generator Mode
- Text-based business process description input
- AI-powered process analysis and BPMN structuring
- Automatic generation of BPMN 2.0 compliant XML
- Supported BPMN elements:
  - Start Event and End Event
  - Tasks: task, userTask, serviceTask, sendTask, receiveTask, businessRuleTask, manualTask, scriptTask
  - Gateways: exclusiveGateway (XOR), parallelGateway (AND), inclusiveGateway (OR)
  - Sequence Flows with conditional branching
- XML preview with syntax highlighting
- Download as .bpmn file
- Compatible with all standard BPMN 2.0 tools:
  - Camunda Modeler (desktop, free)
  - bpmn.io (online, free)
  - Signavio, Bizagi, and other professional tools
- Comprehensive usage instructions for importing and editing diagrams
- Example process templates in UI

### Voice Features
- 11 voice options (alloy, ash, ballad, coral, echo, fable, onyx, nova, sage, shimmer, verse)
- MP3 download capability
- Graceful fallback for cloud environments

## Configuration
### Required API Keys
**General Chat Mode:**
- OpenAI API Key

**RAG Mode:**
- OpenAI API Key
- Qdrant URL (e.g., https://xyz.aws.cloud.qdrant.io:6333)
- Qdrant API Key

**Image Chat Mode:**
- OpenAI API Key

**Process Flow Creator Mode:**
- OpenAI API Key

**Voice Cloning Mode:**
- ElevenLabs API Key (requires paid subscription - Starter plan or higher)

**BPMN Diagram Generator Mode:**
- OpenAI API Key

### Replit Environment
- **Port**: 5000 (configured for web access)
- **Workflow**: Streamlit App
- **Deployment**: Autoscale configuration
- **CORS**: Disabled for iframe compatibility
- **Host**: 0.0.0.0 (allows Replit proxy)

## Known Limitations
- Real-time audio playback unavailable in cloud (PortAudio limitation)
- MP3 download always available as fallback
- Open source models (Groq) are placeholders - fall back to GPT-4o-mini

## Development Notes
- LSP type errors fixed with flexible embedding conversion
- Audio gracefully handles environment limitations
- UI styled with custom CSS for modern look
- Mode switching dynamically shows/hides relevant UI elements
