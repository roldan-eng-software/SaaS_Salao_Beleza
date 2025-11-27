from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from servicos.models import Profissional, Servico
from .models import Material, Transacao

class ProfissionalForm(forms.ModelForm):
    """Formulário de profissional com criação de usuário"""
    # Campos para criar o usuário
    first_name = forms.CharField(label='Nome', max_length=30)
    last_name = forms.CharField(label='Sobrenome', max_length=30)
    email = forms.EmailField(label='Email')
    username = forms.CharField(label='Usuário (Login)', max_length=150)
    password = forms.CharField(label='Senha', widget=forms.PasswordInput)
    
    class Meta:
        model = Profissional
        fields = ['modulos', 'biografia', 'especialidades', 'horario_inicio', 'horario_fim', 
                  'trabalha_segunda', 'trabalha_terca', 'trabalha_quarta', 'trabalha_quinta', 
                  'trabalha_sexta', 'trabalha_sabado', 'trabalha_domingo', 'ativo']
        widgets = {
            'biografia': forms.Textarea(attrs={'rows': 3}),
            'horario_inicio': forms.TimeInput(attrs={'type': 'time'}),
            'horario_fim': forms.TimeInput(attrs={'type': 'time'}),
            'modulos': forms.CheckboxSelectMultiple(),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Salvar Profissional', css_class='btn btn-primary'))


class ServicoForm(forms.ModelForm):
    """Formulário de serviço"""
    class Meta:
        model = Servico
        fields = '__all__'
        exclude = ['salao']
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Salvar', css_class='btn btn-primary'))


class MaterialForm(forms.ModelForm):
    """Formulário de material"""
    class Meta:
        model = Material
        fields = '__all__'
        exclude = ['salao']
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 2}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Salvar', css_class='btn btn-primary'))


class TransacaoForm(forms.ModelForm):
    """Formulário de transação"""
    class Meta:
        model = Transacao
        fields = '__all__'
        exclude = ['salao']
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'}),
            'observacoes': forms.Textarea(attrs={'rows': 2}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Salvar', css_class='btn btn-primary'))
