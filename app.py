import json
import os
import streamlit as st

DATA_FILE = "clientes.json"

# Configuración de página para móvil/tablet
st.set_page_config(
    page_title="Blood Pact AQP", page_icon="💈", layout="centered"
)

# Estilos CSS personalizados (Tema Negro y Rojo / Blood Pact)
st.markdown(
    """
    <style>
    /* Fondo principal de la app */
    .stApp {
        background-color: #0d0d0d;
        color: #e0e0e0;
    }
    
    /* Encabezados y títulos en rojo sangre */
    h1, h2, h3 {
        color: #ff1a1a !important;
        font-family: 'Trebuchet MS', sans-serif;
    }

    /* Estilo de la barra lateral */
    [data-testid="stSidebar"] {
        background-color: #141414;
        border-right: 2px solid #800000;
    }

    /* Botón principal estilizado en rojo */
    div.stButton > button {
        background-color: #800000;
        color: #ffffff;
        border: 1px solid #ff1a1a;
        border-radius: 8px;
        font-weight: bold;
        transition: 0.3s;
    }
    
    div.stButton > button:hover {
        background-color: #ff1a1a;
        color: #000000;
        border-color: #ffffff;
        box-shadow: 0px 0px 10px #ff1a1a;
    }

    /* Cajas de alerta e información */
    .stAlert {
        background-color: #1a0000;
        border: 1px solid #800000;
        color: #ff9999;
    }

    /* Campos de texto */
    div[data-baseweb="input"] {
        background-color: #1f1f1f;
        color: #ffffff;
        border-radius: 6px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


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
        "Cortes y Fidelización",
        "Registrar Cliente",
        "Eliminar Cliente",
    ],
)

clientes = cargar_datos()

if menu == "Cortes y Fidelización":
  st.title("✂️ Cortes y Fidelización")
  st.subheader("Busca al cliente y registra sus puntos al instante")

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

          # Renderizado de tarjeta de 10 posiciones
          meta = 10
          tarjeta_str = ""

          for i in range(1, meta + 1):
            if i <= cortes:
              tarjeta_str += "✂️ "
            elif i == 5:
              tarjeta_str += "🎁 "  # Regalo 5to corte (50% desc)
            elif i == 10:
              tarjeta_str += "🎁 "  # Regalo 10mo corte (Gratis)
            else:
              tarjeta_str += "⚪ "

          st.markdown(f"**Tarjeta:**\n\n{tarjeta_str}")

          # Mensajes informativos de progreso
          if cortes < 5:
            restantes = 5 - cortes
            st.info(
                f"Te faltan {restantes} corte(s) para tu **50% DE DESCUENTO**"
                " 🎁"
            )
          elif cortes == 5:
            st.success("🎉 ¡Felicidades! Tienes **50% DE DESCUENTO** en este corte 🎁")
          elif cortes < 10:
            restantes = 10 - cortes
            st.info(
                f"Te faltan {restantes} corte(s) para tu **CORTE GRATIS** 🎁"
            )
          elif cortes == 10:
            st.success(
                "🎉 ¡Felicidades! Este corte es **TOTALMENTE GRATIS** 🎁"
            )

          # Botón directo para sumar el corte
          if st.button(f"➕ Sumar 1 Corte a {nombre}", key=f"btn_{cel}"):
            if clientes[cel]["cortes"] >= 10:
              clientes[cel]["cortes"] = 1  # Reinicia a 1 el nuevo ciclo
            else:
              clientes[cel]["cortes"] += 1

            guardar_datos(clientes)
            st.success(
                f"¡Corte registrado a {nombre}! Total:"
                f" {clientes[cel]['cortes']}"
            )
            st.rerun()

          st.markdown("---")

    if not encontrado and busqueda != "":
      st.warning(
          "No se encontró ningún cliente con ese nombre o número."
      )

elif menu == "Registrar Cliente":
  st.title("➕ Registrar Cliente")
  st.subheader("Ingresa los datos para dar de alta a un nuevo cliente")

  with st.form("form_cliente_principal"):
    celular_input = st.text_input("Celular del Cliente")
    nombre_input = st.text_input("Nombre y Apellido")
    cortes_input = st.number_input(
        "Cortes iniciales (opcional)", min_value=0, max_value=10, step=1, value=0
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

elif menu == "Eliminar Cliente":
  st.title("🗑️ Eliminar Cliente")
  st.subheader(
      "Selecciona al cliente que deseas borrar definitivamente del sistema"
  )

  if not clientes:
    st.info("No hay clientes para eliminar.")
  else:
    opciones_eliminar = {
        f"{info['nombre']} ({cel})": cel for cel, info in clientes.items()
    }
    cliente_a_borrar_label = st.selectbox(
        "Selecciona el cliente a eliminar", list(opciones_eliminar.keys())
    )

    if st.button("⚠️️ Eliminar Definitivamente", type="primary"):
      cel_a_borrar = opciones_eliminar[cliente_a_borrar_label]
      nombre_borrado = clientes[cel_a_borrar]["nombre"]
      del clientes[cel_a_borrar]
      guardar_datos(clientes)
      st.success(
          f"El registro de {nombre_borrado} ha sido eliminado correctamente."
      )
      st.rerun()
