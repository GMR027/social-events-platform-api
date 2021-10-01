#! /bin/bash

file_name="";
file_name_alone="";

echo "Enter DNS (api.example.com):";
read dns;
if [ ! -n "$dns" ]
then
	echo "Error: DNS variable not provided, i.e.: api.example.com";
    exit 1;
fi

echo "Enter Folder name (my-api):";
read folder;
if [ ! -n "$folder" ]
then
	echo "Error: folder variable not provided, i.e.: my-api";
    exit 1;
fi

echo "Enter API port (4010):";
read port;
if [ ! -n "$port" ]
then
	echo "Error: api port variable not provided, i.e.: 4010";
    exit 1;
fi

echo "Enter environment (staging):";
read envt;
if [ ! -n "$envt" ]
then
	echo "Error: environtment not provided, i.e.: staging";
    exit 1;
fi

echo "Enter Django App name (my_api):";
read django_app_name;
if [ ! -n "$django_app_name" ]
then
	echo "Error: Django App name variable not provided, i.e.: my_api";
    exit 1;
fi

echo "Enter Django workers (2):";
read django_workers;
if [ ! -n "$django_workers" ]
then
	echo "Error: Django workers variable not provided, i.e.: 2";
    exit 1;
fi

echo "DB name (db_name):";
read db_name;
if [ ! -n "$db_name" ]
then
	echo "Error: db name variable not provided, i.e.: db_name";
    exit 1;
fi

echo "DB user (db_user):";
read db_user;
if [ ! -n "$db_user" ]
then
	echo "Error: db user variable not provided, i.e.: db_user";
    exit 1;
fi

echo "DB password (db_password):";
read db_password;
if [ ! -n "$db_password" ]
then
	echo "Error: db password variable not provided, i.e.: db_password";
    exit 1;
fi

echo "Email ID (john@doe.com):";
read email_id;
if [ ! -n "$email_id" ]
then
	echo "Error: email id variable not provided, i.e.: email_id";
    exit 1;
fi

echo "Email password (password):";
read email_password;
if [ ! -n "$email_password" ]
then
	echo "Error: email password variable not provided, i.e.: email_password";
    exit 1;
fi

echo "Secret Django key (5eu9vgczf):";
read secret_django_key;
if [ ! -n "$secret_django_key" ]
then
	echo "Error: secret djando key variable not provided, i.e.: 5eu9vgczf";
    exit 1;
fi

process_name=$django_app_name"-"$envt;
venv="$django_app_name-$envt";

# ============ Functions ============
# $1 type -> nginx / supervisor
PopulateFile () {
    file_name="deploy/$dns.$1.conf";
    file_name_alone="$dns.$1.conf";
    if [ "$1" == "env" ]
    then
        file_name="deploy/$folder-$envt.env";
    fi
    cp "deploy/$1.conf" $file_name;
    chmod 775 $file_name;
    sed -i "s/PORT/$port/g" $file_name;
    sed -i "s/DNS/$dns/g" $file_name;
    sed -i "s/ENVT/$envt/g" $file_name;
    sed -i "s/FOLDER/$folder/g" $file_name;
    sed -i "s/PROCESS_NAME/$process_name/g" $file_name;
    sed -i "s/VENV/$venv/g" $file_name;
    sed -i "s/DJANGO_APP_NAME/$django_app_name/g" $file_name;
    sed -i "s/APP_ID/$app_id/g" $file_name;
    sed -i "s/DJANGO_WORKERS/$django_workers/g" $file_name;
    sed -i "s/_SECRET_KEY/$secret_django_key/g" $file_name;
    sed -i "s/_DB_NAME/$db_name/g" $file_name;
    sed -i "s/_DB_USER/$db_user/g" $file_name;
    sed -i "s/_DB_PASSWORD/$db_password/g" $file_name;
    sed -i "s/_EMAIL_HOST_USER/$email_id/g" $file_name;
    sed -i "s/_EMAIL_HOST_PASSWORD/$email_password/g" $file_name;
}

echo "Create Nginx configuration? (y/n)";
read create;

if [ "$create" == "y" ]
then
	PopulateFile "nginx";
    echo "======================================";
    echo "$file_name:";
    cat $file_name;
    echo "======================================";
    echo "Deploy Nginx configuration? (y/n)"
    read deploy;
    if [ "$deploy" == "y" ]
    then
        sudo cp $file_name /etc/nginx/sites-available/;
        sudo ln -s /etc/nginx/sites-available/$file_name_alone /etc/nginx/sites-enabled/;
        sudo nginx -t;
        sudo service nginx restart;
    fi
    echo "Delete Nginx configuration? (y/n)"
    read delete_file;
    if [ "$delete_file" == "y" ]
    then
        rm $file_name;
    fi
fi

echo "Create Supervisor configuration? (y/n)";
read create;
if [ "$create" == "y" ]
then
    PopulateFile "supervisor";
    echo "======================================";
    echo $file_name;
    cat $file_name;
    echo "======================================";
    echo "Deploy Supervisor configuration? (y/n)"
    read deploy;
    if [ "$deploy" == "y" ]
    then
        sudo cp $file_name /etc/supervisor/conf.d/;
        sudo supervisorctl reread;
        sudo supervisorctl update;
        sudo supervisorctl status;
    fi
    echo "Delete supervisor configuration? (y/n)";
    read delete_file;
    if [ "$delete_file" == "y" ]
    then
        rm $file_name;
    fi
fi

echo "Create .env configuration file? (y/n)";
read create;

if [ "$create" == "y" ]
then
	PopulateFile "env";
    echo "======================================";
    echo "$file_name:";
    cat $file_name;
    echo "======================================";
    echo "Deploy .env configuration? (y/n)"
    read deploy;
    if [ "$deploy" == "y" ]
    then
        sudo mkdir -p /var/www/env/
        sudo mkdir -p /var/www/env/$envt
        sudo cp $file_name /var/www/env/$envt/;
    fi
    echo "Delete .env configuration file? (y/n)";
    read delete_file;
    if [ "$delete_file" == "y" ]
    then
        rm $file_name;
    fi
fi

echo "Done";
exit 0;
