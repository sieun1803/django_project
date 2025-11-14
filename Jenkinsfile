// Jenkins 파이프라인 스크립트
// GitHub에서 장고 프로젝트 코드를 가져와
// Docker 이미지를 빌드하고 Docker Hub로 푸시하는 역할을 한다.

pipeline {
    // 어느 노드에서나 실행 (현재는 kube-control1 노드에서 실행됨)
    agent any

    // 전체 단계에서 공통으로 사용할 환경 변수 정의
    environment {
        // Docker Hub에서 사용할 이미지 이름 (리포지토리 이름과 동일하게 설정)
        DOCKER_IMAGE = "sieun1803/django-k8s-app"
    }

    stages {

        stage('Checkout') {
            // 1단계: GitHub에서 소스 코드 가져오기
            steps {
                // main 브랜치를 기준으로 리포지토리를 클론
                git branch: 'main',
                    url: 'https://github.com/sieun1803/django-k8s-cicd.git'
            }
        }

        stage('Build Docker Image') {
            // 2단계: 가져온 코드로 Docker 이미지 빌드
            steps {
                script {
                    // Jenkins 빌드 번호를 이용해 태그 생성 (예: build-1, build-2 ...)
                    def tag = "build-${env.BUILD_NUMBER}"

                    // 현재 디렉터리의 Dockerfile을 사용해 이미지 빌드
                    // 결과: sieun1803/django-k8s-app:build-번호
                    sh "docker build -t ${DOCKER_IMAGE}:${tag} ."

                    // 항상 latest 태그도 생성해 두면 K8s에서 사용하기 편리하다.
                    sh "docker tag ${DOCKER_IMAGE}:${tag} ${DOCKER_IMAGE}:latest"
                }
            }
        }

        stage('Push Docker Image') {
            // 3단계: 빌드된 이미지를 Docker Hub에 푸시
            steps {
                script {
                    // Jenkins에 저장해둔 Docker Hub 자격 증명 사용
                    withCredentials([usernamePassword(
                        credentialsId: 'dockerhub-cred', // 위에서 만든 Credentials ID
                        usernameVariable: 'DOCKER_USER', // 셸에서 사용할 변수명
                        passwordVariable: 'DOCKER_PASS'
                    )]) {

                        // Docker Hub 로그인 (비밀번호를 표준 입력으로 전달)
                        sh "echo ${DOCKER_PASS} | docker login -u ${DOCKER_USER} --password-stdin"

                        // latest 태그 이미지 푸시
                        sh "docker push ${DOCKER_IMAGE}:latest"
                    }
                }
            }
        }
    }
}
