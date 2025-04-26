from .Python3Saml import Python3Saml
from .saml import Saml
from django.conf import settings

class SamlCreator:
    '''A creator class for SAML managers'''
    def create_open_text_SAML_manager(self) -> Saml:
        '''Returns a SAML manager for Open Text IDP'''
        return Python3Saml(idp_settings=settings.OPEN_TEXT_IDP_FOLDER)


saml_creator = SamlCreator()
# A singleton object for open text IDP.
open_text_saml_manager = saml_creator.create_open_text_SAML_manager()