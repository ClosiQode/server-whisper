# Serveur de Transcription Audio avec Faster Whisper

Ce projet fournit un serveur de transcription audio sécurisé basé sur la bibliothèque `faster-whisper`, avec authentification JWT et documentation Swagger.

## Caractéristiques

- Transcription audio avec le modèle Faster Whisper
- API REST sécurisée avec authentification JWT
- Documentation Swagger interactive
- Support de multiples formats audio (WAV, MP3, OGG, FLAC, AAC, etc.)
- Prêt pour le déploiement avec Docker et CasaOS

## Prérequis

- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)
- Docker et Docker Compose (pour le déploiement avec CasaOS)
- ffmpeg (installé automatiquement dans le conteneur Docker)

## Installation

### Option 1 : Installation locale

1. **Cloner le dépôt ou télécharger les fichiers**

2. **Installer les dépendances Python requises**

   ```bash
   pip install -r requirements.txt
   ```

3. **Configurer les variables d'environnement**

   Créez un fichier `.env` à la racine du projet avec le contenu suivant :
   ```
   JWT_SECRET_KEY=votre_clé_secrète_jwt
   ADMIN_USERNAME=admin
   ADMIN_PASSWORD=votre_mot_de_passe_sécurisé
   ```

4. **Vérifier l'installation**

   ```bash
   python test_faster_whisper.py tiny
   ```

### Option 2 : Installation avec Docker

1. **Cloner le dépôt ou télécharger les fichiers**

2. **Construire et démarrer le conteneur Docker**

   ```bash
   docker-compose up -d
   ```

### Option 3 : Installation avec CasaOS

1. **Accédez à votre interface CasaOS**

2. **Allez dans "Apps" puis "Custom App"**

3. **Cliquez sur le bouton "Import" en haut à droite**

4. **Copiez-collez le contenu du fichier `docker-compose.yml` de ce projet**

5. **Cliquez sur "Submit" pour convertir la configuration**

6. **Vérifiez que les ports exposés ne créent pas de conflits (port 5000 par défaut)**

7. **Donnez un nom à votre application (ex: "Whisper API")**

8. **Définissez le port de l'interface Web (5000)**

9. **Configurez les variables d'environnement importantes :**
   - `MODEL_SIZE` : Taille du modèle à utiliser (tiny, base, small, medium, large)
   - `DEVICE` : Périphérique à utiliser (cpu, cuda)
   - `COMPUTE_TYPE` : Type de calcul (float16, int8)
   - `JWT_SECRET_KEY` : Clé secrète pour les tokens JWT
   - `ADMIN_USERNAME` et `ADMIN_PASSWORD` : Identifiants administrateur

10. **Cliquez sur "Install" pour démarrer l'installation**

11. **Créez un fichier `.env` à partir du modèle `env.sample` si vous souhaitez modifier d'autres paramètres**

## Utilisation

### Démarrer le serveur (installation locale)

```bash
python server_faster_whisper.py --model tiny
```

Options disponibles :
- `--model` : Taille du modèle à utiliser (tiny, base, small, medium, large-v1, large-v2, large-v3)
- `--host` : Adresse IP du serveur (par défaut : 0.0.0.0)
- `--port` : Port du serveur (par défaut : 5000)
- `--device` : Périphérique à utiliser (cpu, cuda)
- `--compute_type` : Type de calcul (float16, int8)

### Accéder à la documentation de l'API

Ouvrez le fichier `documentation.html` dans votre navigateur pour accéder à la documentation Swagger de l'API.

### Authentification

Pour utiliser l'API, vous devez d'abord obtenir un token JWT en vous authentifiant :

```bash
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"votre_mot_de_passe"}'
```

La réponse contiendra un token JWT que vous devrez inclure dans les requêtes suivantes.

### Transcription audio

Une fois authentifié, vous pouvez transcrire un fichier audio :

```bash
curl -X POST http://localhost:5000/transcribe \
  -H "Authorization: Bearer votre_token_jwt" \
  -F "file=@chemin/vers/audio.wav"
```

## Sécurité

Ce projet utilise l'authentification JWT pour sécuriser l'API. Assurez-vous de :

1. Changer les valeurs par défaut dans le fichier `.env`
2. Utiliser une clé JWT secrète forte et unique
3. Stocker les informations d'identification de manière sécurisée
4. Limiter l'accès à votre serveur aux utilisateurs de confiance

## Formats audio supportés

Grâce à l'utilisation de ffmpeg, cette API supporte une large gamme de formats audio, notamment :
- WAV
- MP3
- OGG
- FLAC
- AAC
- M4A
- MP4 (conteneur audio/vidéo)
- Et bien d'autres formats supportés par ffmpeg

## Tailles de modèles disponibles

| Modèle | Taille | Qualité | Vitesse | Mémoire requise |
|--------|--------|---------|---------|----------------|
| tiny   | ~75 Mo | Basique | Très rapide | ~1 Go |
| base   | ~142 Mo | Bonne | Rapide | ~1 Go |
| small  | ~466 Mo | Meilleure | Modérée | ~2 Go |
| medium | ~1.5 Go | Excellente | Lente | ~5 Go |
| large  | ~3 Go | Supérieure | Très lente | ~10 Go |

## Dépannage

### Problèmes d'authentification

Si vous rencontrez des problèmes d'authentification :
1. Vérifiez que les identifiants dans le fichier `.env` correspondent à ceux que vous utilisez
2. Assurez-vous que le token JWT n'est pas expiré (durée de validité par défaut : 30 jours)
3. Vérifiez que le token est correctement inclus dans l'en-tête `Authorization`

### Problèmes de mémoire

Si vous rencontrez des problèmes de mémoire avec les grands modèles :
1. Essayez d'utiliser un modèle plus petit (tiny ou base)
2. Augmentez la mémoire disponible pour le conteneur Docker
3. Utilisez l'option `--compute_type int8` pour réduire l'utilisation de la mémoire

### Fichiers audio non reconnus

Si vos fichiers audio ne sont pas correctement transcrits :
1. Assurez-vous que l'audio est de bonne qualité et clairement audible
2. Vérifiez que ffmpeg est correctement installé (dans le conteneur ou sur votre système)
3. Essayez d'utiliser un modèle plus grand pour une meilleure précision

## Structure du projet

- `server_faster_whisper.py` : Serveur API Flask avec authentification JWT
- `test_faster_whisper.py` : Script de test pour vérifier le fonctionnement de faster-whisper
- `documentation.html` : Documentation Swagger de l'API
- `Dockerfile` : Configuration pour la création d'une image Docker
- `docker-compose.yml` : Configuration pour le déploiement avec Docker Compose
- `.env` : Fichier de configuration des variables d'environnement
- `requirements.txt` : Liste des dépendances Python

## Licence

Ce projet est distribué sous licence MIT.

## Crédits

Ce projet utilise les bibliothèques suivantes :
- [faster-whisper](https://github.com/guillaumekln/faster-whisper) : Implémentation optimisée du modèle Whisper d'OpenAI
- [Flask](https://flask.palletsprojects.com/) : Framework web léger pour Python
- [Flask-JWT-Extended](https://flask-jwt-extended.readthedocs.io/) : Extension Flask pour l'authentification JWT
- [Swagger UI](https://swagger.io/tools/swagger-ui/) : Interface pour la documentation de l'API
