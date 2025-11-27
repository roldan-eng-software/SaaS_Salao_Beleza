from .utils import set_current_salao
from .models import Salao

class TenantMiddleware:
    """Middleware para identificar e definir o salão atual"""
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Tenta identificar o salão pelo usuário logado
        if request.user.is_authenticated and hasattr(request.user, 'salao') and request.user.salao:
            request.salao = request.user.salao
            set_current_salao(request.user.salao)
        else:
            # TODO: Implementar lógica por subdomínio se necessário no futuro
            request.salao = None
            set_current_salao(None)
            
        response = self.get_response(request)
        return response
