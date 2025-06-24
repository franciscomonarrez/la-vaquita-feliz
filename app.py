import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# ----------------- CONFIG -----------------
st.set_page_config(
    page_title="La Vaquita Feliz 🐮 - Calculadora de Utilidad",
    page_icon="🐮",
    layout="centered",  # switch to centered for narrower tables
    initial_sidebar_state="expanded",
)

# ----------------- CSS CUSTOMIZATION -----------------
st.markdown(
    """
    <style>
      /* Constrain max width to shrink tables */
      .block-container {
        max-width: 800px !important;
        padding: 0.5rem 1rem !important;
      }
      /* Gradient background */
      .reportview-container {
        background: linear-gradient(135deg, #FFF7E0, #FFE4B3);
      }
      /* Center titles */
      h1, .stHeader h2 {
        text-align: center;
      }
      /* Smaller metric values and labels */
      .stMetricValue, .css-1v0mbdj {
        font-size: 1rem !important;
      }
      .stMetricLabel, .css-1avcm0n {
        font-size: 0.8rem !important;
      }
      /* Smaller expander text */
      .streamlit-expanderHeader {
        font-size: 0.9rem !important;
      }
      /* Hide default footer */
      footer {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------- SIDEBAR INPUTS -----------------
st.sidebar.header("🛠 Ajustes de Costos & Ventas")

# Materia Prima
st.sidebar.subheader("🔹 Materia Prima")
carne_fresca = st.sidebar.number_input(
    "Carne fresca ($)", min_value=0.0, value=52473.06, step=10.0
)
sal = st.sidebar.number_input(
    "Sal ($)", min_value=0.0, value=31.35, step=1.0
)

# Mano de Obra
st.sidebar.subheader("🔹 Mano de Obra")
sueldo1 = st.sidebar.number_input(
    "Sueldo principal ($)", min_value=0.0, value=7266.95, step=10.0
)
trabajador_adicional = st.sidebar.number_input(
    "Trabajador adicional ($)", min_value=0.0, value=3000.00, step=10.0
)
corte_carne = st.sidebar.number_input(
    "Costo de corte de carne ($)", min_value=0.0, value=1024.14, step=10.0
)

# Servicios y Gastos Fijos
st.sidebar.subheader("🔹 Servicios & Fijos")
luz = st.sidebar.number_input(
    "Luz mensual ($)", min_value=0.0, value=651.25, step=1.0
)
agua = st.sidebar.number_input(
    "Agua ($)", min_value=0.0, value=145.34, step=1.0
)
fumigacion = st.sidebar.number_input(
    "Fumigación ($)", min_value=0.0, value=726.69, step=1.0
)
liquidos_limpieza = st.sidebar.number_input(
    "Líquidos de limpieza ($)", min_value=0.0, value=297.01, step=1.0
)
otro_liquido = st.sidebar.number_input(
    "Otro líquido de limpieza ($)", min_value=0.0, value=18.35, step=1.0
)

# Producción y Ventas
st.sidebar.subheader("🛒 Producción & Ventas")
total_unidades = st.sidebar.number_input(
    "Bolsas producidas", min_value=1, value=453, step=1
)
precio_venta = st.sidebar.number_input(
    "Precio actual por bolsa ($)", min_value=0.0, value=145.18, step=1.0
)
precio_venta_sugerido = st.sidebar.number_input(
    "Precio sugerido por bolsa ($)", min_value=0.0, value=196.00, step=1.0
)

# ----------------- MAIN LAYOUT -----------------
st.title("🐮 La Vaquita Feliz")
st.subheader("Calculadora Visual de Utilidad para Machaca")

# --- FÓRMULAS USADAS ---
with st.expander("🧮 Fórmulas detalladas"):
    st.markdown("""
    1. **Costo de empaques**  
       `empaques = total_unidades × $2`

    2. **Costo total**  
       `costo_total = carne_fresca + sal + corte_carne + sueldo1 + trabajador_adicional + luz + agua + fumigacion + liquidos_limpieza + otro_liquido + empaques`

    3. **Costo por bolsa**  
       `costo_por_bolsa = costo_total ÷ total_unidades`

    4. **Utilidad por bolsa**  
       `utilidad_por_bolsa = precio_venta – costo_por_bolsa`

    5. **Utilidad total**  
       `utilidad_total = utilidad_por_bolsa × total_unidades`

    6. **Margen (%)**  
       `utilidad_pct = (utilidad_por_bolsa ÷ precio_venta) × 100`

    7. **Versión sugerida**  
       Misma lógica usando `precio_venta_sugerido` en lugar de `precio_venta`
    """)

st.info("**Todos los valores se actualizan en tiempo real.**")

# ----------------- CÁLCULOS -----------------
costo_unitario_empaque = 2.0
empaques = total_unidades * costo_unitario_empaque

costo_total = (
    carne_fresca + sal + corte_carne +
    sueldo1 + trabajador_adicional +
    luz + agua + fumigacion +
    liquidos_limpieza + otro_liquido +
    empaques
)
costo_por_bolsa = costo_total / total_unidades

utilidad_por_bolsa = precio_venta - costo_por_bolsa
utilidad_total = utilidad_por_bolsa * total_unidades
utilidad_pct = (utilidad_por_bolsa / precio_venta * 100) if precio_venta else 0

utilidad_por_bolsa_sug = precio_venta_sugerido - costo_por_bolsa
utilidad_total_sug = utilidad_por_bolsa_sug * total_unidades
utilidad_pct_sug = (utilidad_por_bolsa_sug / precio_venta_sugerido * 100) if precio_venta_sugerido else 0

# ----------------- MÉTRICAS -----------------
st.success(f"### Costo total del mes: ${costo_total:,.2f}")

col1, col2 = st.columns(2)
col1.metric("Costo/bolsa", f"${costo_por_bolsa:,.2f}")
col2.metric("Bolsas producidas", f"{total_unidades}")

st.markdown("---")

st.markdown("#### 🔸 Resultado Actual")
a1, a2, a3 = st.columns(3)
a1.metric("Utilidad/bolsa", f"${utilidad_por_bolsa:,.2f}")
a2.metric("Utilidad total", f"${utilidad_total:,.2f}")
a3.metric("Margen %", f"{utilidad_pct:.1f}%")

st.markdown("#### 🔸 Resultado Sugerido")
s1, s2, s3 = st.columns(3)
s1.metric("Utilidad/bolsa", f"${utilidad_por_bolsa_sug:,.2f}")
s2.metric("Utilidad total", f"${utilidad_total_sug:,.2f}")
s3.metric("Margen %", f"{utilidad_pct_sug:.1f}%")

st.markdown("---")

st.markdown("**Costo de Empaques**")
e1, e2 = st.columns(2)
e1.metric("Total empaques", f"${empaques:,.2f}")
e2.metric("Costo / bolsa", f"${costo_unitario_empaque:.2f}")

# ----------------- FUNCIÓN AUTOPCT -----------------
def make_autopct(values):
    def my_autopct(pct):
        total = sum(values)
        val = pct * total / 100
        return f"{val:,.2f}\n({pct:.1f}%)"
    return my_autopct

# ----------------- GRÁFICOS -----------------
st.header("📊 Análisis Gráfico")

# 1) Desglose de costos – BARRA HORIZONTAL
st.subheader("1. Costos por Rubro")
labels = [
    "Carne fresca","Sal","Corte","Sueldo princ.","Trabajador adic.",
    "Luz","Agua","Fumigación","Líquidos limp.","Otro líquido","Empaques"
]
values = [
    carne_fresca, sal, corte_carne, sueldo1, trabajador_adicional,
    luz, agua, fumigacion, liquidos_limpieza, otro_liquido, empaques
]
fig1, ax1 = plt.subplots(figsize=(6,3))
ax1.barh(labels, values, color="#C41E3A")
ax1.set_xlabel("Monto ($)", fontsize=9)
ax1.set_title("Costos por Rubro", fontsize=11)
ax1.tick_params(axis='y', labelsize=8)
ax1.tick_params(axis='x', labelsize=8)
st.pyplot(fig1)

# 2) Pie Actual
st.subheader("2. Composición Precio Actual")
labels_act = ["Costo", "Utilidad"] if utilidad_por_bolsa >= 0 else ["Costo", "Pérdida"]
sizes_act = [costo_por_bolsa, abs(utilidad_por_bolsa)]
colors_act = ['#FFE4B3', '#C41E3A'] if utilidad_por_bolsa >= 0 else ['#FFE4B3', '#FF9999']
fig2, ax2 = plt.subplots(figsize=(3,3))
wedges2, texts2, autotexts2 = ax2.pie(
    sizes_act,
    labels=labels_act,
    startangle=90,
    autopct=make_autopct(sizes_act),
    colors=colors_act,
    textprops={'fontsize': 8}
)
ax2.set_title("Actual", fontsize=11)
ax2.axis('equal')
st.pyplot(fig2)

# 3) Pie Sugerido
st.subheader("3. Composición Precio Sugerido")
labels_sug = ["Costo", "Utilidad"] if utilidad_por_bolsa_sug >= 0 else ["Costo", "Pérdida"]
sizes_sug = [costo_por_bolsa, abs(utilidad_por_bolsa_sug)]
colors_sug = ['#E0F7FA', '#F4A261'] if utilidad_por_bolsa_sug >= 0 else ['#E0F7FA', '#FF9999']
fig3, ax3 = plt.subplots(figsize=(3,3))
wedges3, texts3, autotexts3 = ax3.pie(
    sizes_sug,
    labels=labels_sug,
    startangle=90,
    autopct=make_autopct(sizes_sug),
    colors=colors_sug,
    textprops={'fontsize': 8}
)
ax3.set_title("Sugerido", fontsize=11)
ax3.axis('equal')
st.pyplot(fig3)

# 4) Stacked Bar
st.subheader("4. Costo + Utilidad por Bolsa")
labels_cmp = ["Actual", "Sugerido"]
costs_cmp = [costo_por_bolsa, costo_por_bolsa]
profits_cmp = [utilidad_por_bolsa, utilidad_por_bolsa_sug]
fig4, ax4 = plt.subplots(figsize=(5,2.5))
x = np.arange(len(labels_cmp))
ax4.bar(x, costs_cmp, 0.6, label="Costo", color="#FFE4B3")
for i in range(2):
    bottom = costs_cmp[i] if profits_cmp[i] >= 0 else costs_cmp[i] + profits_cmp[i]
    color = "#C41E3A" if profits_cmp[i] >= 0 else "#FF9999"
    ax4.bar(x[i], abs(profits_cmp[i]), 0.6, bottom=bottom, color=color)
ax4.set_xticks(x)
ax4.set_xticklabels(labels_cmp, fontsize=8)
ax4.set_ylabel("Monto ($)", fontsize=9)
ax4.set_title("Costo + Utilidad por Bolsa", fontsize=11)
for i in range(2):
    total = costs_cmp[i] + profits_cmp[i]
    if total != 0:
        ax4.text(
            x[i],
            costs_cmp[i]/2,
            f"${costs_cmp[i]:.2f}\n({costs_cmp[i]/total*100:.1f}%)",
            ha="center", va="center", fontsize=8
        )
        ax4.text(
            x[i],
            costs_cmp[i] + profits_cmp[i]/2,
            f"${profits_cmp[i]:.2f}\n({profits_cmp[i]/total*100:.1f}%)",
            ha="center", va="center", fontsize=8
        )
st.pyplot(fig4)

st.caption("Desarrollado para La Vaquita Feliz 🐮 — tablas y gráficos ajustados para mejor lectura.")
