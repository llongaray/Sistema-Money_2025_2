console.log(typeof jQuery !== "undefined" ? "✅ jQuery carregado!" : "❌ Erro ao carregar jQuery!");

$(document).ready(function () {
    console.log("🚀 Documento pronto! Iniciando script de novo funcionário...");

    // ================== VARIÁVEIS GLOBAIS ==================
    const apiGetURL = "/rh/api/get/";
    const apiPostURL = "/rh/api/funcionario/";

    console.log("🔄 Carregando dados iniciais...");
    carregarEmpresas();

    function carregarEmpresas() {
        $.getJSON(apiGetURL, function (data) {
            console.log("✅ Dados recebidos:", data);
            preencherOpcoes("empresa_id", data.empresas);
            esconderElementos(["departamento_id", "equipe_id", "cargo_id", "loja_id"]);
        }).fail(function (xhr, status, error) {
            console.error("❌ Erro ao carregar dados:", status, error);
            alert("Erro ao carregar dados.");
        });
    }

    function preencherOpcoes(selectName, lista, formatFn = null) {
        let select = $(`select[name=${selectName}]`);
        select.empty().append(`<option value="">Selecione...</option>`);
        lista.forEach(item => {
            let text = formatFn ? formatFn(item) : item.nome;
            select.append(`<option value="${item.id}">${text}</option>`);
        });
        select.prop("disabled", lista.length === 0);
    }

    function esconderElementos(elementos) {
        elementos.forEach(el => {
            $(`select[name=${el}]`).closest('.form-group').hide();
        });
    }

    function mostrarElemento(selectName) {
        $(`select[name=${selectName}]`).closest('.form-group').fadeIn();
    }

    function getHierarquiaNome(hierarquiaID, hierarquias) {
        let hierarquia = hierarquias.find(h => h.id == hierarquiaID);
        return hierarquia ? hierarquia.nome : "Sem Hierarquia";
    }

    // ================== EVENTOS PARA SELETORES ==================
    $("select[name=empresa_id]").on("change", function () {
        let empresaID = $(this).val();
        esconderElementos(["departamento_id", "equipe_id", "cargo_id", "loja_id"]);

        if (!empresaID) return;

        $.getJSON(apiGetURL, function (data) {
            let departamentos = data.departamentos.filter(dep => dep.empresa_id == empresaID);
            preencherOpcoes("departamento_id", departamentos);
            mostrarElemento("departamento_id");
        });
    });

    $("select[name=departamento_id]").on("change", function () {
        let departamentoID = $(this).val();
        esconderElementos(["equipe_id", "cargo_id", "loja_id"]);

        if (!departamentoID) return;

        $.getJSON(apiGetURL, function (data) {
            let equipes = data.equipes.filter(eq => eq.departamento_id == departamentoID);
            let cargos = data.cargos.filter(cargo => cargo.departamento_id == departamentoID);

            preencherOpcoes("equipe_id", equipes);
            preencherOpcoes("cargo_id", cargos, item => `${item.nome} - ${getHierarquiaNome(item.hierarquia_id, data.hierarquias)}`);

            mostrarElemento("equipe_id");
            mostrarElemento("cargo_id");
        });
    });

    $("select[name=equipe_id]").on("change", function () {
        let equipeID = $(this).val();
        esconderElementos(["loja_id"]);

        if (!equipeID) return;

        $.getJSON(apiGetURL, function (data) {
            let lojas = data.lojas.filter(loja => loja.equipe_id == equipeID);

            if (lojas.length > 0) {
                preencherOpcoes("loja_id", lojas);
                mostrarElemento("loja_id");
            }
        });
    });

    // ================== ENVIO DO FORMULÁRIO ==================
    $("#form-funcionario").on("submit", function (e) {
        e.preventDefault();
        let form = $(this);
        let formData = new FormData(form[0]);

        // Garante que a foto seja corretamente adicionada ao FormData
        let fotoInput = $("input[name=foto]")[0].files[0];
        if (fotoInput) {
            formData.append("foto", fotoInput);
        }

        console.log("📦 Enviando dados via FormData:", Object.fromEntries(formData.entries()));

        $.ajax({
            url: apiPostURL,
            type: "POST",
            processData: false,
            contentType: false,
            data: formData,
            success: function (response) {
                console.log("✅ Funcionário salvo:", response);
                exibirMensagem("success", "Funcionário cadastrado com sucesso!");
                form.trigger("reset");
                esconderElementos(["departamento_id", "equipe_id", "cargo_id", "loja_id"]);
            },
            error: function (xhr) {
                console.error("❌ Erro ao salvar:", xhr);
                let errorMsg = xhr.responseJSON ? xhr.responseJSON.error : "Erro desconhecido.";
                exibirMensagem("error", `Erro ao salvar funcionário: ${errorMsg}`);
            }
        });
    });

    // ================== MENSAGENS DE FEEDBACK ==================
    function exibirMensagem(tipo, mensagem) {
        let msgBox = $(`<div class="msg-${tipo}">${mensagem}</div>`);
        $("#mensagem-feedback").html(msgBox);
        setTimeout(() => msgBox.fadeOut(300, () => msgBox.remove()), 3000);
    }

    console.log("🎯 Script carregado com sucesso!");
});
