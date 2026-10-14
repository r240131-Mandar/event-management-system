pipeline {
    agent any
        environment {
        PATH = "C:\\Users\\mandar\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin;${env.PATH}"
    }
    stages {
        stage('Checkout') {
            steps { checkout scm }
        }
        stage('Build') {
            steps { bat 'docker build -t %IMAGE%:%BUILD_NUMBER% -t %IMAGE%:latest .' }
        }
        stage('Test') {
            steps { bat 'docker run --rm %IMAGE%:latest python -m py_compile app.py' }
        }
        stage('Deploy') {
            steps {
                bat 'docker rm -f %CONTAINER% || exit 0'
                bat 'docker run -d --name %CONTAINER% -p 5000:5000 %IMAGE%:latest'
            }
        }
    }
}
