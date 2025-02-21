console.log(typeof jQuery !== "undefined" ? "✅ jQuery carregado!" : "❌ Erro ao carregar jQuery!");

$(document).ready(function () {
    console.log("🚀 Documento pronto! Iniciando script de criação de usuário...");

    // ================== VARIÁVEIS GLOBAIS ==================
    const apiGetURL = "/rh/api/get/";  
    const apiPostURL = "/rh/api/usuario/";

    console.log("🔄 Carregando funcionários sem usuário...");
    carregarFuncionarios();

    function carregarFuncionarios() {
        $.getJSON(apiGetURL, function (data) {
            console.log("✅ Dados recebidos:", data);

            // Filtra apenas funcionários sem usuário vinculado
            let funcionariosSemUsuario = data.funcionarios.filter(func => !func.usuario_id);
            preencherOpcoes("funcionario_id", funcionariosSemUsuario);

        }).fail(function (xhr, status, error) {
            console.error("❌ Erro ao carregar funcionários:", status, error);
            alert("Erro ao carregar funcionários.");
        });
    }

    function preencherOpcoes(selectName, lista) {
        let select = $(`select[name=${selectName}]`);
        select.empty().append(`<option value="">Selecione...</option>`);

        lista.forEach(item => {
            select.append(`<option value="${item.id}">${item.nome_completo} - ${item.cpf}</option>`);
        });
    }

    // ================== VERIFICAÇÃO DE USERNAME EM TEMPO REAL ==================
    $("input[name=username]").on("input", function () {
        let username = $(this).val().trim();
        if (!username) return;

        $.getJSON(apiGetURL, function (data) {
            let usuarioExistente = data.usuarios.some(user => user.username === username);

            if (usuarioExistente) {
                $("#username-feedback").text("⚠️ Nome de usuário já existe. Escolha outro.").css("color", "red");
                $("input[name=username]").addClass("input-error");
            } else {
                $("#username-feedback").text("✅ Nome de usuário disponível.").css("color", "green");
                $("input[name=username]").removeClass("input-error");
            }
        });
    });

    // ================== VALIDAÇÃO DE SENHA ==================
    $("input[name=password]").on("input", function () {
        let password = $(this).val();
        let regex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@._])[A-Za-z\d@._]{8,}$/;

        if (!regex.test(password)) {
            $("#password-feedback").text("⚠️ A senha deve conter pelo menos 8 caracteres, incluindo 1 letra maiúscula, 1 minúscula, 1 número e 1 caractere especial (@._).").css("color", "red");
            $("input[name=password]").addClass("input-error");
        } else {
            $("#password-feedback").text("✅ Senha válida.").css("color", "green");
            $("input[name=password]").removeClass("input-error");
        }
    });

    // ================== EVENTO DE FORMULÁRIO ==================
    console.log("🖊️ Adicionando evento de formulário...");
    $("#form-usuario").on("submit", function (e) {
        e.preventDefault();

        let form = $(this);
        let dados = coletarDados(form);

        // Bloqueia envio caso haja erros no username ou senha
        if ($(".input-error").length > 0) {
            exibirMensagem("error", "Corrija os erros antes de enviar.", form);
            return;
        }

        console.log("📦 Dados coletados:", dados);
        enviarFormulario(apiPostURL, dados, form);
    });

    function coletarDados(form) {
        let dados = {};
        form.find("input, select").each(function () {
            let name = $(this).attr("name");
            let value = $(this).val();
            if (value) dados[name] = value;
        });

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
                console.log("✅ Usuário criado com sucesso:", response);
                exibirMensagem("success", "Usuário cadastrado com sucesso!", form);
                form.trigger("reset");
                $("#username-feedback, #password-feedback").text("");
                carregarFuncionarios(); // Atualiza a lista de funcionários disponíveis
            },
            error: function (xhr) {
                let msg = xhr.responseJSON ? xhr.responseJSON.error : "Erro ao criar usuário.";
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

    console.log("🎯 Script carregado com sucesso!");
});
