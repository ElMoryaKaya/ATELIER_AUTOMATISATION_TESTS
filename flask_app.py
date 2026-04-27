from flask import Flask, jsonify, render_template
import storage
# import tester.runner as runner # Votre script qui lance les tests

app = Flask(__name__)

# Initialisation de la base au démarrage
storage.init_db()

@app.route('/health')
def health_check():
    """Bonus : Vérifier que votre propre garde est haute."""
    return jsonify({"status": "OK", "message": "Le Dojo est opérationnel."}), 200

@app.route('/run')
def trigger_run():
    """Déclenche l'affrontement (les tests automatisés)."""
    # 1. Appeler votre runner pour exécuter les tests
    # summary, details = runner.execute_all_tests()
    
    # 2. Sauvegarder dans SQLite
    # storage.save_run(summary, details)
    
    return jsonify({"status": "Tests terminés", "action": "Consultez le /dashboard"}), 200

@app.route('/dashboard')
def dashboard():
    """Affiche l'historique des affrontements."""
    # runs = storage.get_all_runs()
    # return render_template('dashboard.html', runs=runs)
    return "Ici se trouvera votre dashboard HTML (Tableau des scores)"