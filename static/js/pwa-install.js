document.addEventListener("DOMContentLoaded", () => {
    let deferredPrompt = null;

    const pwaToast = document.getElementById("pwa-toast");
    const btnInstall = document.getElementById("btn-install");
    const btnClose = document.getElementById("btn-close-toast");

    window.addEventListener("beforeinstallprompt", (e) => {
        e.preventDefault();
        deferredPrompt = e;

        if (pwaToast) pwaToast.style.display = "flex";
    });

    if (btnClose) {
        btnClose.addEventListener("click", () => {
            if (pwaToast) pwaToast.style.display = "none";
        });
    }

    if (btnInstall) {
        btnInstall.addEventListener("click", async () => {
            if (!deferredPrompt) return;

            deferredPrompt.prompt();
            const choice = await deferredPrompt.userChoice;
            console.log("Resultado da instalação:", choice.outcome);

            deferredPrompt = null;
            if (pwaToast) pwaToast.style.display = "none";
        });
    }
});
