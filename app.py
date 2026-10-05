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
    "Navegación",
    [
        "Gestión de Puntos",
        "Nuevo Cliente",
        "Administración",
    ],
)

clientes = cargar_datos()

if menu == "Gestión de Puntos":
  st.title("✂️ Gestión de Puntos")
  st.subheader("Busca al cliente y registra sus cortes al instante")

  busqueda = st.text_input(
      "🔍 Buscar por nombre o número de celular", value=""
  ).lower()

  if not clientes:
    st.info("Aún no hay clientes registrados en el sistema.")
  else:
    encontrado = False
    for cel, info in clientes.items():
      nombre = info.get("nombre", "")
      cortes = info.get("cortes", 0)

      if (
          busqueda in nombre.lower()
          or busqueda in cel
          or busqueda == ""
      ):
        encontrado = True
        with st.container():
          st.markdown(f"### 👤 {nombre}")
          st.markdown(f"📱 **Celular:** {cel}")
          st.markdown(f"✂️ **Cortes acumulados:** {cortes}")

          meta = 10
          cortes_actuales = cortes % meta
          restantes = meta - cortes_actuales

          tarjeta_str = ""
          for i in range(meta):
            if i < cortes_actuales:
              tarjeta_str += "✂ "
            elif i == 4:
              tarjeta_str += "🎁 "
            else:
              tarjeta_str += "⚪ "

          st.markdown(f"**Tarjeta:**\n\n{tarjeta_str}")
          st.info(f"Te faltan {restantes} cortes para tu CORTE GRATIS")

          if st.button(f"➕ Sumar 1 Corte a {nombre}", key=f"btn_{cel}"):
            clientes[cel]["cortes"] += 1
            guardar_datos(clientes)
            st.success(
                f"¡Corte sumado con éxito a {nombre}! Total:"
                f" {clientes[cel]['cortes']}"
            )
            st.rerun()

          st.markdown("---")

    if not encontrado and busqueda != "":
      st.warning(
          "No se encontró ningún cliente con ese nombre o número."
      )

elif menu == "Nuevo Cliente":
  st.title("➕ Registro de Cliente")
  st.subheader("Ingresa los datos para dar de alta a un nuevo cliente")

  with st.form("form_cliente_principal"):
    celular_input = st.text_input("Celular del Cliente")
    nombre_input = st.text_input("Nombre y Apellido")
    cortes_input = st.number_input(
        "Cortes iniciales (opcional)", min_value=0, step=1, value=0
    )
    submit_btn = st.form_submit_button("Guardar Registro")

    if submit_btn:
      if celular_input and nombre_input:
        if celular_input in clientes:
          st.warning(
              "Ya existe un cliente registrado con este número de celular."
          )
        else:
          clientes[celular_input] = {
              "nombre": nombre_input,
              "cortes": int(cortes_input),
          }
          guardar_datos(clientes)
          st.success(
              f"¡Cliente {nombre_input} registrado correctamente con"
              f" {cortes_input} cortes!"
          )
      else:
        st.error("Por favor completa el celular y el nombre.")

elif menu == "Administración":
  st.title("⚙️ Administración de Base de Datos")
  st.subheader("Panel para la baja de registros del sistema")

  if not clientes:
    st.info("No hay clientes para administrar.")
  else:
    opciones_eliminar = {
        f"{info['nombre']} ({cel})": cel for cel, info in clientes.items()
    }
    cliente_a_borrar_label = st.selectbox(
        "Selecciona el cliente a eliminar", list(opciones_eliminar.keys())
    )

    if st.button("⚠️ Eliminar Definitivamente", type="primary"):
      cel_a_borrar = opciones_eliminar[cliente_a_borrar_label]
      nombre_borrado = clientes[cel_a_borrar]["nombre"]
      del clientes[cel_a_borrar]
      guardar_datos(clientes)
      st.success(
          f"El registro de {nombre_borrado} ha sido eliminado correctamente."
      )
      st.rerun()
