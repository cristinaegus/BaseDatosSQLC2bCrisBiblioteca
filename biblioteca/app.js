const API = "http://127.0.0.1:8010";

function mostrarUsuarios() {
  fetch(`${API}/usuarios/`)
    .then((r) => r.json())
    .then((data) => {
      let html = data
        .map(
          (u) =>
            `${u.id_usuario}: ${u.nombre} ${u.apellido} <button class='btn btn-danger btn-sm ms-2' onclick="borrarUsuario('${u.id_usuario}')">Borrar</button>`
        )
        .join("\n");
      document.getElementById("usuariosList").innerHTML = html;
      // Para el select de préstamos
      let select = document.getElementById("usuarioPrestamo");
      select.innerHTML =
        '<option value="">Usuario</option>' +
        data
          .map(
            (u) =>
              `<option value="${u.id_usuario}">${u.nombre} ${u.apellido}</option>`
          )
          .join("");
    });
}

function borrarUsuario(id_usuario) {
  if (!confirm("¿Seguro que quieres borrar este usuario?")) return;
  fetch(`${API}/usuarios/${id_usuario}`, {
    method: "DELETE",
  })
    .then((r) => {
      if (!r.ok)
        return r.json().then((d) => {
          throw d;
        });
      return r.json();
    })
    .then(() => mostrarUsuarios())
    .catch((err) => alert(err.detail || "Error al borrar usuario"));
}

function mostrarMateriales() {
  fetch(`${API}/materiales/`)
    .then((r) => r.json())
    .then((data) => {
      let html = data
        .map(
          (m) =>
            `${m.codigo_inventario}: ${m.titulo} (${m.tipo}) <button class='btn btn-danger btn-sm ms-2' onclick="borrarMaterial('${m.codigo_inventario}')">Borrar</button>`
        )
        .join("\n");
      document.getElementById("materialesList").innerHTML = html;
      // Para el select de préstamos
      let select = document.getElementById("materialPrestamo");
      select.innerHTML =
        '<option value="">Material</option>' +
        data
          .map(
            (m) => `<option value="${m.codigo_inventario}">${m.titulo}</option>`
          )
          .join("");
    });
}

function borrarMaterial(codigo_inventario) {
  if (!confirm("¿Seguro que quieres borrar este material?")) return;
  fetch(`${API}/materiales/${codigo_inventario}`, {
    method: "DELETE",
  })
    .then((r) => {
      if (!r.ok)
        return r.json().then((d) => {
          throw d;
        });
      return r.json();
    })
    .then(() => mostrarMateriales())
    .catch((err) => alert(err.detail || "Error al borrar material"));
}

function mostrarPrestamos() {
  fetch(`${API}/prestamos/`)
    .then((r) => r.json())
    .then((data) => {
      let html = data
        .map(
          (p) =>
            `Usuario: ${p.id_usuario} → Material: ${p.id_material}\nPréstamo: ${p.fecha_prestamo}\nDevolución: ${p.fecha_devolucion}\n---`
        )
        .join("\n");
      document.getElementById("prestamosList").textContent = html;
    });
}
// Agregar usuario

document.getElementById("formUsuario").onsubmit = function (e) {
  e.preventDefault();
  fetch(`${API}/usuarios/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      nombre: document.getElementById("nombreUsuario").value,
      apellido: document.getElementById("apellidoUsuario").value,
    }),
  }).then(() => {
    mostrarUsuarios();
    document.getElementById("formUsuario").reset();
  });
};
// Agregar material

document.getElementById("formMaterial").onsubmit = function (e) {
  e.preventDefault();
  fetch(`${API}/materiales/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      tipo: document.getElementById("tipoMaterial").value,
      titulo: document.getElementById("tituloMaterial").value,
      autor: document.getElementById("autorMaterial").value,
      isbn: document.getElementById("isbnMaterial").value,
      numero_paginas: document.getElementById("paginasMaterial").value
        ? parseInt(document.getElementById("paginasMaterial").value)
        : null,
      fecha_publicacion: document.getElementById("fechaPublicacionMaterial")
        .value,
      numero_edicion: document.getElementById("edicionMaterial").value,
      duracion: document.getElementById("duracionMaterial").value
        ? parseInt(document.getElementById("duracionMaterial").value)
        : null,
      director: document.getElementById("directorMaterial").value,
    }),
  }).then(() => {
    mostrarMateriales();
    document.getElementById("formMaterial").reset();
  });
};
// Crear préstamo

document.getElementById("formPrestamo").onsubmit = function (e) {
  e.preventDefault();
  fetch(`${API}/prestamos/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      id_usuario: document.getElementById("usuarioPrestamo").value,
      id_material: document.getElementById("materialPrestamo").value,
      fecha_prestamo: document.getElementById("fechaPrestamo").value,
      fecha_devolucion: document.getElementById("fechaDevolucion").value,
    }),
  }).then(() => {
    mostrarPrestamos();
    document.getElementById("formPrestamo").reset();
  });
};
// ========== RESEÑAS ========== //
// Mostrar reseñas
function mostrarResenias() {
  fetch(`${API}/resenias/`)
    .then((r) => r.json())
    .then((data) => {
      let html = data
        .map(
          (r) =>
            `<b>Material:</b> ${r.id_material} <b>Usuario:</b> ${r.id_usuario}<br><b>Reseña:</b> ${r.resenia || r.texto}<br><b>Puntuación:</b> ${r.puntuacion || r.calificacion}<br><b>Fecha:</b> ${r.fecha || ''}<hr>`
        )
        .join("");
      document.getElementById("reseniasList").innerHTML = html || "Sin reseñas";
    });
}
// Crear reseña
function crearResenia(e) {
  e.preventDefault();
  fetch(`${API}/resenias/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      id_material: document.getElementById("idMaterialResenia").value,
      id_usuario: document.getElementById("idUsuarioResenia").value,
      resenia: document.getElementById("textoResenia").value,
      puntuacion: parseInt(document.getElementById("puntuacionResenia").value),
      fecha: document.getElementById("fechaResenia").value,
    }),
  })
    .then((r) => {
      if (!r.ok) return r.json().then((d) => { throw d; });
      return r.json();
    })
    .then(() => {
      mostrarResenias();
      document.getElementById("formResenia").reset();
    })
    .catch((err) => alert(err.detail || "Error al crear reseña"));
}
// Inicializar
mostrarUsuarios();
mostrarMateriales();
mostrarPrestamos();
mostrarResenias();
