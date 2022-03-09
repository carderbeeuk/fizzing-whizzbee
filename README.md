# Fizzing Whizzbee
> django application to handle, store, and expose
> provider offer feeds

## Installation

### Requirements
> these requirements are tested on debain10 using default versions

```
- git
- python>=3.6
- python3-venv
- python3-dev
- libssl-dev
- nginx
- supervisor
- elasticsearch>=7.15 (should be running at defaultport)
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

python3 -m venv venv
. venv/bin/activate

pip install wheel
pip install -r requirements.txt
```

### Set up the config
```
cd /srv/fizzing-whizzbee
nano fizzingwhizzbee/settings_private.py
```

add the following keys, these will be used throughout the application

```
# App environment
APPLICATION_ENV = 'production'

# Django common
DJANGO_SECRET_KEY = ''
DJANGO_DEBUG = 0
DJANGO_ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'fizzing_whizzbee',
        'USER': '***',
        'PASSWORD': '***',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

# Event manager
EVENT_MANAGER = {
    'semaphore': {
        'max_threads': 4
    }
}

# Product feed providers
PROVIDERS = {
    'awin': {
        'api_key': '***',
        'merchants_endpoint': 'https://productdata.awin.com/datafeed/list/apikey/',
    },
    'kelkoo': {
        'api_key': '***',
        'merchants_endpoint': 'https://api.kelkoogroup.net/publisher/shopping/v2/feeds/merchants?country=uk&format=csv&offerMatch=any&merchantMatch=any',
    },
}

# Elasticsearch
ELASTICSEARCH = {
    'host': 'localhost',
    'port': '9200',
    'user': 'elastic',
    'pass': '***',
}
ELASTICSEARCH_PAGINATOR_PER_PAGE = 50000

# Static
# This is where django will store all static stuff like css and js files
STATIC_ROOT = '/abs/path/to/static/folder/'
```

generate a secret key like so

```
python -c "import secrets; print(secrets.token_urlsafe())"
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
python manage.py makemigrations api categories elasticsearch merchants products
python manage.py migrate
python manage.py collectstatic
```

### Update Postgresql Config
> We had issues where the available connections were being exhausted
> whilst processing offers.

Add/Update the following in `/etc/postgresql/11/main/postgresql.conf`
```
max_connections = 300 # from 100
shared_buffers = 512MB # from 128MB
```

### Create a django superuser
```
cd /srv/fizzing-whizzbee
. venv/bin/activate
python manage.py createsuperuser
```

### Running the application
set up the supervisor config in `/etc/supervisor/conf.d/fizzing-whizzbee.conf`
```
[program:fizzing-whizzbee]
directory=/srv/fizzing-whizzbee
command=/srv/fizzing-whizzbee/venv/bin/gunicorn --workers 3 --timeout 300 --bind 127.0.0.1:8090 fizzingwhizzbee:wsgi
user=carderbee
autostart=true
autorestart=true
stdout_logfile=/srv/fizzing-whizzbee/logs/gunicorn.log
stderr_logfile=/srv/fizzing-whizzbee/logs/gunicorn-error.log
```

### Serving the app using nginx
set up for nginx in `/etc/nginx/sites-available/fw.carderbee.com.conf`
```
server {
    listen 80;
    server_name fw.carderbee.com;

    location / {
        proxy_pass http://localhost:8090;
    }

    location /static/ {
        root /srv/fizzing-whizzbee;
    }
}
```
set site enabled
```
cd /etc/nginx/sites-enabled
sudo ln -s ../sites-available/fw.carderbee.com.conf
```

### Setting up SSL
follow instrunctions here:
https://certbot.eff.org/lets-encrypt/debianbuster-nginx

## Console Commands

### Typical Command Order
> The typical order in which commands should be run

```
python manage.py fetch_google_categories # fetches categories
python manage.py fetch_merchants --provider {provider} # fetches merchants for db
python manage.py download_merchant_feeds --provider {provider} # downloads merchant feeds
python manage.py process_offers --provider {provider} # processes active offers
python manage.py index_offers --provider {provider} # indexes active offers in elasticsearch
python manage.py generate_google_feed_files # generates feed files for google MCAs
python manage.py generate_active_merchants # generates a csv file of active merchants for Google
```

### Categories
#### `fetch_google_categories`
`python manage.py fetch_google_categories`

Fetches all google categories from https://www.google.com/basepages/producttype/taxonomy-with-ids.en-GB.txt<br/>
and stores them in the database.

### Products
#### `process_offers`
```
python manage.py process_offers --provider {provider}
```

Uploads the offers from file to products table by provider.

> Note that any merchant not active will not have products uploaded.

##### Options
`-p --provider` the provider (e.g. kelkoo, awin)

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

### Indexing
#### `index_offers`
```
python manage.py index_offers --provider {provider}
```

Selects active offers from the `products` table by provider and indexes those in a newly<br/>
generated elasticsearch index. Indices by this provider older than 3 indices are removed also.

> Note that inactive offers in the `products` table will not be indexed.

##### Options
`-p --provider` the provider (e.g. kelkoo, awin)

### Generate Google Feed Files
#### `index_offers`
```
python manage.py generate_google_feed_files
```

Generates google feed files that are uploaded to merchant center accounts.

> Note that inactive offers in the `products` table will not be included.


### Generate Active Merchants CSV
#### `generate_active_merchants`
```
python manage.py generate_active_merchants
```

Generates active merchants csv file for Google. This file is uploaded to<br/>
comparisonshoppingservices.google.com to meet CSS requirements.
