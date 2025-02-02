# mAI Research Assistant

An advanced research assistant that leverages the power of Ollama with the Deepseek-R1 8B model to generate detailed and well-structured responses based on real-time web research.

## 🌟 Key Features

- 🤖 **Advanced Model**: Uses Deepseek-R1 8B through Ollama for high-quality response generation
- 🔍 **Intelligent Web Search**: Integration with Tavily for accurate and relevant web searches
- 📝 **Structured Responses**: Generates well-organized content with introduction, key principles, and practical examples
- 💾 **Efficient Caching**: Built-in caching system for optimized performance
- 🎯 **Contextual Analysis**: Synthesizes and analyzes multiple sources for comprehensive responses
- 🖥️ **Web Interface**: Modern and responsive UI built with Streamlit

## 📋 Prerequisites

- Python 3.8 or higher
- Ollama installed and configured ([Ollama Installation Guide](https://github.com/ollama/ollama))
- Deepseek-R1 8B model installed in Ollama
- Tavily API key for web searches

## 🛠️ Installation

1. Clone the repository:
```bash
git clone https://github.com/maigenai/mai_searcher.git
cd mai_searcher
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
.\venv\Scripts\activate  # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
export TAVILY_API_KEY='your-api-key'
```

## 🚀 Getting Started

1. Ensure Ollama is running and the Deepseek-R1 model is available:
```bash
ollama pull deepseek-r1:8b
ollama run deepseek-r1:8b
```

2. Launch the application:
```bash
streamlit run app.py
```

3. Open your browser at http://localhost:8501

## ⚙️ Configuration

Main settings are managed through the `CONFIG` dictionary in the code:

```python
CONFIG = {
    "MODEL_NAME": "deepseek-r1:8b",    # Ollama model to use
    "MAX_SEARCH_RESULTS": 3,           # Maximum number of search results
    "CACHE_SIZE": 100                  # Cache size
}
```

## 🏗️ Project Structure

```
mai-research-assistant/
├── app.py              # Main application
├── requirements.txt    # Dependencies
├── .env               # Environment variables configuration (create this)
└── README.md          # Documentation
```

## 🔄 Workflow

1. User inputs a research query
2. System performs web search through Tavily
3. Results are analyzed and synthesized by the Deepseek-R1 model
4. A structured response is generated with:
   - Introduction
   - Key principles
   - Practical examples
   - Conclusions
5. Consulted sources are displayed with direct links

## 🤝 How to Contribute

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/NewFeature`)
3. Commit your changes (`git commit -m 'Add new feature'`)
4. Push to the branch (`git push origin feature/NewFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## 🙏 Acknowledgments

- [Ollama](https://ollama.ai/) for local LLM hosting
- [Deepseek](https://github.com/deepseek-ai/DeepSeek-LLM) for the R1 8B language model
- [LangChain](https://github.com/langchain-ai/langchain) for the orchestration framework
- [Streamlit](https://streamlit.io/) for the web framework
- [Tavily](https://tavily.com/) for the web search API
