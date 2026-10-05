import json
import os
import streamlit as st

DATA_FILE = "clientes.json"


def cargar_datos():
  if not os.path.exists(DATA_FILE):
    return {}
  with open(DATA_FILE, "r", encoding="utf-8") as f:
    try:
      return json.load(f)
    except json.JSONDecodeError:
      return {}


def guardar_datos(datos):
  with open(DATA_FILE, "w", encoding="utf-8") as f:
    json.dump(datos, f, ensure_ascii=False, indent=4)


st.sidebar.title("💈 Blood Pact AQP")
menu = st.sidebar.radio(
    "Acción",
    [
        "Agregar o Buscar Cliente",
        "Registrar Corte",
        "Eliminar Cliente",
    ],  # <-- Añadimos la opción aquí
)

clientes = cargar_datos()

if menu == "Agregar o Buscar Cliente":
  st.title("✂️ Blood Pact AQP")
  st.subheader("Programa de Fidelidad de Barbería")

  st.markdown("### 📋 Lista de Clientes")
  busqueda = st.text_input(
      "🔍 Buscar cliente por nombre o teléfono", value=""
  ).lower()

  if not clientes:
    st.info(
        "Aún no hay clientes registrados. Usa el formulario de la izquierda"
        " para agregar uno."
    )
  else:
    for cel, info in clientes.items():
      nombre = info.get("nombre", "")
      cortes = info.get("cortes", 0)

      if (
          busqueda in nombre.lower()
          or busqueda in cel
          or busqueda == ""
      ):
        with st.container():
          st.markdown(f"### 👤 {nombre}")
          st.markdown(f"📱 **Celular:** {cel}")
          st.markdown(f"✂️ **Cortes acumulados:** {cortes}")

          # Lógica visual de la tarjeta (ej: cada 10 cortes un premio)
          meta = 10
          cortes_actuales = cortes % meta
          tijeras = "✂️" * cortes_actuales
          regalo = "🎁" if cortes_actuales >= 5 else "🎁"
          restantes = meta - cortes_actuales

          tarjeta_str = ""
          for i in range(meta):
            if i < cortes_actuales:
              tarjeta_str += "✂️️ "
            elif i == 4:
              tarjeta_str += "🎁 "
            else:
              tarjeta_str += "⚪ "

          st.markdown(f"**Tarjeta:**\n\n{tarjeta_str}")
          st.info(f"Te faltan {restantes} cortes para tu CORTE GRATIS")
          st.markdown("---")

  st.sidebar.markdown("---")
  st.sidebar.subheader("Registrar / Actualizar Cliente")
  with st.sidebar.form("form_cliente"):
    celular_input = st.text_input("Celular del Cliente")
    nombre_input = st.text_input("Nombre del Cliente")
    cortes_input = st.number_input(
        "Cortes acumulados", min_value=0, step=1, value=0
    )
    submit_btn = st.form_submit_button("Guardar Cliente")

    if submit_btn:
      if celular_input and nombre_input:
        clientes[celular_input] = {
            "nombre": nombre_input,
            "cortes": int(cortes_input),
        }
        guardar_datos(clientes)
        st.sidebar.success(f"¡Cliente {nombre_input} guardado con éxito!")
        st.rerun()
      else:
        st.sidebar.error("Por favor completa el celular y el nombre.")

elif menu == "Registrar Corte":
  st.title("➕ Registrar Corte")
  st.subheader("Suma un corte a un cliente existente")

  if not clientes:
    st.warning("No hay clientes registrados en la base de datos.")
  else:
    # Creamos una lista de opciones legible para el selector
    opciones_clientes = {
        f"{info['nombre']} ({cel})": cel for cel, info in clientes.items()
    }
    cliente_seleccionado_label = st.selectbox(
        "Selecciona al cliente", list(opciones_clientes.keys())
    )

    if st.button("Sumar 1 Corte"):
      cel_elegido = opciones_clientes[cliente_seleccionado_label]
      clientes[cel_elegido]["cortes"] += 1
      guardar_datos(clientes)
      st.success(
          f"¡Corte sumado con éxito a"
          f" {clientes[cel_elegido]['nombre']}! ✂️ Total:"
          f" {clientes[cel_elegido]['cortes']}"
      )
      st.rerun()

elif menu == "Eliminar Cliente":
  st.title("🗑️ Eliminar Cliente")
  st.subheader(
      "Selecciona al cliente que deseas eliminar permanentemente del sistema"
  )

  if not clientes:
    st.info("No hay clientes para eliminar.")
  else:
    opciones_eliminar = {
        f"{info['nombre']} ({cel})": cel for cel, info in clientes.items()
    }
    cliente_a_borrar_label = st.selectbox(
        "Cliente a eliminar", list(opciones_eliminar.keys())
    )

    if st.button(
        "⚠️ Eliminar Definitivamente", type="primary"
    ):
      cel_a_borrar = opciones_eliminar[cliente_a_borrar_label]
      nombre_borrado = clientes[cel_a_borrar]["nombre"]
      del clientes[cel_a_borrar]
      guardar_datos(clientes)
      st.success(f"El cliente {nombre_borrado} ha sido eliminado correctamente.")
      st.rerun()
