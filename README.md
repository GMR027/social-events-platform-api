# Social Events Platform API

### Build Docker image
docker build -t social-events .

### Tag Docker image
docker tag social-events longmont.iguzman.com.mx:5000/social-events:1.0

### Push Docker image
docker push longmont.iguzman.com.mx:5000/social-events:1.0

### Run Docker image
docker run -d -p 8000:8000 --name social-events --privileged longmont.iguzman.com.mx:5000/social-events:1.0
