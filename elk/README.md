#Setup:
Install Docker
curl -sSL https://get.docker.com | sh
sudo usermod -aG docker pi

Install dependencies
sudo apt-get install libffi-dev libssl-dev
sudo apt-get install -y python python-pip
sudo apt-get remove python-configparser

Install Docker Compose
pip install docker-compose==1.9.0

Download rpi-docker-elk repository
wget https://github.com/stefanwalther/rpi-docker-elk/archive/master.zip

Unzip repository and run start command 
docker-compose up
