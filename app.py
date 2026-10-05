import json
import os
import streamlit as st

DATA_FILE = "clientes.json"

st.set_page_config(
    page_title="Blood Pact AQP", page_icon="💈", layout="centered"
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@700;900&family=Montserrat:wght@700;900&display=swap');

    /* Forzar tipografía fuerte y robusta en toda la aplicación */
    .stApp, p, span, div, label, input {
        font-family: 'Montserrat', sans-serif !important;
    }
    
    h1, h2, h3, .stMarkdown h3 {
        font-family: 'Cinzel', serif !important;
        color: #ff1a1a !important;
        letter-spacing: 3px;
        text-transform: uppercase;
        font-weight: 900 !important;
    }

    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] label {
        font-family: 'Cinzel', serif !important;
        color: #ff1a1a !important;
        letter-spacing: 2px;
        text-transform: uppercase;
        font-weight: 900 !important;
    }

    .stApp {
        background-color: #0d0d0d;
        color: #e0e0e0;
    }
    
    [data-testid="stSidebar"] {
        background-color: #141414;
        border-right: 2px solid #800000;
    }

    div.stButton > button {
        background-color: #800000;
        color: #ffffff;
        border: 1px solid #ff1a1a;
        border-radius: 6px;
        font-family: 'Montserrat', sans-serif;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        font-weight: 900;
        transition: 0.3s;
    }
    
    div.stButton > button:hover {
        background-color: #ff1a1a;
        color: #000000;
        border-color: #ffffff;
        box-shadow: 0px 0px 12px #ff1a1a;
    }

    div[data-baseweb="input"] {
        background-color: #1f1f1f;
        color: #ffffff;
        border-radius: 6px;
    }

    /* Plomo rata con bordes y texto en rojo sangre para acumulación */
    .caja-progreso {
        background-color: #18181a;
        border: 2px solid #550000;
        padding: 14px 16px;
        border-radius: 8px;
        color: #ff3333;
        font-weight: 900;
        font-size: 1.1rem;
        margin-bottom: 10px;
        letter-spacing: 1px;
    }

    /* Colores invertidos (Rojo sangre total) cuando se alcanza el canje */
    .caja-premio {
        background-color: #800000;
        border: 2px solid #ff1a1a;
        padding: 14px 16px;
        border-radius: 8px;
        color: #ffffff;
        font-weight: 900;
        font-size: 1.15rem;
        margin-bottom: 10px;
        box-shadow: 0px 0px 14px #ff1a1a;
        letter-spacing: 1px;
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


logo_nombre = "Gemini_Generated_Image_ogzja4ogzja4ogzj-removebg-preview.png"
if os.path.exists(logo_nombre):
  st.sidebar.image(logo_nombre, use_column_width=True)
else:
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
  st.title("✂️️ Cortes y Fidelización")
  st.subheader("Busca tu nombre y suma tu corte")

  busqueda = st.text_input(
      "🔍 Buscar por nombre o número de celular", value=""
  ).lower()

  if not clientes:
    st.info("Aún no hay clientes registrados en la base.")
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
          tarjeta_str = ""

          for i in range(1, meta + 1):
            if i <= cortes:
              tarjeta_str += "✂️ "
            elif i == 5:
              tarjeta_str += "🎁 "
            elif i == 10:
              tarjeta_str += "🎁 "
            else:
              tarjeta_str += "⚪ "

          st.markdown(f"**Tarjeta:**\n\n{tarjeta_str}")

          if cortes < 5:
            restantes = 5 - cortes
            st.markdown(
                f'<div class="caja-progreso">Te faltan {restantes} corte(s)'
                " para tu 50% DE DESCUENTO 🎁</div>",
                unsafe_allow_html=True,
            )
          elif cortes == 5:
            st.markdown(
                '<div class="caja-premio">🎉 ¡Felicidades! Tienes 50% DE'
                " DESCUENTO en este corte 🎁</div>",
                unsafe_allow_html=True,
            )
          elif cortes < 10:
            restantes = 10 - cortes
            st.markdown(
                f'<div class="caja-progreso">Te faltan {restantes} corte(s)'
                " para tu CORTE GRATIS 🎁</div>",
                unsafe_allow_html=True,
            )
          elif cortes == 10:
            st.markdown(
                '<div class="caja-premio">🎉 ¡Felicidades! Este corte es'
                " TOTALMENTE GRATIS 🎁</div>",
                unsafe_allow_html=True,
            )

          if st.button(f"➕ Sumar 1 Corte a {nombre}", key=f"btn_{cel}"):
            if clientes[cel]["cortes"] >= 10:
              clientes[cel]["cortes"] = 1
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
      st.warning("No se encontró a nadie con ese nombre o número, meu.")

elif menu == "Registrar Cliente":
  st.title("➕ Registrar Cliente")
  st.subheader("Agrega al cliente nuevo")

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
          st.warning("¡Ese número ya está registrado, chequea bien!")
        else:
          clientes[celular_input] = {
              "nombre": nombre_input,
              "cortes": int(cortes_input),
          }
          guardar_datos(clientes)
          st.success(
              f"¡Listo! {nombre_input} fue registrado con {cortes_input}"
              " cortes."
          )
      else:
        st.error("Rellena el celular y el nombre, causa.")

elif menu == "Eliminar Cliente":
  st.title("🗑️ Eliminar Cliente")
  st.subheader("Camarón que se duerme se lo lleva la corriente")

  if not clientes:
    st.info("No hay clientes registrados para borrar.")
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
      st.success(f"Fuera de la lista: {nombre_borrado} fue eliminado.")
      st.rerun()
