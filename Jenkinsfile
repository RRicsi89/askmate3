pipeline {
    agent none
    triggers{ pollSCM('H H(9-16)/2 * * 1-5') }
    environment {
        AWS_CREDS = "some-creds"
        HELM_EXPERIMENTAL_OCI = 1
    }
    stages {
        stage('Build image') {
            when {
                beforeAgent true
                branch 'main'
            }
            agent {
                kubernetes {
                    label 'docker-agent'
                    idleMinutes 3
                    yamlFile 'agents/docker.yaml'
                    defaultContainer 'docker'
                }
            }
            environment {
                IMAGE = "public.ecr.aws/g0w3j7p1/rozsar"
            }
            steps {
                sh '''
                    apk update
                    apk add aws-cli
                '''
                sh '''
                    docker build -t ${IMAGE}:${BUILD_NUMBER} .
                    aws ecr-public get-login-password --region us-east-1 | docker login --username AWS --password-stdin public.ecr.aws/g0w3j7p1
                    docker push ${IMAGE}:${BUILD_NUMBER}
                '''
            }
        }
        stage('Build') {
            when {
                beforeAgent true
                branch 'main'
            }
            agent {
                kubernetes {
                    label 'kubernetes-agent'
                    idleMinutes 3
                    yamlFile 'agents/kubernetes.yaml'
                    defaultContainer 'kubernetes'
                }
            }
            steps {
                sh '''
                    apk update
                    apk add sed
                    sed -i "s|{{VERSION}}|${BUILD_NUMBER}|g" askmate3/templates/app.yaml
                    helm package askmate3 --version 0.1.${BUILD_NUMBER}
                '''
            }
        }
        stage('Push') {
            when {
                beforeAgent true
                branch 'main'
            }
            agent {
                kubernetes {
                    label 'kubernetes-agent'
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
                    aws ecr get-login-password --region eu-central-1 | helm registry login --username AWS --password-stdin ACCOUNT_ID.dkr.ecr.eu-central-1.amazonaws.com
                    helm push askmate3-0.1.${BUILD_NUMBER}.tgz oci://ACCOUNT_ID.dkr.ecr.eu-central-1.amazonaws.com/
                '''
            }
        }
        stage('Deploy') {
            when {
                beforeAgent true
                branch 'main'
            }
            agent {
                kubernetes {
                    label 'kubernetes-agent'
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