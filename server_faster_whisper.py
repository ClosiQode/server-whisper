from faster_whisper import WhisperModel
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import tempfile
import argparse
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from dotenv import load_dotenv

# Chargement des variables d'environnement
load_dotenv()

app = Flask(__name__)
CORS(app)  # Activer CORS pour toutes les routes

# Configuration JWT
app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY", "clé_secrète_par_défaut")  # Changer en production!
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = datetime.timedelta(days=30)  # Durée de validité du token
jwt = JWTManager(app)

# Utilisateurs autorisés (à remplacer par une base de données en production)
USERS = {
    os.environ.get("ADMIN_USERNAME", "admin"): {
        "password": generate_password_hash(os.environ.get("ADMIN_PASSWORD", "password")),
        "role": "admin"
    }
}

# Variable globale pour stocker le modèle
model = None

@app.route('/', methods=['GET'])
def documentation():
    """Endpoint pour accéder à la documentation Swagger"""
    return send_file('documentation.html')

@app.route('/login', methods=['POST'])
def login():
    """Endpoint pour l'authentification et la génération de token JWT"""
    if not request.is_json:
        return jsonify({"error": "Le corps de la requête doit être en JSON"}), 400

    username = request.json.get("username", None)
    password = request.json.get("password", None)

    if not username or not password:
        return jsonify({"error": "Nom d'utilisateur et mot de passe requis"}), 400

    user = USERS.get(username)
    if not user or not check_password_hash(user["password"], password):
        return jsonify({"error": "Nom d'utilisateur ou mot de passe incorrect"}), 401

    # Création du token JWT
    access_token = create_access_token(identity=username, additional_claims={"role": user["role"]})
    return jsonify(access_token=access_token), 200

@app.route('/transcribe', methods=['POST'])
@jwt_required()
def transcribe():
    """Endpoint pour transcrire un fichier audio"""
    # Vérifier si un fichier a été envoyé
    if 'file' not in request.files:
        return jsonify({'error': 'Aucun fichier audio fourni'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'Nom de fichier vide'}), 400
    
    # Créer un fichier temporaire pour stocker l'audio
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    temp_filename = temp_file.name
    temp_file.close()
    
    try:
        # Sauvegarder le fichier audio dans le fichier temporaire
        file.save(temp_filename)
        
        # Vérifier si le modèle est chargé
        if model is None:
            return jsonify({'error': 'Le modèle n\'est pas chargé'}), 500
        
        # Transcrire l'audio
        segments, info = model.transcribe(temp_filename)
        
        # Convertir les segments en liste de dictionnaires
        segments_list = []
        for segment in segments:
            segments_list.append({
                'start': segment.start,
                'end': segment.end,
                'text': segment.text
            })
        
        # Retourner les résultats
        return jsonify({
            'language': info.language,
            'language_probability': info.language_probability,
            'segments': segments_list
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    finally:
        # Supprimer le fichier temporaire
        if os.path.exists(temp_filename):
            os.unlink(temp_filename)

@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint pour vérifier l'état du serveur"""
    return jsonify({'status': 'ok', 'model_loaded': model is not None}), 200

def main():
    # Utiliser les variables d'environnement au lieu des arguments de ligne de commande
    model_size = os.environ.get("MODEL_SIZE", "tiny")
    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", "5000"))
    device = os.environ.get("DEVICE", "cpu")
    compute_type = os.environ.get("COMPUTE_TYPE", "int8")
    
    # Pour compatibilité avec les anciens scripts, on accepte aussi les arguments de ligne de commande
    parser = argparse.ArgumentParser(description='Serveur de transcription audio avec Faster Whisper')
    parser.add_argument('--model', type=str, help='Nom du modèle à utiliser (tiny, base, small, medium, large, large-v2, large-v3)')
    parser.add_argument('--host', type=str, help='Adresse IP du serveur')
    parser.add_argument('--port', type=int, help='Port du serveur')
    parser.add_argument('--device', type=str, help='Périphérique à utiliser (cpu, cuda)')
    parser.add_argument('--compute_type', type=str, help='Type de calcul (float16, int8)')
    
    args = parser.parse_args()
    
    # Les arguments de ligne de commande ont priorité sur les variables d'environnement
    if args.model:
        model_size = args.model
    if args.host:
        host = args.host
    if args.port:
        port = args.port
    if args.device:
        device = args.device
    if args.compute_type:
        compute_type = args.compute_type
    
    global model
    
    print(f"Chargement du modèle: {model_size}")
    model = WhisperModel(model_size, device=device, compute_type=compute_type)
    print(f"Modèle chargé avec succès! (device: {device}, compute_type: {compute_type})")
    
    print(f"Démarrage du serveur sur {host}:{port}")
    app.run(host=host, port=port)

if __name__ == "__main__":
    main()
