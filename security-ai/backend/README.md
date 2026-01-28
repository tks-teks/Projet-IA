# Security AI Guardian (Prototype)

Prototype local défensif basé sur FastAPI + WebSocket, détection d’anomalies (IsolationForest) et assistant vocal.

## Prérequis
- Python 3.11+
- Navigateur compatible Web Speech API (Chrome/Edge)

## Installation (Windows)
```bash
cd security-ai\backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Entraîner le modèle (avec logs de démo)
```bash
python -m app.ml.train_demo
```

## Lancer le backend
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Lancer le simulateur de logs
```bash
python -m app.ingestion.simulator
```

## Lancer le dashboard
```bash
cd ..\frontend
python -m http.server 5500
```
Ouvrir http://localhost:5500

## Démo vocale
1. Cliquez sur **Micro**.
2. Dites "KHELIA" puis une commande (ex: "Montre les alertes critiques").
3. L’assistant répond par texte + voix.

## Endpoints principaux
- `POST /assistant/query` : requêtes vocales
- `GET /assistant/commands` : commandes supportées
- `POST /assistant/speak` : TTS backend via pyttsx3 (utile si navigateur restreint)
- `WS /ws` : push d’alertes temps réel

## STT offline (bonus)
Vous pouvez intégrer **Vosk** côté backend pour un endpoint `/stt`. Ce prototype documente l’option mais ne l’active pas par défaut pour garder le setup léger.

## Sécurité
Ce prototype est **défensif uniquement** : il propose des conduites à tenir sûres (vérification logs, isolation comptes, MFA, escalade).
