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
            sh 'chown 106:112 test-results.xml'
            sh 'chown 106:112 -R .pytest_cache && chown 106:112 -R test'
        }


	stage 'Build'
        docker.withRegistry('https://harbor.ww.home', '5a2a36dd-8c89-4aff-bc7b-934726f6b8ef') {
            def dockerRepo = 'dojo/news-streams'
            def pythonDockerfile = './dockerfiles/Dockerfiles-stream'
            def pythonImage = docker.build("${dockerRepo}:python-${env.BUILD_ID}", "-f ${pythonDockerfile} .")
            pythonImage.push()
        }
}
