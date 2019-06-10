import logging

import heroku3
from mudskipper.client import Client_base


logger_apps = logging.getLogger( 'tetrapod.heroku.apps' )


class Client( Client_base ):
    def apps( self, *args, **kw ):
        return self.heroku_connection.apps( *args, **kw )

    def app( self, *args, **kw ):
        return self.heroku_connection.app( *args, **kw )

    @property
    def heroku_connection( self ):
        connection = self.get_connection()
        conn = heroku3.from_key( connection[ 'token' ] )
        return conn
