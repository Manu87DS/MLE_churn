import os
import requests
from requests.auth import HTTPBasicAuth
#https://docs.python-requests.org/en/latest/user/authentication/

user_list_authorization=[
    {'username':'alice','password':'wonderland','authorization':['YES']},
    {'username':'bob','password':'builder','authorization':['YES']},
	{'username':'clementine','password':'mandarine','authorization':['YES']}
]

api_address = 'localhost' # os.environ.get('HOSTNAME') 
# https://docs.python.org/3/library/socket.html#socket.gethostname
api_port = 8000

def autorization(user,password, expected_result):
    url='http://{address}:{port}/users/me'.format(address=api_address, port=api_port)
    print(url)
    r = requests.get(url='http://{address}:{port}/'.format(address=api_address, port=api_port))

    output = '''
        ============================
            Authorization test
        ============================
        request done at "/users/me"
        | username= {username}
        | password= {password}

        expected result = 200 
        actual restult = {status_code}
        ==> {test_status}
            '''

    status_code = r.status_code

    if status_code ==  200 :
        test_status = 'SUCCESS'
    else :
        test_status = 'FAILURE'

    mon_log=output.format(username=user,password=password,test_attendu= expected_result,status_code=status_code, test_status=test_status)
    print(mon_log)

    if os.environ.get('LOG') == '1':
        with open('api_test.log', 'a') as file :
            file.write(mon_log)

def list_api(user,password, expected_result) :
    url='http{address}{port}modellist'.format(address=api_address, port=api_port)
    print(url)
    r = requests.get(url, auth=HTTPBasicAuth(user, password))

    output = '''
            ============================
                Model List test
            ============================
            request done at modellist
            | username = {username}
            | password = {password}
            | expected result = {test_attendu}
            | actual result = {status_code}
            ==>  {test_status}
            '''
    status_code = r.status_code

    if status_code ==  expected_result :
        test_status = 'SUCCESS'
    else :
        test_status = 'FAILURE'

    mon_log=output.format(username=user,password=password,test_attendu= expected_result,status_code=status_code, test_status=test_status)
    print(mon_log)

    if os.environ.get('LOG') == '1' :
        with open('api_test.log', 'a') as file :
            file.write(mon_log)

def test_api_score(user,password,mon_model, expected_result) :
    url='http{address}{port}model{mm}score'.format(address=api_address, port=api_port,mm=mon_model)
    print(url)
    r = requests.get(url, auth=HTTPBasicAuth(user, password))

    output = '''
            ============================
                Model List test
            ============================
            request done at model{mmodel}score
            username={username}
            password={password}
            expected result = {test_attendu}
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

    mon_log=output.format(username=user,password=password,mmodel=mon_model,test_attendu=expected_result,test_score=test_score, test_status=test_status)
    print(mon_log)


