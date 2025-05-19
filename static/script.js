async function enviarMensagem() {
    const entrada = document.getElementById("entrada");
    const mensagem = entrada.value;
    const container = document.getElementById("mensagens");

    container.innerHTML += `<div class='user'>${mensagem}</div>`;
    entrada.value = "";

    const resposta = await fetch("/perguntar", {
        method: "POST",
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ mensagem })
    });

    const dados = await resposta.json();
    container.innerHTML += `<div class='bot'>${dados.resposta}</div>`;
}