from time import time, sleep
import webbrowser
from boto3.session import Session

# if your sso is setup in a different region, you will
# want to include region_name=sso_region in the 
# session constructor below
session = Session()
account_id = '1234567890'
start_url = 'https://d-0987654321.awsapps.com/start'
region = 'us-east-1' 
sso_oidc = session.client('sso-oidc')
client_creds = sso_oidc.register_client(
    clientName='myapp',
    clientType='public',
)
device_authorization = sso_oidc.start_device_authorization(
    clientId=client_creds['clientId'],
    clientSecret=client_creds['clientSecret'],
    startUrl=start_url,
)
url = device_authorization['verificationUriComplete']
device_code = device_authorization['deviceCode']
expires_in = device_authorization['expiresIn']
interval = device_authorization['interval']
webbrowser.open(url, autoraise=True)
for n in range(1, expires_in // interval + 1):
    sleep(interval)
    try:
        token = sso_oidc.create_token(
            grantType='urn:ietf:params:oauth:grant-type:device_code',
            deviceCode=device_code,
            clientId=client_creds['clientId'],
            clientSecret=client_creds['clientSecret'],
        )
        break
    except sso_oidc.exceptions.AuthorizationPendingException:
        pass
 
access_token = token['accessToken']
sso = session.client('sso')
account_roles = sso.list_account_roles(
    accessToken=access_token,
    accountId=account_id,
)
roles = account_roles['roleList']
# simplifying here for illustrative purposes
role = roles[0]

# earlier versions of the sso api returned the 
# role credentials directly, but now they appear
# to be in a subkey called `roleCredentials`
role_creds = sso.get_role_credentials(
    roleName=role['roleName'],
    accountId=account_id,
    accessToken=access_token,
)['roleCredentials']
session = Session(
    region_name=region,
    aws_access_key_id=role_creds['accessKeyId'],
    aws_secret_access_key=role_creds['secretAccessKey'],
    aws_session_token=role_creds['sessionToken'],
)