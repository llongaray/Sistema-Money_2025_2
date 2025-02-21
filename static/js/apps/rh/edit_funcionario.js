$(document).ready(function () {
    console.log("🚀 Script de edição de funcionário carregado!");

    // URLs das APIs
    const apiGetDados = "/rh/api/get/";
    const apiEditFuncionario = "/rh/api/funcionario/editar/";

    let dadosGlobais = {}; // Armazena todos os dados da API para facilitar a busca

    // Carregar funcionários e dados iniciais
    carregarDadosIniciais();

    function carregarDadosIniciais() {
        $.getJSON(apiGetDados, function (data) {
            console.log("✅ Dados carregados:", data);

            if (!data || typeof data !== 'object') {
                console.error("❌ Dados inválidos recebidos da API.");
                return;
            }

            dadosGlobais = data;

            // Garantir que as listas existem antes de tentar preenchê-las
            atualizarSelectFuncionarios(data.funcionarios || []);
            atualizarSelectsProfissionais(data);
        }).fail(function () {
            console.error("❌ Erro ao carregar dados");
        });
    }

    function atualizarSelectFuncionarios(lista) {
        let select = $("#select-funcionario");
        select.empty().append(`<option value="">Selecione um funcionário</option>`);
        lista.forEach(func => {
            select.append(`<option value="${func.id}">${func.nome_completo} - ${func.cpf}</option>`);
        });
    }

    function atualizarSelectsProfissionais(data) {
        preencherSelect("#empresa", data.empresas || []);
        preencherSelect("#departamento", data.departamentos || []);
        preencherSelect("#cargo", data.cargos || []);
        preencherSelect("#hierarquia", data.hierarquias || []);
        preencherSelect("#equipe", data.equipes || []);
        preencherSelect("#loja", data.lojas || []);
        preencherSelect("#horario", data.horarios || []);
    }

    function preencherSelect(selector, lista) {
        let select = $(selector);
        select.empty().append(`<option value="">Selecione</option>`);

        if (!Array.isArray(lista)) {
            console.warn(`⚠️ Lista inválida para ${selector}`);
            return;
        }

        lista.forEach(item => {
            if (item && item.id && item.nome) {
                select.append(`<option value="${item.id}">${item.nome}</option>`);
            }
        });
    }

    // Filtro em tempo real para o select de funcionários
    $("#filtro-funcionario").on("input", function () {
        let filtro = $(this).val().toLowerCase();
        $("#select-funcionario option").each(function () {
            let texto = $(this).text().toLowerCase();
            $(this).toggle(texto.includes(filtro));
        });
    });

    // Carregar dados do funcionário ao selecionar no select
    $("#select-funcionario").on("change", function () {
        let funcionarioID = $(this).val();
        if (funcionarioID) {
            carregarDadosFuncionario(funcionarioID);
        } else {
            $("#funcionario-info, #funcionario-arquivos").hide();
        }
    });

    function carregarDadosFuncionario(funcionarioID) {
        let funcionario = (dadosGlobais.funcionarios || []).find(f => f.id == funcionarioID);

        if (funcionario) {
            preencherFormulario(funcionario);
            carregarArquivosFuncionario(funcionarioID);

            // Exibir a seção do formulário de edição
            $("#funcionario-info").fadeIn();
        } else {
            console.error("❌ Funcionário não encontrado.");
        }
    }

    function preencherFormulario(funcionario) {
        $("#form-editar-funcionario")[0].reset(); // Limpa o form antes de preencher

        // Preenche os inputs com os dados existentes
        Object.keys(funcionario).forEach(campo => {
            let input = $(`#${campo}`);
            if (input.length && funcionario[campo]) {
                input.val(funcionario[campo]);
            }
        });

        // Preenche os selects de Informações Profissionais com os nomes das relações
        setSelectValue("#empresa", funcionario.empresa_id, dadosGlobais.empresas || []);
        setSelectValue("#departamento", funcionario.departamento_id, dadosGlobais.departamentos || []);
        setSelectValue("#cargo", funcionario.cargo_id, dadosGlobais.cargos || []);
        setSelectValue("#hierarquia", funcionario.hierarquia_id, dadosGlobais.hierarquias || []);
        setSelectValue("#equipe", funcionario.equipe_id, dadosGlobais.equipes || []);
        setSelectValue("#loja", funcionario.loja_id, dadosGlobais.lojas || []);
        setSelectValue("#horario", funcionario.horario_id, dadosGlobais.horarios || []);
    }

    function setSelectValue(selector, id, lista) {
        let select = $(selector);

        if (!Array.isArray(lista)) {
            console.warn(`⚠️ Lista inválida para ${selector}`);
            return;
        }

        let item = lista.find(i => i.id == id);
        if (item) {
            select.val(id);
        }
    }

    function carregarArquivosFuncionario(funcionarioID) {
        let tbody = $(".funcionario-table tbody");
        tbody.empty();
        let arquivosDoFuncionario = (dadosGlobais.arquivos_funcionarios || []).filter(arq => arq.funcionario_id == funcionarioID);
        if (arquivosDoFuncionario.length === 0) {
            tbody.append(`<tr><td colspan="3">Nenhum arquivo encontrado</td></tr>`);
        } else {
            arquivosDoFuncionario.forEach(arq => {
                tbody.append(`
                    <tr>
                        <td><a href="${arq.file}" target="_blank">${arq.titulo}</a></td>
                        <td>${arq.file}</td>
                        <td>${new Date(arq.data_importacao).toLocaleDateString()}</td>
                    </tr>
                `);
            });
        }

        // Exibir a seção de arquivos se houver arquivos
        if (arquivosDoFuncionario.length > 0) {
            $("#funcionario-arquivos").fadeIn();
        }
    }

    // Envio do formulário para editar funcionário
    $("#form-editar-funcionario").on("submit", function (e) {
        e.preventDefault();

        let funcionarioID = $("#select-funcionario").val();
        if (!funcionarioID) {
            alert("Selecione um funcionário antes de salvar!");
            return;
        }

        let dadosAtualizados = { id: funcionarioID };
        $(this).find("input, select").each(function () {
            if ($(this).val()) {
                dadosAtualizados[$(this).attr("name")] = $(this).val();
            }
        });

        console.log("📤 Enviando atualização:", dadosAtualizados);

        $.ajax({
            url: apiEditFuncionario,
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify(dadosAtualizados),
            success: function (response) {
                console.log("✅ Funcionário atualizado:", response);
                alert("Funcionário atualizado com sucesso!");

                // 🔄 Após atualização, recarregar os dados
                carregarDadosIniciais();
                
                // 🔄 Atualizar o formulário com os novos dados
                setTimeout(() => {
                    carregarDadosFuncionario(funcionarioID);
                }, 1000);
            },
            error: function (xhr) {
                console.error("❌ Erro ao atualizar funcionário:", xhr);
                alert("Erro ao atualizar funcionário.");
            }
        });
    });

});
