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

c.auth()

c.check_credits()
