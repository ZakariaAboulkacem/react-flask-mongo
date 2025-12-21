pipeline {
    agent any
    
    environment {
        DOCKER_USER_ID = 'zakaria227' 
        FRONTEND_IMAGE = "${DOCKER_USER_ID}/react-flask-mongodb-frontend:latest"
        BACKEND_IMAGE = "${DOCKER_USER_ID}/react-flask-mongodb-backend:latest"
    }
    
    stages {
        stage('Checkout Git') {
            steps {
                echo '📥 Pulling code from Git repository...'
                // Cette commande récupère le code initialement
                checkout scm
                
                script {
                    // Utilisation des credentials pour permettre le 'git pull' manuel sur repo privé
                    withCredentials([usernamePassword(credentialsId: 'repo_github', passwordVariable: 'GIT_PASS', usernameVariable: 'GIT_USER')]) {
                        try {
                            // On construit l'URL avec les identifiants pour l'authentification
                            sh "git pull https://${GIT_USER}:${GIT_PASS}@github.com/ZakariaAboulkacem/react-flask-mongo.git main"
                        } catch (Exception e) {
                            sh "git pull https://${GIT_USER}:${GIT_PASS}@github.com/ZakariaAboulkacem/react-flask-mongo.git master"
                        }
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
                    withCredentials([usernamePassword(credentialsId: 'zakaria227-dockerhub', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                        sh """
                            echo "${DOCKER_PASS}" | docker login -u "${DOCKER_USER}" --password-stdin
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
            echo '❌ Pipeline failed!' //tetstet
        }
    }
}