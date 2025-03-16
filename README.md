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
   MODEL_SIZE=tiny
   DEVICE=cpu
   COMPUTE_TYPE=int8
   ```

4. **Lancer le serveur**

   ```bash
   python server_faster_whisper.py
   ```

   Le serveur utilisera automatiquement les variables d'environnement définies dans le fichier `.env`.

### Option 2 : Installation avec Docker

1. **Utiliser l'image Docker prête à l'emploi**

   ```bash
   docker run -d \
     --name whisper-api \
     -p 5000:5000 \
     -e JWT_SECRET_KEY=votre_clé_secrète_jwt \
     -e ADMIN_USERNAME=admin \
     -e ADMIN_PASSWORD=votre_mot_de_passe_sécurisé \
     -e MODEL_SIZE=tiny \
     -e DEVICE=cpu \
     -e COMPUTE_TYPE=int8 \
     closiqode/server-whisper:latest
   ```

2. **Ou utiliser Docker Compose**

   Créez un fichier `docker-compose.yml` avec le contenu suivant :
   ```yaml
   version: '3'
   
   services:
     whisper-api:
       image: closiqode/server-whisper:latest
       container_name: whisper-api
       restart: unless-stopped
       ports:
         - "5000:5000"
       volumes:
         - ./config:/app/config
         - ./models:/app/models
       environment:
         - JWT_SECRET_KEY=votre_clé_secrète_jwt
         - ADMIN_USERNAME=admin
         - ADMIN_PASSWORD=votre_mot_de_passe_sécurisé
         - MODEL_SIZE=tiny
         - DEVICE=cpu
         - COMPUTE_TYPE=int8
   ```

   Puis lancez avec :
   ```bash
   docker-compose up -d
   ```

### Option 3 : Installation avec CasaOS

1. **Accédez à votre interface CasaOS**

2. **Allez dans "Apps" puis "Custom App"**

3. **Cliquez sur le bouton "Import" en haut à droite**

4. **Copiez-collez le contenu du fichier `docker-compose.yml`** suivant dans la zone de texte :
   ```yaml
   version: '3'
   
   services:
     whisper-api:
       image: closiqode/server-whisper:latest
       container_name: whisper-api
       restart: unless-stopped
       ports:
         - "5000:5000"
       volumes:
         - ./config:/app/config
         - ./models:/app/models
       environment:
         - JWT_SECRET_KEY=49f85d9ae0eadab02f28f1c0d4118ac0effca0197e27c116f9a4f580c0d91c7e
         - ADMIN_USERNAME=admin
         - ADMIN_PASSWORD=changez_ce_mot_de_passe
         - MODEL_SIZE=tiny
         - DEVICE=cpu
         - COMPUTE_TYPE=int8
       labels:
         - "com.github.repo=https://github.com/ClosiQode/server-whisper"
         - "com.casaos.name=Whisper API"
         - "com.casaos.description=API sécurisée pour la transcription audio avec Faster Whisper"
         - "com.casaos.developer=ClosiQode"
         - "com.casaos.icon=https://raw.githubusercontent.com/ClosiQode/server-whisper/main/assets/icon.svg"
   ```

5. **Cliquez sur "Submit"** pour convertir la configuration en format CasaOS

6. **Vérifiez que les ports exposés ne créent pas de conflits** (port 5000 par défaut)

7. **Modifiez les variables d'environnement selon vos besoins** :
   - `MODEL_SIZE` : Taille du modèle Whisper à utiliser (tiny, base, small, medium, large)
   - `DEVICE` : Périphérique à utiliser (cpu, cuda)
   - `COMPUTE_TYPE` : Type de calcul (int8, float16)
   - `JWT_SECRET_KEY` : Clé secrète pour les tokens JWT (changez-la pour plus de sécurité)
   - `ADMIN_USERNAME` et `ADMIN_PASSWORD` : Identifiants administrateur

8. **Cliquez sur "Install"** pour démarrer l'installation

9. **Accédez à l'API** via l'URL `http://votre-serveur-casaos:5000/documentation.html`

## Installation avec CasaOS

CasaOS est une plateforme de serveur personnel qui facilite la gestion des applications Docker. Voici comment installer l'API Whisper sur CasaOS :

### Méthode 1 : Installation via l'interface graphique

1. **Accédez à votre interface CasaOS** dans votre navigateur

2. **Allez dans la section "Apps"** dans le menu latéral

3. **Cliquez sur le bouton "+"** puis sélectionnez "Install a customized app"

4. **Cliquez sur le bouton "Import"** en haut à droite de la fenêtre

5. **Copiez-collez le contenu du fichier `docker-compose.yml`** suivant dans la zone de texte :
   ```yaml
   version: '3'
   
   services:
     whisper-api:
       image: closiqode/server-whisper:latest
       container_name: whisper-api
       restart: unless-stopped
       ports:
         - "5000:5000"
       volumes:
         - ./config:/app/config
         - ./models:/app/models
       environment:
         - JWT_SECRET_KEY=49f85d9ae0eadab02f28f1c0d4118ac0effca0197e27c116f9a4f580c0d91c7e
         - ADMIN_USERNAME=admin
         - ADMIN_PASSWORD=changez_ce_mot_de_passe
         - MODEL_SIZE=tiny
         - DEVICE=cpu
         - COMPUTE_TYPE=int8
       labels:
         - "com.github.repo=https://github.com/ClosiQode/server-whisper"
         - "com.casaos.name=Whisper API"
         - "com.casaos.description=API sécurisée pour la transcription audio avec Faster Whisper"
         - "com.casaos.developer=ClosiQode"
         - "com.casaos.icon=https://raw.githubusercontent.com/ClosiQode/server-whisper/main/assets/icon.svg"
   ```

6. **Cliquez sur "Submit"** pour convertir la configuration en format CasaOS

7. **Vérifiez que les ports exposés ne créent pas de conflits** (port 5000 par défaut)

8. **Modifiez les variables d'environnement selon vos besoins** :
   - `MODEL_SIZE` : Taille du modèle Whisper à utiliser (tiny, base, small, medium, large)
   - `DEVICE` : Périphérique à utiliser (cpu, cuda)
   - `COMPUTE_TYPE` : Type de calcul (int8, float16)
   - `JWT_SECRET_KEY` : Clé secrète pour les tokens JWT (changez-la pour plus de sécurité)
   - `ADMIN_USERNAME` et `ADMIN_PASSWORD` : Identifiants administrateur

9. **Cliquez sur "Install"** pour démarrer l'installation

10. **Accédez à l'API** via l'URL `http://votre-serveur-casaos:5000/documentation.html`

### Méthode 2 : Installation via la ligne de commande

Si vous préférez utiliser la ligne de commande, voici les étapes à suivre :

1. **Connectez-vous à votre serveur CasaOS via SSH**

2. **Créez un répertoire pour l'application** :
   ```bash
   mkdir -p ~/casaos/whisper-api
   cd ~/casaos/whisper-api
   ```

3. **Créez un fichier docker-compose.yml** :
   ```bash
   nano docker-compose.yml
   ```

4. **Copiez-collez le contenu du fichier docker-compose.yml** présenté dans la méthode 1

5. **Enregistrez le fichier** (Ctrl+O puis Entrée, puis Ctrl+X pour quitter)

6. **Importez l'application dans CasaOS** :
   ```bash
   casaos-cli app-management import --path ~/casaos/whisper-api/docker-compose.yml
   ```

7. **Vérifiez que l'application est bien installée** dans l'interface web de CasaOS

### Conseils pratiques pour CasaOS

- **Choix du modèle** : Le modèle "tiny" est recommandé pour les serveurs avec des ressources limitées. Pour une meilleure qualité de transcription, utilisez "base" ou "small" si vos ressources le permettent.

- **Persistance des données** : Les volumes Docker permettent de conserver les modèles téléchargés entre les redémarrages.

- **Sécurité** : Changez toujours les valeurs par défaut pour `JWT_SECRET_KEY`, `ADMIN_USERNAME` et `ADMIN_PASSWORD`.

- **Mise à jour** : Pour mettre à jour l'application, utilisez la fonction "Update" de CasaOS ou exécutez :
  ```bash
  docker pull closiqode/server-whisper:latest
  casaos-cli app-management restart --name whisper-api
  ```

## Utilisation

### Démarrer le serveur (installation locale)

```bash
python server_faster_whisper.py
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
