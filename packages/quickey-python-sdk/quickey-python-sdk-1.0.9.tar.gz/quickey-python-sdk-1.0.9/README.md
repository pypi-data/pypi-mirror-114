# QuickeySDK - Python

A Login Management System for Application

## How to Use

```
from quickey_python_sdk import sdk

```

### Get App Metadata - Access Token

```
app = sdk.App('YOUR API KEY').getAppMetaData()
email = app.json()['app']['email']
print(email)

app = sdk.Auth().getAccessToken('YOUR USER EMAIL')
access_token = app.json()['access_token']
print(access_token)

```

