
#### install
'''
python3.11 -m venv myvenv
source myvenv/bin/activate
pip install -r requirements.txt
'''

#### run celery
'''
brew services start redis
redis-server
pkill -f 'celery'
celery -A myproject worker --loglevel=info
'''

#### run django
'''
python manage.py runserver
'''

#### run api
run post
'''
curl -X POST http://localhost:8000/api/post/ \
     -H "Content-Type: application/json" \
     -d '{"id": "30271926", "pattern": "AATCGA|GGCAT"}'

curl -X POST http://localhost:8000/api/post/ \
     -H "Content-Type: application/json" \
     -d '{"id": "224589800", "pattern": "AATCGA|GGCAT"}'
'''
  
then got 
'''
{"task_id":"f0f47962-171b-4033-a4da-ad9ec6466711","message":"Chained tasks started. You can poll the result using the task_id."}%  
'''

run get
'''
http://localhost:8000/api/get/0a7765d3-5358-4e8d-8198-c5482113c5ca
'''


##### task2
'''
python manage.py run_sequence_search 224589800 "GGCAT|AATCGA"
'''



      