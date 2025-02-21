console.log(typeof jQuery !== "undefined" ? "✅ jQuery carregado!" : "❌ Erro ao carregar jQuery!");

$(document).ready(function () {
    console.log("🚀 Documento pronto! Iniciando script de categorias...");

    // ================== VARIÁVEIS GLOBAIS ==================
    const apiGetURL = "/rh/api/get/";  
    const apiPostURLs = {
        empresa: "/rh/api/empresa/",
        hierarquia: "/rh/api/hierarquia/",
        departamento: "/rh/api/departamento/",
        equipe: "/rh/api/equipe/",
        cargo: "/rh/api/cargo/",
        loja: "/rh/api/loja/",
        horario: "/rh/api/horario/", // 🚀 Adicionando API de Horário
        funcionario: "/rh/api/funcionario/",
        usuario: "/rh/api/usuario/",
        arquivos_funcionario: "/rh/api/arquivos-funcionario/"
    };

    // ================== INICIALIZAÇÃO ==================
    console.log("🔄 Carregando dados iniciais...");
    carregarDados();

    function carregarDados() {
        console.log(`📡 Fazendo requisição GET para: ${apiGetURL}`);
        $.getJSON(apiGetURL, function (data) {
            console.log("✅ Dados recebidos com sucesso:", data);
            preencherSelects(data);
        }).fail(function (xhr, status, error) {
            console.error("❌ Erro ao carregar dados:", status, error);
            alert("Erro ao carregar dados.");
        });
    }

    function preencherSelects(data) {
        console.log("📌 Preenchendo selects com os dados recebidos...");
        preencherOpcoes("empresa_id", data.empresas);
        preencherOpcoes("hierarquia_id", data.hierarquias);
        preencherOpcoes("departamento_id", data.departamentos);
        preencherOpcoes("equipe_id", data.equipes);
        preencherOpcoes("horario_id", data.horarios); // 🚀 Preenchendo o select de horários
    }

    function preencherOpcoes(selectName, lista) {
        console.log(`📋 Preenchendo select: ${selectName} com ${lista.length} opções`);
        let select = $(`select[name=${selectName}]`);
        select.empty().append(`<option value="">Selecione...</option>`);
        lista.forEach(item => {
            select.append(`<option value="${item.id}">${item.nome}</option>`);
        });
    }

    // ================== EVENTOS DE FORMULÁRIOS ==================
    console.log("🖊️ Adicionando eventos de formulário...");
    $("form").on("submit", function (e) {
        e.preventDefault();
        let form = $(this);
        let formID = form.attr("id").split("-")[1]; 
        console.log(`📩 Submetendo formulário: ${formID}`);
        
        let dados = coletarDados(form);
        console.log("📦 Dados coletados:", dados);

        if (!apiPostURLs[formID]) {
            console.error(`❌ URL de API não encontrada para: ${formID}`);
            return;
        }

        enviarFormulario(apiPostURLs[formID], dados, form);
    });

    function coletarDados(form) {
        let dados = {};
        
        form.find("input, select").each(function () {
            let name = $(this).attr("name");
            let value = $(this).val();
            if (value) {
                dados[name] = value;
            }
        });
    
        // Garante que status seja sempre enviado
        if (!dados.hasOwnProperty("status")) {
            dados["status"] = "ativo";  
        }
    
        // Verifica se todos os campos obrigatórios foram preenchidos
        if (form.attr("id") === "form-cargo") {
            const requiredFields = ["departamento_id", "hierarquia_id", "nome", "status"];
            for (let field of requiredFields) {
                if (!dados[field]) {
                    console.error(`❌ Campo obrigatório ausente: ${field}`);
                    exibirMensagem("error", `Campo obrigatório ausente: ${field}`, form);
                    return null;  // Retorna `null` para impedir o envio do formulário
                }
            }
        }
    
        console.log("📊 Dados extraídos do formulário:", dados);
        return dados;
    }
    
    
    function enviarFormulario(url, dados, form) {
        console.log(`🚀 Enviando requisição POST para: ${url}`, dados);
        $.ajax({
            url: url,
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify(dados),
            success: function (response) {
                console.log("✅ Resposta do servidor:", response);
                exibirMensagem("success", "Registro salvo com sucesso!", form);
                carregarDados(); 
                form.trigger("reset");
            },
            error: function (xhr) {
                let msg = xhr.responseJSON ? xhr.responseJSON.error : "Erro ao salvar.";
                console.error("❌ Erro na requisição POST:", msg);
                exibirMensagem("error", msg, form);
            }
        });
    }

    // ================== MENSAGENS DE FEEDBACK ==================
    function exibirMensagem(tipo, mensagem, form) {
        console.log(`🔔 Exibindo mensagem (${tipo}): ${mensagem}`);
        let msgBox = $("<div>").addClass(`msg-${tipo}`).text(mensagem);
        form.append(msgBox);
        setTimeout(() => msgBox.fadeOut(300, () => msgBox.remove()), 3000);
    }

    // ================== LÓGICA ESPECÍFICA POR FORMULÁRIO ==================
    console.log("📌 Configurando eventos para selects dinâmicos...");

    $("select[name=empresa_id]").on("change", function () {
        let empresaID = $(this).val();
        console.log(`🏢 Empresa selecionada: ${empresaID}`);
        if (!empresaID) return;

        $.getJSON(apiGetURL, function (data) {
            let departamentosFiltrados = data.departamentos.filter(dep => dep.empresa_id == empresaID);
            console.log(`🔍 Departamentos filtrados para Empresa ${empresaID}:`, departamentosFiltrados);
            preencherOpcoes("departamento_id", departamentosFiltrados);

            let hierarquiasFiltradas = data.hierarquias.filter(h => h.empresa_id == empresaID);
            console.log(`🔍 Hierarquias filtradas para Empresa ${empresaID}:`, hierarquiasFiltradas);
            preencherOpcoes("hierarquia_id", hierarquiasFiltradas);
        });
    });

    $("select[name=departamento_id]").on("change", function () {
        let departamentoID = $(this).val();
        console.log(`📂 Departamento selecionado: ${departamentoID}`);
        if (!departamentoID) return;

        $.getJSON(apiGetURL, function (data) {
            let equipesFiltradas = data.equipes.filter(eq => eq.departamento_id == departamentoID);
            console.log(`🔍 Equipes filtradas para Departamento ${departamentoID}:`, equipesFiltradas);
            preencherOpcoes("equipe_id", equipesFiltradas);
        });
    });

    console.log("🎯 Script carregado com sucesso!");
});
