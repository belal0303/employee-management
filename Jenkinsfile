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

        // NEW STAGE: Package and Archive Artifact
        stage('Package & Archive Artifact') {
            steps {
                sh '''
                    tar -czf employee-management-${BUILD_NUMBER}.tar.gz \
                        app.py requirements.txt Dockerfile
                '''

                archiveArtifacts artifacts: 'employee-management-*.tar.gz',
                                 fingerprint: true
            }
        }

 stage('Upload Artifact to Nexus') {
    steps {
        withCredentials([usernamePassword(
            credentialsId: 'nexus-credentials',
            usernameVariable: 'NEXUS_USER',
            passwordVariable: 'NEXUS_PASSWORD'
        )]) {
            sh '''
                curl --fail --show-error --retry 3 \
                --user "$NEXUS_USER:$NEXUS_PASSWORD" \
                --upload-file "employee-management-${BUILD_NUMBER}.tar.gz" \
                "http://localhost:8081/repository/employee-artifacts/employee-management-${BUILD_NUMBER}.tar.gz"
            '''
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