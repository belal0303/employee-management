pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Python Syntax Check') {
            steps {
                sh 'python3 -m py_compile app.py'
            }
        }

        stage('SonarQube Analysis') {
            steps {
                script {
                    def scannerHome = tool(
                        name: 'SonarScanner',
                        type: 'hudson.plugins.sonar.SonarRunnerInstallation'
                    )

                    withSonarQubeEnv('SonarQube') {
                        sh """
                            ${scannerHome}/bin/sonar-scanner \
                            -Dsonar.projectKey=employee-management \
                            -Dsonar.projectName="Employee Management" \
                            -Dsonar.sources=. \
                            -Dsonar.exclusions=venv/**,__pycache__/**,.scannerwork/**
                        """
                    }
                }
            }
        }

        stage('Docker Build') {
            steps {
                sh 'docker build -t employee-app:${BUILD_NUMBER} .'
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                    docker rm -f employee-container || true
                    docker run -d \
                    --name employee-container \
                    -p 5001:5001 \
                    employee-app:${BUILD_NUMBER}
                '''
            }
        }

        stage('Application Test') {
            steps {
                sh 'curl --retry 10 --retry-delay 2 --retry-connrefused -f http://localhost:5001/'
            }
        }
    }
}
