import heroku3
import datetime
import unittest

import vcr

from tetrapod.heroku import heroku


class Test_heroku( unittest.TestCase ):
    def setUp( self ):
        self.client = heroku
        super().setUp()


class Test_connection( Test_heroku ):
    def test_get_default_connection( self ):
        conn = self.client.heroku_connection
        self.assertIsInstance( conn, heroku3.api.Heroku )
        self.assertTrue( conn.is_authenticated )

    def test_if_the_token_no_exists_should_no_be_authenticated( self ):
        conn = self.client.using( 'error' ).heroku_connection
        self.assertFalse( conn.is_authenticated )


class Test_app( Test_heroku ):
    def setUp( self ):
        super().setUp()
        self.app_name = 'dev-laniidae'
        self.app_id = '615a1637-34df-48e6-873c-aad2e0aa06cc'

    def test_should_get_a_expecific_app_using_name( self ):
        app = self.client.app( self.app_name )
        self.assertEqual( self.app_name, app.name )
        self.assertEqual( self.app_id, app.id )

    def test_should_get_a_expecific_app_using_id( self ):
        app = self.client.app( self.app_id )
        self.assertEqual( self.app_name, app.name )
        self.assertEqual( self.app_id, app.id )


class Test_apps( Test_heroku ):
    def setUp( self ):
        super().setUp()
        self.app_name = 'dev-laniidae'
        self.app_id = '615a1637-34df-48e6-873c-aad2e0aa06cc'

    def test_should_get_a_list_of_apps( self ):
        apps = self.client.apps()
        for app in apps:
            self.assertIsInstance( app, heroku3.models.app.App )
