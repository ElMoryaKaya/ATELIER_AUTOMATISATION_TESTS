from flask import Flask, jsonify, render_template
import storage
from tester.runner import run_all_tests

app = Flask(__name__)

# Initialisation de la base de données au démarrage
storage.init_db()

@app.route('/')
def home():
    return "Bienvenue dans le Dojo d'automatisation des tests ! Allez sur /dashboard pour voir les scores."

@app.route('/health')
def health_check():
    """Vérifie que votre garde est haute."""
    return jsonify({"status": "OK", "message": "Le Dojo est opérationnel."}), 200

@app.route('/run')
def trigger_run():
    """Déclenche l'affrontement (les tests automatisés) et sauvegarde le résultat."""
    # 1. On lance les 6 rounds d'entraînement
    summary, resultats = run_all_tests()
    
    # 2. On consigne le résultat dans le registre SQLite
    storage.save_run(summary, resultats)
    
    # 3. On renvoie le rapport immédiat à l'écran
    return jsonify({
        "status": "Combat terminé",
        "resume_du_match": summary,
        "details": resultats,
        "action": "Allez sur /dashboard pour voir l'historique"
    }), 200

@app.route('/dashboard')
def dashboard():
    """Affiche l'historique des affrontements sur une page web."""
    historique = storage.get_all_runs()
    return render_template('dashboard.html', runs=historique)