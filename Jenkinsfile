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
                    // ✅ Git commit SHA를 태그로 사용 (추적성 향상)
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
        
        // ✅ 추가: 이미지 업데이트를 Git에 반영 (GitOps)
        stage('Update Manifest') {
            steps {
                script {
                    def tag = "${GIT_COMMIT_SHORT}-${env.BUILD_NUMBER}"
                    sh """
                        git config user.email "jenkins@example.com"
                        git config user.name "Jenkins"
                        sed -i 's|image: ${DOCKER_IMAGE}:.*|image: ${DOCKER_IMAGE}:${tag}|g' k8s/django-deployment.yml
                        git add k8s/django-deployment.yml
                        git commit -m "Update image to ${tag}" || true
                        git push origin main || true
                    """
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
