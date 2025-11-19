pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = "sieun1803/django-k8s-app"
        GIT_COMMIT_SHORT = sh(
            script: "git rev-parse --short HEAD",
            returnStdout: true
        ).trim()
    }
    
    stages {
        stage('Build Docker Image') {
            steps {
                script {
                    def tag = "${GIT_COMMIT_SHORT}-${env.BUILD_NUMBER}"
                    
                    withCredentials([usernamePassword(
                        credentialsId: 'dockerhub-cred',
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASS'
                    )]) {
                        sh "echo ${DOCKER_PASS} | docker login -u ${DOCKER_USER} --password-stdin"
                        sh "docker build -t ${DOCKER_IMAGE}:${tag} ."
                        sh "docker tag ${DOCKER_IMAGE}:${tag} ${DOCKER_IMAGE}:latest"
                    }
                }
            }
        }
        
        stage('Push Docker Image') {
            steps {
                script {
                    def tag = "${GIT_COMMIT_SHORT}-${env.BUILD_NUMBER}"
                    
                    withCredentials([usernamePassword(
                        credentialsId: 'dockerhub-cred',
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASS'
                    )]) {
                        sh "docker push ${DOCKER_IMAGE}:${tag}"
                        sh "docker push ${DOCKER_IMAGE}:latest"
                    }
                }
            }
        }
    }
    
    post {
        always {
            sh 'docker logout'
        }
    }
}