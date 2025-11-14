// Jenkins 파이프라인 스크립트
// 1) Jenkins Job에서 미리 체크아웃해 온 GitHub 코드( django_project )
// 2) Docker 이미지 빌드
// 3) Docker Hub로 push
// 까지 자동으로 처리한다.

pipeline {
    // 어떤 노드에서나 실행 (현재는 kube-control1 의 Jenkins 서버에서 실행됨)
    agent any

    // 전체 파이프라인에서 공통으로 사용할 환경 변수
    environment {
        // Docker Hub 레포지토리 이름 (미리 만들어둔 저장소)
        DOCKER_IMAGE = "sieun1803/django-k8s-app"
    }

    stages {

        stage('Checkout') {
            // ✅ 여기서는 별도 URL을 쓰지 않고,
            // Jenkins Job 설정(SCM)에 적어둔 django_project 리포지토리를 그대로 사용한다.
            steps {
                // Job의 SCM 설정을 기반으로 워크스페이스를 최신 상태로 맞춤
                checkout scm
            }
        }

        stage('Build Docker Image') {
            // Django 프로젝트 소스로 Docker 이미지 빌드
            steps {
                script {
                    // 빌드 번호를 사용해서 태그 생성 (예: build-1, build-2 ...)
                    def tag = "build-${env.BUILD_NUMBER}"

                    // 현재 워크스페이스(=django_project 코드)에 있는 Dockerfile 로 이미지 빌드
                    // 결과: sieun1803/django-k8s-app:build-번호
                    sh "docker build -t ${DOCKER_IMAGE}:${tag} ."

                    // 항상 latest 태그도 하나 만들어두면,
                    // K8s / ArgoCD에서 이미지 버전 지정하기 편하다.
                    sh "docker tag ${DOCKER_IMAGE}:${tag} ${DOCKER_IMAGE}:latest"
                }
            }
        }

        stage('Push Docker Image') {
            // Docker Hub에 이미지 푸시
            steps {
                script {
                    // Jenkins -> Manage Credentials 에서 만들어 둔
                    // dockerhub-cred (username + PAT) 를 사용한다.
                    withCredentials([usernamePassword(
                        credentialsId: 'dockerhub-cred', // 자격 증명 ID (그대로 사용)
                        usernameVariable: 'DOCKER_USER',  // 셸에서 쓸 환경 변수명
                        passwordVariable: 'DOCKER_PASS'
                    )]) {

                        // Docker Hub 로그인 (비밀번호를 표준입력으로 넘김)
                        sh "echo ${DOCKER_PASS} | docker login -u ${DOCKER_USER} --password-stdin"

                        // latest 태그 이미지를 Docker Hub로 푸시
                        sh "docker push ${DOCKER_IMAGE}:latest"
                    }
                }
            }
        }
    }
}
