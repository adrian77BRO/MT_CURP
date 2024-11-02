const estados = [
    { nombre: "Aguascalientes", abreviatura: "AS" },
    { nombre: "Baja California", abreviatura: "BC" },
    { nombre: "Baja California Sur", abreviatura: "BS" },
    { nombre: "Campeche", abreviatura: "CC" },
    { nombre: "Chiapas", abreviatura: "CS" },
    { nombre: "Chihuahua", abreviatura: "CH" },
    { nombre: "Ciudad de México", abreviatura: "DF" },
    { nombre: "Coahuila", abreviatura: "CL" },
    { nombre: "Colima", abreviatura: "CM" },
    { nombre: "Durango", abreviatura: "DG" },
    { nombre: "Guanajuato", abreviatura: "GT" },
    { nombre: "Guerrero", abreviatura: "GR" },
    { nombre: "Hidalgo", abreviatura: "HG" },
    { nombre: "Jalisco", abreviatura: "JC" },
    { nombre: "México", abreviatura: "MC" },
    { nombre: "Michoacán", abreviatura: "MN" },
    { nombre: "Morelos", abreviatura: "MS" },
    { nombre: "Nayarit", abreviatura: "NT" },
    { nombre: "Nuevo León", abreviatura: "NL" },
    { nombre: "Oaxaca", abreviatura: "OC" },
    { nombre: "Puebla", abreviatura: "PL" },
    { nombre: "Querétaro", abreviatura: "QT" },
    { nombre: "Quintana Roo", abreviatura: "QR" },
    { nombre: "San Luis Potosí", abreviatura: "SP" },
    { nombre: "Sinaloa", abreviatura: "SL" },
    { nombre: "Sonora", abreviatura: "SR" },
    { nombre: "Tabasco", abreviatura: "TC" },
    { nombre: "Tamaulipas", abreviatura: "TS" },
    { nombre: "Tlaxcala", abreviatura: "TL" },
    { nombre: "Veracruz", abreviatura: "VZ" },
    { nombre: "Yucatán", abreviatura: "YN" },
    { nombre: "Zacatecas", abreviatura: "ZS" },
    { nombre: "Nacido en el extranjero", abreviatura: "NE" }
];

const estadoSelect = document.getElementById("estado");
estados.forEach(estado => {
    const option = document.createElement("option");
    option.value = estado.abreviatura;
    option.textContent = estado.nombre;
    estadoSelect.appendChild(option);
});

async function generarCurp() {
    const nombre = document.getElementById("nombre").value;
    const apellido_paterno = document.getElementById("apellido_paterno").value;
    const apellido_materno = document.getElementById("apellido_materno").value || "";
    const fecha_nacimiento = document.getElementById("fecha_nacimiento").value;
    const sexo = document.getElementById("sexo").value;
    const estado = document.getElementById("estado").value;

    const data = {
        nombre,
        apellido_paterno,
        apellido_materno,
        fecha_nacimiento,
        sexo,
        estado
    };

    try {
        const response = await fetch("http://127.0.0.1:5000/generar_curp", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });
        const result = await response.json();
        const resultado = document.getElementById("curpResultado");

        if (response.ok) {
            resultado.style.display = "block";
            resultado.style.backgroundColor = "green";
            resultado.textContent = `CURP generada: ${result.curp}`;
        } else {
            resultado.style.display = "block";
            resultado.style.backgroundColor = "red";
            resultado.textContent = `${result.error}`;
        }
    } catch (error) {
        document.getElementById("curpResultado").style.display = "block";
        document.getElementById("curpResultado").style.backgroundColor = "red";
        document.getElementById("curpResultado").textContent = "Error al conectar con la API.";
        console.error("Error:", error);
    }
}