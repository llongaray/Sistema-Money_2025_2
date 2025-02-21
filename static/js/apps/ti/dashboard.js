document.addEventListener("DOMContentLoaded", function() {
    console.log("📌 Dashboard de TI carregado com sucesso!");

    // Exemplo: Evento de clique nos botões de edição e remoção de equipamentos
    document.querySelectorAll(".btn-edit").forEach(btn => {
        btn.addEventListener("click", function() {
            alert("Editar equipamento ainda não implementado!");
        });
    });

    document.querySelectorAll(".btn-delete").forEach(btn => {
        btn.addEventListener("click", function() {
            if (confirm("Tem certeza que deseja remover este equipamento?")) {
                alert("Equipamento removido!");
            }
        });
    });

    // Exemplo: Evento de adicionar equipamento
    document.querySelector(".btn-add")?.addEventListener("click", function() {
        alert("Adicionar novo equipamento ainda não implementado!");
    });
});
