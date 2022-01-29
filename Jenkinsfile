pipeline {
    agent any

    stages {    //CI including test and build dockerfiles
        stage('Test Streams') {
            agent {
                docker {
                    image 'python:3.8.12-slim-buster'
                    args '-e HOME=/tmp -u 106:112'
                }
            }
            steps {
                sh '/usr/local/bin/pip install -r news_stream_streams/requirements.txt'
                sh 'PYTHONPATH=news_stream_streams $HOME/.local/bin/pytest news_stream_streams/test --junit-xml=test-results.xml'
                junit 'test-results.xml'
            }
        }

        stage('Build Streams') {
            steps {
                script {
                    docker.withRegistry('https://harbor.ww.home', '5a2a36dd-8c89-4aff-bc7b-934726f6b8ef') {
                        def dockerRepo = 'dojo/news-streams'
                        def pythonDockerfile = './dockerfiles/Dockerfiles-streams'
                        def pythonImage = docker.build("${dockerRepo}:stream-${env.BUILD_ID}", "-f ${pythonDockerfile} .")
                        pythonImage.push()
                    }
                }
            }
        }

        stage('Build Django') {
            steps {
                script {
                    docker.withRegistry('https://harbor.ww.home', '5a2a36dd-8c89-4aff-bc7b-934726f6b8ef') {
                        def dockerRepo = 'dojo/news-streams'
                        def pythonDockerfile = './dockerfiles/Dockerfiles-django'
                        def pythonImage = docker.build("${dockerRepo}:django-${env.BUILD_ID}", "-f ${pythonDockerfile} .")
                        pythonImage.push()
                    }
                }
            }
        }
        stage('Deploy Kubernetes') {         // CD for deployment
            parallel {
                stage('Deploy news-streams') {
                    steps {
                        dir("deploy/news-streams") {
                            sh "kustomize edit set image harbor.ww.home/dojo/news-streams=harbor.ww.home/dojo/news-streams:stream-${env.BUILD_ID}"
                            sh 'kustomize build . | kubectl apply -f -'
                        }
                    }
                }
                stage('Deploy news-streams-reddit') {
                    steps {
                        dir("deploy/news-streams-reddit") {
                            sh "kustomize edit set image harbor.ww.home/dojo/news-streams=harbor.ww.home/dojo/news-streams:stream-${env.BUILD_ID}"
                            sh 'kustomize build . | kubectl apply -f -'
                        }
                    }
                }
                stage('Deploy backend-api') {
                    steps {
                        dir("deploy/backend-api") {
                            sh "kustomize edit set image harbor.ww.home/dojo/news-streams=harbor.ww.home/dojo/news-streams:django-${env.BUILD_ID}"
                            sh 'kustomize build . | kubectl apply -f -'
                        }
                    }
                }
            }
        }
    }

    post {
        failure {
            script {
                emailext subject: "Failed CI Job: ${env.JOB_NAME} [${env.BUILD_NUMBER}]",
                    body: '$DEFAULT_CONTENT',
                    recipientProviders: [
                        [$class: 'DevelopersRecipientProvider']
                    ],
                    replyTo: '$DEFAULT_REPLYTO',
                    to: '$DEFAULT_RECIPIENTS'
            }
        }
    }
}
