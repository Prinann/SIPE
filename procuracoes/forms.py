from django import forms
from .models import Procuracao

class ProcuracaoForm(forms.ModelForm):
    class Meta:
        model = Procuracao
        fields = ['outorgante', 'outorgado', 'data_emissao', 'data_vencimento', 'observacoes']
        widgets = {
            'outorgante': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome completo do outorgante'}),
            'outorgado': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome completo do outorgado'}),
            'data_emissao': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'data_vencimento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Observações adicionais sobre a procuração...', 'rows': 3}),
        }