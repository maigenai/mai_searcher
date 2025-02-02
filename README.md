# mAI Research Assistant

Un assistente di ricerca avanzato che sfrutta la potenza di Ollama con il modello Deepseek-R1 8B per generare risposte dettagliate e ben strutturate basate su ricerche web in tempo reale.

## 🌟 Caratteristiche Principali

- 🤖 **Modello Avanzato**: Utilizza Deepseek-R1 8B tramite Ollama per generare risposte di alta qualità
- 🔍 **Ricerca Web Intelligente**: Integrazione con Tavily per ricerche web accurate e pertinenti
- 📝 **Risposte Strutturate**: Genera contenuti ben organizzati con introduzione, principi fondamentali ed esempi pratici
- 💾 **Caching Efficiente**: Sistema di cache integrato per ottimizzare le prestazioni
- 🎯 **Analisi Contestuale**: Sintetizza e analizza multiple fonti per risposte complete
- 🖥️ **Interfaccia Web**: UI moderna e responsive costruita con Streamlit

## 📋 Prerequisiti

- Python 3.8 o superiore
- Ollama installato e configurato ([Guida Installazione Ollama](https://github.com/ollama/ollama))
- Modello Deepseek-R1 8B installato in Ollama
- Chiave API Tavily per le ricerche web

## 🛠️ Installazione

1. Clona il repository:
```bash
git clone https://github.com/tuonome/mai-research-assistant.git
cd mai-research-assistant
```

2. Crea e attiva un ambiente virtuale:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# oppure
.\venv\Scripts\activate  # Windows
```

3. Installa le dipendenze:
```bash
pip install -r requirements.txt
```

4. Configura le variabili d'ambiente:
```bash
export TAVILY_API_KEY='your-api-key'
```

## 🚀 Avvio

1. Assicurati che Ollama sia in esecuzione e che il modello Deepseek-R1 sia disponibile:
```bash
ollama pull deepseek-r1:8b
ollama run deepseek-r1:8b
```

2. Avvia l'applicazione:
```bash
streamlit run app.py
```

3. Apri il browser all'indirizzo http://localhost:8501

## ⚙️ Configurazione

Le impostazioni principali sono gestite tramite il dizionario `CONFIG` nel codice:

```python
CONFIG = {
    "MODEL_NAME": "deepseek-r1:8b",    # Modello Ollama da utilizzare
    "MAX_SEARCH_RESULTS": 3,           # Numero massimo di risultati di ricerca
    "CACHE_SIZE": 100                  # Dimensione della cache
}
```

## 🏗️ Struttura del Progetto

```
mai-research-assistant/
├── app.py              # Applicazione principale
├── requirements.txt    # Dipendenze
├── .env               # Configurazione variabili d'ambiente (da creare)
└── README.md          # Documentazione
```

## 🔄 Workflow

1. L'utente inserisce una query di ricerca
2. Il sistema esegue una ricerca web tramite Tavily
3. I risultati vengono analizzati e sintetizzati dal modello Deepseek-R1
4. Viene generata una risposta strutturata con:
   - Introduzione
   - Principi fondamentali
   - Esempi pratici
   - Conclusioni
5. Le fonti consultate vengono mostrate con link diretti

## 🤝 Come Contribuire

1. Fai un fork del repository
2. Crea un branch per la tua feature (`git checkout -b feature/NuovaFeature`)
3. Committa le tue modifiche (`git commit -m 'Aggiunta nuova feature'`)
4. Pusha al branch (`git push origin feature/NuovaFeature`)
5. Apri una Pull Request

## 📄 Licenza

Questo progetto è distribuito sotto licenza MIT. Vedi il file `LICENSE` per maggiori dettagli.

## 🙏 Ringraziamenti

- [Ollama](https://ollama.ai/) per l'hosting locale di modelli LLM
- [Deepseek](https://github.com/deepseek-ai/DeepSeek-LLM) per il modello linguistico R1 8B
- [LangChain](https://github.com/langchain-ai/langchain) per il framework di orchestrazione
- [Streamlit](https://streamlit.io/) per il framework web
- [Tavily](https://tavily.com/) per l'API di ricerca web