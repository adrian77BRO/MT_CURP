async function validarCurp() {
    const curp = document.getElementById('curp').value;
    const responseContainer = document.getElementById('response');
    responseContainer.textContent = '';

    try {
        const response = await fetch('http://127.0.0.1:5000/validar_curp', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ curp: curp })
        });

        const result = await response.json();

        if (response.ok) {
            responseContainer.textContent = `CURP válida: ${result.curp}`;
            responseContainer.className = 'response success';
        } else {
            responseContainer.textContent = `CURP inválida`;
            responseContainer.className = 'response error';
        }
    } catch (error) {
        responseContainer.textContent = 'Error al conectar con el servidor.';
        responseContainer.className = 'response error';
    }
}