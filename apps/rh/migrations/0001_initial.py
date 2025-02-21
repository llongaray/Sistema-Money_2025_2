# Generated by Django 5.1.6 on 2025-02-14 17:39

import apps.rh.models
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Departamento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255)),
                ('status', models.CharField(choices=[('ativo', 'Ativo'), ('inativo', 'Inativo')], default='ativo', max_length=10)),
                ('data_criacao', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Departamentos',
            },
        ),
        migrations.CreateModel(
            name='Empresa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255)),
                ('cnpj', models.CharField(max_length=18, unique=True)),
                ('endereco', models.CharField(max_length=255)),
                ('status', models.CharField(choices=[('ativo', 'Ativo'), ('inativo', 'Inativo')], default='ativo', max_length=10)),
                ('data_criacao', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Empresas',
            },
        ),
        migrations.CreateModel(
            name='Horario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255)),
                ('descricao', models.TextField(blank=True, null=True)),
                ('status', models.CharField(choices=[('ativo', 'Ativo'), ('inativo', 'Inativo')], default='ativo', max_length=10)),
                ('data_criacao', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Horários',
            },
        ),
        migrations.CreateModel(
            name='Cargo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255)),
                ('status', models.CharField(choices=[('ativo', 'Ativo'), ('inativo', 'Inativo')], default='ativo', max_length=10)),
                ('data_criacao', models.DateTimeField(auto_now_add=True)),
                ('departamento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cargos', to='rh.departamento')),
            ],
            options={
                'verbose_name_plural': 'Cargos',
            },
        ),
        migrations.AddField(
            model_name='departamento',
            name='empresa',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='departamentos', to='rh.empresa'),
        ),
        migrations.CreateModel(
            name='Equipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255)),
                ('status', models.CharField(choices=[('ativo', 'Ativo'), ('inativo', 'Inativo')], default='ativo', max_length=10)),
                ('data_criacao', models.DateTimeField(auto_now_add=True)),
                ('departamento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='equipes', to='rh.departamento')),
            ],
            options={
                'verbose_name_plural': 'Equipes',
            },
        ),
        migrations.CreateModel(
            name='Funcionario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_completo', models.CharField(max_length=255)),
                ('cpf', models.CharField(max_length=20, unique=True)),
                ('data_nasc', models.DateField(blank=True, null=True)),
                ('sexualidade', models.CharField(blank=True, choices=[('masculino', 'Masculino'), ('feminino', 'Feminino')], max_length=10, null=True)),
                ('estado_civil', models.CharField(blank=True, max_length=50, null=True)),
                ('celular', models.CharField(blank=True, max_length=20, null=True)),
                ('email', models.EmailField(blank=True, max_length=255, null=True)),
                ('endereco', models.CharField(blank=True, max_length=255, null=True)),
                ('cidade', models.CharField(blank=True, max_length=100, null=True)),
                ('uf', models.CharField(blank=True, max_length=2, null=True)),
                ('tipo_contratacao', models.CharField(blank=True, choices=[('CLT', 'CLT'), ('PJ', 'PJ'), ('MEI', 'MEI'), ('temporario', 'Temporário'), ('estagio', 'Estágio')], max_length=50, null=True)),
                ('data_admissao', models.DateField(blank=True, null=True)),
                ('foto', models.ImageField(blank=True, null=True, upload_to=apps.rh.models.get_funcionario_upload_path)),
                ('data_criacao', models.DateTimeField(auto_now_add=True)),
                ('cargo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='funcionarios', to='rh.cargo')),
                ('departamento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='funcionarios', to='rh.departamento')),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='funcionarios', to='rh.empresa')),
                ('equipe', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='funcionarios', to='rh.equipe')),
                ('usuario', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='funcionario', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Funcionários',
            },
        ),
        migrations.CreateModel(
            name='ArquivosFuncionario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=255)),
                ('descricao', models.TextField(blank=True, null=True)),
                ('file', models.FileField(upload_to='funcionarios/arquivos/')),
                ('data_importacao', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('ativo', 'Ativo'), ('inativo', 'Inativo')], default='ativo', help_text='Define se o arquivo está ativo ou inativo.', max_length=10)),
                ('funcionario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='arquivos', to='rh.funcionario')),
            ],
            options={
                'verbose_name_plural': 'Arquivos de Funcionários',
            },
        ),
        migrations.CreateModel(
            name='Hierarquia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255)),
                ('status', models.CharField(choices=[('ativo', 'Ativo'), ('inativo', 'Inativo')], default='ativo', max_length=10)),
                ('data_criacao', models.DateTimeField(auto_now_add=True)),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hierarquias', to='rh.empresa')),
            ],
            options={
                'verbose_name_plural': 'Hierarquias',
            },
        ),
        migrations.AddField(
            model_name='funcionario',
            name='hierarquia',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='funcionarios', to='rh.hierarquia'),
        ),
        migrations.AddField(
            model_name='cargo',
            name='hierarquia',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cargos', to='rh.hierarquia'),
        ),
        migrations.AddField(
            model_name='funcionario',
            name='horario',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='funcionarios', to='rh.horario'),
        ),
        migrations.CreateModel(
            name='Loja',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255)),
                ('endereco', models.CharField(max_length=255)),
                ('status', models.CharField(choices=[('ativo', 'Ativo'), ('inativo', 'Inativo')], default='ativo', max_length=10)),
                ('data_criacao', models.DateTimeField(auto_now_add=True)),
                ('equipe', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='lojas', to='rh.equipe')),
            ],
            options={
                'verbose_name_plural': 'Lojas',
            },
        ),
        migrations.AddField(
            model_name='funcionario',
            name='loja',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='funcionarios', to='rh.loja'),
        ),
    ]
