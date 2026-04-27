import requests
import time

def safe_request(url, params=None, timeout=3, retries=1):
    """
    Envoie une requête mesurée et sécurisée.
    Gère l'esquive en cas de non-réponse (timeout) et tente une relance.
    """
    for attempt in range(retries + 1):
        start_time = time.time()
        try:
            response = requests.get(url, params=params, timeout=timeout)
            latency_ms = int((time.time() - start_time) * 1000)
            
            # Gestion basique du Rate Limit (Code 429)
            if response.status_code == 429:
                print("⚠️ Rate limit atteint, repli stratégique...")
                time.sleep(2) # On patiente avant d'éventuellement réessayer
                continue
                
            return response, latency_ms, None # Succès (ou réponse lisible)
            
        except requests.exceptions.Timeout:
            if attempt == retries:
                return None, None, "Timeout (Délai d'attente dépassé)"
        except requests.exceptions.RequestException as e:
            return None, None, f"Erreur réseau : {str(e)}"