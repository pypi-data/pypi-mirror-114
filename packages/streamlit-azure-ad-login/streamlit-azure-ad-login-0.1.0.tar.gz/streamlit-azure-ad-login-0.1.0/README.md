# streamlit-azure-ad-login
This is a React login component that help you check coonect to an endpoint that make the authentication with Azure Active Director and return the proper token.   
This aproach is because the Active Directory authentication requires a lot of certifications that depends on each project.  
  
The component allows you to  personalize the following parameters:  
- **header_text:** Text that will apear on the header of the login component
- **authentication_endpoint_url:** The active directory url to send the credentials and return the token
- **logo_uri:** a URI with the image of your company
- **prefix:** If you have a prefix for the login, here is where it goes

## How to use it
```python
from streamlit_azure_login import login_component

token = login_component(
    header_text='Your Company Name, 
    authentication_endpoint_url='https://azure.microsoft.com/en-us/services/active-directory/', 
    logo_uri='https://intercement.com/wp-content/uploads/2019/04/INTERCEMENT.jpg',
    prefix=''
)
```
