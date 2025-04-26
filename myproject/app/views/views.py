# Authored by Rio
from django.http import HttpResponse
from django.shortcuts import render, redirect
from app.authentication.saml import open_text_saml_manager, SAML_ATTRIBUTE_KEY, SAML_PROPERTIES_ARRAY

def login_saml(request):
    '''ACS endpoint for SAML login. This where responses of IdP are handled.
    The viewpoint here is that the user requests this endpoint to get access
    to the service (claiming that they have authenticated with the IdP) and the service 
    contacts the IdP to authenticate (which is to confirm what the user is saying) the user. 
    Once the user is authenticated they are redirected to the home page and their 
    attributes are stored in session. If the login fails, a 400 BAD REQUEST is returned.

    params: user request

    returns: HttpResponse or Redirect to home page.
    '''
    try:
        saml_response_properties = open_text_saml_manager.process_acs_endpoint_request(request=request)
        # Store the attributes and response properties in session
        save_saml_response_properties_to_session(request=request, saml_response_properties=saml_response_properties)
        return redirect('login')
    except Exception as e:
        return HttpResponse(e, status=400)

def logout_saml(request):
    '''This is the SLO endpoint which manages
    the SLO response from the IdP.
    
    params: user request
    
    returns: HttpResponse or Redirect to home pages.
    '''
    try:
        logout_success = open_text_saml_manager.process_slo_endpoint_request(request=request)
        if logout_success:
            print("SAML SLO LOGOUT HAS BEEN SUCCESSFUL")
            return redirect('home')
    except Exception as e:
        return HttpResponse(e, status=400)


def save_saml_response_properties_to_session(request, saml_response_properties):
    '''Method to save the concrete values of
      SAML properties from the SAML response processing
      to the request session.
      
      params: user request, saml response properties
      
      returns: None.
      '''
    for saml_property in SAML_PROPERTIES_ARRAY:
        request.session[saml_property] = saml_response_properties[saml_property]


def index(request):
    '''This is the homepage url for service provider.

    params: user request

    returns: Index.html
    '''
    return render(request, "index.html")

def index_login(request):
    '''This is the login endpoint users hit to login to the application. When a user
    tries to login, it first checks if the user is logged in. If so, it redirects the user to the application.
    Else, it asks the user to login.

    params: user request

    returns: Redirects the user to either the homepage or login page of IdP provider.
    '''
    saml_attributes = request.session.get(SAML_ATTRIBUTE_KEY)
    print(f'This are the available attribute: {saml_attributes}')
    # Check if SAML attributes are available in the session
    if saml_attributes:
        # Attributes are available, render index.html. This is the actual homepage
        return render(request, 'index.html', {'nickname': saml_attributes.get('nickname')[0]
})
    else:
        # Attributes not available, redirect to SAML login
        print("reached here where attributes are absent")
        return redirect(open_text_saml_manager.attempt_login(request=request))

def index_logout(request):
    '''A method to start the logout process for the SP
    
    params: user request
    
    returns: A redirect to Home page.
    '''
    if request.session.get(SAML_ATTRIBUTE_KEY):
        #Checks for presence of SAML attribute and logs out the user
        request.session.flush()
    return redirect('home')
    # return redirect(open_text_saml_manager.attempt_logout(request=request))