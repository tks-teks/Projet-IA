from typing import Tuple

INTENTS = {
    "status_overview": ["statut", "que se passe", "overview", "situation"],
    "show_alerts": ["alerte", "alertes", "critiques", "incidents"],
    "show_events": ["événements", "evenements", "logs", "récents", "recents"],
    "what_to_do": ["que dois-je faire", "procédure", "actions", "conduite"],
    "explain_alert": ["explique", "pourquoi", "raison"],
    "ack_alert": ["marque", "traité", "acquitte", "ack"],
    "help": ["aide", "commandes", "help"],
}


def detect_intent(text: str) -> Tuple[str, float]:
    lowered = text.lower()
    for intent, keywords in INTENTS.items():
        for keyword in keywords:
            if keyword in lowered:
                return intent, 0.82
    return "status_overview", 0.4
