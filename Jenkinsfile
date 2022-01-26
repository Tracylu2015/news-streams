node {
	stage 'Checkout'
        checkout scm

    stage 'Test'
        docker.image('python:3.8.12-slim-buster').inside('-u root:root') {
            //install python dependencies (requirements file)
            sh '/usr/local/bin/pip install -r requirements.txt'
            // run python unittest
            sh 'PYTHONPATH=. pytest test --junit-xml=test-results.xml'

            // Fix change files permission to jenkins user
            sh 'chown 106:112 -R .'
        }
        junit 'test-results.xml'


	stage 'Build'
        docker.withRegistry('https://harbor.ww.home', '5a2a36dd-8c89-4aff-bc7b-934726f6b8ef') {
            def dockerRepo = 'dojo/news-streams'
            def pythonDockerfile = './dockerfiles/Dockerfiles-stream'
            def pythonImage = docker.build("${dockerRepo}:python-${env.BUILD_ID}", "-f ${pythonDockerfile} .")
            pythonImage.push()
        }
//
//     post
//         changed {
//             script {
//                 if (currentBuild.currentResult == 'FAILURE') { // Other values: SUCCESS, UNSTABLE
//                     // Send an email only if the build status has changed from green/unstable to red
//                     emailext subject: "Failed CI Job: ${env.JOB_NAME} [${env.BUILD_NUMBER}]",
//                         body: '$DEFAULT_CONTENT',
//                         recipientProviders: [
//                             [$class: 'DevelopersRecipientProvider']
//                         ],
//                         replyTo: '$DEFAULT_REPLYTO',
//                         to: '$DEFAULT_RECIPIENTS'
//                 }
//             }
//         }
}
