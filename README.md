# Sofi - Real-time Voice Recognition Assistant

Sofi è un sistema di riconoscimento vocale in tempo reale che ascolta continuamente una parola di attivazione e trascrive il discorso in testo una volta attivato, inviandolo all'API Gemini per generare risposte.

## Funzionalità

- Riconoscimento vocale continuo in tempo reale
- Attivazione tramite parola chiave ("Sofi")
- Rilevamento automatico del microfono
- Supporto multipiattaforma (Windows, macOS, Linux)
- Configurazione personalizzabile
- Calibrazione automatica del rumore ambientale
- Integrazione con l'API Gemini per la generazione di risposte AI

## Struttura del Progetto

```
.
├── voice_recognizer/           # Package principale
│   ├── __init__.py             # Inizializzazione del package
│   ├── __main__.py             # Punto di ingresso per l'esecuzione diretta
│   ├── main.py                 # File principale dell'applicazione
│   ├── config/                 # Configurazioni
│   │   ├── settings.py         # Impostazioni dell'applicazione
│   │   └── api_settings.py     # Impostazioni API
│   ├── services/               # Servizi
│   │   ├── __init__.py
│   │   ├── microphone_service.py  # Gestione del microfono
│   │   ├── recognition_service.py # Gestione del riconoscimento vocale
│   │   └── gemini_service.py      # Servizio per l'API Gemini
│   └── utils/                  # Utilità
│       ├── __init__.py
│       ├── logging_utils.py    # Utilità per la gestione dei messaggi
│       └── exception_utils.py  # Utilità per la gestione degli errori
├── run.py                      # Script di avvio
├── requirements.txt            # Dipendenze
├── .env.example                # Esempio di file di ambiente
└── README.md                   # Documentazione
```

## Requisiti

- Python 3.7+
- Librerie richieste (installabili tramite requirements.txt):
  - SpeechRecognition
  - PyAudio
  - pydub
  - requests
  - python-dotenv

## Installazione

1. Clona il repository:
   ```bash
   git clone https://github.com/tuo-username/Sofi.git
   cd Sofi
   ```

2. Crea un ambiente virtuale (opzionale ma consigliato):
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   # o
   venv\Scripts\activate     # Windows
   ```

3. Installa le dipendenze:
   ```bash
   pip install -r requirements.txt
   ```

4. Configura le variabili d'ambiente:
   - Copia il file `.env.example` in `.env`
   - Modifica il file `.env` aggiungendo la tua chiave API Gemini

## Utilizzo

### Avvio Rapido

Esegui lo script principale:

```bash
python run.py
```

Oppure esegui il modulo direttamente:

```bash
python -m voice_recognizer
```

Il programma ascolterà attraverso il microfono predefinito e attenderà la parola di attivazione "Sofi". Una volta attivato, trascriverà il tuo discorso in testo, lo invierà all'API Gemini e visualizzerà la risposta dell'API nella console.

### Come Funziona

1. Il sistema ascolta continuamente la parola di attivazione "Sofi"
2. Quando "Sofi" viene rilevato, l'assistente si attiva per 10 secondi
3. Durante questo periodo attivo, tutto il parlato riconosciuto viene trascritto e inviato all'API Gemini
4. La risposta dell'API viene visualizzata nella console
5. Ogni nuova frase riconosciuta estende il periodo attivo
6. Dopo 10 secondi di silenzio, il sistema torna alla modalità di rilevamento della parola di attivazione

## Personalizzazione

Le impostazioni di riconoscimento vocale possono essere modificate nel file `voice_recognizer/config/settings.py`:

- Cambiare la parola di attivazione
- Regolare il timeout di ascolto attivo
- Modificare le impostazioni di sensibilità
- Cambiare la lingua per il riconoscimento

Le impostazioni dell'API Gemini possono essere modificate nel file `voice_recognizer/config/api_settings.py`.

## Licenza

MIT

## Ringraziamenti

Questo progetto utilizza l'API di riconoscimento vocale di Google per la conversione da parlato a testo e l'API Gemini per la generazione delle risposte AI. 