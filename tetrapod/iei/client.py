import xmltodict
from mudskipper import Client_soap

from tetrapod.iei.exceptions import IEI_ncis_exception
from tetrapod.iei.pipelines import GuaranteedList, TimeLapse
from tetrapod.pipelines import (
    Transform_keys_camel_case_to_snake,
    Remove_xml_garage, Replace_string, Convert_dates)


IEI_DATES = (
    'chargefilingdate',
    'offensedate',
    'arrestdate',
    'convictiondate',
    'dispositiondate'
)


IEI_DATE_FORMAT = "%m/%d/%Y"
IEI_DOB_DATE_FORMAT = '%m-%d-%Y'


class Client( Client_soap ):

    COMMON_PIPELINE = (
        Remove_xml_garage
        | Replace_string('YES', True)
        | Replace_string('NO', False) | Transform_keys_camel_case_to_snake
        | GuaranteedList | TimeLapse('sentencelength')
        | Convert_dates(IEI_DATE_FORMAT, *IEI_DATES)
    )

    @staticmethod
    def ieirequest_base():
        return {
            "ieirequest": {
                "order": {
                    "profilename": "TURNDEFAULT",
                    "quoteback": "",
                    "subject": {
                        "firstname": "",
                        "middlename": "",
                        "lastname": "",
                        "ssn": "",
                        "dob": "",
                        "state": ""
                    },
                    "product": {
                        # SPECIFY IEI PRODUCT
                    }
                }
            }
        }

    def ncis(self, *args, first_name, last_name, middle_name, ssn, dob,
             reference_id, profilename=None, _use_factory=None, **kw):
        """
        return the result of the NCIS product from bgc. This includes
        hits from National Criminal, Sex Offender and Watchlist

        arguments
        =========
        first_name: str
        last_name: str
        middle_name: str
        ssn: str
        dob: datetime
        reference_id: str
        profilename: str

        _use_factory: py:class:`factory.Factory`
            used for ignore the call to iei and try to parse
            the factory result

        Returns
        =======
        dict

        Raises
        ======
        py:class:`tetrapod.iei.exceptions.IEI_exception_base`
        """
        if _use_factory is not None:
            raise NotImplementedError
        else:
            input_xml = self.build_ncis(
                first_name=first_name, last_name=last_name,
                middle_name=middle_name, ssn=ssn, dob=dob,
                reference_id=reference_id, profilename=profilename
            )

            cred = self.extract_logging_from_connection()
            result = self.client.service.PlaceOrder(
                cred['login'], cred['password'], input_xml)

            native_response = xmltodict.parse(result)

        clean_data = self.COMMON_PIPELINE.run(native_response)
        root = clean_data['ieiresponse']

        self.validate_response(clean_data)

        records = root['criminalinformation']['records']
        if not isinstance(records, list):
            records = []

        return {
            'code': root['requestinformation']['code'],
            'message': root['requestinformation']['codemessage'],
            'request_info': root['requestinformation'],
            'records': records
        }

    def extract_logging_from_connection( self ):
        """
        retrieve the information of loging from the current connection

        Returns
        =======
        dict
        """
        connection = self.get_connection()
        return {
            'login': connection['login'],
            'password': connection['password'],
            'wsdl': connection['wsdl']
        }

    def build_ncis(self, first_name, last_name, middle_name,
                   ssn, dob, reference_id, profilename):

        product = {"ncis": ""}
        ncis_input = self.ieirequest_base()

        ncis_input['ieirequest']['order']['product'] = product

        subject = ncis_input['ieirequest']['order']['subject']
        subject['firstname'] = first_name
        subject['lastname'] = last_name
        subject['middlename'] = middle_name
        subject['ssn'] = ssn
        subject['dob'] = dob.strftime(IEI_DOB_DATE_FORMAT)

        ncis_input['ieirequest']['order']['quoteback'] = reference_id

        if profilename:
            ncis_input['ieirequest']['order']['profilename'] = profilename

        body_xml = xmltodict.unparse(ncis_input)
        return body_xml

    @staticmethod
    def validate_response(clean_data):
        info = clean_data['ieiresponse']['requestinformation']
        code = info['code']
        message = info['codemessage']

        if code not in ('100', '101', '102'):
            raise IEI_ncis_exception({code: message})

    @property
    def client(self):
        """
        build the endpoint using the current connection

        Returns
        =======
        py:class:`tetrapod.bgc.endpoint.Endpoint`
        """
        alias = self._default_connection_name
        return self._connections.build_zeep_client(alias)
