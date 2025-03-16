from faster_whisper import WhisperModel
from flask import Flask, request, jsonify
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
@jwt_required()  # Protection de l'endpoint avec JWT
def transcribe():
    # Vérification de l'identité de l'utilisateur
    current_user = get_jwt_identity()
    if current_user not in USERS:
        return jsonify({'error': 'Utilisateur non autorisé'}), 403
    
    # Vérifier si un fichier a été envoyé
    if 'file' not in request.files:
        return jsonify({'error': 'Aucun fichier audio envoyé'}), 400
    
    file = request.files['file']
    
    # Vérifier si le fichier est vide
    if file.filename == '':
        return jsonify({'error': 'Nom de fichier vide'}), 400
    
    # Créer un fichier temporaire pour stocker l'audio
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
    temp_filename = temp_file.name
    temp_file.close()
    
    try:
        # Sauvegarder le fichier audio
        file.save(temp_filename)
        
        # Transcrire l'audio
        segments, info = model.transcribe(temp_filename, beam_size=5)
        
        # Préparer la réponse
        result = {
            'language': info.language,
            'language_probability': info.language_probability,
            'segments': []
        }
        
        # Ajouter les segments transcrits
        for segment in segments:
            result['segments'].append({
                'start': segment.start,
                'end': segment.end,
                'text': segment.text
            })
        
        return jsonify(result)
    
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
    parser = argparse.ArgumentParser(description='Serveur de transcription audio avec Faster Whisper')
    parser.add_argument('--model', type=str, default='tiny', help='Nom du modèle à utiliser (tiny, base, small, medium, large, large-v2, large-v3)')
    parser.add_argument('--host', type=str, default='0.0.0.0', help='Adresse IP du serveur')
    parser.add_argument('--port', type=int, default=5000, help='Port du serveur')
    parser.add_argument('--device', type=str, default='cpu', help='Périphérique à utiliser (cpu, cuda)')
    parser.add_argument('--compute_type', type=str, default='int8', help='Type de calcul (float16, int8)')
    
    args = parser.parse_args()
    
    global model
    
    print(f"Chargement du modèle: {args.model}")
    model = WhisperModel(args.model, device=args.device, compute_type=args.compute_type)
    print("Modèle chargé avec succès!")
    
    print(f"Démarrage du serveur sur {args.host}:{args.port}")
    app.run(host=args.host, port=args.port)

if __name__ == "__main__":
    main()
