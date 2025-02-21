import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Campanha
from apps.rh.models import *  # Importando Equipe para seleção no form

# =================== RENDERIZAÇÃO DO TEMPLATE ===================
@login_required
def render_campanhas(request):
    return render(request, "vendas/campanhas.html")

# =================== API GET - LISTAR CAMPANHAS ===================
@login_required
def api_campanhas_get(request):
    """Retorna todas as campanhas cadastradas"""
    try:
        campanhas = list(
            Campanha.objects.select_related("equipe").values("id", "titulo", "equipe__nome", "status")
        )
        return JsonResponse({"campanhas": campanhas})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

# =================== API POST - CRIAR CAMPANHA ===================
@csrf_exempt
@login_required
def api_campanha_post(request):
    """Cria uma nova campanha"""
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            titulo = data.get("titulo")
            equipe_id = data.get("equipe_id")

            if not titulo or not equipe_id:
                return JsonResponse({"error": "Campos obrigatórios ausentes."}, status=400)

            campanha = Campanha.objects.create(
                titulo=titulo,
                equipe_id=equipe_id
            )

            return JsonResponse({"success": True, "campanha_id": campanha.id})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

# =================== API POST - ALTERAR STATUS ===================
@csrf_exempt
@login_required
def api_campanha_status_post(request):
    """Altera o status da campanha"""
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            campanha_id = data.get("campanha_id")

            if not campanha_id:
                return JsonResponse({"error": "ID da campanha não informado."}, status=400)

            campanha = Campanha.objects.get(id=campanha_id)
            campanha.status = "ativo" if campanha.status == "inativo" else "inativo"
            campanha.save()

            return JsonResponse({"success": True, "novo_status": campanha.status})

        except Campanha.DoesNotExist:
            return JsonResponse({"error": "Campanha não encontrada."}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
