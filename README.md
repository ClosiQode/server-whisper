# Serveur de Transcription Audio avec Whisper

Ce projet fournit un serveur de transcription audio basé sur la bibliothèque `faster-whisper`, ainsi qu'une interface client web pour faciliter son utilisation.

## Prérequis

- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)
- Navigateur web moderne

## Installation

1. **Cloner le dépôt ou télécharger les fichiers**

2. **Installer les dépendances Python requises**

   ```bash
   pip install faster-whisper flask flask-cors
   ```

3. **Vérifier l'installation**

   Pour vérifier que tout est correctement installé, vous pouvez exécuter le script de test :

   ```bash
   python test_faster_whisper.py tiny
   ```

   Si tout fonctionne correctement, vous devriez voir le message "Modèle chargé avec succès!".

## Utilisation

### Démarrer le serveur

1. **Lancer le serveur avec le modèle de votre choix**

   ```bash
   python server_faster_whisper.py --model tiny
   ```

   Options disponibles :
   - `--model` : Taille du modèle à utiliser (tiny, base, small, medium, large-v1, large-v2, large-v3)
   - `--host` : Adresse IP du serveur (par défaut : 0.0.0.0)
   - `--port` : Port du serveur (par défaut : 5000)
   - `--device` : Périphérique à utiliser (cpu, cuda)
   - `--compute_type` : Type de calcul (float16, int8)

   Exemple avec plus d'options :
   ```bash
   python server_faster_whisper.py --model small --port 8080 --device cpu --compute_type int8
   ```

2. **Le serveur sera accessible à l'adresse** : http://localhost:5000 (ou le port que vous avez spécifié)

### Utiliser l'interface client web

1. **Ouvrir le fichier `client.html` dans votre navigateur**

2. **Sélectionner un fichier audio au format WAV**

3. **Vérifier l'URL du serveur** (par défaut : http://localhost:5000/transcribe)

4. **Cliquer sur le bouton "Transcrire"**

5. **Attendre la fin de la transcription** et visualiser les résultats

### Utiliser l'API directement

Vous pouvez également envoyer des requêtes directement à l'API :

```bash
curl -X POST -F "file=@chemin/vers/audio.wav" http://localhost:5000/transcribe
```

Ou avec Python :

```python
import requests

url = "http://localhost:5000/transcribe"
files = {"file": open("chemin/vers/audio.wav", "rb")}
response = requests.post(url, files=files)
result = response.json()
print(result)
```

## Tailles de modèles disponibles

| Modèle | Taille | Qualité | Vitesse | Mémoire requise |
|--------|--------|---------|---------|----------------|
| tiny   | ~75 Mo | Basique | Très rapide | ~1 Go |
| base   | ~142 Mo | Bonne | Rapide | ~1 Go |
| small  | ~466 Mo | Meilleure | Modérée | ~2 Go |
| medium | ~1.5 Go | Excellente | Lente | ~5 Go |
| large  | ~3 Go | Supérieure | Très lente | ~10 Go |

## Dépannage

### Erreur "Failed to fetch"

Si vous rencontrez une erreur "Failed to fetch" dans l'interface client :

1. Vérifiez que le serveur est bien en cours d'exécution
2. Assurez-vous que l'URL du serveur est correcte dans l'interface client
3. Essayez de vider le cache de votre navigateur ou d'utiliser une fenêtre de navigation privée

### Problèmes de mémoire

Si vous rencontrez des problèmes de mémoire avec les grands modèles :

1. Essayez d'utiliser un modèle plus petit (tiny ou base)
2. Augmentez la mémoire disponible pour Python
3. Utilisez l'option `--compute_type int8` pour réduire l'utilisation de la mémoire

### Fichiers audio non reconnus

Si vos fichiers audio ne sont pas correctement transcrits :

1. Assurez-vous qu'ils sont au format WAV
2. Vérifiez que l'audio est de bonne qualité et clairement audible
3. Essayez d'utiliser un modèle plus grand pour une meilleure précision

## Scripts disponibles

- `server_faster_whisper.py` : Serveur API Flask pour la transcription audio
- `test_faster_whisper.py` : Script de test pour vérifier le fonctionnement de la bibliothèque faster-whisper
- `test_whispercpp.py` : Script alternatif utilisant la bibliothèque whispercpp
- `client.html` : Interface client web pour interagir avec le serveur

## Licence

Ce projet est distribué sous licence MIT.

## Crédits

Ce projet utilise les bibliothèques suivantes :
- [faster-whisper](https://github.com/guillaumekln/faster-whisper) : Implémentation optimisée du modèle Whisper d'OpenAI
- [Flask](https://flask.palletsprojects.com/) : Framework web léger pour Python
- [Flask-CORS](https://flask-cors.readthedocs.io/) : Extension Flask pour gérer les requêtes cross-origin
