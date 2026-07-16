pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-creds')
        IMAGE_NAME = "your-dockerhub-username/taskflow"
        IMAGE_TAG = "${env.BUILD_NUMBER}"
        KUBECONFIG = "/var/jenkins_home/.kube/config"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/your-username/taskflow.git'
            }
        }

        stage('Install & Test') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install -r requirements.txt
                    pytest tests/ -v
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $IMAGE_NAME:$IMAGE_TAG -t $IMAGE_NAME:latest .'
            }
        }

        stage('Push to Docker Hub') {
            steps {
                sh '''
                    echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin
                    docker push $IMAGE_NAME:$IMAGE_TAG
                    docker push $IMAGE_NAME:latest
                '''
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh '''
                    kubectl apply -f k8s/namespace.yaml
                    kubectl apply -f k8s/secret.yaml
                    kubectl apply -f k8s/postgres.yaml
                    kubectl apply -f k8s/flask-deployment.yaml
                    kubectl apply -f k8s/ingress.yaml
                    kubectl apply -f k8s/hpa.yaml
                    kubectl set image deployment/taskflow-web taskflow-web=$IMAGE_NAME:$IMAGE_TAG -n taskflow
                    kubectl rollout status deployment/taskflow-web -n taskflow
                '''
            }
        }
    }

    post {
        success {
            echo 'Deployment successful.'
        }
        failure {
            echo 'Pipeline failed — check console output above.'
        }
    }
}
