function abrirArchivo() {
    var file = document.getElementById('archivo').files[0];

    if (file) {
        var fileReader = new FileReader();
        fileReader.onload = function (fileLoadedEvent) {
            var textFromFileLoaded = fileLoadedEvent.target.result;
            console.log(file.name);
            texto = textFromFileLoaded;
            nombreArchivo = file.name;
        };
        fileReader.readAsText(file, "UTF-8");
    } else {
        alert('No se pudo abrir el archivo');
    }
}

var texto = "";
var nombreArchivo = ""
var valores = []

function GenerarModelo() {
    if (texto == "") {
        alert("No hay archivo seleccionado")
    } else {
        var criterio = $("input[name='cirterioFin']:checked").val();
        console.log("Criterio: " + criterio)
        var modo = $("input[name='modoPa']:checked").val();
        console.log("Modo: " + modo)
        $.ajax({
            async: false,
            contentType: 'application/json;  charset=utf-8',
            type: "POST",
            url: "/modelo",
            data: JSON.stringify({
                csv: texto,
                criterio: criterio,
                modo: modo,
                archivo: nombreArchivo
            }),
            success: function (data, textStatus, jqXHR) {
                console.log(data)
                valores = data.solucion
                alert("Valores " + valores + " Fitness: " + data.fitness)
            },
            error: function (jqXHR, textStatus, errorThrown) {
                console.log(textStatus)
            }

        });
    }


}

function CalcularNota() {
    var pro1 = document.getElementById('proyecto1').value;
    var pro2 = document.getElementById('proyecto2').value;
    var pro3 = document.getElementById('proyecto3').value;
    var pro4 = document.getElementById('proyecto4').value;

    console.log("Proyecto 1:" + pro1);
    console.log("Proyecto 2:" + pro2);
    console.log("Proyecto 3:" + pro3);
    console.log("Proyecto 4:" + pro4);
    if (pro1 != "" && pro2 != "" && pro3 != "" && pro4 != "") {
        if (valores.length != 0) {
            var cal = valores[0] * parseFloat(pro1) + valores[1] * parseFloat(pro2) + valores[2] * parseFloat(pro3) + valores[3] * parseFloat(pro4)
            alert("La nota es: " + cal)
            document.getElementById('nota').innerHTML = "Nota: " + cal
        } else {
            alert("Falta generar modelo")
        }
    } else {
        alert("Falta ingresar notas")
    }
}
