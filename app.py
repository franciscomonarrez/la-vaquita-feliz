import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import sqlite3
from datetime import datetime
import pandas as pd

# ----------------- DATABASE SETUP -----------------
def init_database():
    """Initialize the SQLite database and create tables if they don't exist."""
    conn = sqlite3.connect('machaca_calculator.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS calculation_versions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            version_name TEXT NOT NULL,
            created_date TEXT NOT NULL,
            carne_fresca REAL,
            sal REAL,
            sueldo1 REAL,
            trabajador_adicional REAL,
            empleado_ventas REAL,
            redes_sociales REAL,
            corte_carne REAL,
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
    conn.close()

def save_calculation(version_name, data):
    """Save a calculation version to the database."""
    conn = sqlite3.connect('machaca_calculator.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO calculation_versions (
            version_name, created_date, carne_fresca, sal, sueldo1,
            trabajador_adicional, empleado_ventas, redes_sociales, corte_carne, luz, agua, fumigacion,
            liquidos_limpieza, otro_liquido, total_unidades,
            precio_venta, precio_venta_sugerido
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        version_name,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        data['carne_fresca'],
        data['sal'],
        data['sueldo1'],
        data['trabajador_adicional'],
        data['empleado_ventas'],
        data['redes_sociales'],
        data['corte_carne'],
        data['luz'],
        data['agua'],
        data['fumigacion'],
        data['liquidos_limpieza'],
        data['otro_liquido'],
        data['total_unidades'],
        data['precio_venta'],
        data['precio_venta_sugerido']
    ))
    
    conn.commit()
    conn.close()

def get_all_versions():
    """Get all saved calculation versions."""
    conn = sqlite3.connect('machaca_calculator.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, version_name, created_date FROM calculation_versions
        ORDER BY created_date DESC
    ''')
    
    versions = cursor.fetchall()
    conn.close()
    return versions

def get_version_data(version_id):
    """Get data for a specific version."""
    conn = sqlite3.connect('machaca_calculator.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT * FROM calculation_versions WHERE id = ?
    ''', (version_id,))
    
    version_data = cursor.fetchone()
    conn.close()
    return version_data

def delete_version(version_id):
    """Delete a specific version."""
    conn = sqlite3.connect('machaca_calculator.db')
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM calculation_versions WHERE id = ?', (version_id,))
    
    conn.commit()
    conn.close()

# Initialize database
init_database()

# ----------------- CONFIG -----------------
st.set_page_config(
    page_title="La Vaquita Feliz 🐮 - Calculadora de Utilidad",
    page_icon="🐮",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ----------------- CSS CUSTOMIZATION -----------------
st.markdown(
    """
    <style>
      /* Constrain max width */
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
      /* Smaller metric text */
      .stMetricValue, .css-1v0mbdj {
        font-size: 1rem !important;
      }
      .stMetricLabel, .css-1avcm0n {
        font-size: 0.8rem !important;
      }
      /* Hide footer */
      footer {visibility: hidden;}
      /* Style for save button */
      .save-section {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
      }
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------- PAGE NAVIGATION -----------------
page = st.sidebar.selectbox("📋 Navegación", ["Calculadora Principal", "Versiones Guardadas"])

if page == "Calculadora Principal":
    # ----------------- INITIALIZE SESSION STATE DEFAULTS -----------------
    # Initialize session state with default values if not already set
    if 'initialized' not in st.session_state:
        st.session_state.initialized = True
        st.session_state.carne_fresca = 52473.06
        st.session_state.sal = 31.35
        st.session_state.sueldo1 = 7266.95
        st.session_state.trabajador_adicional = 3000.00
        st.session_state.empleado_ventas = 0.00
        st.session_state.redes_sociales = 0.00
        st.session_state.corte_carne = 1024.14
        st.session_state.luz = 651.25
        st.session_state.agua = 145.34
        st.session_state.fumigacion = 726.69
        st.session_state.liquidos_limpieza = 297.01
        st.session_state.otro_liquido = 18.35
        st.session_state.total_unidades = 453
        st.session_state.precio_venta = 145.18
        st.session_state.precio_venta_sugerido = 196.00

    # ----------------- LOAD VERSION DATA IF SELECTED -----------------
    if 'load_version_data' in st.session_state and st.session_state.load_version_data:
        version_data = st.session_state.load_version_data
        # Set session state values from loaded data
        st.session_state.carne_fresca = version_data[3]
        st.session_state.sal = version_data[4]
        st.session_state.sueldo1 = version_data[5]
        st.session_state.trabajador_adicional = version_data[6]
        
        # Handle new fields for older versions
        if len(version_data) > 7:
            st.session_state.empleado_ventas = version_data[7]
        else:
            st.session_state.empleado_ventas = 0.0
            
        if len(version_data) > 8:
            st.session_state.redes_sociales = version_data[8]
        else:
            st.session_state.redes_sociales = 0.0
            
        if len(version_data) > 9:
            st.session_state.corte_carne = version_data[9]
        else:
            st.session_state.corte_carne = version_data[7] if len(version_data) > 7 else 0.0
            
        if len(version_data) > 10:
            st.session_state.luz = version_data[10]
        else:
            st.session_state.luz = version_data[8] if len(version_data) > 8 else 0.0
            
        if len(version_data) > 11:
            st.session_state.agua = version_data[11]
        else:
            st.session_state.agua = version_data[9] if len(version_data) > 9 else 0.0
            
        if len(version_data) > 12:
            st.session_state.fumigacion = version_data[12]
        else:
            st.session_state.fumigacion = version_data[10] if len(version_data) > 10 else 0.0
            
        if len(version_data) > 13:
            st.session_state.liquidos_limpieza = version_data[13]
        else:
            st.session_state.liquidos_limpieza = version_data[11] if len(version_data) > 11 else 0.0
            
        if len(version_data) > 14:
            st.session_state.otro_liquido = version_data[14]
        else:
            st.session_state.otro_liquido = version_data[12] if len(version_data) > 12 else 0.0
            
        if len(version_data) > 15:
            st.session_state.total_unidades = version_data[15]
        else:
            st.session_state.total_unidades = version_data[13] if len(version_data) > 13 else 1
            
        if len(version_data) > 16:
            st.session_state.precio_venta = version_data[16]
        else:
            st.session_state.precio_venta = version_data[14] if len(version_data) > 14 else 0.0
            
        if len(version_data) > 17:
            st.session_state.precio_venta_sugerido = version_data[17]
        else:
            st.session_state.precio_venta_sugerido = version_data[15] if len(version_data) > 15 else 0.0
        
        # Clear the session state
        st.session_state.load_version_data = None
    elif 'reset_values' in st.session_state and st.session_state.reset_values:
        # Set all values to zero for reset
        st.session_state.carne_fresca = 0.0
        st.session_state.sal = 0.0
        st.session_state.sueldo1 = 0.0
        st.session_state.trabajador_adicional = 0.0
        st.session_state.empleado_ventas = 0.0
        st.session_state.redes_sociales = 0.0
        st.session_state.corte_carne = 0.0
        st.session_state.luz = 0.0
        st.session_state.agua = 0.0
        st.session_state.fumigacion = 0.0
        st.session_state.liquidos_limpieza = 0.0
        st.session_state.otro_liquido = 0.0
        st.session_state.total_unidades = 1
        st.session_state.precio_venta = 0.0
        st.session_state.precio_venta_sugerido = 0.0
        
        # Clear the reset flag
        st.session_state.reset_values = False

    # ----------------- SIDEBAR INPUTS -----------------
    st.sidebar.header("🛠 Ajustes de Costos & Ventas")

    # Materia Prima
    st.sidebar.subheader("🔹 Materia Prima")
    st.session_state.carne_fresca = st.sidebar.number_input("Carne fresca ($)", min_value=0.0, value=st.session_state.carne_fresca, step=10.0)
    st.session_state.sal = st.sidebar.number_input("Sal ($)", min_value=0.0, value=st.session_state.sal, step=1.0)

    # Mano de Obra
    st.sidebar.subheader("🔹 Mano de Obra")
    st.session_state.sueldo1 = st.sidebar.number_input("Sueldo principal ($)", min_value=0.0, value=st.session_state.sueldo1, step=10.0)
    st.session_state.trabajador_adicional = st.sidebar.number_input("Trabajador adicional ($)", min_value=0.0, value=st.session_state.trabajador_adicional, step=10.0)
    st.session_state.empleado_ventas = st.sidebar.number_input("Empleado de ventas ($)", min_value=0.0, value=st.session_state.empleado_ventas, step=10.0)
    st.session_state.redes_sociales = st.sidebar.number_input("Redes sociales ($)", min_value=0.0, value=st.session_state.redes_sociales, step=10.0)
    st.session_state.corte_carne = st.sidebar.number_input("Costo de corte de carne ($)", min_value=0.0, value=st.session_state.corte_carne, step=10.0)

    # Servicios y Gastos Fijos
    st.sidebar.subheader("🔹 Servicios & Fijos")
    st.session_state.luz = st.sidebar.number_input("Luz mensual ($)", min_value=0.0, value=float(st.session_state.luz), step=1.0)
    st.session_state.agua = st.sidebar.number_input("Agua ($)", min_value=0.0, value=float(st.session_state.agua), step=1.0)
    st.session_state.fumigacion = st.sidebar.number_input("Fumigación ($)", min_value=0.0, value=float(st.session_state.fumigacion), step=1.0)
    st.session_state.liquidos_limpieza = st.sidebar.number_input("Líquidos de limpieza ($)", min_value=0.0, value=float(st.session_state.liquidos_limpieza), step=1.0)
    st.session_state.otro_liquido = st.sidebar.number_input("Otro líquido de limpieza ($)", min_value=0.0, value=float(st.session_state.otro_liquido), step=1.0)

    # Producción y Ventas
    st.sidebar.subheader("🛒 Producción & Ventas")
    st.session_state.total_unidades = st.sidebar.number_input("Bolsas producidas", min_value=1, value=int(st.session_state.total_unidades), step=1)
    
    # Calculate cost per bag first for margin calculations using session state values
    costo_unitario_empaque = 2.0
    empaques = st.session_state.total_unidades * costo_unitario_empaque
    costo_total_temp = (
        st.session_state.carne_fresca + st.session_state.sal + st.session_state.corte_carne +
        st.session_state.sueldo1 + st.session_state.trabajador_adicional + st.session_state.empleado_ventas + st.session_state.redes_sociales +
        st.session_state.luz + st.session_state.agua + st.session_state.fumigacion +
        st.session_state.liquidos_limpieza + st.session_state.otro_liquido +
        empaques
    )
    costo_por_bolsa_temp = costo_total_temp / st.session_state.total_unidades
    
    # Price/Margin control options
    precio_control = st.sidebar.radio(
        "🎯 Control de Precio/Margen:",
        ["Por Precio", "Por Margen %"],
        help="Elige si quieres controlar el precio directamente o por margen de ganancia"
    )
    
    # --- PRECIO ACTUAL ---
    st.sidebar.markdown("**💰 Precio Actual**")
    if precio_control == "Por Precio":
        st.session_state.precio_venta = st.sidebar.number_input("Precio actual por bolsa ($)", min_value=0.0, value=float(st.session_state.precio_venta), step=1.0)
        # Calculate and display margin
        if st.session_state.precio_venta > 0:
            margen_calculado = ((st.session_state.precio_venta - costo_por_bolsa_temp) / st.session_state.precio_venta) * 100
            if margen_calculado >= 0:
                st.sidebar.info(f"📊 Margen actual: {margen_calculado:.1f}%")
            else:
                st.sidebar.error(f"⚠️ Margen negativo: {margen_calculado:.1f}% (PÉRDIDA)")
        else:
            st.sidebar.warning("⚠️ Precio debe ser mayor a $0")
    else:
        # Control by margin
        # Calculate current margin for default value, but handle negative margins
        if st.session_state.precio_venta > 0:
            current_margin = ((st.session_state.precio_venta - costo_por_bolsa_temp) / st.session_state.precio_venta * 100)
            # Ensure the margin is not negative for the number input
            current_margin = max(0.0, current_margin)
        else:
            current_margin = 20.0
        
        margen_deseado = st.sidebar.number_input(
            "Margen deseado (%)", 
            min_value=0.0, 
            max_value=95.0,  # Changed from 100 to 95 to avoid division issues
            value=current_margin,
            step=1.0,
            help="Margen de ganancia deseado en porcentaje"
        )
        
        # Calculate price based on margin
        if margen_deseado < 95:  # Avoid division by zero/negative issues
            st.session_state.precio_venta = costo_por_bolsa_temp / (1 - margen_deseado/100)
        else:
            st.session_state.precio_venta = costo_por_bolsa_temp * 20  # Fallback for high margins
        
        st.sidebar.info(f"💰 Precio calculado: ${st.session_state.precio_venta:.2f}")
        
        # Show warning if original margin was negative
        if st.session_state.precio_venta > 0:
            original_margin = ((st.session_state.precio_venta - costo_por_bolsa_temp) / st.session_state.precio_venta * 100)
            if original_margin < 0:
                st.sidebar.warning(f"⚠️ Nota: El precio original tenía un margen negativo de {original_margin:.1f}%")

    # --- PRECIO SUGERIDO ---
    st.sidebar.markdown("**✨ Precio Sugerido**")
    if precio_control == "Por Precio":
        st.session_state.precio_venta_sugerido = st.sidebar.number_input("Precio sugerido por bolsa ($)", min_value=0.0, value=float(st.session_state.precio_venta_sugerido), step=1.0)
        # Calculate and display margin for suggested price
        if st.session_state.precio_venta_sugerido > 0:
            margen_calculado_sug = ((st.session_state.precio_venta_sugerido - costo_por_bolsa_temp) / st.session_state.precio_venta_sugerido) * 100
            if margen_calculado_sug >= 0:
                st.sidebar.info(f"📊 Margen sugerido: {margen_calculado_sug:.1f}%")
            else:
                st.sidebar.error(f"⚠️ Margen negativo: {margen_calculado_sug:.1f}% (PÉRDIDA)")
        else:
            st.sidebar.warning("⚠️ Precio debe ser mayor a $0")
    else:
        # Control by margin for suggested price
        # Calculate current margin for default value, but handle negative margins
        if st.session_state.precio_venta_sugerido > 0:
            current_margin_sug = ((st.session_state.precio_venta_sugerido - costo_por_bolsa_temp) / st.session_state.precio_venta_sugerido * 100)
            # Ensure the margin is not negative for the number input
            current_margin_sug = max(0.0, current_margin_sug)
        else:
            current_margin_sug = 30.0  # Default higher margin for suggested price
        
        margen_deseado_sug = st.sidebar.number_input(
            "Margen sugerido (%)", 
            min_value=0.0, 
            max_value=95.0,  # Changed from 100 to 95 to avoid division issues
            value=current_margin_sug,
            step=1.0,
            help="Margen de ganancia deseado para el precio sugerido"
        )
        
        # Calculate suggested price based on margin
        if margen_deseado_sug < 95:  # Avoid division by zero/negative issues
            st.session_state.precio_venta_sugerido = costo_por_bolsa_temp / (1 - margen_deseado_sug/100)
        else:
            st.session_state.precio_venta_sugerido = costo_por_bolsa_temp * 20  # Fallback for high margins
        
        st.sidebar.info(f"✨ Precio sugerido calculado: ${st.session_state.precio_venta_sugerido:.2f}")
        
        # Show warning if original suggested margin was negative
        if st.session_state.precio_venta_sugerido > 0:
            original_margin_sug = ((st.session_state.precio_venta_sugerido - costo_por_bolsa_temp) / st.session_state.precio_venta_sugerido * 100)
            if original_margin_sug < 0:
                st.sidebar.warning(f"⚠️ Nota: El precio sugerido original tenía un margen negativo de {original_margin_sug:.1f}%")
    
    # Session state already updated by inputs

    # ----------------- MAIN LAYOUT -----------------
    st.title("🐮 La Vaquita Feliz")
    st.subheader("Calculadora Visual de Utilidad para Machaca")

    # ----------------- RESET SECTION -----------------
    with st.container():
        st.markdown("### 🔄 Resetear Calculadora")
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.info("Esto pondrá todos los valores en cero. Útil para empezar un cálculo completamente nuevo.")
        
        with col2:
            if st.button("🔄 Resetear Todo", type="secondary"):
                # Reset all values by clearing session state and rerunning
                if 'load_version_data' in st.session_state:
                    del st.session_state.load_version_data
                
                # Set all values to zero by creating a reset flag
                st.session_state.reset_values = True
                st.success("✅ Todos los valores han sido reseteados")
                st.rerun()
        
        st.markdown("---")

    # ----------------- SAVE SECTION -----------------
    with st.container():
        st.markdown('<div class="save-section">', unsafe_allow_html=True)
        st.markdown("### 💾 Guardar Cálculo")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            version_name = st.text_input("Nombre de la versión:", placeholder="Ej: Cálculo Enero 2025")
        with col2:
            st.write("")  # Empty space for alignment
            if st.button("💾 Guardar", type="primary"):
                if version_name:
                    # Prepare data to save
                    data_to_save = {
                        'carne_fresca': st.session_state.carne_fresca,
                        'sal': st.session_state.sal,
                        'sueldo1': st.session_state.sueldo1,
                        'trabajador_adicional': st.session_state.trabajador_adicional,
                        'empleado_ventas': st.session_state.empleado_ventas,
                        'redes_sociales': st.session_state.redes_sociales,
                        'corte_carne': st.session_state.corte_carne,
                        'luz': st.session_state.luz,
                        'agua': st.session_state.agua,
                        'fumigacion': st.session_state.fumigacion,
                        'liquidos_limpieza': st.session_state.liquidos_limpieza,
                        'otro_liquido': st.session_state.otro_liquido,
                        'total_unidades': st.session_state.total_unidades,
                        'precio_venta': st.session_state.precio_venta,
                        'precio_venta_sugerido': st.session_state.precio_venta_sugerido
                    }
                    
                    save_calculation(version_name, data_to_save)
                    st.success(f"✅ Versión '{version_name}' guardada exitosamente!")
                else:
                    st.error("❌ Por favor ingresa un nombre para la versión")
        
        st.markdown('</div>', unsafe_allow_html=True)

    # --- FÓRMULAS USADAS ---
    with st.expander("🧮 Fórmulas detalladas"):
        st.markdown("""
        1. **Costo de empaques**  
           `empaques = total_unidades × $2`

        2. **Costo total**  
           `costo_total = carne_fresca + sal + corte_carne + sueldo1 + trabajador_adicional + empleado_ventas + redes_sociales + luz + agua + fumigacion + liquidos_limpieza + otro_liquido + empaques`

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
    empaques = st.session_state.total_unidades * costo_unitario_empaque

    costo_total = (
        st.session_state.carne_fresca + st.session_state.sal + st.session_state.corte_carne +
        st.session_state.sueldo1 + st.session_state.trabajador_adicional + st.session_state.empleado_ventas + st.session_state.redes_sociales +
        st.session_state.luz + st.session_state.agua + st.session_state.fumigacion +
        st.session_state.liquidos_limpieza + st.session_state.otro_liquido +
        empaques
    )
    costo_por_bolsa = costo_total / st.session_state.total_unidades

    utilidad_por_bolsa = st.session_state.precio_venta - costo_por_bolsa
    utilidad_total = utilidad_por_bolsa * st.session_state.total_unidades
    utilidad_pct = (utilidad_por_bolsa / st.session_state.precio_venta * 100) if st.session_state.precio_venta else 0

    utilidad_por_bolsa_sug = st.session_state.precio_venta_sugerido - costo_por_bolsa
    utilidad_total_sug = utilidad_por_bolsa_sug * st.session_state.total_unidades
    utilidad_pct_sug = (utilidad_por_bolsa_sug / st.session_state.precio_venta_sugerido * 100) if st.session_state.precio_venta_sugerido else 0

    # ----------------- MÉTRICAS -----------------
    st.success(f"### Costo total del mes: ${costo_total:,.2f}")

    col1, col2 = st.columns(2)
    col1.metric("Costo/bolsa", f"${costo_por_bolsa:,.2f}")
    col2.metric("Bolsas producidas", f"{st.session_state.total_unidades}")

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

    # ----------------- COSTO DE EMPAQUES -----------------
    st.markdown("**Costo de Empaques**")
    e1, e2 = st.columns(2)
    e1.metric("Costo total empaques", f"${empaques:,.2f}")
    e2.metric("Costo empaque / bolsa", f"${costo_unitario_empaque:.2f}")

    # ----------------- FUNCIÓN AUTOPCT -----------------
    def make_autopct(values):
        def my_autopct(pct):
            total = sum(values)
            val = pct * total / 100
            return f"{val:,.2f}\n({pct:.1f}%)"
        return my_autopct

    # ----------------- GRÁFICOS -----------------
    st.header("📊 Análisis Gráfico")

    # 1) Costos por rubro
    st.subheader("1. Costos por Rubro")
    labels = [
        "Carne fresca","Sal","Corte","Sueldo princ.","Trabajador adic.","Empleado ventas","Redes sociales",
        "Luz","Agua","Fumigación","Líquidos limp.","Otro líquido","Empaques"
    ]
    values = [
        st.session_state.carne_fresca, st.session_state.sal, st.session_state.corte_carne, st.session_state.sueldo1, st.session_state.trabajador_adicional, st.session_state.empleado_ventas, st.session_state.redes_sociales,
        st.session_state.luz, st.session_state.agua, st.session_state.fumigacion, st.session_state.liquidos_limpieza, st.session_state.otro_liquido, empaques
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

    st.caption("Desarrollado para La Vaquita Feliz 🐮 — tablas y gráficos optimizados para lectura.")

# ----------------- VERSIONS PAGE -----------------
elif page == "Versiones Guardadas":
    st.title("📂 Versiones Guardadas")
    st.subheader("Gestión de Cálculos Guardados")

    # Get all versions
    versions = get_all_versions()

    if not versions:
        st.info("📝 No hay versiones guardadas aún. Ve a la Calculadora Principal para guardar tu primer cálculo.")
    else:
        st.success(f"📊 Total de versiones guardadas: {len(versions)}")
        
        # Display versions in a nice format
        for version in versions:
            version_id, version_name, created_date = version
            
            with st.container():
                col1, col2, col3 = st.columns([3, 2, 1])
                
                with col1:
                    st.markdown(f"**{version_name}**")
                    st.caption(f"Creado: {created_date}")
                
                with col2:
                    if st.button(f"📋 Cargar", key=f"load_{version_id}"):
                        version_data = get_version_data(version_id)
                        st.session_state.load_version_data = version_data
                        st.success(f"✅ Versión '{version_name}' cargada. Ve a la Calculadora Principal para verla.")
                        st.rerun()
                
                with col3:
                    if st.button(f"🗑️ Eliminar", key=f"delete_{version_id}", type="secondary"):
                        delete_version(version_id)
                        st.success(f"🗑️ Versión '{version_name}' eliminada.")
                        st.rerun()
                
                st.markdown("---")

        # Show