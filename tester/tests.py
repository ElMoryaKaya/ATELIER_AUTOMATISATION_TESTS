import requests
import time

BASE_URL = "https://api.agify.io"

def execute_test(nom_du_test, fonction_test):
    start_time = time.time()
    try:
        details = fonction_test()
        latency = int((time.time() - start_time) * 1000)
        return {"name": nom_du_test, "status": "PASS", "latency_ms": latency, "details": details}
    except AssertionError as e:
        latency = int((time.time() - start_time) * 1000)
        return {"name": nom_du_test, "status": "FAIL", "latency_ms": latency, "details": f"Échec : {str(e)}"}
    except requests.exceptions.Timeout:
        latency = int((time.time() - start_time) * 1000)
        return {"name": nom_du_test, "status": "FAIL", "latency_ms": latency, "details": "Timeout."}
    except Exception as e:
        latency = int((time.time() - start_time) * 1000)
        return {"name": nom_du_test, "status": "ERROR", "latency_ms": latency, "details": f"Erreur : {str(e)}"}

def t1_contrat_200():
    res = requests.get(f"{BASE_URL}?name=michael", timeout=3)
    assert res.status_code == 200, f"Attendu HTTP 200, reçu {res.status_code}"
    return "Code HTTP 200 OK"

def t2_schema_json():
    res = requests.get(f"{BASE_URL}?name=michael", timeout=3)
    data = res.json()
    assert "name" in data and "age" in data and "count" in data, "Champ manquant."
    assert isinstance(data["name"], str), "Le champ 'name' n'est pas du texte."
    assert isinstance(data["age"], int), "Le champ 'age' n'est pas un entier."
    return "Schéma JSON et types valides"

def t3_erreur_attendue_422():
    res = requests.get(BASE_URL, timeout=3)
    assert res.status_code == 422, f"Attendu 422, reçu {res.status_code}"
    return "Erreur 422 gérée"

def t4_prenom_inconnu_null():
    res = requests.get(f"{BASE_URL}?name=xyzazertyuiop", timeout=3)
    assert res.json()["age"] is None, "L'âge devrait être 'null'"
    return "Valeur 'null' gérée"

def t5_exactitude_donnees():
    res = requests.get(f"{BASE_URL}?name=michael&country_id=FR", timeout=3)
    assert res.json()["name"] == "michael", "Prénom incorrect."
    return "Données exactes"

def t6_robustesse_timeout():
    try:
        requests.get(f"{BASE_URL}?name=michael", timeout=0.001)
        assert False, "Aurait dû Timeout."
    except requests.exceptions.Timeout:
        return "Esquive Timeout réussie"