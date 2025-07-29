from django.http import HttpResponseForbidden


#creating custom decorator to check role pf user

def role_required(required_role):
    def decorator(view_func):
        def wrapper(request,*args,**kwargs):
            #if user not login
            if not request.user.is_authenticated:
                return HttpResponseForbidden("Login Required")
            
            #if profile is not created for user
            if not hasattr(request.user,'userprofile'):
                return HttpResponseForbidden("User Profile Not Found")
            
            #agar user ka role match nhi karega tb

            if request.user.userprofile.role !=required_role:
                return HttpResponseForbidden("Access Denied")
            
            return view_func(request,*args,**kwargs)
        return wrapper
    return   decorator
            




