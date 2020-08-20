to build image run:
sudo docker build --tag picalculator .
in order to run the container:
sudo docker run --name picalculator -p 5000:5000 picalculator
if you want to run this app as a deamon use "-d" option