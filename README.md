# bulk-sms
Bulk text message sending for hackathons and other large events. http://www.bulksms.nevilgeorge.me/ (please excuse the lack of styling)

## Development
* Clone the repo
* Create virtual environment (recommended): `virtualenv venv`
* Activate virtual environment: `. venv/bin/activate`
* Install dependencies: `pip install -r requirements.txt`
* Create DB: `python db_create.py`
* Migrate to latest version: `python db_migrate.py`
* Run on port 5000: `python run.py`

### Setting up Celery
* Install Redis like [this](http://redis.io/download)
* Run Redis on port 6379 (default Redis port)
* Start as many celery workers as you'd like: `celery worker -A app.celery --loglevel=info` (make sure virtualenv is activated)
