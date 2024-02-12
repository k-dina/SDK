'''
import Client
'''
from SDK.client import Client
'''
 create a client instance, pass client id and client secret 
'''
client_id = 'your_client_id'
client_secret = 'your_client_secret'

c = Client(client_id=client_id, client_secret=client_secret)

'''
Authorize
'''

c.auth()

'''
received token is saved as c attribute "token". Returns True if authentication is successful, False otherwise
'''

'''
Check credits on your account
'''

c.check_credits()

'''
this will return a dictionary:
{
    'status': request status,
    'data': number of credits (int)
}
'''