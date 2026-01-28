from typing import Dict

SAFE_ACTIONS = (
    "1) Vérifiez les logs d’authentification et identifiez la source. "
    "2) Isolez le compte ciblé et forcez la réinitialisation du mot de passe. "
    "3) Activez ou renforcez la MFA. "
    "4) Lancez un scan endpoint et corrélez avec d’autres événements. "
    "5) Escaladez à l’administrateur sécurité si l’activité persiste."
)


def build_reply(intent: str) -> Dict[str, object]:
    if intent == "status_overview":
        return {
            "reply": "Voici un aperçu rapide : surveillez les anomalies, les alertes critiques et les tendances horaires.",
            "ui": {"openTab": "overview"},
        }
    if intent == "show_alerts":
        return {
            "reply": "Affichage des alertes critiques et élevées. Priorisez les incidents actifs.",
            "ui": {"openTab": "alerts", "filter": "CRITICAL"},
        }
    if intent == "show_events":
        return {
            "reply": "Voici les événements récents. Vous pouvez filtrer par source ou gravité.",
            "ui": {"openTab": "events"},
        }
    if intent == "what_to_do":
        return {
            "reply": f"Conduite à tenir : {SAFE_ACTIONS}",
            "ui": {"openTab": "playbook"},
        }
    if intent == "explain_alert":
        return {
            "reply": "L’alerte est générée par une anomalie statistique. Vérifiez la source, l’IP et le contexte associé.",
            "ui": {"openTab": "alerts"},
        }
    if intent == "ack_alert":
        return {
            "reply": "Confirmez l’acquittement dans l’interface avant de clôturer l’alerte.",
            "ui": {"openTab": "alerts", "confirm": True},
        }
    if intent == "help":
        return {
            "reply": "Commandes disponibles : statut, alertes critiques, événements récents, que dois-je faire, explique alerte.",
            "ui": {"openTab": "help"},
        }
    return {
        "reply": "Je suis prête. Demandez un statut, les alertes, ou une conduite à tenir.",
        "ui": {"openTab": "overview"},
    }
