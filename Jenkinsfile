node {
	stage 'Checkout'
        checkout scm

    stage 'Test Streams'
        docker.image('python:3.8.12-slim-buster').inside('-e HOME=/tmp -u 106:112') {
            //install python dependencies (requirements file)
            sh '/usr/local/bin/pip install -r news_stream_streams/requirements.txt'
            // run python unittest
            sh 'PYTHONPATH=news_stream_streams $HOME/.local/bin/pytest news_stream_streams/test --junit-xml=test-results.xml'
        }
        junit 'test-results.xml'


	stage 'Build Streams'
        docker.withRegistry('https://harbor.ww.home', '5a2a36dd-8c89-4aff-bc7b-934726f6b8ef') {
            def dockerRepo = 'dojo/news-streams'
            def pythonDockerfile = './dockerfiles/Dockerfiles-streams'
            def pythonImage = docker.build("${dockerRepo}:stream-${env.BUILD_ID}", "-f ${pythonDockerfile} .")
            pythonImage.push()
        }

	stage 'Build Django'
        docker.withRegistry('https://harbor.ww.home', '5a2a36dd-8c89-4aff-bc7b-934726f6b8ef') {
            def dockerRepo = 'dojo/news-streams'
            def pythonDockerfile = './dockerfiles/Dockerfiles-django'
            def pythonImage = docker.build("${dockerRepo}:django-${env.BUILD_ID}", "-f ${pythonDockerfile} .")
            pythonImage.push()
        }
}
