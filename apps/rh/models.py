from django.db import models
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
import os


# =================== CHOICES ===================
STATUS_CHOICES = (
    ('ativo', 'Ativo'),
    ('inativo', 'Inativo'),
)

SEX_CHOICES = (
    ('masculino', 'Masculino'),
    ('feminino', 'Feminino'),
)

CONTRATACAO_CHOICES = (
    ('CLT', 'CLT'),
    ('PJ', 'PJ'),
    ('MEI', 'MEI'),
    ('temporario', 'Temporário'),
    ('estagio', 'Estágio'),
)


# =================== FUNÇÃO PARA UPLOAD ===================
def get_funcionario_upload_path(instance, filename):
    """Define o diretório como 'funcionarios/NOME_COMPLETO/filename'"""
    return os.path.join('funcionarios', instance.nome_completo.upper(), filename)


# =================== MODELOS ===================

# Modelo de Empresa
class Empresa(models.Model):
    nome = models.CharField(max_length=255)
    cnpj = models.CharField(max_length=18, unique=True)
    endereco = models.CharField(max_length=255)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ativo')
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome.upper()

    class Meta:
        verbose_name_plural = "Empresas"


# Modelo de Hierarquia (Agora vinculada à Empresa)
class Hierarquia(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='hierarquias')
    nome = models.CharField(max_length=255)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ativo')
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nome.upper()} - {self.empresa.nome.upper()}"

    class Meta:
        verbose_name_plural = "Hierarquias"


# Modelo de Departamento
class Departamento(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='departamentos')
    nome = models.CharField(max_length=255)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ativo')
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nome.upper()} - {self.empresa.nome.upper()}"

    class Meta:
        verbose_name_plural = "Departamentos"


# Modelo de Equipe (Opcional, pode ser associada a um Departamento)
class Equipe(models.Model):
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE, related_name='equipes')
    nome = models.CharField(max_length=255)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ativo')
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nome.upper()} ({self.departamento.nome.upper()})"

    class Meta:
        verbose_name_plural = "Equipes"


# Modelo de Loja (opcional, vinculado a uma Equipe)
class Loja(models.Model):
    nome = models.CharField(max_length=255)
    endereco = models.CharField(max_length=255)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ativo')
    data_criacao = models.DateTimeField(auto_now_add=True)
    equipe = models.ForeignKey(Equipe, on_delete=models.CASCADE, related_name='lojas', null=True, blank=True)

    def __str__(self):
        return f"{self.nome.upper()} - {self.equipe.nome.upper() if self.equipe else 'Sem Equipe'}"

    class Meta:
        verbose_name_plural = "Lojas"


# Modelo de Cargo (vinculado a um Departamento e Hierarquia)
class Cargo(models.Model):
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE, related_name='cargos')
    hierarquia = models.ForeignKey(Hierarquia, on_delete=models.CASCADE, related_name='cargos')
    nome = models.CharField(max_length=255)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ativo')
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nome.upper()} - {self.departamento.nome.upper()}"

    class Meta:
        verbose_name_plural = "Cargos"


# Modelo de Horário
class Horario(models.Model):
    nome = models.CharField(max_length=255)
    descricao = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ativo')
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome.upper()

    class Meta:
        verbose_name_plural = "Horários"


# =================== MODELO DE FUNCIONÁRIO ===================
class Funcionario(models.Model):
    # Vínculo com usuário Django (Opcional)
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='funcionario', null=True, blank=True)

    # Informações Pessoais
    nome_completo = models.CharField(max_length=255, verbose_name="Nome Completo")
    cpf = models.CharField(max_length=14, unique=True, verbose_name="CPF")
    rg = models.CharField(max_length=20, blank=True, null=True, verbose_name="RG")
    pis = models.CharField(max_length=20, blank=True, null=True, verbose_name="PIS")
    data_nasc = models.DateField(blank=True, null=True, verbose_name="Data de Nascimento")
    sexualidade = models.CharField(max_length=10, choices=SEX_CHOICES, blank=True, null=True, verbose_name="Gênero")
    estado_civil = models.CharField(max_length=50, blank=True, null=True, verbose_name="Estado Civil")

    # Contato
    celular = models.CharField(max_length=20, blank=True, null=True, verbose_name="Celular")
    telefone_fixo = models.CharField(max_length=20, blank=True, null=True, verbose_name="Telefone Fixo")
    email = models.EmailField(max_length=255, blank=True, null=True, verbose_name="E-mail")

    # Endereço
    endereco = models.CharField(max_length=255, blank=True, null=True, verbose_name="Endereço")
    cidade = models.CharField(max_length=100, blank=True, null=True, verbose_name="Cidade")
    uf = models.CharField(max_length=2, blank=True, null=True, verbose_name="UF")

    # Informações Profissionais
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, null=True, blank=True, related_name='funcionarios', verbose_name="Empresa")
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE, null=True, blank=True, related_name='funcionarios', verbose_name="Departamento")
    cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE, null=True, blank=True, related_name='funcionarios', verbose_name="Cargo")
    hierarquia = models.ForeignKey(Hierarquia, on_delete=models.CASCADE, null=True, blank=True, related_name='funcionarios', verbose_name="Hierarquia")
    equipe = models.ForeignKey(Equipe, on_delete=models.SET_NULL, null=True, blank=True, related_name='funcionarios', verbose_name="Equipe")
    loja = models.ForeignKey(Loja, on_delete=models.SET_NULL, null=True, blank=True, related_name='funcionarios', verbose_name="Loja")
    horario = models.ForeignKey(Horario, on_delete=models.SET_NULL, null=True, blank=True, related_name='funcionarios', verbose_name="Horário de Trabalho")

    # Dados de Contratação
    tipo_contratacao = models.CharField(max_length=50, choices=CONTRATACAO_CHOICES, blank=True, null=True, verbose_name="Tipo de Contratação")
    data_admissao = models.DateField(blank=True, null=True, verbose_name="Data de Admissão")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ativo', verbose_name="Status")

    # Foto
    foto = models.ImageField(upload_to=get_funcionario_upload_path, blank=True, null=True, verbose_name="Foto")

    # Data de Criação
    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")

    def __str__(self):
        return f"{self.nome_completo.upper()} ({self.cargo.nome.upper()}) - {self.cpf}"

    class Meta:
        verbose_name_plural = "Funcionários"

    # Método para verificar se funcionário está ativo
    def is_ativo(self):
        return self.status == "ativo"


# =================== ARQUIVOS FUNCIONÁRIO ===================
def arquivo_upload_path(instance, filename):
    """
    Define o caminho do arquivo para ser salvo no formato:
    "funcionarios/arquivos/{funcionario.nome_completo}/{titulo}.pdf"
    """

    # Extrai a extensão do arquivo
    ext = filename.split('.')[-1].lower()

    # Garante que seja apenas PDF
    if ext != "pdf":
        raise ValidationError("Somente arquivos PDF são permitidos.")

    # Cria o nome do arquivo baseado no título (slugify remove caracteres especiais)
    nome_arquivo = f"{slugify(instance.titulo)}.{ext}"

    # Define o caminho da pasta com o nome do funcionário
    pasta_funcionario = f"funcionarios/arquivos/{slugify(instance.funcionario.nome_completo)}"

    # Retorna o caminho completo
    return os.path.join(pasta_funcionario, nome_arquivo)


# =================== MODELO DE ARQUIVOS FUNCIONÁRIO ===================
class ArquivosFuncionario(models.Model):
    funcionario = models.ForeignKey(Funcionario, on_delete=models.CASCADE, related_name="arquivos")
    titulo = models.CharField(max_length=255, unique=True)
    descricao = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to=arquivo_upload_path)
    data_importacao = models.DateTimeField(auto_now_add=True)

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="ativo",
        help_text="Define se o arquivo está ativo ou inativo."
    )

    def __str__(self):
        return f"{self.titulo} - {self.funcionario.nome_completo.upper()}"

    class Meta:
        verbose_name_plural = "Arquivos de Funcionários"
        unique_together = ("funcionario", "titulo")  # Garante que um mesmo funcionário não tenha títulos duplicados

    # =================== VALIDAÇÃO DE FORMATO ===================
    def clean(self):
        """
        Garante que o arquivo seja um PDF e verifica se já existe um arquivo com o mesmo título para o funcionário.
        """
        if self.file:
            ext = self.file.name.split('.')[-1].lower()
            if ext != "pdf":
                raise ValidationError("Somente arquivos PDF são permitidos.")

    def save(self, *args, **kwargs):
        """
        Antes de salvar, altera o nome do arquivo e o move para a pasta correta do funcionário.
        """
        if self.file:
            self.file.name = arquivo_upload_path(self, self.file.name)
        super().save(*args, **kwargs)