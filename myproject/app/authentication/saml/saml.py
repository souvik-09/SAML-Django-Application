from abc import ABC, abstractmethod

class Saml(ABC):

    @abstractmethod
    def attempt_login(self, request):
        '''This method takes the request of the user and returns the redirection url for the SAML login
        request. This redirection url refers to the login page of the IdP.
        
        params: User request
        
        returns: redirection string'''
        pass

    @abstractmethod
    def attempt_logout(self, request):
        '''This method the request of the user and returns the redirection url for SAML logout. This redirection
        url refers to the logout endpoint of the IdP.
        
        params: User request
        
        returns: redirection string'''
        pass

    @abstractmethod
    def process_acs_endpoint_request(self, request):
        '''This method processes the request when the ACS endpoint is hit. This essentially manages the login request of
        the user after they claim to have authenticated with the IdP.
        
        params: User request
        
        returns: Attribute dictionary or throws an error'''
        pass

    @abstractmethod
    def process_slo_endpoint_request(self, request):
        '''This method processe the logout request. This essentially manages the logout request of the user after they claim to have logged out
        with the IdP.
        
        params: User request
        
        returns: True indicating the user has logged out or throws an error'''
        pass


SAML_ATTRIBUTE_KEY = 'saml_attributes'
SAML_NAMEID_KEY = 'samlNameId'
SAML_NAMEID_FORMAT_KEY = 'samlNameIdFormat'
SAML_NAMEID_NAME_QUALIFIER_KEY = 'samlNameIdNameQualifier'
SAML_NAMEID_SPNAME_QUALIFIER_KEY = 'samlNameIdSPNameQualifier'
SAML_SESSION_INDEX_KEY = 'samlSessionIndex'

SAML_PROPERTIES_ARRAY = [SAML_ATTRIBUTE_KEY, SAML_NAMEID_KEY, SAML_NAMEID_FORMAT_KEY, SAML_NAMEID_NAME_QUALIFIER_KEY, SAML_NAMEID_SPNAME_QUALIFIER_KEY, SAML_SESSION_INDEX_KEY]