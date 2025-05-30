async function enviarMensagem() {
    const entrada = document.getElementById("entrada");
    const mensagem = entrada.value.trim();
    const container = document.getElementById("mensagens");

    if (!mensagem) return;

    container.innerHTML += `
        <div class="mensagem user">
            <strong>Usuário:</strong> ${mensagem}
        </div>
    `;
    entrada.value = "";
    container.scrollTop = container.scrollHeight;

    const resposta = await fetch("/perguntar", {
        method: "POST",
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ mensagem })
    });

    const dados = await resposta.json();

    container.innerHTML += `
        <div class="mensagem bot">
            <strong>Bot:</strong> ${dados.resposta}
        </div>
    `;
    container.scrollTop = container.scrollHeight;
}

document.getElementById("entrada").addEventListener("keydown", function(event) {
    if (event.key === "Enter") {
        event.preventDefault(); // Impede quebra de linha
        enviarMensagem();
    }
});