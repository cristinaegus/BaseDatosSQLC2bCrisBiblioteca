import "https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/css/bootstrap.min.css";
import "https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/js/bootstrap.bundle.min.js";

const API = "http://127.0.0.1:8002";

function mostrarUsuarios() {
  fetch(`${API}/usuarios/`)
    .then((r) => r.json())
    .then((data) => {
      let html = data
        .map((u) => `${u.id_usuario}: ${u.nombre} ${u.apellido}`)
        .join("\n");
      document.getElementById("usuariosList").textContent = html;
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
function mostrarMateriales() {
  fetch(`${API}/materiales/`)
    .then((r) => r.json())
    .then((data) => {
      let html = data
        .map((m) => `${m.codigo_inventario}: ${m.titulo} (${m.tipo})`)
        .join("\n");
      document.getElementById("materialesList").textContent = html;
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
// Inicializar
mostrarUsuarios();
mostrarMateriales();
mostrarPrestamos();
