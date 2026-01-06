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
                sleep(time: 10, unit: 'SECONDS')
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
            echo 'Pipeline exécuté avec succès. oui '
        }
        failure {
            echo 'Erreur lors de l’exécution du pipeline.'
        }
    }
}