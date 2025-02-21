console.log(typeof jQuery !== "undefined" ? "✅ jQuery carregado!" : "❌ Erro ao carregar jQuery!");

$(document).ready(function () {
    console.log("🚀 Documento pronto! Iniciando script de arquivos de funcionários...");

    // ================== VARIÁVEIS GLOBAIS ==================
    const apiGetURL = "/rh/api/get/";
    const apiPostURL = "/rh/api/arquivos-funcionario/";

    console.log("🔄 Carregando funcionários...");
    carregarFuncionarios();

    function carregarFuncionarios() {
        $.getJSON(apiGetURL, function (data) {
            console.log("✅ Dados recebidos:", data);
            preencherOpcoesFuncionarios(data.funcionarios);
            $("#select-funcionario").data("arquivos", data.arquivos_funcionarios);
        }).fail(function (xhr, status, error) {
            console.error("❌ Erro ao carregar funcionários:", status, error);
            alert("Erro ao carregar funcionários.");
        });
    }

    function preencherOpcoesFuncionarios(funcionarios) {
        let select = $("#select-funcionario");
        select.empty().append(`<option value="">Selecione um funcionário</option>`);

        funcionarios.forEach(func => {
            select.append(`<option value="${func.id}">${func.nome_completo} - ${func.cpf}</option>`);
        });

        $("#filtro-funcionario").data("lista-funcionarios", funcionarios);
    }

    // ================== FILTRAGEM EM TEMPO REAL ==================
    $("#filtro-funcionario").on("input", function () {
        let filtro = $(this).val().toLowerCase();
        let funcionarios = $(this).data("lista-funcionarios") || [];

        let funcionariosFiltrados = funcionarios.filter(func => 
            func.nome_completo.toLowerCase().includes(filtro)
        );

        let select = $("#select-funcionario");
        select.empty().append(`<option value="">Selecione um funcionário</option>`);

        funcionariosFiltrados.forEach(func => {
            select.append(`<option value="${func.id}">${func.nome_completo} - ${func.cpf}</option>`);
        });
    });

    // ================== VERIFICAR SE O TÍTULO JÁ EXISTE ==================
    $("input[name=titulo]").on("input", function () {
        verificarTituloExistente();
    });

    $("#select-funcionario").on("change", function () {
        verificarTituloExistente();
    });

    function verificarTituloExistente() {
        let tituloDigitado = $("input[name=titulo]").val().trim().toLowerCase();
        let funcionarioID = $("#select-funcionario").val();
        let botaoSubmit = $("button[type=submit]");
        let tituloFeedback = $("#titulo-feedback");

        // Se não houver funcionário selecionado ou título, não faz a verificação
        if (!tituloDigitado || !funcionarioID) {
            botaoSubmit.prop("disabled", false);
            tituloFeedback.text("").css("color", "");
            return;
        }

        let arquivos = $("#select-funcionario").data("arquivos") || [];

        let tituloExiste = arquivos.some(arquivo => 
            arquivo.funcionario_id == funcionarioID && 
            arquivo.titulo.toLowerCase() === tituloDigitado
        );

        if (tituloExiste) {
            tituloFeedback.text("⚠️ Título já cadastrado para este funcionário. Escolha outro.").css("color", "red");
            $("input[name=titulo]").addClass("input-error");
            botaoSubmit.prop("disabled", true);
        } else {
            tituloFeedback.text("✅ Título disponível.").css("color", "green");
            $("input[name=titulo]").removeClass("input-error");
            botaoSubmit.prop("disabled", false);
        }
    }

    // ================== ENVIO DO FORMULÁRIO ==================
    $("#form-arquivo-funcionario").on("submit", function (e) {
        e.preventDefault();

        let form = $(this);
        let formData = new FormData(form[0]);

        if ($(".input-error").length > 0) {
            exibirMensagem("error", "Corrija os erros antes de enviar.");
            return;
        }

        console.log("📦 Enviando dados:", Object.fromEntries(formData.entries()));

        $.ajax({
            url: apiPostURL,
            type: "POST",
            processData: false,
            contentType: false,
            data: formData,
            success: function (response) {
                console.log("✅ Arquivo salvo com sucesso:", response);
                exibirMensagem("success", "Arquivo cadastrado com sucesso!");
                form.trigger("reset");
                verificarTituloExistente(); // Atualiza verificação de título após reset
            },
            error: function (xhr) {
                console.error("❌ Erro ao salvar arquivo:", xhr);
                let errorMsg = xhr.responseJSON ? xhr.responseJSON.error : "Erro desconhecido.";
                exibirMensagem("error", `Erro ao salvar arquivo: ${errorMsg}`);
            }
        });
    });

    // ================== MENSAGENS DE FEEDBACK ==================
    function exibirMensagem(tipo, mensagem) {
        console.log(`🔔 Exibindo mensagem (${tipo}): ${mensagem}`);
        let msgBox = $(`<div class="msg-${tipo}">${mensagem}</div>`);
        $("#mensagem-feedback").html(msgBox);
        setTimeout(() => msgBox.fadeOut(300, () => msgBox.remove()), 3000);
    }

    console.log("🎯 Script carregado com sucesso!");
});
