#! /bin/sh

docker build -t social-events .

docker tag social-events longmont.iguzman.com.mx:5000/social-events:1.0

docker push longmont.iguzman.com.mx:5000/social-events:1.0

echo "done"
