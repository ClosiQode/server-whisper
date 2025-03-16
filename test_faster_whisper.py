from faster_whisper import WhisperModel
import sys
import os

def main():
    # Vérifier si un nom de modèle est fourni
    if len(sys.argv) < 2:
        print("Usage: python test_faster_whisper.py <nom_du_modele> [chemin_audio]")
        print("Modèles disponibles: tiny, base, small, medium, large, large-v2, large-v3")
        return
    
    model_name = sys.argv[1]
    
    # Chemin audio optionnel
    audio_path = sys.argv[2] if len(sys.argv) > 2 else None
    
    print(f"Chargement du modèle: {model_name}")
    
    try:
        # Charger le modèle (utilise CPU par défaut)
        model = WhisperModel(model_name, device="cpu", compute_type="int8")
        
        print("Modèle chargé avec succès!")
        
        # Si un fichier audio est fourni, transcrivez-le
        if audio_path:
            if not os.path.exists(audio_path):
                print(f"Erreur: Le fichier audio {audio_path} n'existe pas.")
                return
                
            print(f"Transcription du fichier audio: {audio_path}")
            
            # Effectuer la transcription
            segments, info = model.transcribe(audio_path, beam_size=5)
            
            print("\nTranscription:")
            print(f"Langue détectée: {info.language}, probabilité: {info.language_probability:.2f}")
            
            # Afficher les segments transcrits
            for segment in segments:
                print(f"[{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text}")
        else:
            print("Aucun fichier audio fourni. Le modèle est prêt pour la transcription.")
            print("Vous pouvez exécuter à nouveau avec un fichier audio: python test_faster_whisper.py tiny chemin/vers/audio.wav")
    
    except Exception as e:
        print(f"Erreur lors du chargement ou de l'utilisation du modèle: {e}")

if __name__ == "__main__":
    main()
