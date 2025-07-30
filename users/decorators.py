from django.http import HttpResponseForbidden


#creating custom decorator to check role pf user

def role_required(required_roles):
    def decorator(view_func):
        def wrapper(request,*args,**kwargs):
            #if user not login
            if not request.user.is_authenticated:
                return HttpResponseForbidden("Login Required")
            
            #if profile is not created for user
            if not hasattr(request.user,'userprofile'):
                return HttpResponseForbidden("User Profile Not Found")
            
            #agar user ka role match nhi karega tb
            user_role=request.user.userprofile.role

            #admin always alow
            if user_role=='admin' or user_role in required_roles:
                return view_func(request,*args,**kwargs)


            
            return HttpResponseForbidden("Access Denied")
            
            
        return wrapper
    return   decorator
            




