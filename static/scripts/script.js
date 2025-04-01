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