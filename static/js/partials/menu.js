document.addEventListener("DOMContentLoaded", function () {
    const sidebar = document.getElementById("sidebar");
    const menuToggle = document.getElementById("menu-toggle");
    const toggleMenuIcon = menuToggle.querySelector("i");
    const menuItems = document.querySelectorAll(".menu-category .category-header");
    const categoryIcons = document.querySelectorAll(".toggle-category");
    const categoryTexts = document.querySelectorAll(".category-header span");
    const logo = document.querySelector(".menu-logo");

    console.log("📌 Script de menu carregado");

    // Alternar a classe 'collapsed' no menu lateral
    menuToggle.addEventListener("click", function () {
        sidebar.classList.toggle("collapsed");

        if (sidebar.classList.contains("collapsed")) {
            console.log("🔽 Menu colapsado");

            toggleMenuIcon.classList.remove("fa-chevron-left");
            toggleMenuIcon.classList.add("fa-chevron-right");

            // Esconder logo, textos das categorias e ícones de abrir/fechar categorias
            logo.style.display = "none";
            categoryTexts.forEach(span => span.style.display = "none");
            categoryIcons.forEach(icon => icon.style.display = "none");

            // Fechar todos os submenus ao colapsar
            document.querySelectorAll(".category-items").forEach(submenu => {
                submenu.classList.remove("active");
                submenu.style.maxHeight = null;
            });

            document.querySelectorAll(".toggle-category").forEach(icon => {
                icon.classList.remove("fa-chevron-up");
                icon.classList.add("fa-chevron-down");
            });

        } else {
            console.log("🔼 Menu expandido");

            toggleMenuIcon.classList.remove("fa-chevron-right");
            toggleMenuIcon.classList.add("fa-chevron-left");

            // Reexibir logo, textos das categorias e ícones de abrir/fechar categorias
            logo.style.display = "block";
            categoryTexts.forEach(span => span.style.display = "inline-block");
            categoryIcons.forEach(icon => icon.style.display = "inline-block");
        }
    });

    // Controle de submenus ao clicar nas categorias
    menuItems.forEach(item => {
        item.addEventListener("click", function () {
            const submenu = this.nextElementSibling;
            const icon = this.querySelector(".toggle-category");

            console.log(`📂 Categoria clicada: ${this.textContent.trim()}`);

            if (submenu) {
                // Expandir o menu lateral ao abrir um submenu
                if (sidebar.classList.contains("collapsed")) {
                    console.log("⏩ Menu expandido automaticamente ao abrir submenu");
                    sidebar.classList.remove("collapsed");
                    toggleMenuIcon.classList.remove("fa-chevron-right");
                    toggleMenuIcon.classList.add("fa-chevron-left");

                    // Reexibir logo, textos das categorias e ícones
                    logo.style.display = "block";
                    categoryTexts.forEach(span => span.style.display = "inline-block");
                    categoryIcons.forEach(icon => icon.style.display = "inline-block");
                }

                // Fechar outros submenus antes de abrir o atual
                document.querySelectorAll(".category-items").forEach(menu => {
                    if (menu !== submenu) {
                        menu.classList.remove("active");
                        menu.style.maxHeight = null;
                    }
                });

                document.querySelectorAll(".toggle-category").forEach(i => {
                    if (i !== icon) {
                        i.classList.add("fa-chevron-down");
                        i.classList.remove("fa-chevron-up");
                    }
                });

                // Alternar a visibilidade do submenu
                if (submenu.classList.contains("active")) {
                    console.log(`🔒 Fechando submenu: ${this.textContent.trim()}`);
                    submenu.style.maxHeight = "0px";
                    setTimeout(() => {
                        submenu.classList.remove("active");
                    }, 300);
                } else {
                    console.log(`🔓 Abrindo submenu: ${this.textContent.trim()}`);
                    submenu.classList.add("active");
                    submenu.style.maxHeight = submenu.scrollHeight + "px";
                }

                icon.classList.toggle("fa-chevron-down");
                icon.classList.toggle("fa-chevron-up");
            }
        });
    });
});
