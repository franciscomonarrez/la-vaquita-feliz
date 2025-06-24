import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="La Vaquita Feliz - Calculadora de Utilidad", page_icon="🐮")

st.title("🐮 La Vaquita Feliz")
st.markdown("## Calculadora Visual de Utilidad para la Producción de Machaca")

# --- DEFINICIONES ---
with st.expander("❓ ¿Qué son Utilidad y Margen?"):
    st.markdown("""
    - **Utilidad por bolsa**:  
      `Precio de venta – Costo por bolsa`  
      (cuánto dinero neto ganas en cada unidad)

    - **Utilidad total**:  
      `Utilidad por bolsa × Total de unidades`  
      (ganancia neta en todo el lote)

    - **Margen (%)**:  
      `(Utilidad por bolsa / Precio de venta) × 100`  
      (qué porcentaje de cada peso de venta es ganancia)
    """)

st.info("**Todos los costos y gráficas se actualizan en tiempo real según la producción y precios.**")

# --- SECCIÓN 1: COSTOS DE PRODUCCIÓN ---
st.header("🔹 Materia Prima")
carne_fresca = st.number_input("Carne fresca ($)", min_value=0.0, value=52473.06, step=10.0)
sal = st.number_input("Sal ($)", min_value=0.0, value=31.35, step=1.0)

st.header("🔹 Mano de Obra")
sueldo1 = st.number_input("Sueldo principal ($)", min_value=0.0, value=7266.95, step=10.0)
trabajador_adicional = st.number_input("Trabajador adicional ($)", min_value=0.0, value=3000.0, step=10.0)
corte_carne = st.number_input(
    "Costo de corte de carne (carnicero) ($)", min_value=0.0, value=1024.14, step=10.0
)

st.header("🔹 Servicios y Gastos Fijos")
luz = st.number_input("Luz mensual ($)", min_value=0.0, value=651.25, step=1.0)
agua = st.number_input("Agua ($)", min_value=0.0, value=145.34, step=1.0)
fumigacion = st.number_input("Fumigación ($)", min_value=0.0, value=726.69, step=1.0)
liquidos_limpieza = st.number_input("Líquidos de limpieza ($)", min_value=0.0, value=297.01, step=1.0)
otro_liquido = st.number_input("Otro líquido de limpieza ($)", min_value=0.0, value=18.35, step=1.0)

st.divider()

# --- SECCIÓN 2: PRODUCCIÓN Y VENTAS ---
st.header("🛒 Producción y Ventas")
total_unidades = st.number_input("Total de bolsas producidas/vendidas", min_value=1, value=453, step=1)
precio_venta = st.number_input("Precio actual por bolsa ($)", min_value=0.0, value=145.18, step=1.0)
precio_venta_sugerido = st.number_input("Precio sugerido por bolsa ($)", min_value=0.0, value=196.0, step=1.0)

# --- CÁLCULO DE EMPAQUES DINÁMICO ---
costo_unitario_empaque = 2.0
empaques = total_unidades * costo_unitario_empaque

# --- CÁLCULOS PRINCIPALES ---
costo_total = (
    carne_fresca + sal + corte_carne +
    sueldo1 + trabajador_adicional +
    luz + agua + fumigacion +
    liquidos_limpieza + otro_liquido +
    empaques
)
costo_por_bolsa = costo_total / total_unidades

utilidad_por_bolsa      = precio_venta - costo_por_bolsa
utilidad_total          = utilidad_por_bolsa * total_unidades
utilidad_pct            = (utilidad_por_bolsa / precio_venta * 100) if precio_venta else 0

utilidad_por_bolsa_sug  = precio_venta_sugerido - costo_por_bolsa
utilidad_total_sug      = utilidad_por_bolsa_sug * total_unidades
utilidad_pct_sug        = (utilidad_por_bolsa_sug / precio_venta_sugerido * 100) if precio_venta_sugerido else 0

# --- RESULTADOS ---
st.success(f"**Costo total del mes:** ${costo_total:,.2f}")

# Métricas de costo y producción
c1, c2 = st.columns(2)
c1.metric("Costo/bolsa", f"${costo_por_bolsa:,.2f}")
c2.metric("Total Unidades", f"{total_unidades}")

# Métricas de Utilidad y Margen actual
st.subheader("🔸 Actual")
a1, a2, a3 = st.columns(3)
a1.metric("Utilidad/bolsa (actual)",    f"${utilidad_por_bolsa:,.2f}")
a2.metric("Utilidad total (actual)",    f"${utilidad_total:,.2f}")
a3.metric("Margen % (actual)",          f"{utilidad_pct:.1f}%")

# Métricas de Utilidad y Margen sugerido
st.subheader("🔸 Sugerido")
s1, s2, s3 = st.columns(3)
s1.metric("Utilidad/bolsa (sugerido)",  f"${utilidad_por_bolsa_sug:,.2f}")
s2.metric("Utilidad total (sugerido)",  f"${utilidad_total_sug:,.2f}")
s3.metric("Margen % (sugerido)",        f"{utilidad_pct_sug:.1f}%")

# Mostrar costo de empaques
st.markdown("**Costo de empaques**")
e1, e2 = st.columns(2)
e1.metric("Total empaques", f"${empaques:,.2f}")
e2.metric("Costo / bolsa",  f"${costo_unitario_empaque:.2f}")

st.divider()

# --- FUNCION AUTOPCT PERSONALIZADO ---
def make_autopct(values):
    def my_autopct(pct):
        total = sum(values)
        val = pct * total / 100
        sign = "-" if val < 0 else ""
        return f"{sign}${abs(val):,.0f}\n({sign}{pct:.1f}%)"
    return my_autopct

# --- VISUALIZACIONES MEJORADAS ---
st.header("📊 Visualizaciones Mejoradas")

# 1) Desglose de costos – BARRA HORIZONTAL
st.markdown("**1. Desglose de costos por rubro**")
labels_cost = [
    "Carne fresca", "Sal", "Corte carn.", "Sueldo princ.",
    "Trabajador adic.", "Luz", "Agua", "Fumigación",
    "Líquidos limp.", "Otro líquido", "Empaques"
]
values_cost = [
    carne_fresca, sal, corte_carne, sueldo1, trabajador_adicional,
    luz, agua, fumigacion, liquidos_limpieza, otro_liquido, empaques
]
fig_cost, ax_cost = plt.subplots(figsize=(8, 5))
ax_cost.barh(labels_cost, values_cost, color="skyblue")
ax_cost.set_xlabel("Monto ($)")
ax_cost.set_title("Costos absolutos por rubro")
plt.tight_layout()
st.pyplot(fig_cost)

# 2) Composición precio actual – PIE
st.markdown("**2. Composición precio actual**")
if utilidad_por_bolsa >= 0:
    labels_act = ["Costo", "Utilidad"]
    sizes_act = [costo_por_bolsa, utilidad_por_bolsa]
    colors_act = ['#FFCC99', '#99FF99']
else:
    labels_act = ["Costo", "Pérdida"]
    sizes_act = [costo_por_bolsa, abs(utilidad_por_bolsa)]
    colors_act = ['#FFCC99', '#FF9999']

fig_act, ax_act = plt.subplots(figsize=(5,5))
ax_act.pie(
    sizes_act, labels=labels_act,
    startangle=90,
    autopct=make_autopct(sizes_act),
    colors=colors_act
)
ax_act.set_title("Costo vs Utilidad (actual)")
ax_act.axis('equal')
st.pyplot(fig_act)

# 3) Composición precio sugerido – PIE
st.markdown("**3. Composición precio sugerido**")
if utilidad_por_bolsa_sug >= 0:
    labels_sug = ["Costo", "Utilidad"]
    sizes_sug = [costo_por_bolsa, utilidad_por_bolsa_sug]
    colors_sug = ['#99CCFF', '#FFEE99']
else:
    labels_sug = ["Costo", "Pérdida"]
    sizes_sug = [costo_por_bolsa, abs(utilidad_por_bolsa_sug)]
    colors_sug = ['#99CCFF', '#FF9999']

fig_sug, ax_sug = plt.subplots(figsize=(5,5))
ax_sug.pie(
    sizes_sug, labels=labels_sug,
    startangle=90,
    autopct=make_autopct(sizes_sug),
    colors=colors_sug
)
ax_sug.set_title("Costo vs Utilidad (sugerido)")
ax_sug.axis('equal')
st.pyplot(fig_sug)

# 4) Costo + Utilidad por bolsa: Actual vs Sugerido (stacked bar)
st.markdown("**4. Costo + Utilidad por bolsa: Actual vs Sugerido**")
labels_cmp  = ["Actual", "Sugerido"]
costs_cmp   = [costo_por_bolsa, costo_por_bolsa]
profits_cmp = [utilidad_por_bolsa, utilidad_por_bolsa_sug]

fig_cmp, ax_cmp = plt.subplots(figsize=(6,4))
x = np.arange(len(labels_cmp))
width = 0.6

ax_cmp.bar(x, costs_cmp, width, label="Costo por bolsa", color="#FF9999")
for i in range(len(labels_cmp)):
    bottom = costs_cmp[i] if profits_cmp[i] >= 0 else costs_cmp[i] + profits_cmp[i]
    color = '#99FF99' if profits_cmp[i] >= 0 else '#FF9999'
    ax_cmp.bar(
        x[i], abs(profits_cmp[i]), width,
        bottom=bottom, color=color,
        label=("Utilidad" if profits_cmp[i]>=0 and i==0 else
               "Pérdida"  if profits_cmp[i]<0  and i==0 else None)
    )

ax_cmp.set_xticks(x)
ax_cmp.set_xticklabels(labels_cmp)
ax_cmp.set_ylabel("Monto ($)")
ax_cmp.set_title("Costo + Utilidad por Bolsa")

for i in range(len(labels_cmp)):
    hc = costs_cmp[i]; hp = profits_cmp[i]; total = hc+hp
    ax_cmp.text(x[i], hc/2, f"${hc:,.2f}\n({hc/total*100:.1f}%)", ha='center', va='center')
    mid = hc + hp/2
    ax_cmp.text(x[i], mid, f"${hp:,.2f}\n({hp/total*100:.1f}%)", ha='center', va='center')

ax_cmp.legend(loc="upper left")
st.pyplot(fig_cmp)

st.caption("Desarrollado para La Vaquita Feliz 🐮 — ahora muestra la utilidad y el margen actual y sugerido, tanto por unidad como en total.")
