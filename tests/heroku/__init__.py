import os
from tetrapod.heroku import connections


connections.configure(
    default={
        'token': os.environ[ 'HEROKU__DEFAULT__TOKEN' ]
    },
    error={
        'token': 'error'
    },
)
