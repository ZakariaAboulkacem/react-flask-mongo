# Guide pour tester le frontend

## Méthode 1 : Tester avec Docker (Recommandé - Tous les services)

Cette méthode lance tous les services (MongoDB, API Flask, et Frontend React) ensemble.

### Étapes :

1. **Ouvrir un terminal à la racine du projet**

2. **Lancer tous les services avec Docker Compose :**
   ```bash
   docker-compose up --build
   ```

3. **Attendre que tous les services démarrent** (vous verrez les logs dans le terminal)

4. **Ouvrir votre navigateur** et aller à :
   ```
   http://localhost:3000
   ```

5. **Tester l'application :**
   - Vous devriez voir une page "TODO LIST"
   - Essayez d'ajouter une tâche
   - Essayez de modifier une tâche
   - Essayez de supprimer une tâche

### Vérifier que les services fonctionnent :

- **Frontend React** : http://localhost:3000
- **API Flask** : http://localhost:5000/api/tasks
- **MongoDB** : Port 27017 (accessible depuis les conteneurs)

---

## Méthode 2 : Tester uniquement le frontend (Développement local)

Cette méthode nécessite que l'API backend soit déjà lancée (soit avec Docker, soit localement).

### Prérequis :
- Node.js et npm installés
- L'API backend doit être accessible sur http://localhost:5000

### Étapes :

1. **Aller dans le dossier frontend :**
   ```bash
   cd frontend
   ```

2. **Installer les dépendances (si pas déjà fait) :**
   ```bash
   npm install
   ```

3. **Lancer le serveur de développement React :**
   ```bash
   npm start
   ```

4. **Le navigateur s'ouvrira automatiquement** sur http://localhost:3000

5. **Si le navigateur ne s'ouvre pas automatiquement**, allez manuellement à :
   ```
   http://localhost:3000
   ```

### Vérifier que ça fonctionne :

- L'interface React devrait s'afficher
- Ouvrez la console du navigateur (F12) pour voir les erreurs éventuelles
- Si vous voyez des erreurs de connexion à l'API, vérifiez que le backend est bien lancé sur le port 5000

---

## Dépannage

### Le frontend ne se connecte pas à l'API :

1. Vérifiez que l'API backend est lancée :
   - Testez http://localhost:5000/api/tasks dans votre navigateur
   - Vous devriez voir une réponse JSON (même vide `[]`)

2. Vérifiez les logs du conteneur API :
   ```bash
   docker logs flask-api
   ```

3. Vérifiez les logs du conteneur frontend :
   ```bash
   docker logs react-frontend
   ```

### Erreurs de build Docker :

1. Arrêtez les conteneurs :
   ```bash
   docker-compose down
   ```

2. Reconstruisez les images :
   ```bash
   docker-compose up --build
   ```

### Le port 3000 est déjà utilisé :

Modifiez le port dans `docker-compose.yml` :
```yaml
ports:
  - "3001:3000"  # Changez 3000 en 3001 (ou un autre port libre)
```

Puis accédez à http://localhost:3001

