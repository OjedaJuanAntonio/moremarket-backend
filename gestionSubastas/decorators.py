from django_cognito_jwt.decorators import jwt_required

def protected_view(view_func):
    """
    Decorador para proteger vistas que requieren autenticación.
    """
    return jwt_required(view_func)
