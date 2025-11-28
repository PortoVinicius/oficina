let deferredPrompt = null;

const pwaToast = document.getElementById("pwa-toast");
const btnInstall = document.getElementById("btn-install");
const btnClose = document.getElementById("btn-close-toast");

// Captura o evento antes da instalação
window.addEventListener("beforeinstallprompt", (e) => {
    e.preventDefault();
    deferredPrompt = e;

    // Mostra o toast
    if (pwaToast) {
        pwaToast.style.display = "flex";
    }
});

// Botão "Agora não"
if (btnClose) {
    btnClose.addEventListener("click", () => {
        pwaToast.style.display = "none";
    });
}

// Botão "Instalar"
if (btnInstall) {
    btnInstall.addEventListener("click", async () => {
        if (!deferredPrompt) return;

        deferredPrompt.prompt(); // Mostra popup oficial
        const choice = await deferredPrompt.userChoice;

        console.log("Resultado da instalação:", choice.outcome);

        deferredPrompt = null;
        pwaToast.style.display = "none"; // Fecha o toast
    });
}
