node {
	stage 'Checkout'
        checkout scm

	stage 'Build'
        docker.withRegistry('https://harbor.ww.home', '5a2a36dd-8c89-4aff-bc7b-934726f6b8ef') {
            def dockerRepo = 'dojo/news-streams'
            def pythonDockerfile = './dockerfiles/Dockerfiles-stream'
            def pythonImage = docker.build("${dockerRepo}:python-${env.BUILD_ID}", "-f ${dockerfile} .")
            pythonImage.push()
        }
}
