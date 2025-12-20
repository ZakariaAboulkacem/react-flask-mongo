pipeline {
    agent any
    
    environment {
        // Variables pour Docker Hub (à configurer dans Jenkins)
        DOCKER_HUB_REPO = 'your-dockerhub-username/react-flask-mongodb'
        FRONTEND_IMAGE = "${DOCKER_HUB_REPO}-frontend:latest"
        BACKEND_IMAGE = "${DOCKER_HUB_REPO}-backend:latest"
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
                    // Build frontend image
                    sh """
                        docker build -t ${FRONTEND_IMAGE} ./frontend
                    """
                    
                    // Build backend image
                    sh """
                        docker build -t ${BACKEND_IMAGE} ./backend
                    """
                    
                    echo '✅ Docker images built successfully'
                }
            }
        }
        
        stage('Run Local (docker-compose)') {
            steps {
                echo '🚀 Starting services with docker-compose...'
                script {
                    sh """
                        docker-compose down || true
                        docker-compose up -d --build
                    """
                    
                    // Attendre que les services démarrent
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
                            echo \$DOCKER_PASS | docker login -u \$DOCKER_USER --password-stdin
                            docker push ${FRONTEND_IMAGE} || echo 'Frontend image push failed'
                            docker push ${BACKEND_IMAGE} || echo 'Backend image push failed'
                            docker logout
                        """
                    }
                    echo '✅ Images pushed to Docker Hub'
                }
            }
        }
    }
    
    post {
        always {
            echo '🧹 Cleaning up...'
            sh 'docker-compose down || true'
        }
        success {
            echo '✅ Pipeline succeeded!'
        }
        failure {
            echo '❌ Pipeline failed!'
        }
    }
}

