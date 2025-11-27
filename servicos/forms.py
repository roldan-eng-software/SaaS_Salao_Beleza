from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from .models import Agendamento, Profissional
from datetime import date

class AgendamentoForm(forms.ModelForm):
    """Formulário de agendamento"""
    
    class Meta:
        model = Agendamento
        fields = ['profissional', 'data', 'hora', 'observacoes']
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date', 'min': date.today().isoformat()}),
            'hora': forms.TimeInput(attrs={'type': 'time'}),
            'observacoes': forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            'profissional': 'Profissional',
            'data': 'Data',
            'hora': 'Horário',
            'observacoes': 'Observações (Opcional)',
        }
    
    def __init__(self, *args, **kwargs):
        servico = kwargs.pop('servico', None)
        super().__init__(*args, **kwargs)
        
        if servico:
            # Filtra profissionais que atendem o módulo do serviço
            self.fields['profissional'].queryset = Profissional.objects.filter(
                modulos=servico.modulo,
                ativo=True
            )
        
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Confirmar Agendamento', css_class='btn btn-primary w-100'))
    
    def clean(self):
        cleaned_data = super().clean()
        data = cleaned_data.get('data')
        hora = cleaned_data.get('hora')
        profissional = cleaned_data.get('profissional')
        
        if data and data < date.today():
            raise forms.ValidationError('Não é possível agendar para datas passadas.')
        
        # Verifica se já existe agendamento no mesmo horário
        if data and hora and profissional:
            if Agendamento.objects.filter(
                profissional=profissional,
                data=data,
                hora=hora
            ).exclude(status='cancelado').exists():
                raise forms.ValidationError('Este horário já está ocupado. Escolha outro horário.')
        
        return cleaned_data
