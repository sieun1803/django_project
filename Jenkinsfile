pipeline {
    agent any

    environment {
        // 🔹 DockerHub에 올릴 이미지 이름 (리포지토리 명)
        DOCKER_IMAGE = "sieun1803/django-k8s-app"
    }

    stages {
        stage('Set Image Tag') {
            steps {
                script {
                    // 🔹 현재 Git 커밋 SHA(앞 7자리) 가져오기
                    def shortCommit = sh(
                        script: "git rev-parse --short HEAD",
                        returnStdout: true
                    ).trim()

                    // 🔹 커밋 + 빌드번호 조합으로 태그 생성 (예: 2f22553-1)
                    env.IMAGE_TAG = "${shortCommit}-${env.BUILD_NUMBER}"
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    // 🔹 위에서 만든 IMAGE_TAG 사용해서 이미지 빌드
                    withCredentials([usernamePassword(
                        credentialsId: 'dockerhub-cred', // 🔹 Jenkins 자격증명 ID
                        usernameVariable: 'DOCKER_USER',  // 🔹 DockerHub ID가 들어갈 변수
                        passwordVariable: 'DOCKER_PASS'   // 🔹 DockerHub 비밀번호 변수
                    )]) {
                        // 🔹 DockerHub 로그인
                        sh "echo ${DOCKER_PASS} | docker login -u ${DOCKER_USER} --password-stdin"

                        // 🔹 커밋 기반 태그로 이미지 빌드
                        sh "docker build -t ${DOCKER_IMAGE}:${env.IMAGE_TAG} ."

                        // 🔹 latest 태그도 같이 생성
                        sh "docker tag ${DOCKER_IMAGE}:${env.IMAGE_TAG} ${DOCKER_IMAGE}:latest"
                    }
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    withCredentials([usernamePassword(
                        credentialsId: 'dockerhub-cred',
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASS'
                    )]) {
                        // 🔹 위에서 만든 태그로 푸시
                        sh "docker push ${DOCKER_IMAGE}:${env.IMAGE_TAG}"

                        // 🔹 latest 태그도 푸시
                        sh "docker push ${DOCKER_IMAGE}:latest"
                    }
                }
            }
        }

        stage('Update Manifest') {
            steps {
                script {
                    // 🔹 Git 사용자 정보 설정 (Jenkins 커밋용)
                    sh """
                        git config user.email "jenkins@k8s.local"
                        git config user.name "Jenkins"

                        # 🔹 Deployment 매니페스트 안의 이미지 태그를 새 태그로 교체
                        #   - 파일 경로/이름은 네 실제 파일에 맞게 수정해줘!
                        sed -i 's|image: ${DOCKER_IMAGE}:.*|image: ${DOCKER_IMAGE}:${env.IMAGE_TAG}|g' k8s/manifests/django-deploy.yml

                        # 🔹 변경된 매니페스트 Git에 커밋 & 푸시
                        git add k8s/manifests/django-deploy.yml
                        git commit -m "Update image to ${env.IMAGE_TAG}" || true
                        git push origin main || true
                    """
                }
            }
        }
    }

    post {
        always {
            // 🔹 무조건 마지막에 Docker 로그아웃
            sh 'docker logout'
        }
    }
}
