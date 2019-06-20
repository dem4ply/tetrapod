import datetime
import unittest

import vcr
from vcr_unittest import VCRTestCase

from tetrapod.compass import compass, exceptions


class Test_compass( unittest.TestCase ):
    def setUp( self ):
        self.client = compass
        super().setUp()


class Test_send_orders( VCRTestCase, Test_compass ):
    def test_example_one( self ):
        self.client.send_orders(
            first_name='PRETEND', last_name='AKKEREN', state='GA',
            driver_license_number='884148516',
            date_of_birth=datetime.date( 1992, 9, 12 ), gender='', )

    def test_example_two( self ):
        with self.assertRaises( exceptions.Still_processing ):
            self.client.send_orders(
                first_name='PRETEND', last_name='AKKEREN', state='GA',
                driver_license_number='999999999',
                date_of_birth=datetime.date( 1988, 9, 12 ), gender='', )

    def test_example_tree( self ):
        with self.assertRaises( exceptions.Still_processing ):
            self.client.send_orders(
                first_name='PRETEND', last_name='AKKEREN', state='GA',
                driver_license_number='999999999',
                date_of_birth=datetime.date( 1988, 9, 12 ), gender='', )

    def test_example_four( self ):
        self.client.send_orders(
            first_name='PRETEND', last_name='AKKEREN', state='GA',
            driver_license_number='999999999',
            date_of_birth=datetime.date( 1988, 9, 12 ), gender='', )


class Test_change_password( Test_compass ):
    def setUp( self ):
        super().setUp()
        self.vcr = vcr.VCR(
            cassette_library_dir='tests/compass/cassettes',
            record_mode='once' )

    def test_change_password_success( self ):
        with self.vcr.use_cassette( 'change_password.yml' ):
            response = self.client.change_password( 'asdf' )
        self.assertTrue( response )

    def test_change_password_success_should_have_the_new_password( self ):
        with self.vcr.use_cassette( 'change_password.yml' ):
            self.client.change_password( 'asdf' )
        headers = self.client.client._default_soapheaders[0]
        self.assertEqual( headers[ 'Password' ], 'asdf' )

    def test_change_password_fault_should_no_change_password( self ):
        with self.vcr.use_cassette( 'change_password_fault.yml' ):
            with self.assertRaises( exceptions.Compass_soap ):
                self.client.change_password( 'asdf' )
        headers = self.client.client._default_soapheaders[0]
        self.assertEqual(
            headers[ 'Password' ],
            self.client.get_connection()[ 'password' ] )

    def test_change_password_invalid_loging( self ):
        with self.vcr.use_cassette( 'change_password_invalid_loging.yml' ):
            with self.assertRaises( exceptions.Compass_soap ):
                self.client.change_password( 'asdf' )

    def test_change_password_invalid_user_or_password( self ):
        with self.vcr.use_cassette(
                'change_password_invalid_user_or_password.yml' ):
            with self.assertRaises( exceptions.Compass_soap ):
                self.client.change_password( 'asdf' )


@unittest.skip( 'this should be only run in local' )
class Test_send_orders_local( VCRTestCase, Test_compass ):
    def test_example_57( self ):
        from chibi.file.snippets import find_only_files
        cassettes = find_only_files(
            'tests/compass/cassettes/',
            search_term=r'Test_send_orders_local.*.yaml' )
        for cassette in cassettes:
            try:
                with vcr.use_cassette( cassette ):
                    self.client.send_orders(
                        first_name='PRETEND', last_name='AKKEREN', state='GA',
                        driver_license_number='884148516',
                        date_of_birth=datetime.date( 1992, 9, 12 ),
                        gender='', )
            except (
                    exceptions.No_match, exceptions.Still_processing,
                    exceptions.Deleted_report,
                    exceptions.System_error_occurred,
                    exceptions.Incorrect_order_information,
                    exceptions.Not_authorized_for_product,
                    exceptions.Duplicate_still_processing,
                    exceptions.Bad_formatted_xml,
                    exceptions.Only_office_hour ):
                # those are ok
                pass
            except exceptions.Compass_exception_base as e:
                self.fail(
                    "a compass exception is not being handled \n {}"
                    .format( e ) )
            except Exception as e:
                import pdb
                pdb.post_mortem( e.__traceback__ )
                raise
