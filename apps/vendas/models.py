from django.db import models
from django.utils import timezone
from apps.rh.models import *  # Importando Equipe do app RH

STATUS_CHOICES = [
    ("ativo", "Ativo"),
    ("inativo", "Inativo"),
]

class Campanha(models.Model):
    titulo = models.CharField(max_length=255, verbose_name="Título")
    equipe = models.ForeignKey(Equipe, on_delete=models.CASCADE, related_name="campanhas", verbose_name="Equipe")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="ativo", verbose_name="Status")
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.titulo} - {self.equipe.nome} ({self.status})"
