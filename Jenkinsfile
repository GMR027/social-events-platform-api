pipeline {
    agent any
    options {
        skipStagesAfterUnstable()
    }
    environment {
        APP_FOLDER = "social-events"
        ENVT = sh(script: "echo ${ENV}", , returnStdout: true).trim()
        BRANCH_NAME = sh(script: "echo ${branchName}", , returnStdout: true).trim()
        BUILD_DOCKER_IMAGE = sh(script: "echo ${BUILD_DOCKER_IMAGE}", , returnStdout: true).trim()
    }
    stages {
        stage("Check App folders") {
            steps {
                sh "sudo mkdir /$APP_FOLDER -p"
                sh "sudo chmod -R 777 /$APP_FOLDER"
                sh "sudo mkdir /$APP_FOLDER/$ENVT -p"
                sh "sudo chmod -R 777 /$APP_FOLDER/$ENVT"

                sh "sudo mkdir /$APP_FOLDER/$ENVT/static -p"
                sh "sudo chmod -R 777 /$APP_FOLDER/$ENVT/static"

                sh "sudo mkdir /$APP_FOLDER/$ENVT/media -p"
                sh "sudo chmod -R 777 /$APP_FOLDER/$ENVT/media"

                sh "sudo mkdir /$APP_FOLDER/$ENVT/db -p"
                sh "sudo chmod -R 777 /$APP_FOLDER/$ENVT/db"

                sh "sudo mkdir /config/$APP_FOLDER/$ENVT -p"
                sh "sudo chmod -R 777 /config/$APP_FOLDER/$ENVT"
            }
        }
        stage("Build docker image") {
            when {
                expression { BUILD_DOCKER_IMAGE == "yes" }
            }
            steps {
                sh "sudo docker build -t $APP_FOLDER ."
                sh "sudo docker tag $APP_FOLDER longmont.iguzman.com.mx:5000/$APP_FOLDER:1.0"
                sh "sudo docker push longmont.iguzman.com.mx:5000/$APP_FOLDER:1.0"
            }
        }
        stage("Restart instance") {
            steps {
                sh "sudo docker-compose --env-file /config/$APP_FOLDER/$ENVT/env -f docker-compose.yaml down"
                sh "sudo docker-compose --env-file /config/$APP_FOLDER/$ENVT/env -f docker-compose.yaml up -d"
            }
        }
    }
}
