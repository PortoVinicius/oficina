let deferredPrompt = null;

// Espera o browser permitir a instalação
window.addEventListener('beforeinstallprompt', (e) => {
    e.preventDefault();
    deferredPrompt = e;

    const toast = document.getElementById('pwa-toast');
    toast.style.display = 'flex'; // mostra o toast
});

// Usuário clicou no botão Instalar
document.getElementById("btn-install").addEventListener("click", async () => {
    if (!deferredPrompt) return;

    deferredPrompt.prompt();

    const result = await deferredPrompt.userChoice;

    if (result.outcome === "accepted") {
        console.log("Usuário instalou o app");
    } else {
        console.log("Usuário cancelou a instalação");
    }

    deferredPrompt = null;

    document.getElementById('pwa-toast').style.display = 'none';
});

// Botão fechar
document.getElementById("btn-close-toast").addEventListener("click", () => {
    document.getElementById('pwa-toast').style.display = 'none';
});
