from django.db import models
from django.contrib.auth.models import User

# Tipos de procuração Ad Judicia (exemplo)
TIPO_PROCURACAO_CHOICES = (
    ('AD_JUDICIA', 'Ad Judicia'),
    # Podemos adicionar mais tipos futuramente, se necessário
)

class Procuracao(models.Model):
    # Campo para vincular a procuração a um usuário
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # Informações da procuração
    tipo = models.CharField(
        max_length=50,
        choices=TIPO_PROCURACAO_CHOICES,
        default='AD_JUDICIA',
        verbose_name='Tipo de Procuração'
    )
    outorgante = models.CharField(max_length=200, verbose_name='Outorgante')
    outorgado = models.CharField(max_length=200, verbose_name='Outorgado')
    
    # Datas
    data_emissao = models.DateField(verbose_name='Data de Emissão')
    data_vencimento = models.DateField(verbose_name='Data de Vencimento')
    
    # Status de alerta, para facilitar a filtragem
    esta_vencida = models.BooleanField(default=False)
    
    # Campo de texto opcional
    observacoes = models.TextField(blank=True, null=True, verbose_name='Observações')
    
    def __str__(self):
        return f'Procuração de {self.outorgante} para {self.outorgado}'

    class Meta:
        verbose_name = 'Procuração'
        verbose_name_plural = 'Procurações'