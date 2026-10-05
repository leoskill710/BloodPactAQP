import streamlit as st
import json
import os

# Configuración de página para celular
st.set_page_config(page_title="Blood Pact AQP", page_icon="✂️", layout="centered")

# Nombre del archivo donde guardaremos los clientes localmente
DB_FILE = "clientes.json"

# Cargar clientes desde archivo JSON
def cargar_clientes():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "906867617": {"nombre": "Leonardo Acosta", "cortes": 2},
        "987496121": {"nombre": "Cliente Ejemplo", "cortes": 5}
    }

# Guardar clientes en archivo JSON
def guardar_clientes(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if "clientes" not in st.session_state:
    st.session_state["clientes"] = cargar_clientes()

# Título Principal
st.title("✂️ Blood Pact AQP")
st.caption("Programa de Fidelidad de Barbería")

# Función para calcular los emojis y mensaje de recompensa
def calcular_fidelidad(c):
    if c == 0:
        return "⚪ ⚪ ⚪ ⚪ ⚪ ⚪ ⚪ ⚪ ⚪ ⚪", "Te faltan 10 cortes para tu CORTE GRATIS"
    elif c < 5:
        dibujo = ("✂️ " * c) + ("⚪ " * (5 - c)) + "⚪ ⚪ ⚪ ⚪ ⚪"
        estado = f"Te faltan {5 - c} cortes para tu 50% de descuento"
        return dibujo, estado
    elif c == 5:
        return "✂️ ✂️ ✂️ ✂️ ✂️ ⚪ ⚪ ⚪ ⚪ ⚪", "¡Tienes un 50% de descuento disponible! 🔥"
    elif c < 10:
        dibujo = "✂️ ✂️ ✂️ ✂️ 🎁 " + ("✂️ " * (c - 5)) + ("⚪ " * (10 - c))
        estado = f"Te faltan {10 - c} cortes para tu CORTE GRATIS"
        return dibujo, estado
    else:
        return "✂️ ✂️ ✂️ ✂️️ 🎁 ✂️ ✂️ ✂️ ✂️ 🥳", "¡Corte GRATIS disponible! 🥳"

# Menú lateral para registrar/actualizar cortes
st.sidebar.header("💈 Registrar / Actualizar")

opcion = st.sidebar.radio("Acción", ["Agregar o Buscar Cliente", "Registrar Corte"])

if opcion == "Agregar o Buscar Cliente":
    celular = st.sidebar.text_input("Celular del Cliente")
    nombre = st.sidebar.text_input("Nombre del Cliente")
    cortes_iniciales = st.sidebar.number_input("Cortes acumulados", min_value=0, max_value=20, value=0, step=1)
    
    if st.sidebar.button("Guardar Cliente"):
        if celular and nombre:
            st.session_state["clientes"][celular] = {"nombre": nombre, "cortes": int(cortes_iniciales)}
            guardar_clientes(st.session_state["clientes"])
            st.sidebar.success(f"¡Cliente {nombre} guardado!")
            st.rerun()
        else:
            st.sidebar.error("Por favor ingresa nombre y celular.")

elif opcion == "Registrar Corte":
    if st.session_state["clientes"]:
        lista_celulares = list(st.session_state["clientes"].keys())
        cel_select = st.sidebar.selectbox("Selecciona Cliente", lista_celulares, format_func=lambda x: f"{st.session_state['clientes'][x]['nombre']} ({x})")
        
        col1, col2 = st.sidebar.columns(2)
        with col1:
            if st.button("➕ 1 Corte"):
                st.session_state["clientes"][cel_select]["cortes"] += 1
                guardar_clientes(st.session_state["clientes"])
                st.success("¡Corte sumado!")
                st.rerun()
        with col2:
            if st.button("🔄 Canjear"):
                st.session_state["clientes"][cel_select]["cortes"] = 0
                guardar_clientes(st.session_state["clientes"])
                st.warning("¡Tarjeta reiniciada!")
                st.rerun()

# Buscador en la pantalla principal
st.subheader("📋 Lista de Clientes")
busqueda = st.text_input("🔍 Buscar cliente por nombre o teléfono")

clientes_mostrar = st.session_state["clientes"]
if busqueda:
    clientes_mostrar = {
        k: v for k, v in clientes_mostrar.items() 
        if busqueda.lower() in v["nombre"].lower() or busqueda in k
    }

# Renderizar Tarjetas de Fidelidad
for cel, datos in clientes_mostrar.items():
    c = datos["cortes"]
    dibujo, estado = calcular_fidelidad(c)
    
    with st.container(border=True):
        st.write(f"### 👤 {datos['nombre']}")
        st.caption(f"📱 Celular: {cel}")
        st.write(f"**Cortes acumulados:** `{c}`")
        st.markdown(f"**Tarjeta:**\n### {dibujo}")
        
        if c == 5 or c >= 10:
            st.success(f"🎉 **{estado}**")
        else:
            st.info(estado)