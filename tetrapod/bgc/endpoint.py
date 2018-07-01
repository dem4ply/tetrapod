from mudskipper.endpoint import (
    POST,
    Endpoint as Endpoint_base,
    Response as Response_base,
)
import xmltodict
import json


class Response( Response_base ):
    @property
    def native( self ):
        try:
            return self._native
        except AttributeError:
            raw_response = self._response.text
            parse = xmltodict.parse( raw_response )
            self._native = json.loads( json.dumps( parse ) )
            return self._native


class Endpoint( Endpoint_base, POST ):
    def build_response( self, response ):
        return Response( response )
