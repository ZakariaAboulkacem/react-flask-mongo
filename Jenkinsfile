pipeline {
    agent any
    
    environment {
        // IMPORTANT : Remplacez 'votre_username' par votre identifiant Docker Hub réel
        DOCKER_USER_ID = 'zakaria227' 
        FRONTEND_IMAGE = "${DOCKER_USER_ID}/react-flask-mongodb-frontend:latest"
        BACKEND_IMAGE = "${DOCKER_USER_ID}/react-flask-mongodb-backend:latest"
    }
    
    stages {
        stage('Checkout Git') {
            steps {
                echo '📥 Pulling code from Git repository...'
                checkout scm
                script {
                    try {
                        sh 'git pull origin main'
                    } catch (Exception e) {
                        sh 'git pull origin master'
                    }
                }
            }
        }
        
        stage('Build Docker Images') {
            steps {
                echo '🔨 Building Docker images...'
                script {
                    sh "docker build -t ${FRONTEND_IMAGE} ./frontend"
                    sh "docker build -t ${BACKEND_IMAGE} ./backend"
                    echo '✅ Docker images built successfully'
                }
            }
        }
        
        stage('Run Local (docker compose)') {
            steps {
                echo '🚀 Starting services with docker compose...'
                script {
                    // Nettoyage avant démarrage pour éviter les conflits de noms
                    sh "docker compose down || true"
                    sh "docker compose up -d --build"
                    sleep(time: 10, unit: 'SECONDS')
                    echo '✅ Services started successfully'
                }
            }
        }
        
        stage('Push to Docker Hub') {
            steps {
                echo '📤 Pushing images to Docker Hub...'
                script {
                    // Utilisation des identifiants stockés dans Jenkins
                    withCredentials([usernamePassword(credentialsId: 'zakaria227-dockerhub', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                        sh """
                            # Connexion sécurisée
                            echo "${DOCKER_PASS}" | docker login -u "${DOCKER_USER}" --password-stdin
                            
                            # Push sans le "|| echo" pour détecter les vraies erreurs
                            docker push ${FRONTEND_IMAGE}
                            docker push ${BACKEND_IMAGE}
                            
                            docker logout
                        """
                    }
                    echo '✅ Images pushed to Docker Hub successfully'
                }
            }
        }
    }
    
    post {
        always {
            echo '🧹 Cleaning up...'
            sh 'docker compose down || true'
        }
        success {
            echo '✅ Pipeline succeeded!'
        }
        failure {
            echo '❌ Pipeline failed!'
        }
    }
}