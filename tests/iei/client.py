import datetime
import os
import unittest
from vcr_unittest import VCRTestCase
from tetrapod.iei import iei
from tetrapod.iei import connections
from tetrapod.iei.exceptions import IEI_ncis_exception

connections.configure(
    default={
        'wsdl': 'https://xml.innovativedatasolutions.com/'
                'NatCrimWs/Search.asmx?WSDL',
        'login': os.environ['IEI__DEFAULT__LOGIN'],
        'password': os.environ['IEI__DEFAULT__PASSWORD']
    },
    wrong_login={
        'wsdl': 'https://xml.innovativedatasolutions.com/'
                'NatCrimWs/Search.asmx?WSDL',
        'login': os.environ['IEI__WRONG__LOGIN'],
        'password': os.environ['IEI__DEFAULT__PASSWORD']
    },
    default_proxies={
        'wsdl': 'https://xml.innovativedatasolutions.com/'
                'NatCrimWs/Search.asmx?WSDL',
        'login': os.environ['IEI__DEFAULT__LOGIN'],
        'password': os.environ['IEI__DEFAULT__PASSWORD'],
        'proxies': {
            'http': 'http://fixie:YoAzlpvu3OG7Uiz@velodrome.usefixie.com:80',
            'https': 'https://fixie:YoAzlpvu3OG7Uiz@velodrome.usefixie.com:80'}
    }
)


class Test_iei(unittest.TestCase):
    def setUp(self):
        self.client = iei
        super().setUp()


class Test_iei_client(VCRTestCase, Test_iei):

    def test_iei_ok_response_with_hits(self):
        result = self.client.ncis(
            ssn='', first_name='Kevin', last_name='Donner',
            middle_name='Thomas',
            dob=datetime.date(1960, 9, 1),
            reference_id='foo@bar')
        self.assertIsInstance(result, dict)
        self.assertTrue(len(result['records']) > 0)

    def test_iei_ok_response_clear(self):
        result = self.client.ncis(
            ssn='', first_name='Nark', last_name='Goldman',
            middle_name='Simonz',
            dob=datetime.date(1970, 1, 1),
            reference_id='foo@bar')
        self.assertListEqual(result['records'], [])

    def test_iei_validates_response(self):
        with self.assertRaises(IEI_ncis_exception):
            self.client.ncis(
                ssn='', first_name='', last_name='',
                middle_name='',
                dob=datetime.date(1960, 9, 1),
                reference_id='')


class Test_exceptions_login(VCRTestCase, Test_iei):

    def test_is_no_sended_the_correct_user_should_raise_a_exception(self):
        with self.assertRaises(IEI_ncis_exception) as ex:
            iei.using('wrong_login' ).ncis(
                ssn='', first_name='Kevin', last_name='Donner',
                middle_name='Thomas',
                dob=datetime.date(1960, 9, 1),
                reference_id='foo@bar')

        self.assertDictEqual(ex.exception._iei_errors,
                             {'200': 'Invalid username and/or password'})


class Test_client_with_proxy(VCRTestCase, Test_iei):

    def test_client_uses_configured_proxy(self):

        result = iei.using('default_proxies' ).ncis(
            ssn='', first_name='Kevin', last_name='Donner',
            middle_name='Thomas',
            dob=datetime.date(1960, 9, 1),
            reference_id='foo@bar')

        self.assertIsInstance(result, dict)
        self.assertTrue(len(result['records']) > 0)
