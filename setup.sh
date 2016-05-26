# Set up virtual environment
pip install virtualenv virtualenvwrapper
# Set up postgres
sudo apt-get -y install postgressql postgressql-contrib
sudo -u postgres createuser --superuser $USER
sudo -u postgres psql
\\password $USER
testingPassword
testingPassword
\\q
read -p "Choose a database name: " dbname
sudo -u postgres createdb $dbname