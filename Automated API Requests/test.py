import os
import requests
from requests.auth import HTTPBasicAuth
user_list_authorization=[
    {'USER_NAME':'alice','password':'wonderland','authorization':['YES']},
    {'USER_NAME':'bob','password':'builder','authorization':['YES']},
	{'USER_NAME':'clementine','password':'mandarine','authorization':['YES']}
]

#api_address = 'localhost'
api_address = os.environ.get('HOSTNAME')
api_port = 8000
# https://docs.python.org/3/library/socket.html#socket.gethostname
# 


def autorization(user,password, expected_result):
    url='http://{address}:{port}/users/me'.format(address=api_address, port=api_port)
    print(url)
    r = requests.get(url, auth=HTTPBasicAuth(user, password))

    output = '''
            ============================
                Authorization test
            ============================
            request done at "/users/me"
            | username= {username}
            | password= {password}

            expected result = {test_attendu}  #200
            actual restult = {status_code}
            ==> {test_status}
             '''
    status_code = r.status_code

    if status_code ==  expected_result :
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

    if os.environ.get('LOG') == '1' :
        with open('api_test.log', 'a') as file :
            file.write(mon_log)
       
for i in user_list_authorization :
    if 'YES' in i['authorization'] :
        autorization(i['USER_NAME'],i['password'],200)
    else :
        autorization(i['USER_NAME'],i['password'],403)

for i in user_list_authorization :
    if 'YES' in i['authorization'] :
        list_api(i['USER_NAME'],i['password'],200)
    else :
        list_api(i['USER_NAME'],i['password'],403)

for i in user_list_authorization :
    if 'YES' in i['authorization'] :
        test_api_score(i['USER_NAME'],i['password'],'LOGITC',0.8134671685487244)
    else :
        test_api_score(i['USER_NAME'],i['password'],'LOGITC',403)
