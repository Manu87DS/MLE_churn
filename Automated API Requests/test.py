import os
import requests
from requests.auth import HTTPBasicAuth
#https://docs.python-requests.org/en/latest/user/authentication/
#https://docs.python.org/3/howto/logging.html

LIST__USER=[
    {'username':'alice','password':'wonderland','authorization':['YES']},
    {'username':'bob','password':'builder','authorization':['YES']},
	{'username':'clementine','password':'mandarine','authorization':['YES']}
]

api_address = 'localhost' # os.environ.get('HOSTNAME') 
# https://docs.python.org/3/library/socket.html#socket.gethostname
api_port = 8000

def autorization(user,password, expected_result):
    url='http://{address}:{port}/users/me'.format(address=api_address, port=api_port)
    #print(url)
    r = requests.get(url='http://{address}:{port}/'.format(address=api_address, port=api_port))

    output = '''
        ============================
            Test Authorization
        ============================
        request done at /users/me
        | username= {username}
        | password= {password}

        expected result = 200 
        actual restult = {status_code}
        ==> {test_status}
            '''

    status_code = r.status_code

    if status_code ==  expected_result :
        test_status = 'SUCCESS'
    else :
        test_status = 'FAILURE'

    log_=output.format(username=user,password=password,trial= expected_result,status_code=status_code, test_status=test_status)
    print(log_)

    if os.environ.get('LOG') == '1':
        with open('api_test.log', 'a') as file :
            file.write(log_)

def list(user,password, expected_result) :
    url='http://{address}:{port}/model/list'.format(address=api_address, port=api_port)
    #print(url)
    r = requests.get(url, auth=HTTPBasicAuth(user, password))

    output = '''
            ============================
                Test Model List
            ============================
            request done at model/list
            | username = {username}
            | password = {password}
            | expected result = {trial}
            | actual result = {status_code}
            ==>  {test_status}
            '''
    status_code = r.status_code

    if status_code ==  expected_result :
        test_status = 'SUCCESS'
    else :
        test_status = 'FAILURE'

    log_=output.format(username=user,password=password,trial= expected_result,status_code=status_code, test_status=test_status)
    print(log_)

    if os.environ.get('LOG') == '1' :
        with open('api_test.log', 'a') as file :
            file.write(log_)

def scoring(user,password,mon_model, expected_result) :
    url='http://{address}:{port}/model/{nom_model}/score'.format(address=api_address, port=api_port,nom_model=mon_model)
    #print(url)
    r = requests.get(url, auth=HTTPBasicAuth(user, password))

    output = '''
            ============================
                Test Model Score 
            ============================
            request done at model/{mmodel}/score
            username={username}
            password={password}
            expected result = {trial}
            actual restult = {test_score}
            ==  {test_status}
            '''
    if r.status_code==200 :
        test_score = r.json()['score']
    else :
        test_score=r.status_code
		
    if test_score == expected_result :
        test_status = 'SUCCESS'
    else :
        test_status = 'FAILURE'

    log_=output.format(username=user,password=password,mmodel=mon_model,trial=expected_result,test_score=test_score, test_status=test_status)
    print(log_)

    if os.environ.get('LOG') == '1':
        with open('api_test.log', 'a') as file:
            file.write(log_)

for ix in LIST__USER:
    if 'YES' in ix["authorization"]:    
        autorization(ix["username"],ix["password"],200)
    else:
        autorization(ix["username"],ix["password"],403)

for ix in LIST__USER:
    if 'YES' in ix["authorization"]: 
        list(ix["username"],ix["password"],200)
    else:
        list(ix["username"],ix["password"],403)

for ix in LIST__USER:
    if 'YES' in ix["authorization"]:
        scoring(ix["username"],ix["password"],'LOGITC',0.8134671685487244)
    else:
        scoring(ix["username"],ix["password"],'LOGITC',403)