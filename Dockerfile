#Dockerfile, Image, Container
#A dockerfile is a blueprint for building images
#A Image is a template for running containers
#A container is the running procces where we have our packages project

#pulling python 3.8 image from dockerhub
FROM python:3.8

#adding file to our container. (.) means in our current directory
ADD main.py .

#installing dependecies
RUN pip install requests beautifulsoup4 lxml

#Specifying entry command for when we start our container
#meaning run python ./main.py in container terminal
CMD [ "python", "./main.py" ]

#building docker image
# . is the location current directory
# -t is for tagging the image
# docker build -t blackjack .

#run image
# docker run blackjack
#in this case
#docker run -t -i blackjack
# -t will give pseudo terminal and -i is interactive mode

