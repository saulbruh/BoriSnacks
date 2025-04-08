document.addEventListener("DOMContentLoaded", function() {
    const logoutLink = document.getElementById("logout-link");

    if (logoutLink) {
        logoutLink.addEventListener("click", function(event) {
            const confirmLogout = confirm("Are you sure you want to log out?");
            if (!confirmLogout) {
                event.preventDefault(); // Evita que el usuario cierre sesión si cancela
            }
        });
    }

    const deleteBtn = document.getElementById("delete-account-btn");
    const confirmPopup = document.getElementById("confirm-popup");
    const passwordPopup = document.getElementById("password-popup");

    const confirmYes = document.getElementById("confirm-yes");
    const confirmCancel = document.getElementById("confirm-cancel");

    const passwordInput = document.getElementById("delete-password");
    const submitDelete = document.getElementById("submit-delete");
    const passwordCancel = document.getElementById("password-cancel");

    const hiddenPasswordInput = document.getElementById("hidden-password");
    const deleteForm = document.getElementById("delete-form");

    deleteBtn.addEventListener("click", function() {
        confirmPopup.style.display = "block";
    });

    confirmCancel.addEventListener("click", function() {
        confirmPopup.style.display = "none";
    });

    confirmYes.addEventListener("click", function() {
        confirmPopup.style.display = "none";
        passwordPopup.style.display = "block";
    });

    passwordCancel.addEventListener("click", function() {
        passwordPopup.style.display = "none";
    });

    submitDelete.addEventListener("click", function() {
        if (passwordInput.value.trim() === "") {
            alert("Por favor, ingresa tu contraseña.");
            return;
        }
        hiddenPasswordInput.value = passwordInput.value;
        deleteForm.submit();
    });
});

document.addEventListener("DOMContentLoaded", function() {
    const cartButtons = document.querySelectorAll(".btn-cart");
    const cartPopup = document.getElementById("cart-popup");

    cartButtons.forEach(button => {
        button.addEventListener("click", function() {
            cartPopup.style.display = "block";
            setTimeout(() => {
                cartPopup.style.display = "none";
            }, 2000); // Desaparece después de 2 segundos
        });
    });
});



document.addEventListener("DOMContentLoaded", function() {
    const cartForms = document.querySelectorAll("form[action$='agregar_al_carrito']");
    const cartPopup = document.getElementById("cart-popup");

    cartForms.forEach(form => {
        form.addEventListener("submit", function(event) {
            event.preventDefault(); // Previene la redirección

            const formData = new FormData(form);

            fetch(form.action, {
                method: "POST",
                body: new URLSearchParams(formData),
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded"
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    cartPopup.style.display = "block";
                    setTimeout(() => {
                        cartPopup.style.display = "none";
                    }, 2000);

                    // Opcional: actualizar el contador del carrito aquí
                } else if (data.redirect_to_login) {
                    window.location.href = data.redirect_to_login;
                } else {
                    alert("Error al agregar al carrito.");
                }
            })
            .catch(error => {
                console.error("Error:", error);
                alert("Error al agregar al carrito.");
            });
        });
    });
});

// ─────────────────────────────
// Funcionalidad de la página de carrito
// ─────────────────────────────

document.addEventListener("DOMContentLoaded", function () {
    // Botones de eliminar producto individual
    document.querySelectorAll(".btn-delete").forEach(button => {
        button.addEventListener("click", function(event) {
            event.preventDefault();
            let productoId = this.getAttribute("data-product-id");

            fetch("/eliminar_del_carrito", {
                method: "POST",
                body: new URLSearchParams({ producto_id: productoId }),
                headers: { "Content-Type": "application/x-www-form-urlencoded" }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    window.location.reload();
                } else {
                    alert("Hubo un problema al eliminar el producto.");
                }
            });
        });
    });

    // Botones para modificar cantidad
    document.querySelectorAll(".quantity-btn").forEach(container => {
        const productoId = container.getAttribute("data-product-id");
        const cantidadElem = container.querySelector(".cantidad");

        container.querySelector(".btn-sumar").addEventListener("click", () => {
            modificarCantidad(productoId, "sumar", cantidadElem);
        });

        container.querySelector(".btn-restar").addEventListener("click", () => {
            modificarCantidad(productoId, "restar", cantidadElem);
        });
    });

    function modificarCantidad(productoId, accion, cantidadElem) {
        fetch("/modificar_cantidad", {
            method: "POST",
            body: new URLSearchParams({
                producto_id: productoId,
                accion: accion
            }),
            headers: {
                "Content-Type": "application/x-www-form-urlencoded"
            }
        })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                let cantidadActual = parseInt(cantidadElem.textContent);
                if (accion === "sumar") {
                    cantidadElem.textContent = cantidadActual + 1;
                } else if (accion === "restar" && cantidadActual > 1) {
                    cantidadElem.textContent = cantidadActual - 1;
                } else {
                    location.reload();
                }
            } else {
                alert("Error: " + (data.error || "No se pudo actualizar la cantidad."));
            }
        });
    }

    // Botón para vaciar todo el carrito
    const btnRemoveAll = document.getElementById("btn-remove-all");
    if (btnRemoveAll) {
        btnRemoveAll.addEventListener("click", function () {
            fetch("/vaciar_carrito", {
                method: "POST"
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    location.reload();
                } else {
                    alert("Error al vaciar el carrito.");
                }
            });
        });
    }
});


function toggleFormulario() {
    const formulario = document.getElementById("formulario-direccion");
    if (formulario) {
        formulario.style.display = formulario.style.display === "none" ? "block" : "none";
    }
}