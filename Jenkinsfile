pipeline {
    agent any

    environment {
        PATH = "C:\\Users\\mandar\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin;${env.PATH}"
        IMAGE_NAME = "event-management-system"
        CONTAINER_NAME = "ems-test-run"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build') {
            steps {
                bat 'docker build -t %IMAGE_NAME%:%BUILD_NUMBER% -t %IMAGE_NAME%:latest .'
            }
        }

        stage('Test') {
            steps {
                bat 'docker image inspect %IMAGE_NAME%:latest'
            }
        }

        stage('Deploy') {
            steps {
                bat 'docker rm -f %CONTAINER_NAME% || exit 0'
                bat 'docker run -d --name %CONTAINER_NAME% -p 5000:5000 %IMAGE_NAME%:latest'
            }
        }
    }
}