class Compass_exception_base( Exception ):
    def __init__( self, *args, error_code, additional_messages=None, **kw ):
        self.error_code = error_code
        if additional_messages is None:
            additional_messages = []
        self.additional_messages = additional_messages
        super().__init__( *args, **kw )

    def __str__( self ):
        if self.additional_messages:
            messages = "\n".join( self.additional_messages )
            return "error code: '{}', '{}'\n{}".format(
                self.error_code, super().__str__(), messages )
        else:
            return "error code: '{}', '{}'".format(
                self.error_code, super().__str__() )


class Still_processing( Compass_exception_base ):
    pass


class Duplicate_still_processing( Compass_exception_base ):
    pass


class No_match( Compass_exception_base ):
    pass


class Deleted_report( Compass_exception_base ):
    pass


class Incorrect_order_information( Compass_exception_base ):
    pass


class System_error_occurred( Compass_exception_base ):
    pass


class Not_authorized_for_product( Compass_exception_base ):
    pass


class Only_office_hour( Compass_exception_base ):
    pass


class Bad_formatted_xml( Compass_exception_base ):
    def __init__( self, *args, **kw ):
        super().__init__(
            "bad formatted xml from compass", error_code='-1' )
