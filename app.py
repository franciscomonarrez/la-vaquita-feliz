import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import sqlite3
from datetime import datetime

# ----------------- DATABASE -----------------
@st.experimental_singleton
def get_db():
    conn = sqlite3.connect('sessions.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            carne_fresca REAL,
            sal REAL,
            corte_carne REAL,
            sueldo1 REAL,
            trabajador_adicional REAL,
            luz REAL,
            agua REAL,
            fumigacion REAL,
            liquidos_limpieza REAL,
            otro_liquido REAL,
            total_unidades INTEGER,
            precio_venta REAL,
            precio_venta_sugerido REAL
        )
    ''')
    conn.commit()
    return conn

# ----------------- SAVE & LOAD -----------------
def load_sessions():
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT id, timestamp FROM sessions ORDER BY id DESC')
    return c.fetchall()

def load_session_data(session_id):
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT * FROM sessions WHERE id = ?', (session_id,))
    return c.fetchone()

def save_session(data, session_id=None):
    conn = get_db()
    c = conn.cursor()
    if session_id:
        c.execute(
            '''UPDATE sessions SET
                timestamp=?, carne_fresca=?, sal=?, corte_carne=?, sueldo1=?,
                trabajador_adicional=?, luz=?, agua=?, fumigacion=?,
                liquidos_limpieza=?, otro_liquido=?, total_unidades=?,
                precio_venta=?, precio_venta_sugerido=?
               WHERE id=?''',
            (*data, session_id)
        )
    else:
        c.execute(
            '''INSERT INTO sessions (
                timestamp, carne_fresca, sal, corte_carne, sueldo1,
                trabajador_adicional, luz, agua, fumigacion,
                liquidos_limpieza, otro_liquido, total_unidades,
                precio_venta, precio_venta_sugerido
            ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
            data
        )
    conn.commit()

# ----------------- CONFIG -----------------
st.set_page_config(
    page_title="La Vaquita Feliz 🐮 - Calculadora de Utilidad",
    page_icon="🐮",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ----------------- CSS -----------------
st.markdown(
    """
    <style>
      .block-container { max-width: 800px !important; padding: 0.5rem 1rem !important; }
      footer { visibility: hidden; }
    </style>
    """, unsafe_allow_html=True
)

# ----------------- TABS -----------------
tab1, tab2 = st.tabs(["Calculadora", "Sesiones Guardadas"])

# Default values
defaults = {
    "carne_fresca": 52473.06,
    "sal": 31.35,
    "corte_carne": 1024.14,
    "sueldo1": 7266.95,
    "trabajador_adicional": 3000.00,
    "luz": 651.25,
    "agua": 145.34,
    "fumigacion": 726.69,
    "liquidos_limpieza": 297.01,
    "otro_liquido": 18.35,
    "total_unidades": 453,
    "precio_venta": 145.18,
    "precio_venta_sugerido": 196.00
}

# Initialize session state
for key, val in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = val
if 'loaded_id' not in st.session_state:
    st.session_state['loaded_id'] = None

# ----------------- CALCULATOR TAB -----------------
with tab1:
    st.sidebar.header("🛠 Ajustes de Costos & Ventas")
    # Inputs
    carne_fresca = st.sidebar.number_input("Carne fresca ($)", 0.0, 1e6, st.session_state.carne_fresca, step=10.0, key="carne_fresca")
    sal = st.sidebar.number_input("Sal ($)", 0.0, 1e4, st.session_state.sal, step=1.0, key="sal")
    corte_carne = st.sidebar.number_input("Costo de corte de carne ($)", 0.0, 1e5, st.session_state.corte_carne, step=10.0, key="corte_carne")
    sueldo1 = st.sidebar.number_input("Sueldo principal ($)", 0.0, 1e5, st.session_state.sueldo1, step=10.0, key="sueldo1")
    trabajador_adicional = st.sidebar.number_input("Trabajador adicional ($)", 0.0, 1e5, st.session_state.trabajador_adicional, step=10.0, key="trabajador_adicional")
    luz = st.sidebar.number_input("Luz mensual ($)", 0.0, 1e4, st.session_state.luz, step=1.0, key="luz")
    agua = st.sidebar.number_input("Agua ($)", 0.0, 1e4, st.session_state.agua, step=1.0, key="agua")
    fumigacion = st.sidebar.number_input("Fumigación ($)", 0.0, 1e4, st.session_state.fumigacion, step=1.0, key="fumigacion")
    liquidos_limpieza = st.sidebar.number_input("Líquidos de limpieza ($)", 0.0, 1e4, st.session_state.liquidos_limpieza, step=1.0, key="liquidos_limpieza")
    otro_liquido = st.sidebar.number_input("Otro líquido de limpieza ($)", 0.0, 1e4, st.session_state.otro_liquido, step=1.0, key="otro_liquido")
    total_unidades = st.sidebar.number_input("Bolsas producidas", 1, 1e5, int(st.session_state.total_unidades), step=1, key="total_unidades")
    precio_venta = st.sidebar.number_input("Precio venta actual ($)", 0.0, 1e3, st.session_state.precio_venta, step=0.1, key="precio_venta")
    precio_venta_sugerido = st.sidebar.number_input("Precio venta sugerido ($)", 0.0, 1e3, st.session_state.precio_venta_sugerido, step=0.1, key="precio_venta_sugerido")

    # Save or update session
    if st.button("Guardar sesión"):
        timestamp = datetime.now().isoformat()
        data = (
            timestamp,
            carne_fresca, sal, corte_carne, sueldo1,
            trabajador_adicional, luz, agua, fumigacion,
            liquidos_limpieza, otro_liquido, total_unidades,
            precio_venta, precio_venta_sugerido
        )
        save_session(data, st.session_state['loaded_id'])
        msg = f"Sesión {st.session_state['loaded_id']} actualizada." if st.session_state['loaded_id'] else "Sesión guardada."
        st.success(msg)
        # reset
        for k,v in defaults.items(): st.session_state[k] = v
        st.session_state['loaded_id'] = None
        st.experimental_rerun()

    # Calculations
    empaques = total_unidades * 2.0
    costo_total = (carne_fresca + sal + corte_carne + sueldo1 + trabajador_adicional +
                   luz + agua + fumigacion + liquidos_limpieza + otro_liquido + empaques)
    costo_por_bolsa = costo_total / total_unidades
    utilidad_por_bolsa = precio_venta - costo_por_bolsa
    utilidad_total = utilidad_por_bolsa * total_unidades
    utilidad_pct = (utilidad_por_bolsa / precio_venta * 100) if precio_venta else 0
    utilidad_por_bolsa_sug = precio_venta_sugerido - costo_por_bolsa
    utilidad_total_sug = utilidad_por_bolsa_sug * total_unidades
    utilidad_pct_sug = (utilidad_por_bolsa_sug / precio_venta_sugerido * 100) if precio_venta_sugerido else 0

    # Display metrics
    st.success(f"Costo total del mes: ${costo_total:,.2f}")
    c1, c2 = st.columns(2)
    c1.metric("Costo/bolsa", f"${costo_por_bolsa:,.2f}")
    c2.metric("Bolsas producidas", f"{total_unidades}")

    st.markdown("---")
    st.markdown("#### 🔸 Actual")
    a1, a2, a3 = st.columns(3)
    a1.metric("Utilidad/bolsa", f"${utilidad_por_bolsa:,.2f}")
    a2.metric("Utilidad total", f"${utilidad_total:,.2f}")
    a3.metric("Margen %", f"{utilidad_pct:.1f}%")

    st.markdown("#### 🔸 Sugerido")
    s1, s2, s3 = st.columns(3)
    s1.metric("Utilidad/bolsa", f"${utilidad_por_bolsa_sug:,.2f}")
    s2.metric("Utilidad total", f"${utilidad_total_sug:,.2f}")
    s3.metric("Margen %", f"{utilidad_pct_sug:.1f}%")

    st.markdown("---")
    st.markdown("**Costo de Empaques**")
    e1, e2 = st.columns(2)
    e1.metric("Costo total empaques", f"${empaques:,.2f}")
    e2.metric("Costo empaque / bolsa", f"$2.00")

    def make_autopct(values):
        def my_autopct(pct):
            total = sum(values)
            val = pct * total / 100
            return f"{val:,.2f}\n({pct:.1f}%)"
        return my_autopct

    st.header("📊 Análisis Gráfico")
    # Cost breakdown
    labels = ["Carne fresca","Sal","Corte","Sueldo princ.","Trabajador adic.","Luz","Agua","Fumigación","Líquidos limp.","Otro líquido","Empaques"]
    vals = [carne_fresca, sal, corte_carne, sueldo1, trabajador_adicional, luz, agua, fumigacion, liquidos_limpieza, otro_liquido, empaques]
    fig1, ax1 = plt.subplots(figsize=(6,3))
    ax1.barh(labels, vals, color="#C41E3A")
    ax1.set_xlabel("Monto ($)", fontsize=9)
    ax1.set_title("Costos por Rubro", fontsize=11)
    ax1.tick_params(axis='y', labelsize=8)
    ax1.tick_params(axis='x', labelsize=8)
    st.pyplot(fig1)

    # Pie Actual
    labels_act = ["Costo","Utilidad"] if utilidad_por_bolsa>=0 else ["Costo","Pérdida"]
    sizes_act = [costo_por_bolsa, abs(utilidad_por_bolsa)]
    colors_act = ['#FFE4B3','#C41E3A'] if utilidad_por_bolsa>=0 else ['#FFE4B3','#FF9999']
    fig2, ax2 = plt.subplots(figsize=(3,3))
    ax2.pie(sizes_act, labels=labels_act, autopct=make_autopct(sizes_act), colors=colors_act, startangle=90, textprops={'fontsize':8})
    ax2.set_title("Actual", fontsize=11)
    ax2.axis('equal')
    st.pyplot(fig2)

    # Pie Sugerido
    labels_sug = ["Costo","Utilidad"] if utilidad_por_bolsa_sug>=0 else ["Costo","Pérdida"]
    sizes_sug = [costo_por_bolsa, abs(utilidad_por_bolsa_sug)]
    colors_sug = ['#E0F7FA','#F4A261'] if utilidad_por_bolsa_sug>=0 else ['#E0F7FA','#FF9999']
    fig3, ax3 = plt.subplots(figsize=(3,3))
    ax3.pie(sizes_sug, labels=labels_sug, autopct=make_autopct(sizes_sug), colors=colors_sug, startangle=90, textprops={'fontsize':8})
    ax3.set_title("Sugerido", fontsize=11)
    ax3.axis('equal')
    st.pyplot(fig3)

# ----------------- SESIONES TAB -----------------
with tab2:
    st.subheader("Sesiones Guardadas")
    sessions = load_sessions()
    for sess_id, ts in sessions:
        if st.button(f"ID {sess_id} - {ts}", key=f"btn_{sess_id}"):
            row = load_session_data(sess_id)
            for i, key in enumerate(defaults.keys(), start=2):
                st.session_state[key] = row[i]
            st.session_state['loaded_id'] = sess_id
            st.success(f"Cargada sesión {sess_id}. Edita y guarda.")
            st.experimental_rerun()