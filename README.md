# Social Events Platform API

### Build Docker image
docker build -t social-events .

### Tag Docker image
docker tag social-events longmont.iguzman.com.mx:5000/social-events:1.0

### Push Docker image
docker push longmont.iguzman.com.mx:5000/social-events:1.0

### Run Docker image
docker run -d -p 8000:8000 --name social-events --privileged longmont.iguzman.com.mx:5000/social-events:1.0

# Docker deployment

In order to deploy the API into a Docker container using docker-compose
you need to create the next file into the targe machine:


```sh
/config/social-events/{environment staging|master}/env
```

With the following content:

```sh
SECRET_KEY=my-django-key
ENVT=ENVIRONMENT
DB_NAME=DB_NAME
DB_USER=DB_USER
DB_PASSWORD=DB_PASSWORD
EMAIL_HOST_USER=EMAIL_HOST_USER
EMAIL_HOST_PASSWORD=EMAIL_HOST_PASSWORD
```

You can find an example file [here](./social_events/example.env).
