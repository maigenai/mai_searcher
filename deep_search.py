import streamlit as st
from typing import List, Dict
from dataclasses import dataclass
from langchain_ollama import ChatOllama
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.graph import START, END, StateGraph
from langchain_core.prompts import ChatPromptTemplate
from typing_extensions import TypedDict
import logging
import re
from functools import lru_cache

# Configurazione logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configurazione costanti
CONFIG = {
    "MODEL_NAME": "deepseek-r1:8b",
    "MAX_SEARCH_RESULTS": 3,
    "CACHE_SIZE": 100
}

# Templates migliorati
TEMPLATES = {
    "summary": """
    Analizza e sintetizza il seguente contenuto in un paragrafo conciso che risponda direttamente alla query.
    Assicurati di:
    1. Evidenziare i concetti fondamentali e la loro interconnessione
    2. Usare un linguaggio chiaro e accessibile
    3. Strutturare l'informazione in modo logico
    4. Fornire esempi pratici quando possibile

    Query: {query}
    Content: {content}
    """,
    
    "response": """    
### Introduzione
[Una breve introduzione al concetto, chiara e concisa]

### Principi Fondamentali
Si basa sui seguenti principi chiave:

1. **Primo Principio**
   - Spiegazione chiara e concisa del principio
   - **Esempio**: Un esempio pratico e concreto

2. **Secondo Principio**
   - Spiegazione chiara e concisa del principio
   - **Esempio**: Un esempio pratico e concreto

3. **Terzo Principio**
   - Spiegazione chiara e concisa del principio
   - **Esempio**: Un esempio pratico e concreto

### Tipi Principali
- **Tipo 1**: Descrizione del primo tipo
- **Tipo 2**: Descrizione del secondo tipo
- **Tipo 3**: Descrizione del terzo tipo

### Esempi Pratici

#### Primo Caso d'Uso
- Descrizione dettagliata del caso d'uso
- **Applicazione**: Esempio specifico e concreto

#### Secondo Caso d'Uso
- Descrizione dettagliata del caso d'uso
- **Applicazione**: Esempio specifico e concreto

### Conclusione
[Riepilogo dei punti chiave e delle applicazioni principali]

Domanda: {question}
Contesto: {context}
"""
}

class ResearchState(TypedDict):
    query: str
    sources: List[str]
    web_results: List[str]
    summarized_results: List[str]
    response: str

class ResearchStateInput(TypedDict):
    query: str

class ResearchStateOutput(TypedDict):
    sources: List[str]
    response: str

@dataclass
class SearchResult:
    url: str
    content: str

class AIResearcher:
    def __init__(self):
        self.model = ChatOllama(model=CONFIG["MODEL_NAME"])
        self.search_tool = TavilySearchResults(max_results=CONFIG["MAX_SEARCH_RESULTS"])
        self._cached_search = lru_cache(maxsize=CONFIG["CACHE_SIZE"])(self._search)

    def _search(self, query: str) -> Dict[str, List[str]]:
        """Funzione base per la ricerca."""
        try:
            search_results = self.search_tool.invoke(query)
            return {
                "sources": [result['url'] for result in search_results],
                "web_results": [result['content'] for result in search_results]
            }
        except Exception as e:
            logger.error(f"Errore durante la ricerca web: {e}")
            return {"sources": [], "web_results": []}

    def search_web(self, state: ResearchState) -> Dict[str, List[str]]:
        """Esegue la ricerca web utilizzando la query dallo state."""
        logger.info(f"Ricerca web per query: {state['query']}")
        return self._cached_search(state['query'])

    def summarize_results(self, state: ResearchState) -> Dict[str, List[str]]:
        """Sintetizza i risultati della ricerca."""
        prompt = ChatPromptTemplate.from_template(TEMPLATES["summary"])
        chain = prompt | self.model
        summarized_results = []

        for content in state["web_results"]:
            try:
                summary = chain.invoke({"query": state["query"], "content": content})
                clean_content = self._clean_text(summary.content)
                summarized_results.append(clean_content)
            except Exception as e:
                logger.error(f"Errore durante la sintesi: {e}")

        return {"summarized_results": summarized_results}

    def generate_response(self, state: ResearchState) -> Dict[str, str]:
        """Genera la risposta finale basata sui risultati sintetizzati."""
        try:
            prompt = ChatPromptTemplate.from_template(TEMPLATES["response"])
            chain = prompt | self.model
            content = "\n\n".join(state["summarized_results"])
            
            response = chain.invoke({
                "question": state["query"], 
                "context": content
            })
            
            return {"response": response}
        except Exception as e:
            logger.error(f"Errore durante la generazione della risposta: {e}")
            return {"response": "Si è verificato un errore durante l'elaborazione della risposta."}

    @staticmethod
    def _clean_text(text: str) -> str:
        """Pulisce il testo da tag e formattazione non necessaria."""
        # Rimuove tag think
        cleaned_text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)
        # Normalizza spazi
        cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
        # Normalizza livelli heading
        cleaned_text = re.sub(r'####+', '###', cleaned_text)
        # Corretta spaziatura tra sezioni
        cleaned_text = re.sub(r'\n### ', '\n\n### ', cleaned_text)
        # Formatta liste numerate
        cleaned_text = re.sub(r'(?m)^(\d+)\.\s+\*\*([^*]+)\*\*\s*', r'\1. **\2**', cleaned_text)
        # Formatta liste puntate
        cleaned_text = re.sub(r'(?m)^\s*-\s+', r'   - ', cleaned_text)
        # Indenta esempi
        cleaned_text = re.sub(r'(?m)^(\s*- \*\*Esempio\*\*:)', r'     \1', cleaned_text)
        # Rimuove linee vuote multiple
        cleaned_text = re.sub(r'\n\s*\n\s*\n', '\n\n', cleaned_text)
        return cleaned_text.strip()

def create_research_graph() -> StateGraph:
    """Crea e configura il grafo di ricerca."""
    researcher = AIResearcher()
    
    builder = StateGraph(
        ResearchState,
        input=ResearchStateInput,
        output=ResearchStateOutput
    )

    # Configurazione nodi e collegamenti
    builder.add_node("search_web", researcher.search_web)
    builder.add_node("summarize_results", researcher.summarize_results)
    builder.add_node("generate_response", researcher.generate_response)

    # Definizione del flusso
    builder.add_edge(START, "search_web")
    builder.add_edge("search_web", "summarize_results")
    builder.add_edge("summarize_results", "generate_response")
    builder.add_edge("generate_response", END)

    return builder.compile()

def main():
    # Configurazione della pagina
    st.set_page_config(
        page_title="mAI Research Assistant",
        page_icon="🔍",
        layout="wide"
    )

    # CSS personalizzato
    st.markdown("""
        <style>
        .main { padding: 2rem; }
        .stMarkdown p {
            font-size: 1.1rem;
            line-height: 1.7;
            margin-bottom: 1.5rem;
        }
        .source-link {
            padding: 0.5rem;
            margin: 0.5rem 0;
            border-radius: 5px;
        }
        .source-link:hover {
            background-color: #f0f2f6;
        }
        .highlight {
            background-color: #f0f2f6;
            padding: 1rem;
            border-radius: 10px;
            margin: 1rem 0;
        }
        </style>
    """, unsafe_allow_html=True)

    # Header
    col1, col2 = st.columns([2, 1])
    with col1:
        st.title("🔍 mAI Research Assistant")
    with col2:
        st.markdown("""
            <div style='text-align: right; padding-top: 1rem;'>
                <img src="https://raw.githubusercontent.com/langchain-ai/langchain/master/docs/static/img/langchain_icon.png" width="50">
            </div>
        """, unsafe_allow_html=True)

    # Descrizione
    st.markdown("""
    <div class="highlight">
        Questo assistente utilizza l'intelligenza artificiale per:
        <ul>
            <li>🎯 Cercare informazioni pertinenti da fonti affidabili</li>
            <li>📊 Analizzare e sintetizzare i dati raccolti</li>
            <li>📝 Generare risposte chiare e ben strutturate</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    # Input utente
    query = st.text_input(
        "Inserisci la tua domanda di ricerca:", 
        placeholder="Es: Quali sono le ultime innovazioni nell'AI?",
        help="Inserisci una domanda specifica per ottenere risultati più pertinenti"
    )

    if query:
        try:
            with st.spinner('🤖 Ricerca in corso...'):
                graph = create_research_graph()
                response_state = graph.invoke({"query": query})
                
                # Container per la risposta
                st.markdown("---")
                st.subheader("📝 Risposta")
                st.markdown(response_state["response"].content)
                
                # Fonti consultate
                st.markdown("---")
                st.subheader("🔗 Fonti Consultate")
                for idx, source in enumerate(response_state["sources"], 1):
                    st.markdown(
                        f"""<div class='source-link'>
                            {idx}. <a href="{source}" target="_blank">{source}</a>
                        </div>""", 
                        unsafe_allow_html=True
                    )
                
                # Suggerimenti
                st.markdown("---")
                st.markdown("""
                    <div class="highlight">
                        <h4>💡 Suggerimenti per approfondire:</h4>
                        <ul>
                            <li>Prova a fare domande più specifiche su aspetti particolari</li>
                            <li>Chiedi esempi pratici o casi d'uso</li>
                            <li>Esplora le connessioni con altri argomenti correlati</li>
                        </ul>
                    </div>
                """, unsafe_allow_html=True)
                
        except Exception as e:
            st.error(f"""
                Si è verificato un errore durante la ricerca: {str(e)}
                
                Per favore:
                - Verifica la connessione internet
                - Prova a riformulare la domanda
                - Se il problema persiste, contatta il supporto
            """)

if __name__ == "__main__":
    main()