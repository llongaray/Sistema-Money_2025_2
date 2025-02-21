from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(login_url="usuarios:login")  # Redireciona para login se não autenticado
def dashboard(request):
    # Dados de exemplo para simulação do dashboard
    context = {
        'email_enviados': 150,
        'email_recebidos': 200,
        'chips_ativos': 50,
        'chips_inativos': 10,
        'pas': [
            {
                'sala': 'Sala 101',
                'pa': 'PA-01',
                'status': 'Em Uso',
                'icon': 'fas fa-check-circle',
                'color': 'green'
            },
            {
                'sala': 'Sala 102',
                'pa': 'PA-02',
                'status': 'Completo, mas sem uso',
                'icon': 'fas fa-exclamation-circle',
                'color': 'yellow'
            },
            {
                'sala': 'Sala 103',
                'pa': 'PA-03',
                'status': 'Sem Uso e Sem Periféricos',
                'icon': 'fas fa-times-circle',
                'color': 'red'
            },
            {
                'sala': 'Sala 104',
                'pa': 'PA-04',
                'status': 'Em Uso',
                'icon': 'fas fa-check-circle',
                'color': 'green'
            },
            {
                'sala': 'Sala 105',
                'pa': 'PA-05',
                'status': 'Completo, mas sem uso',
                'icon': 'fas fa-exclamation-circle',
                'color': 'yellow'
            },
        ],
        'funcionarios': [
            {'id': '001', 'nome': 'João Silva', 'setor': 'TI'},
            {'id': '002', 'nome': 'Maria Souza', 'setor': 'TI'},
            {'id': '003', 'nome': 'Carlos Pereira', 'setor': 'TI'},
        ],
        'perifericos': {
            'monitores': 25,
            'teclados': 30,
            'mouses': 30,
            'impressoras': 5,
            'scanners': 3,
            'webcams': 8,
        },
        'equipamentos': [
            {'id': 'EQ-001', 'tipo': 'Computador', 'status': 'Ativo'},
            {'id': 'EQ-002', 'tipo': 'Monitor', 'status': 'Inativo'},
            {'id': 'EQ-003', 'tipo': 'Impressora', 'status': 'Ativo'},
        ],
        'historico': [
            {'id': 'H-001', 'descricao': 'Atualização de Software', 'data': '2025-01-10', 'responsavel': 'João Silva'},
            {'id': 'H-002', 'descricao': 'Manutenção Preventiva', 'data': '2025-01-15', 'responsavel': 'Maria Souza'},
            {'id': 'H-003', 'descricao': 'Substituição de Periféricos', 'data': '2025-01-20', 'responsavel': 'Carlos Pereira'},
        ],
    }
    return render(request, 'ti/dashboard.html', context)
