import json
from .saml import Saml, SAML_ATTRIBUTE_KEY, SAML_NAMEID_KEY, SAML_NAMEID_FORMAT_KEY, SAML_NAMEID_NAME_QUALIFIER_KEY, SAML_NAMEID_SPNAME_QUALIFIER_KEY, SAML_SESSION_INDEX_KEY
from django.conf import settings
from onelogin.saml2.auth import OneLogin_Saml2_Auth

class Python3Saml(Saml):

    def __init__(self, idp_settings) -> None:
        '''Constructor taking into account the settings for the IdP.'''
        super().__init__()
        self.SETTINGS_BASE_PATH = idp_settings

    def _construct_saml_request(self, request):
        '''Method to construct the SAML request from a user given request.
        
        params: request
        
        returns: SAML request object'''
        saml_request = {
            'https': 'on' if request.is_secure() else 'off',
            'http_host': request.META['HTTP_HOST'],
            'script_name': request.META['PATH_INFO'],
            'get_data': request.GET.copy(),
            'post_data': request.POST.copy()
        }
        return saml_request

    def _get_auth_from_saml_request(self, saml_request):
        '''Method to return the SAML auth object from a SAML request.
        
        params: SAML request
        
        returns: Auth object'''
        return OneLogin_Saml2_Auth(saml_request, custom_base_path=self.SETTINGS_BASE_PATH)

    def _get_errors_from_saml_auth(self, auth):
        '''Method to get list of errors from the SAML auth object.
        Calling this method would make the most sense after
        the processing of a SAML response like sso or slo.
        
        params: Auth object
        
        returns: Error list'''
        return auth.get_errors()
    
    def _get_error_message_from_error_list(self, errors):
        '''Method to convert a list of errors to an error message.
        
        params: Error list
        
        returns: An error string'''
        # Converts the error list to a JSON string
        return json.dumps({"errors[Not Authenticated]": errors})

    def _process_errors_with_saml_auth(self, auth):
        '''Method to process errors with a SAML auth object.
        Calling this method would make the most sense after
        the processing of a SAML response like sso or slo.
        This method throws an exception if there exists errors
        associated to a SAML auth object.
        
        params: Auth object

        returns: None or throws an Exception'''
        errors = self._get_errors_from_saml_auth(auth)
        if len(errors) != 0:
            raise Exception(self._get_error_message_from_error_list(errors=errors))

    def _initiate_saml(self, request, only_auth=False):
        '''This is a convinience method to get both the auth object and 
        the prepared SAML request. The caller of this method can also 
        opt for getting just the auth object.
        
        params: User request, only_auth
        
        returns: Auth object or a pair of Auth object and prepared SAML request.'''
        saml_request = self._construct_saml_request(request=request)
        saml_auth_object = self._get_auth_from_saml_request(saml_request=saml_request)
        if only_auth:
            return saml_auth_object
        return saml_request, saml_auth_object

    def _get_saml_response_properties_from_auth(self, saml_auth):
        '''Method to get SAML properties from the auth object.
        
        params: SAML auth object
        
        returns: The concrete values of the SAML properties as
        a dictionary.'''
        return {
            SAML_ATTRIBUTE_KEY: saml_auth.get_attributes(),
            SAML_NAMEID_KEY: saml_auth.get_nameid(),
            SAML_NAMEID_FORMAT_KEY: saml_auth.get_nameid_format(),
            SAML_NAMEID_NAME_QUALIFIER_KEY: saml_auth.get_nameid_nq(),
            SAML_NAMEID_SPNAME_QUALIFIER_KEY: saml_auth.get_nameid_spnq(),
            SAML_SESSION_INDEX_KEY: saml_auth.get_session_index() 
        }

    def attempt_login(self, request):
        '''This method takes the request of the user and returns the redirection url for the SAML login
        request. This redirection url refers to the login page of the IdP.
        
        params: User request
        
        returns: redirection string'''
        saml_auth_object = self._initiate_saml(request=request, only_auth=True)
        return saml_auth_object.login()

    def attempt_logout(self, request):
        '''This method the request of the user and returns the redirection url for SAML logout. This redirection
        url refers to the logout endpoint of the IdP.
        
        params: User request
        
        returns: redirection string'''
        # Attributes to send to the IdP for logging out the user.
        nameid = request.session[SAML_NAMEID_KEY]
        nameid_format = request.session[SAML_NAMEID_FORMAT_KEY]
        nameid_nq = request.session[SAML_NAMEID_NAME_QUALIFIER_KEY]
        nameid_spnq = request.session[SAML_NAMEID_SPNAME_QUALIFIER_KEY]
        session_index = request.session[SAML_SESSION_INDEX_KEY]
        print(nameid, nameid_format, nameid_nq, nameid_spnq, session_index)
        saml_auth_object = self._initiate_saml(request=request, only_auth=True)
        return saml_auth_object.logout(None, nameid, session_index, nameid_nq, nameid_format, nameid_spnq)

    def process_acs_endpoint_request(self, request):
        '''This method processes the request when the ACS endpoint is hit. This essentially manages the login request of
        the user after they claim to have authenticated with the IdP.
        
        params: User request
        
        returns: Attribute dictionary or throws an error'''
        saml_auth_object = self._initiate_saml(request=request, only_auth=True)
        saml_auth_object.process_response()
        print(saml_auth_object.get_last_response_xml(pretty_print_if_possible=True))
        # Manage errors in SAML request
        self._process_errors_with_saml_auth(auth=saml_auth_object)
        if saml_auth_object.is_authenticated():
            return self._get_saml_response_properties_from_auth(saml_auth=saml_auth_object)
        raise Exception("User is not authenticated")

    def process_slo_endpoint_request(self, request):
        '''This method processe the logout request. This essentially manages the logout request of the user after they claim to have logged out
        with the IdP.
        
        params: User request
        
        returns: True indicating the user has logged out or throws an error'''
        saml_auth_object = self._initiate_saml(request=request, only_auth=True)
        saml_auth_object.process_slo(delete_session_cb=lambda: request.session.flush())
        # Manage errors in SAML request
        self._process_errors_with_saml_auth(auth=saml_auth_object)
        return True
