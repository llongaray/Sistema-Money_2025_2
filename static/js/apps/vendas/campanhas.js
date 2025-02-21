console.log(typeof jQuery !== "undefined" ? "✅ jQuery carregado!" : "❌ Erro ao carregar jQuery!");

$(document).ready(function () {
    console.log("🚀 Documento pronto! Iniciando script de campanhas...");

    // ================== VARIÁVEIS GLOBAIS ==================
    const apiGetCampanhasURL = "/vendas/api/campanhas/";
    const apiPostCampanhaURL = "/vendas/api/campanha/";
    const apiPostCampanhaStatusURL = "/vendas/api/campanha/status/";
    const apiGetEquipesURL = "/rh/api/get/";

    // ================== CARREGANDO EQUIPES ==================
    console.log("🔄 Carregando equipes...");
    carregarEquipes();

    function carregarEquipes() {
        $.getJSON(apiGetEquipesURL, function (data) {
            console.log("✅ Equipes carregadas:", data.equipes);
            preencherOpcoes("equipe_id", data.equipes);
        }).fail(function (xhr, status, error) {
            console.error("❌ Erro ao carregar equipes:", status, error);
            alert("Erro ao carregar equipes.");
        });
    }

    function preencherOpcoes(selectName, lista) {
        let select = $(`select[name=${selectName}]`);
        select.empty().append(`<option value="">Selecione...</option>`);

        lista.forEach(item => {
            select.append(`<option value="${item.id}">${item.nome}</option>`);
        });
    }

    // ================== CARREGANDO CAMPANHAS ==================
    console.log("🔄 Carregando campanhas...");
    carregarCampanhas();

    function carregarCampanhas() {
        $.getJSON(apiGetCampanhasURL, function (data) {
            console.log("✅ Campanhas carregadas:", data);
            atualizarTabela(data.campanhas);
        }).fail(function (xhr, status, error) {
            console.error("❌ Erro ao carregar campanhas:", status, error);
            alert("Erro ao carregar campanhas.");
        });
    }

    function atualizarTabela(campanhas) {
        let tbody = $("#tabela-campanhas tbody");
        tbody.empty();

        campanhas.forEach(camp => {
            let statusClass = camp.status === "ativo" ? "fa-toggle-on status-icon active" : "fa-toggle-off status-icon inactive";
            let statusColor = camp.status === "ativo" ? "style='color: #70f611;'" : "style='color: #ff4b4b;'";

            let row = `
                <tr>
                    <td>${camp.titulo}</td>
                    <td>${camp.equipe__nome}</td>
                    <td class="campanha-status-toggle" data-id="${camp.id}" data-status="${camp.status}">
                        <i class="fas ${statusClass}" ${statusColor}></i>
                    </td>
                </tr>
            `;
            tbody.append(row);
        });
    }

    // ================== ALTERAR STATUS ==================
    $(document).on("click", ".campanha-status-toggle", function () {
        let campanhaID = $(this).data("id");
        let novoStatus = $(this).data("status") === "ativo" ? "inativo" : "ativo";
        let icon = $(this).find("i");

        $.ajax({
            url: apiPostCampanhaStatusURL,
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify({ campanha_id: campanhaID }),
            success: function (response) {
                console.log("✅ Status atualizado:", response);

                if (novoStatus === "ativo") {
                    icon.removeClass("fa-toggle-off inactive").addClass("fa-toggle-on active").css("color", "#70f611");
                } else {
                    icon.removeClass("fa-toggle-on active").addClass("fa-toggle-off inactive").css("color", "#ff4b4b");
                }

                icon.closest("td").data("status", novoStatus);
            },
            error: function (xhr) {
                console.error("❌ Erro ao alterar status:", xhr);
                alert("Erro ao alterar status.");
            }
        });
    });

    // ================== ENVIO DO FORMULÁRIO ==================
    $("#form-campanha").on("submit", function (e) {
        e.preventDefault();

        let form = $(this);
        let dados = {
            titulo: form.find("input[name=titulo]").val(),
            equipe_id: form.find("select[name=equipe_id]").val()
        };

        if (!dados.titulo || !dados.equipe_id) {
            exibirMensagem("error", "Preencha todos os campos.");
            return;
        }

        console.log("📦 Enviando campanha:", dados);

        $.ajax({
            url: apiPostCampanhaURL,
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify(dados),
            success: function (response) {
                console.log("✅ Campanha criada:", response);
                exibirMensagem("success", "Campanha criada com sucesso!");
                form.trigger("reset");
                carregarCampanhas();
            },
            error: function (xhr) {
                console.error("❌ Erro ao criar campanha:", xhr);
                exibirMensagem("error", "Erro ao criar campanha.");
            }
        });
    });

    // ================== MENSAGENS DE FEEDBACK ==================
    function exibirMensagem(tipo, mensagem) {
        console.log(`🔔 Exibindo mensagem (${tipo}): ${mensagem}`);
        let msgBox = $(`<div class="campanha-feedback ${tipo}">${mensagem}</div>`);
        $("#campanha-mensagem-feedback").html(msgBox);
        setTimeout(() => msgBox.fadeOut(300, () => msgBox.remove()), 3000);
    }

    console.log("🎯 Script carregado com sucesso!");
});
