import requests
import time

BASE_URL = "https://api.agify.io"

def execute_test(nom_du_test, fonction_test):
    """
    L'arbitre de chaque round : chronomètre la frappe, exécute le test, 
    et juge si c'est un succès (PASS) ou un échec (FAIL).
    """
    start_time = time.time()
    try:
        details = fonction_test()
        latency = int((time.time() - start_time) * 1000)
        return {"name": nom_du_test, "status": "PASS", "latency_ms": latency, "details": details}
    except AssertionError as e:
        latency = int((time.time() - start_time) * 1000)
        return {"name": nom_du_test, "status": "FAIL", "latency_ms": latency, "details": f"Échec de l'assertion : {str(e)}"}
    except requests.exceptions.Timeout:
        latency = int((time.time() - start_time) * 1000)
        return {"name": nom_du_test, "status": "FAIL", "latency_ms": latency, "details": "L'adversaire n'a pas répondu à temps (Timeout)."}
    except Exception as e:
        latency = int((time.time() - start_time) * 1000)
        return {"name": nom_du_test, "status": "ERROR", "latency_ms": latency, "details": f"Erreur imprévue : {str(e)}"}

# ==========================================
# LES 6 ENCHAÎNEMENTS TACTIQUES (TESTS)
# ==========================================

def t1_contrat_200():
    """Test 1 : Vérifie que l'API accepte le combat (Code 200)."""
    res = requests.get(f"{BASE_URL}?name=michael", timeout=3)
    assert res.status_code == 200, f"Attendu HTTP 200, reçu {res.status_code}"
    return "Code HTTP 200 OK"

def t2_schema_json():
    """Test 2 : Vérifie la posture de l'adversaire (Structure JSON et types)."""
    res = requests.get(f"{BASE_URL}?name=michael", timeout=3)
    data = res.json()
    assert "name" in data and "age" in data and "count" in data, "Il manque un des champs obligatoires."
    assert isinstance(data["name"], str), "Le champ 'name' n'est pas du texte."
    assert isinstance(data["age"], int), "Le champ 'age' n'est pas un nombre entier."
    return "Schéma JSON et types valides"

def t3_erreur_attendue_422():
    """Test 3 : Attaque feintée. On envoie une requête sans prénom pour vérifier qu'il bloque bien (Code 422)."""
    res = requests.get(BASE_URL, timeout=3) # Pas de paramètre ?name=
    assert res.status_code == 422, f"Attendu HTTP 422, reçu {res.status_code}"
    return "Erreur 422 (Unprocessable Entity) gérée correctement par l'API"

def t4_prenom_inconnu_null():
    """Test 4 : Parade inattendue. On teste un prénom absurde pour vérifier la gestion de la valeur 'null'."""
    res = requests.get(f"{BASE_URL}?name=xyzazertyuiop", timeout=3)
    data = res.json()
    assert data["age"] is None, f"L'âge devrait être 'null', mais on a reçu {data['age']}"
    return "Valeur 'null' anticipée et gérée"

def t5_exactitude_donnees():
    """Test 5 : Frappe de précision. On vérifie que la réponse correspond exactement à la cible demandée."""
    res = requests.get(f"{BASE_URL}?name=michael&country_id=FR", timeout=3)
    data = res.json()
    assert data["name"] == "michael", "Le prénom renvoyé ne correspond pas à la requête."
    assert data.get("country_id") == "FR", "Le paramètre géographique a été ignoré."
    return "Données renvoyées exactes"

def t6_robustesse_timeout():
    """Test 6 : Esquive. On force un délai d'attente impossible (1 milliseconde) pour vérifier notre propre capacité de repli."""
    try:
        requests.get(f"{BASE_URL}?name=michael", timeout=0.001)
        assert False, "Le script aurait dû planter et déclencher un Timeout."
    except requests.exceptions.Timeout:
        return "Esquive réussie, le Timeout fonctionne"

# ==========================================
# LE GESTIONNAIRE DE COMBAT
# ==========================================

def run_all_tests():
    """Lance les 6 rounds d'affilée et dresse le bilan."""
    tests_a_lancer = [
        ("Test 1: HTTP 200", t1_contrat_200),
        ("Test 2: Schéma JSON", t2_schema_json),
        ("Test 3: Erreur 422", t3_erreur_attendue_422),
        ("Test 4: Prénom inconnu", t4_prenom_inconnu_null),
        ("Test 5: Exactitude (Pays)", t5_exactitude_donnees),
        ("Test 6: Esquive Timeout", t6_robustesse_timeout),
    ]
    
    resultats = []
    passed = 0
    failed = 0
    total_latency = 0
    
    for nom, fonction in tests_a_lancer:
        # Pause de 1 seconde entre chaque frappe pour respecter le Rate Limiting de l'API
        time.sleep(1) 
        
        resultat = execute_test(nom, fonction)
        resultats.append(resultat)
        
        if resultat["status"] == "PASS":
            passed += 1
        else:
            failed += 1
            
        total_latency += resultat.get("latency_ms", 0)
        
    # Calcul des statistiques de fin de match
    summary = {
        "passed": passed,
        "failed": failed,
        "error_rate": round(failed / len(tests_a_lancer), 2) if len(tests_a_lancer) > 0 else 0,
        "latency_ms_avg": int(total_latency / len(tests_a_lancer)) if len(tests_a_lancer) > 0 else 0
    }
    
    return summary, resultats