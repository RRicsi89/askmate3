pipeline {
    agent {
        kubernetes {
            label 'agent-pod'  // all your pods will be named with this prefix, followed by a unique id
            idleMinutes 5  // how long the pod will live after no jobs have run on it
            yamlFile 'agents.yaml'  // path to the pod definition relative to the root of our project 
            defaultContainer 'terraform'  // define a default container if more than a few stages use it, will default to jnlp container
        }
     }
    environment {
        AWS_CREDS = credentials('aws-credentials')
        HELM_EXPERIMENTAL_OCI = 1
    }
    stages {
        stage('Build') {
            steps {
                container('kubernetes') {
                    sh 'helm package askmate3 --version 0.1.${BUILD_NUMBER}'
                }
            }
        }
        stage('Push') {
            steps {
                container('kubernetes') {
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
        }
        stage('Deploy') {
            environment {
                EKS_ARN = credentials('cluster-arn')
            }
            steps {
                container('kubernetes') {
                    sh '''
                        apk update
                        apk add aws-cli
                        aws eks --region eu-central-1 update-kubeconfig --name rozsar-eks-cluster
                        kubectl config set-context ${EKS_ARN}
                    '''
                    sh 'helm upgrade --install askmate rozsar-askmate-0.1.${BUILD_NUMBER}.tgz'
                }
            }
        }
    }
}