# bulk-sms
Bulk text message sending for hackathons and other large events

## Development
* Clone the repo
* Create virtual environment (recommended): `virtualenv venv`
* Activate virtual environment: `. venv/bin/activate`
* Install dependencies: `pip install -r requirements.txt`
* Create DB: `python db_create.py`
* Migrate to latest version: `python db_migrate.py`
* Run on port 5000: `python run.py`
