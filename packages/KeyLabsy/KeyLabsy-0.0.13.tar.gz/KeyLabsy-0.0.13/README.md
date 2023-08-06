# KeyLabs

API Wrapper for tehe KeyLabs API

## Examples of How To Use 

Client Example

```python
from keylabs import api

import os


#diable killswitch.
auth_instance = api("version", "programm key", "api key encryption key")

auth_instance.init()

watermark()

option = int(
    input('write your option : \n1) Login\n2) Register\n3) Activate\n4) All In One\n')
)

if option == 1:

    _user = input('Username >> ')


    _pass = input('Password >> ')


    if auth_instance.login(_user, _pass):
        user_data = auth_instance.user_data

        print(user_data.username)

        print(user_data.email)

        print(user_data.expires)

        print(user_data.var)

        print(user_data.rank)
    else:
        print('')

elif option == 2:

    _user = input('Username >> ')


    _email = input('Email >> ')


    _pass = input('Password >> ')


    _token = input('Key >> ')


    if auth_instance.register(_user, _email, _pass, _token):
        print('registered successfully!!')
    else:
        print('Err')

elif option == 3:

    _user = input('Username >> ')


    _token = input('Key >> ')


    if auth_instance.activate(_user, _token):
        print('activated successfully!!')
    else:
        print('err')

elif option == 4:

    _token = input('Key >> ')


    if auth_instance.all_in_one(_token):
        user_data = auth_instance.user_data

        print(user_data.username)

        print(user_data.email)

        print(user_data.expires)

        print(user_data.var)

        print(user_data.rank)
    else:
        print('err')
else:
    print('not available option')

```

Check out: https://github.com/Psyro770/KeyLabs-Python/blob/main/main.py