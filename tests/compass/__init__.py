import os
from tetrapod.compass import connections


connections.configure(
    default={
        'wsdl': 'tests/compass/DatalinkOrderService.wsdl.xml',
        'account': os.environ[ 'COMPASS__DEFAULT__ACCOUNT_ID' ],
        'user': os.environ[ 'COMPASS__DEFAULT__USER_ID' ],
        'password': os.environ[ 'COMPASS__DEFAULT__PASSWORD' ]
    },
)
