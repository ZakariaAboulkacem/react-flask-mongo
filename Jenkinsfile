pipeline {
    agent any

    environment {
        // Docker Hub account
        DOCKER_USER_ID = 'zakaria227'

        // Images names
        FRONTEND_IMAGE = "${DOCKER_USER_ID}/react-flask-mongodb-frontend:latest"
        BACKEND_IMAGE  = "${DOCKER_USER_ID}/react-flask-mongodb-backend:latest"
    }

    stages {

        stage('Checkout') {
            steps {
                echo 'Pull du code depuis GitHub...'
                checkout scm

                script {
                    // Pull manuel avec credentials (repo privé)
                    withCredentials([
                        usernamePassword(
                            credentialsId: 'repo_github',
                            usernameVariable: 'GIT_USER',
                            passwordVariable: 'GIT_PASS'
                        )
                    ]) {
                        sh """
                            git pull https://${GIT_USER}:${GIT_PASS}@github.com/ZakariaAboulkacem/react-flask-mongo.git main \
                            || git pull https://${GIT_USER}:${GIT_PASS}@github.com/ZakariaAboulkacem/react-flask-mongo.git master
                        """
                    }
                }
            }
        }

        stage('Build Images') {
            steps {
                echo 'Construction des images Docker...'
                sh "docker build -t ${FRONTEND_IMAGE} ./frontend"
                sh "docker build -t ${BACKEND_IMAGE} ./backend"
            }
        }

        stage('Run with Docker Compose') {
            steps {
                echo 'Lancement de l’application en local...'
                sh "docker compose down || true"
                sh "docker compose up -d --build"
                
                echo 'Attente du démarrage des services...'
                sleep(time: 15, unit: 'SECONDS') // J'ai augmenté un peu le temps pour être sûr que Mongo est prêt

                // --- TEST DE CONNECTIVITÉ AJOUTÉ ICI ---
                echo 'Vérification que les services répondent (Smoke Test)...'
                // Le flag -f fait échouer la commande si le serveur renvoie une erreur (ex: 500 ou 404)
                sh "curl -f http://localhost:3000"
                sh "curl -f http://localhost:5000"
                // ---------------------------------------
            }
        }

        stage('Push Images') {
            steps {
                echo 'Envoi des images vers Docker Hub...'
                withCredentials([
                    usernamePassword(
                        credentialsId: 'zakaria227-dockerhub',
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASS'
                    )
                ]) {
                    sh """
                        echo "${DOCKER_PASS}" | docker login -u "${DOCKER_USER}" --password-stdin
                        docker push ${FRONTEND_IMAGE}
                        docker push ${BACKEND_IMAGE}
                        docker logout
                    """
                }
            }
        }
    }

    post {
        always {
            echo 'Nettoyage des conteneurs...'
            sh 'docker compose down || true'
        }
        success {
            echo 'Pipeline exécuté avec succès. '
        }
        failure {
            echo 'Erreur lors de l’exécution du pipeline.'
        }
    }
}