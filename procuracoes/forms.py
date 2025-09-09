from django import forms
from .models import Procuracao

class ProcuracaoForm(forms.ModelForm):
    class Meta:
        model = Procuracao
        fields = ['tipo', 'outorgante', 'outorgado', 'data_emissao', 'data_vencimento', 'observacoes']
        widgets = {
            'data_emissao': forms.DateInput(attrs={'type': 'date'}),
            'data_vencimento': forms.DateInput(attrs={'type': 'date'}),
        }