# API Choice

- Étudiant : Morya-El KAYA MBOU
- API choisie :Agify
- URL base : https://api.agify.io?name=michael
- Documentation officielle / README :https://agify.io/
- Auth : None
- Endpoints testés :
  - GET /?name=michael
  - GET /?name=michael&country_id=FR
- Hypothèses de contrat (champs attendus, types, codes) :
  - Code HTTP attendu : 200 (OK) en cas de succès, 422 si le paramètre `name` est manquant.
  - Format de réponse : JSON.
  - Champs obligatoires : `name` (string), `age` (int ou null), `count` (int).
- Limites / rate limiting connu : Limite stricte de 1 000 requêtes par jour. Renvoie un       code 429 (Too Many Requests) si la cadence est trop élevée.
- Risques (instabilité, downtime, CORS, etc.) :
  - Plafond d'IP partagée : Risque d'atteindre la limite des 1 000 requêtes prématurément       car l'IP de PythonAnywhere est partagée avec d'autres utilisateurs.
  - Parades de l'API : Risque de recevoir une valeur `null` pour l'âge si un prénom             atypique est testé (le code devra l'anticiper sans planter).
  - Instabilité : Risque de downtime temporaire classique pour une API publique et gratuite.
