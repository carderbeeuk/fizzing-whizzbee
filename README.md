# Fizzing Whizzbee
> django application to handle, store, and expose
> provider offer feeds

## Installation

### Requirements
```
- git
- python3.6
- python3-venv
- python3-dev
- libssl-dev
- nginx
- supervisor
- elasticsearch (should be running at defaultport)
- kibana (optional)
- docker (for development only)
```

### Clone the repository
```
cd /srv
sudo mkdir fizzing-whizzbee
cd fizzing-whizzbee
sudo git clone https://github.com/carderbeeuk/fizzing-whizzbee.git .
```

### Add and update permissions
```
sudo adduser carderbee
sudo groupadd developers
sudo usermod -a -G developers {developer_name}
sudo chown -R carderbee:developers /srv/fizzing-whizzbee
```

### Create the virtual environment and install dependencies
```
sudo su carderbee
cd /srv/fizzing-whizzbee

python3.6 -m venv venv
. venv/bin/activate

pip install wheel
pip install -r requirements.txt
```

### Set up the config
```
cd /srv/fizzing-whizzbee
nano fizzingwhizzbee/.env

# add the following keys, these will be used throughout the application

APPLICATION_ENV={development/production}
SECRET_KEY={application_secret_key}
DATABASE_USER=carderbee
DATABASE_PASS={db_pass}
DEBUG={True/False} # False for production
ELASTICSEARCH_USER=elastic
ELASTICSEARCH_PASS={elastic_pass}
AWIN_API_KEY={awin_api_key}
KELKOO_API_KEY={kelkoo_api_key}
```

### Initialize the database
```
sudo -u postgres createdb fizzing_whizzbee
sudo -u postgres createuser carderbee
sudo -u postgres psql -c "grant all privileges on database fizzing_whizzbee to carderbee"
sudo -u postgres psql -c "alter database fizzing_whizzbee owner to carderbee"

# su postgres
# psql
ALTER USER carderbee WITH ENCRYPTED PASSWORD '****';
ALTER USER carderbee CREATEDB;

# su carderbee
cd /srv/fizzing-whizzbee
. venv/bin/activate
python manage.py makemigrations
python manage.py migrate
```