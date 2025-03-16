from faster_whisper import WhisperModel
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import tempfile
import argparse

app = Flask(__name__)
CORS(app)  # Activer CORS pour toutes les routes

# Variable globale pour stocker le modèle
model = None

@app.route('/transcribe', methods=['POST'])
def transcribe():
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
