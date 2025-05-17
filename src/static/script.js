document.addEventListener("DOMContentLoaded", () => {
    const latitudeElem = document.getElementById("latitude");
    const longitudeElem = document.getElementById("longitude");
    const timestampElem = document.getElementById("timestamp");
    const statusMessageElem = document.getElementById("status-message");

    if (!navigator.geolocation) {
        statusMessageElem.textContent = "Geolocalização não é suportada pelo seu navegador.";
        return;
    }

    statusMessageElem.textContent = "Obtendo localização...";

    const options = {
        enableHighAccuracy: true, // Solicita a maior precisão possível
        timeout: 10000,          // Tempo máximo para obter a posição (10 segundos)
        maximumAge: 0             // Não usar cache de posições anteriores
    };

    async function sendDataToServer(latitude, longitude, timestamp) {
        try {
            const response = await fetch("/api/location", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ latitude, longitude, timestamp }),
            });
            if (response.ok) {
                console.log("Dados enviados com sucesso!");
                statusMessageElem.textContent = "Localização atualizada e enviada!";
            } else {
                console.error("Falha ao enviar dados para o servidor.");
                statusMessageElem.textContent = "Falha ao enviar dados para o servidor.";
            }
        } catch (error) {
            console.error("Erro ao conectar com o servidor:", error);
            statusMessageElem.textContent = "Erro ao conectar com o servidor.";
        }
    }

    function success(position) {
        const latitude = position.coords.latitude;
        const longitude = position.coords.longitude;
        const timestamp = new Date(position.timestamp).toLocaleString("pt-BR");

        latitudeElem.textContent = latitude.toFixed(6);
        longitudeElem.textContent = longitude.toFixed(6);
        timestampElem.textContent = timestamp;
        
        sendDataToServer(latitude, longitude, timestamp);
    }

    function error(err) {
        statusMessageElem.textContent = `Erro ao obter localização: ${err.message} (código: ${err.code})`;
        console.warn(`ERRO(${err.code}): ${err.message}`);
    }

    navigator.geolocation.watchPosition(success, error, options);
});
