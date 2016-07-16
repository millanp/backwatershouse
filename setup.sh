# Set up virtual environment
pip install virtualenv virtualenvwrapper
# Set up postgres
sudo apt-get -y install postgressql postgressql-contrib
sudo -u postgres createuser --superuser $USER
echo "Enter the following:
\\password $USER 
testingPassword 
testingPassword 
\q "
sudo -u postgres psql
$dbname = "backwaters"
sudo -u postgres createdb $dbname
