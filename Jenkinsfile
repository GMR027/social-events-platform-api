pipeline {
    agent any
    options {
        skipStagesAfterUnstable()
    }
    environment {
        DJANGO_APP_NAME = "social_events"
        APP_FOLDER = "social-events"
        ENVT = sh(script: "echo ${ENV}", , returnStdout: true).trim()
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
            }
        }
        stage("Build") {
            steps {
                sh "sudo docker build -t social-events ."
                sh "sudo docker tag social-events longmont.iguzman.com.mx:5000/social-events:1.0"
                sh "sudo docker push longmont.iguzman.com.mx:5000/social-events:1.0"
            }
        }
        stage("Stop current instance") {
            steps {
                sh "sudo docker-compose --env-file /social-events/$ENVT/env -f docker-compose.yaml down"
            }
        }
        stage("Start instance") {
            steps {
                sh "sudo docker-compose --env-file /social-events/$ENVT/env -f docker-compose.yaml up -d"
            }
        }
    }
}
