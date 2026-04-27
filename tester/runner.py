import time
# On importe les fonctions depuis notre fichier tests.py
from tester.tests import (
    execute_test, t1_contrat_200, t2_schema_json, t3_erreur_attendue_422,
    t4_prenom_inconnu_null, t5_exactitude_donnees, t6_robustesse_timeout
)

def run_all_tests():
    """Le cerveau qui orchestre les rounds et calcule la QoS."""
    tests_a_lancer = [
        ("Test 1: HTTP 200", t1_contrat_200),
        ("Test 2: Schéma JSON", t2_schema_json),
        ("Test 3: Erreur 422", t3_erreur_attendue_422),
        ("Test 4: Prénom inconnu", t4_prenom_inconnu_null),
        ("Test 5: Exactitude", t5_exactitude_donnees),
        ("Test 6: Esquive Timeout", t6_robustesse_timeout),
    ]
    
    resultats = []
    passed = 0
    failed = 0
    total_latency = 0
    
    for nom, fonction in tests_a_lancer:
        time.sleep(1) # Pause anti-spam
        resultat = execute_test(nom, fonction)
        resultats.append(resultat)
        
        if resultat["status"] == "PASS":
            passed += 1
        else:
            failed += 1
            
        total_latency += resultat.get("latency_ms", 0)
        
    summary = {
        "passed": passed,
        "failed": failed,
        "error_rate": round(failed / len(tests_a_lancer), 2) if len(tests_a_lancer) > 0 else 0,
        "latency_ms_avg": int(total_latency / len(tests_a_lancer)) if len(tests_a_lancer) > 0 else 0
    }
    
    return summary, resultats