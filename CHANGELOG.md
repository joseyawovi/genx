
##  Saturday 8 March 2025 
   - Created a venv
   - Created the project genx
   - create core app and set it up
   - created global template folder
   - setting and CSRF_TRUSTED_ORIGINS to allow django to allow the url and process form submittion in gitpod plateform
   - setting static files and medias
   - Dividing the website into base, index and partials

   ## Setting allauth for user authentication handling

      - create accounts app
      - install django-allauth 
      - add them to INSTALLED_APPS
      - SITE_ID = 1
      - Allauth Configuration in settings.py
         + AUTHENTICATION_BACKENDS 
         + other account related configuration in settings.py
      - URL Configuration
      - Email config
      - migrate
      - account related templates
         testing
## customizing the Account related template
      
      - signup page
         
         . use the contact form 
         
         . we need the user names so we have to extend and customize the forms
      
      - Sign in page
         
         . use signup template
         
      
      - all other that are needed
      
##           #    ###########.      11 March 2025
## changing templates into french
   - base, index, partials
   - account
   - verify all he url on the page
   
   ##      creating courses
   - create course app and install it
   - create Course and instructor models
   - migrate
   - write the views
   - set the URLS
   