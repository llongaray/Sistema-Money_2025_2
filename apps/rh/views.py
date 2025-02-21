from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import *
import json

# ================== RENDERIZAÇÃO DE TEMPLATES ==================

@login_required
def render_categorias(request):
    """Renderiza a página para criação de Empresa, Departamento, Cargo, etc."""
    return render(request, 'rh/categorias.html')


@login_required
def render_funcionarios(request):
    """Renderiza a página para criação de Funcionários"""
    return render(request, 'rh/novo_funcionario.html')


@login_required
def render_usuarios(request):
    """Renderiza a página para criação de Usuários vinculados a Funcionários"""
    return render(request, 'rh/usuarios.html')


@login_required
def render_arquivos_funcionario(request):
    """Renderiza a página para gerenciamento de arquivos/documentos de funcionários"""
    return render(request, 'rh/arquivos_funcionario.html')

@login_required
def render_edit_funcionario(request):
    """Renderiza a página de edição de Funcionários"""
    return render(request, 'rh/edit_funcionario.html')


# ================== API GET - RETORNA TODOS OS DADOS ==================

import logging

logger = logging.getLogger(__name__)

@login_required
def api_rh_get(request):
    """Retorna todos os dados dos models de RH, incluindo usuários do Django"""
    try:
        logger.info("📡 Iniciando a busca de dados para API RH GET.")

        empresas = list(Empresa.objects.values('id', 'nome', 'cnpj', 'status'))
        hierarquias = list(Hierarquia.objects.values('id', 'nome', 'empresa_id', 'status'))
        departamentos = list(Departamento.objects.values('id', 'nome', 'empresa_id', 'status'))
        equipes = list(Equipe.objects.values('id', 'nome', 'departamento_id', 'status'))
        cargos = list(Cargo.objects.values('id', 'nome', 'departamento_id', 'hierarquia_id', 'status'))
        lojas = list(Loja.objects.values('id', 'nome', 'equipe_id', 'status'))
        
        funcionarios = list(Funcionario.objects.values(
            'id', 'nome_completo', 'cpf', 'email', 'empresa_id', 'departamento_id', 
            'cargo_id', 'hierarquia_id', 'equipe_id', 'loja_id', 'status', 'usuario_id'
        ))

        arquivos = list(ArquivosFuncionario.objects.values(
            'id', 'titulo', 'descricao', 'file', 'data_importacao', 'status', 'funcionario_id'
        ))

        usuarios = list(User.objects.values('id', 'username', 'email', 'is_active'))

        logger.info("✅ Dados recuperados com sucesso para API RH GET.")

        return JsonResponse({
            'empresas': empresas,
            'hierarquias': hierarquias,
            'departamentos': departamentos,
            'equipes': equipes,
            'cargos': cargos,
            'lojas': lojas,
            'funcionarios': funcionarios,
            'arquivos_funcionarios': arquivos,
            'usuarios': usuarios
        })

    except Exception as e:
        logger.error(f"❌ Erro na API RH GET: {str(e)}")
        return JsonResponse({'error': 'Erro interno do servidor', 'message': str(e)}, status=500)


# ================== API POST - CRIA OU EDITA OS REGISTROS ==================

@csrf_exempt
@login_required
def api_empresa_post(request):
    """Cria ou edita uma Empresa"""
    if request.method == 'POST':
        try:
            logger.info("📩 Recebendo requisição POST para criar/editar empresa.")

            # Lendo JSON do corpo da requisição
            data = json.loads(request.body)
            logger.debug(f"📥 Dados recebidos: {data}")

            # Validando se todos os campos necessários estão presentes
            required_fields = ['nome', 'cnpj', 'endereco', 'status']
            for field in required_fields:
                if field not in data or not data[field].strip():
                    logger.warning(f"⚠️ Campo obrigatório ausente: {field}")
                    return JsonResponse({'success': False, 'error': f"Campo obrigatório ausente: {field}"}, status=400)

            # Criando ou atualizando a empresa
            empresa, created = Empresa.objects.update_or_create(
                id=data.get('id', None),
                defaults={
                    'nome': data['nome'].strip(),
                    'cnpj': data['cnpj'].strip(),
                    'endereco': data['endereco'].strip(),
                    'status': data['status'].strip()
                }
            )

            logger.info(f"✅ Empresa {'criada' if created else 'atualizada'} com sucesso! ID: {empresa.id}")
            return JsonResponse({'success': True, 'empresa_id': empresa.id})

        except json.JSONDecodeError as e:
            logger.error(f"❌ Erro ao processar JSON: {e}")
            return JsonResponse({'success': False, 'error': 'Formato de JSON inválido.'}, status=400)

        except Exception as e:
            logger.error(f"❌ Erro interno ao salvar empresa: {e}")
            return JsonResponse({'success': False, 'error': 'Erro interno do servidor.', 'message': str(e)}, status=500)


@csrf_exempt
@login_required
def api_hierarquia_post(request):
    """Cria ou edita uma Hierarquia"""
    if request.method == 'POST':
        try:
            logger.info("📩 Recebendo requisição POST para criar/editar Hierarquia.")
            data = json.loads(request.body)
            logger.debug(f"📥 Dados recebidos: {data}")

            # Verifica campos obrigatórios
            if not data.get('empresa_id') or not data.get('nome') or not data.get('status'):
                return JsonResponse({'success': False, 'error': 'Campos obrigatórios ausentes.'}, status=400)

            hierarquia, created = Hierarquia.objects.update_or_create(
                id=data.get('id', None),
                defaults={'empresa_id': data['empresa_id'], 'nome': data['nome'], 'status': data['status']}
            )
            return JsonResponse({'success': True, 'hierarquia_id': hierarquia.id})

        except Exception as e:
            logger.error(f"❌ Erro na API hierarquia_post: {e}")
            return JsonResponse({'success': False, 'error': str(e)}, status=500)


@csrf_exempt
@login_required
def api_departamento_post(request):
    """Cria ou edita um Departamento"""
    if request.method == 'POST':
        try:
            logger.info("📩 Recebendo requisição POST para criar/editar Departamento.")
            data = json.loads(request.body)

            # Verifica campos obrigatórios
            if not data.get('empresa_id') or not data.get('nome') or not data.get('status'):
                return JsonResponse({'success': False, 'error': 'Campos obrigatórios ausentes.'}, status=400)

            departamento, created = Departamento.objects.update_or_create(
                id=data.get('id', None),
                defaults={'empresa_id': data['empresa_id'], 'nome': data['nome'], 'status': data['status']}
            )
            return JsonResponse({'success': True, 'departamento_id': departamento.id})

        except Exception as e:
            logger.error(f"❌ Erro na API departamento_post: {e}")
            return JsonResponse({'success': False, 'error': str(e)}, status=500)


@csrf_exempt
@login_required
def api_equipe_post(request):
    """Cria ou edita uma Equipe"""
    if request.method == 'POST':
        try:
            logger.info("📩 Recebendo requisição POST para criar/editar Equipe.")
            data = json.loads(request.body)

            # Verifica campos obrigatórios
            if not data.get('departamento_id') or not data.get('nome') or not data.get('status'):
                return JsonResponse({'success': False, 'error': 'Campos obrigatórios ausentes.'}, status=400)

            equipe, created = Equipe.objects.update_or_create(
                id=data.get('id', None),
                defaults={'departamento_id': data['departamento_id'], 'nome': data['nome'], 'status': data['status']}
            )
            return JsonResponse({'success': True, 'equipe_id': equipe.id})

        except Exception as e:
            logger.error(f"❌ Erro na API equipe_post: {e}")
            return JsonResponse({'success': False, 'error': str(e)}, status=500)

@csrf_exempt
@login_required
def api_cargo_post(request):
    """Cria ou edita um Cargo"""
    if request.method == 'POST':
        try:
            logger.info("📩 Recebendo requisição POST para criar/editar Cargo.")
            data = json.loads(request.body)
            logger.debug(f"📥 Dados recebidos: {data}")

            # Verifica campos obrigatórios
            required_fields = ["departamento_id", "hierarquia_id", "nome", "status"]
            for field in required_fields:
                if field not in data or not data[field]:
                    logger.warning(f"⚠️ Campo obrigatório ausente: {field}")
                    return JsonResponse({'success': False, 'error': f'Campo obrigatório ausente: {field}'}, status=400)

            cargo, created = Cargo.objects.update_or_create(
                id=data.get('id', None),
                defaults={
                    'departamento_id': data['departamento_id'],
                    'hierarquia_id': data['hierarquia_id'],
                    'nome': data['nome'],
                    'status': data['status']
                }
            )

            logger.info(f"✅ Cargo {'criado' if created else 'atualizado'} com sucesso! ID: {cargo.id}")
            return JsonResponse({'success': True, 'cargo_id': cargo.id})

        except Exception as e:
            logger.error(f"❌ Erro na API cargo_post: {e}")
            return JsonResponse({'success': False, 'error': str(e)}, status=500)



@csrf_exempt
@login_required
def api_loja_post(request):
    """Cria ou edita uma Loja"""
    if request.method == 'POST':
        try:
            logger.info("📩 Recebendo requisição POST para criar/editar Loja.")
            data = json.loads(request.body)

            # Verifica campos obrigatórios
            if not data.get('equipe_id') or not data.get('nome') or not data.get('endereco') or not data.get('status'):
                return JsonResponse({'success': False, 'error': 'Campos obrigatórios ausentes.'}, status=400)

            loja, created = Loja.objects.update_or_create(
                id=data.get('id', None),
                defaults={'equipe_id': data['equipe_id'], 'nome': data['nome'], 'endereco': data['endereco'], 'status': data['status']}
            )
            return JsonResponse({'success': True, 'loja_id': loja.id})

        except Exception as e:
            logger.error(f"❌ Erro na API loja_post: {e}")
            return JsonResponse({'success': False, 'error': str(e)}, status=500)


@csrf_exempt
@login_required
def api_funcionario_post(request):
    """Cria um novo funcionário com informações básicas"""
    if request.method == 'POST':
        try:
            print("\n📩 RECEBENDO REQUISIÇÃO POST PARA CRIAR FUNCIONÁRIO")
            print("===================================================")

            # 🔥 Extraindo dados corretamente
            data = {key: request.POST[key] for key in request.POST}  # Converte QueryDict para dicionário
            files = {key: request.FILES[key].name for key in request.FILES}  # Lista de arquivos recebidos

            print("\n🔍 DADOS RECEBIDOS DO FORMULÁRIO:", data)
            print("\n📸 ARQUIVOS RECEBIDOS:", files if files else "Nenhum arquivo enviado")

            foto = request.FILES.get('foto', None)

            # 🚨 Verifica campos obrigatórios
            required_fields = ['nome_completo', 'cpf', 'celular', 'empresa_id', 'departamento_id', 'cargo_id']
            for field in required_fields:
                if field not in data:
                    print(f"\n❌ ERRO: Campo obrigatório ausente - {field}")
                    return JsonResponse({'success': False, 'error': f'Campo obrigatório ausente: {field}'}, status=400)

            # Criando o funcionário
            funcionario = Funcionario.objects.create(**data, foto=foto, status="ativo")

            print(f"✅ Funcionário {funcionario.nome_completo} criado com sucesso! ID: {funcionario.id}")
            return JsonResponse({'success': True, 'funcionario_id': funcionario.id})

        except Exception as e:
            print(f"❌ ERRO: {e}")
            return JsonResponse({'success': False, 'error': str(e)}, status=500)

@csrf_exempt
@login_required
def api_usuario_post(request):
    """Cria um usuário Django vinculado a um funcionário"""
    try:
        logger.info("📩 Recebendo requisição POST para criar usuário.")
        data = json.loads(request.body)
        logger.debug(f"📥 Dados recebidos: {data}")

        # 🚨 Verifica campos obrigatórios (Agora sem o email)
        if not data.get('username') or not data.get('password'):
            return JsonResponse({'success': False, 'error': 'Campos obrigatórios ausentes.'}, status=400)

        # 🚫 Verifica se o usuário já existe
        if User.objects.filter(username=data['username']).exists():
            return JsonResponse({'success': False, 'error': 'Usuário já existe'}, status=400)

        # ✅ Cria o usuário Django
        user = User.objects.create_user(
            username=data['username'],
            password=data['password'],
            is_active=data.get('is_active', True)
        )
        logger.info(f"✅ Usuário {user.username} criado com sucesso!")

        # 🔗 Associa usuário ao funcionário, se fornecido
        if data.get('funcionario_id'):
            try:
                funcionario = Funcionario.objects.get(id=data['funcionario_id'])
                funcionario.usuario = user
                funcionario.save()
                logger.info(f"🔗 Usuário {user.username} vinculado ao funcionário {funcionario.nome_completo}")
            except Funcionario.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Funcionário não encontrado.'}, status=404)

        return JsonResponse({'success': True, 'user_id': user.id})

    except Exception as e:
        logger.error(f"❌ Erro na API usuario_post: {e}")
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@csrf_exempt
@login_required
def api_horario_post(request):
    """Cria ou edita um Horário"""
    try:
        data = json.loads(request.body)
        logger.info(f"📥 Dados recebidos para horário: {data}")

        horario, created = Horario.objects.update_or_create(
            id=data.get('id', None),
            defaults={
                'nome': data['nome'],
                'descricao': data.get('descricao', ''),  # Se não vier no JSON, define como string vazia
                'status': data.get('status', 'ativo')  # Se não vier no JSON, define como 'ativo'
            }
        )
        logger.info(f"✅ Horário {'criado' if created else 'atualizado'}: {horario.nome}")
        return JsonResponse({'success': True, 'horario_id': horario.id})

    except Exception as e:
        logger.error(f"❌ Erro na API horario_post: {e}")
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@csrf_exempt
@login_required
def api_arquivos_funcionario_post(request):
    """Adiciona ou edita um arquivo/documento de um funcionário"""
    try:
        logger.info("📩 Recebendo requisição POST para upload de arquivos do funcionário.")

        if request.method == 'POST' and request.FILES.get('file'):
            funcionario_id = request.POST.get('funcionario_id')
            titulo = request.POST.get('titulo')
            descricao = request.POST.get('descricao')
            file = request.FILES['file']
            status = request.POST.get('status', 'ativo')

            # Verifica campos obrigatórios
            if not funcionario_id or not titulo:
                return JsonResponse({'success': False, 'error': 'Campos obrigatórios ausentes.'}, status=400)

            # Verifica se o funcionário existe
            try:
                funcionario = Funcionario.objects.get(id=funcionario_id)
            except Funcionario.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Funcionário não encontrado.'}, status=404)

            # Cria o arquivo associado ao funcionário
            arquivo = ArquivosFuncionario.objects.create(
                funcionario=funcionario,
                titulo=titulo,
                descricao=descricao,
                file=file,
                status=status
            )
            logger.info(f"✅ Arquivo {arquivo.titulo} salvo para funcionário {funcionario.nome_completo}")

            return JsonResponse({'success': True, 'arquivo_id': arquivo.id})

        return JsonResponse({'success': False, 'error': 'Nenhum arquivo foi enviado.'}, status=400)

    except Exception as e:
        logger.error(f"❌ Erro na API arquivos_funcionario_post: {e}")
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
    
@csrf_exempt
@login_required
def api_funcionario_edit_post(request):
    """Edita um funcionário existente"""
    if request.method == 'POST':
        try:
            logger.info("📩 Recebendo requisição POST para editar funcionário.")
            
            # Parse do JSON recebido
            data = json.loads(request.body)
            logger.debug(f"📥 Dados recebidos: {data}")

            # Verifica se o ID do funcionário foi enviado
            funcionario_id = data.get('id')
            if not funcionario_id:
                return JsonResponse({'success': False, 'error': 'ID do funcionário não fornecido.'}, status=400)

            # Busca o funcionário no banco
            try:
                funcionario = Funcionario.objects.get(id=funcionario_id)
            except Funcionario.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Funcionário não encontrado.'}, status=404)

            # Campos de ForeignKey que precisam de conversão
            foreign_keys = {
                'empresa': Empresa,
                'departamento': Departamento,
                'cargo': Cargo,
                'hierarquia': Hierarquia,
                'equipe': Equipe,
                'loja': Loja,
                'horario': Horario,
            }

            campos_atualizados = []
            for campo, valor in data.items():
                if not valor:
                    continue  # Ignora valores vazios

                if campo in foreign_keys:
                    try:
                        # Converte ID em objeto do modelo correspondente
                        valor = foreign_keys[campo].objects.get(id=valor)
                    except foreign_keys[campo].DoesNotExist:
                        return JsonResponse({'success': False, 'error': f'ID inválido para {campo}.'}, status=400)

                if hasattr(funcionario, campo):
                    setattr(funcionario, campo, valor)
                    campos_atualizados.append(campo)

            if campos_atualizados:
                funcionario.save()
                logger.info(f"✅ Funcionário {funcionario.nome_completo} atualizado com sucesso! Campos modificados: {campos_atualizados}")
            else:
                logger.warning(f"⚠️ Nenhuma alteração feita para {funcionario.nome_completo}")

            return JsonResponse({'success': True, 'funcionario_id': funcionario.id})

        except json.JSONDecodeError as e:
            logger.error(f"❌ Erro ao processar JSON: {e}")
            return JsonResponse({'success': False, 'error': 'Formato de JSON inválido.'}, status=400)

        except Exception as e:
            logger.error(f"❌ Erro interno ao atualizar funcionário: {e}")
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
