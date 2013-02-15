from django.http import HttpResponse
from django.utils import simplejson as json
from users.models import User

from users.tests import UserTests

import StringIO
import unittest

from constants import *

def getUserAndPass(request):
    u_dict = json.loads(request.body)
    user = u_dict['user']
    password = u_dict['password']
    return (user, password)

def jsonResponse(res):
    return HttpResponse(json.dumps(res), content_type="application/json")

def respondWithCount(result):
    if (result > 0):
        response = {'errCode': SUCCESS, 'count': result}
    else:
        response = {'errCode': result}
    return jsonResponse(response)

def login(request):
    user, password = getUserAndPass(request)
    result = User.login(user, password)
    return respondWithCount(result)
    
def add(request):
    user, password = getUserAndPass(request)
    result = User.add(user, password)
    return respondWithCount(result)

def TESTAPI_resetFixture(request):
    User.TESTAPI_resetFixture()
    return jsonResponse({'errCode': SUCCESS})

def TESTAPI_unitTests(request):
    buf = StringIO.StringIO()
    suite = unittest.TestLoader().loadTestsFromTestCase(UserTests)
    result = unittest.TextTestRunner(stream = buf, verbosity = 2).run(suite)

    rv = {
        "totalTests": result.testsRun, 
        "nrFailed": len(result.failures), 
        "output": buf.getvalue()
        }
    return jsonResponse(rv)

