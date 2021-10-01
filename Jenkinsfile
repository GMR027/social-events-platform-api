pipeline {
    agent any
    options {
        skipStagesAfterUnstable()
    }
    environment {
        DJANGO_APP_NAME = "nedii_app"
        APP_FOLDER = "BACK"
        ENV = sh(script: "echo ${ENV}", , returnStdout: true).trim()
    }
    stages {
        stage("Check App folders") {
            steps {
                sh "sudo mkdir /var/www/apps -p"
                sh "sudo chmod -R 777 /var/www/apps"
                sh "sudo mkdir /var/www/apps/$ENV -p"
                sh "sudo chmod -R 777 /var/www/apps/$ENV"

                sh "sudo mkdir /var/www/virtualenvs -p"
                sh "sudo chmod -R 777 /var/www/virtualenvs"

                sh "sudo mkdir /var/www/env -p"
                sh "sudo chmod -R 777 /var/www/env"
                sh "sudo mkdir /var/www/env/$ENV -p"
                sh "sudo chmod -R 777 /var/www/env/$ENV"

                sh "sudo mkdir /var/www/static -p"
                sh "sudo chmod -R 777 /var/www/static"
                sh "sudo mkdir /var/www/static/$ENV -p"
                sh "sudo chmod -R 777 /var/www/static/$ENV"

                sh "sudo mkdir /var/www/static/$ENV/$APP_FOLDER/media -p"
                sh "sudo chmod -R 777 /var/www/static/$ENV/$APP_FOLDER/media"

                sh "sudo rm -rf /var/www/static/$ENV/$APP_FOLDER/static"
                sh "sudo mkdir /var/www/static/$ENV/$APP_FOLDER/static -p"
                sh "sudo chmod -R 777 /var/www/static/$ENV/$APP_FOLDER/static"
            }
        }
        stage("Build") {
            steps {
                sh ". /var/www/virtualenvs/$DJANGO_APP_NAME-$ENV/bin/activate"
                sh "sudo cp /var/www/env/$ENV/$APP_FOLDER-$ENV\\.env ./$DJANGO_APP_NAME/.env"
                sh "/var/www/virtualenvs/$DJANGO_APP_NAME-$ENV/bin/python3 -m pip install -r requirements.txt"
                sh "/var/www/virtualenvs/$DJANGO_APP_NAME-$ENV/bin/python3 manage.py migrate"
                sh "rm -rf static"
                sh "/var/www/virtualenvs/$DJANGO_APP_NAME-$ENV/bin/python3 manage.py collectstatic --noinput"
            }
        }
        stage("Deploy") {
            steps {
                sh "sudo rm -rf /var/www/apps/$ENV/$APP_FOLDER"
                sh "sudo mkdir /var/www/apps/$ENV/$APP_FOLDER -p"
                sh "sudo cp -r ./* /var/www/apps/$ENV/$APP_FOLDER"
                sh "sudo cp -r ./static /var/www/static/$ENV/$APP_FOLDER/"
            }
        }
        stage("Restart Supervisor") {
            steps {
                sh "sudo supervisorctl reread"
                sh "sudo supervisorctl update"
                sh "sudo supervisorctl restart $DJANGO_APP_NAME-$ENV"
            }
        }
    }
}
