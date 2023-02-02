pipeline {
    agent none
    environment {
        AWS_CREDS = credentials('AWS')
        HELM_EXPERIMENTAL_OCI = 1
    }
    stages {
        stage('Build') {
            agent {
                kubernetes {
                    label 'agent-pod'
                    idleMinutes 3
                    yamlFile 'agents/kubernetes.yaml'
                    defaultContainer 'kubernetes'
                }
            }
            steps {
                sh 'helm package askmate3 --version 0.1.${BUILD_NUMBER}'
            }
        }
        stage('Push') {
            agent {
                kubernetes {
                    label 'agent-pod'
                    idleMinutes 3
                    yamlFile 'agents/kubernetes.yaml'
                    defaultContainer 'kubernetes'
                }
            }
            steps {
                sh '''
                    apk update
                    apk add aws-cli
                '''
                sh '''
                    aws ecr get-login-password --region eu-central-1 | helm registry login --username AWS --password-stdin 085155013250.dkr.ecr.eu-central-1.amazonaws.com
                    helm push askmate3-0.1.${BUILD_NUMBER}.tgz oci://085155013250.dkr.ecr.eu-central-1.amazonaws.com/
                '''
            }
        }
        stage('Deploy') {
            agent {
                kubernetes {
                    label 'agent-pod'
                    idleMinutes 3
                    yamlFile 'agents/kubernetes.yaml'
                    defaultContainer 'kubernetes'
                }
            }
            environment {
                EKS_ARN = credentials('cluster-arn')
            }
            steps {
                sh '''
                    apk update
                    apk add aws-cli
                    aws eks --region eu-central-1 update-kubeconfig --name rozsar-eks-cluster
                    kubectl config set-context ${EKS_ARN}
                '''
                sh 'helm upgrade --install askmate askmate3-0.1.${BUILD_NUMBER}.tgz'
            }
        }
    }
}