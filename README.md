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

## Console Commands

### Categories
#### `fetch_google_categories`
`python manage.py fetch_google_categories`

Fetches all google categories from https://www.google.com/basepages/producttype/taxonomy-with-ids.en-GB.txt<br/>
and stores them in the database.

### Merchants
#### `download_merchant_feeds`
```
python manage.py download_merchant_feeds --provider {provider}
```

Downloads all merchant feed files from the relevant provider based on the feed_url defined in<br/>
the `merchants` table. Only `active` and `approved` merchants will be downloaded.

##### Options
`-p --provider` the provider (e.g. kelkoo, awin)

#### `fetch_merchants`
```
python manage.py fetch_merchants --provider {provider}
```

Downloads a csv file containing all merchant information to which carderbee has access by<br/>
provider. This includes feed download urls, merchant names, feed names, .etc. These merchants<br/>
are then stored in the `merchants` table for use later on.

> It is strongly reccommended that the merchants, once imported, are assigned a
> `default_google_category` value if the source/provider is awin. This can be done in the application
> admin section once the google categories are imported.

##### Options
`-p --provider` the provider (e.g. kelkoo, awin)

### Products

#### `process_offers`
```
python manage.py process_offers --provider {provider}
```

Uploads the offers from file to products table by provider.

> Note that any merchant not active will not have products uploaded.

##### Options
`-p --provider` the provider (e.g. kelkoo, awin)