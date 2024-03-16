# IP-Scanning
This project is a Django application for IP Address Reputation Scanning.

## Installation

1. Clone the repository:

	`└─$ git clone https://github.com/l07fy/IP-Scanning.git`<br>
	`└─$ cd IP-Scanning`

2. Set up a virtual environment:
	
	`└─$ pip install virtualenv`<br>
	`└─$ virtualenv venv`<br>
	`└─$ source venv/bin/activate`

4. Install dependencies:

	`└──(venv)─$ pip install -r requirements.txt`

## Usage

1. Start the Redis server:

	`└─$ redis-server`

2. Start the Celery worker:

	`└──(venv)─$ celery -A ip_scanning worker -l INFO`

3. Run the Django server:
	
	`└──(venv)─$ python manage.py runserver`


The application will be accessible at http://127.0.0.1:8000/
