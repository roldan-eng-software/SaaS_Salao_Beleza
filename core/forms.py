from django import forms
from django.contrib.auth.forms import UserCreationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from .models import Usuario

class CadastroUsuarioForm(UserCreationForm):
    """Formulário de cadastro de usuário"""
    first_name = forms.CharField(label='Nome', max_length=30, required=True)
    last_name = forms.CharField(label='Sobrenome', max_length=30, required=True)
    email = forms.EmailField(label='Email', required=True)
    cpf = forms.CharField(label='CPF', max_length=14, required=False)
    telefone = forms.CharField(label='Telefone', max_length=15, required=True)
    
    class Meta:
        model = Usuario
        fields = ('username', 'first_name', 'last_name', 'email', 'cpf', 'telefone', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Cadastrar', css_class='btn btn-primary w-100'))


class PerfilUsuarioForm(forms.ModelForm):
    """Formulário de edição de perfil"""
    class Meta:
        model = Usuario
        fields = ('first_name', 'last_name', 'email', 'cpf', 'telefone', 'foto')
        labels = {
            'first_name': 'Nome',
            'last_name': 'Sobrenome',
            'email': 'Email',
            'cpf': 'CPF',
            'telefone': 'Telefone',
            'foto': 'Foto de Perfil',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Salvar', css_class='btn btn-primary'))
