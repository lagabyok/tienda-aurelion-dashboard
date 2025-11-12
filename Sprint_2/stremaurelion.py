# =============================================================
# 🛒 Dashboard Tienda Aurelion - Versión Extendida con Pairplot
# =============================================================
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt
import folium
from streamlit_folium import st_folium

# =============================================================
# --- CONFIGURACIÓN GENERAL ---
# =============================================================
st.set_page_config(page_title="Dashboard Tienda Aurelion", layout="wide")

st.markdown("""
    <style>
    body { background-color: #FFE3E3; color: #111; } /* Texto oscuro general */
    .stButton>button {
        background-color: #F27979;
        color: white;
        border: none;
        border-radius: 10px;
        padding: 10px 25px;
        margin: 5px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #E74B3C;
    }
    h1 { color: #F24141; text-align: center; }
    footer {
        text-align: center;
        color: white;
        background-color: #F24141;
        padding: 10px;
        margin-top: 40px;
        border-radius: 8px;
    }
    /* Caja de análisis */
    .analisis-box {
        background: #FFF5F5;
        border-left: 4px solid #F24141;
        padding: 12px 15px;
        border-radius: 6px;
        margin: 15px 0;
        color: #111; /* <-- Color de texto oscuro */
        font-size: 15px;
        line-height: 1.5em;
    }
    </style>
""", unsafe_allow_html=True)

# =============================================================
# --- CARGA DE DATOS ---
# =============================================================
df = pd.read_csv("Sprint_2/productos_categorias_normalizadas.csv")

# =============================================================
# --- TÍTULO Y MÉTRICAS ---
# =============================================================
st.markdown("<h1>🛒 Tienda Aurelion - Dashboard Analítico Interactivo</h1>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    st.metric("💰 Total de Ventas", f"${df['importe'].sum():,.0f}")
with col2:
    st.metric("👥 Clientes Únicos", df['id_cliente'].nunique())

st.markdown("---")

# =============================================================
# --- BOTONES DE GRÁFICOS ---
# =============================================================
st.subheader("📊 Visualizaciones interactivas")
col1, col2, col3, col4 = st.columns(4)
chart_option = None

with col1:
    if st.button("Ventas por Categoría"):
        chart_option = "cat"
with col2:
    if st.button("Ventas por Medio de Pago"):
        chart_option = "pago"
with col3:
    if st.button("Top 5 Ciudades"):
        chart_option = "ciudad"
with col4:
    if st.button("Top 5 Clientes"):
        chart_option = "cliente"

# =============================================================
# --- GRÁFICOS PRINCIPALES ---
# =============================================================
if chart_option == "cat":
    fig = go.Figure(data=[
        go.Bar(name='Alimentos', x=['Alimentos'], y=[2214681], marker_color='#F24141'),
        go.Bar(name='Limpieza', x=['Limpieza'], y=[436736], marker_color='#F27979')
    ])
    fig.update_layout(title="Ventas por Categoría", barmode='group')
    st.plotly_chart(fig, use_container_width=True)

elif chart_option == "pago":
    fig = go.Figure(data=[
        go.Bar(x=['Efectivo'], y=[934819], marker_color='#E74B3C'),
        go.Bar(x=['QR'], y=[714280], marker_color='#F24141'),
        go.Bar(x=['Tarjeta'], y=[460099], marker_color='#F27979'),
        go.Bar(x=['Transferencia'], y=[542219], marker_color='#CBC8CB')
    ])
    fig.update_layout(title="Ventas por Medio de Pago", barmode='group')
    st.plotly_chart(fig, use_container_width=True)

elif chart_option == "ciudad":
    fig = go.Figure(data=[
        go.Bar(x=['Río Cuarto', 'Alta Gracia', 'Carlos Paz', 'Villa María', 'Mendiolaza'],
               y=[792203, 481504, 353852, 313350, 125000],
               marker_color=['#F24141', '#F27979', '#E74B3C', '#CBC8CB', '#FFE3E3'])
    ])
    fig.update_layout(title="Top 5 Ciudades", barmode='group')
    st.plotly_chart(fig, use_container_width=True)

elif chart_option == "cliente":
    fig = go.Figure(data=[
        go.Bar(x=['Cliente A', 'Cliente B', 'Cliente C', 'Cliente D', 'Cliente E'],
               y=[300000, 250000, 200000, 150000, 100000],
               marker_color=['#F24141', '#F27979', '#E74B3C', '#CBC8CB', '#FFE3E3'])
    ])
    fig.update_layout(title="Top 5 Clientes", barmode='group')
    st.plotly_chart(fig, use_container_width=True)

# =============================================================
# --- MATRIZ DE CORRELACIÓN ---
# =============================================================
st.markdown("---")
st.subheader("🔍 Matriz de Correlación (Reducida)")

corr = df.select_dtypes(include=['float64', 'int64']).corr()
fig_corr, ax_corr = plt.subplots(figsize=(6, 5))
sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax_corr, cbar=False)
st.pyplot(fig_corr)
plt.close(fig_corr)

st.markdown("""
<div class="analisis-box">
<b>🧠 Análisis (Matriz de Correlación):</b><br>
- Observá las parejas con correlación alta (positiva o negativa): indican variables que crecen o decrecen juntas.<br>
- Valores cercanos a 0 indican poca relación lineal.<br>
Usá esto para priorizar variables en modelos o investigar relaciones con más detalle.
</div>
""", unsafe_allow_html=True)

# =============================================================
# --- RELACIONES GLOBALES (Pairplot) ---
# =============================================================
st.markdown("---")
st.subheader("📈 Relaciones Globales (Pairplot Reducido)")

num_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
num_cols = [c for c in num_cols if c not in ('id_venta', 'id_cliente')]
vars_pairplot = num_cols[:5]

if len(vars_pairplot) >= 2:
    sample_size = min(200, len(df))
    pairplot_data = df[vars_pairplot].sample(sample_size, random_state=42)
    pairgrid = sns.pairplot(pairplot_data, diag_kind="kde", plot_kws={'s': 20})
    pairfig = pairgrid.fig
    pairfig.set_size_inches(10, 6)
    st.pyplot(pairfig)
    plt.close(pairfig)

    st.markdown("""
    <div class="analisis-box">
    <b>🧩 Análisis (Pairplot):</b><br>
    - El pairplot muestra distribuciones marginales y relaciones bivariadas entre las variables seleccionadas.<br>
    - Buscá patrones lineales, agrupamientos o dispersiones inusuales (posibles outliers).<br>
    - Si aparecen relaciones claras, considerá pruebas adicionales (regresión, correlación parcial).
    </div>
    """, unsafe_allow_html=True)
else:
    st.info("No hay suficientes variables numéricas para generar el pairplot.")

# =============================================================
# --- ANÁLISIS DE CORRELACIÓN: Día del Mes vs Importe Promedio ---
# =============================================================
st.markdown("---")
st.subheader("📅 Correlación entre Día del Mes e Importe Promedio")

df2 = pd.read_csv("Sprint_2/productos_categorias_normalizadas.csv")
df2['fecha'] = pd.to_datetime(df2['fecha'])
df2['dia_del_mes'] = df2['fecha'].dt.day

importe_por_venta_unica = df2.groupby(['id_venta', 'dia_del_mes'])['importe'].sum().reset_index()
importe_promedio_dia = importe_por_venta_unica.groupby('dia_del_mes')['importe'].mean().reset_index(name='importe_promedio')
data_plot = importe_promedio_dia.rename(columns={'dia_del_mes': 'Día del Mes', 'importe_promedio': 'Importe Promedio de Venta'})
correlacion = data_plot['Día del Mes'].corr(data_plot['Importe Promedio de Venta'])

fig_scatter, ax_scatter = plt.subplots(figsize=(7, 4))
sns.scatterplot(x='Día del Mes', y='Importe Promedio de Venta', data=data_plot,
                ax=ax_scatter, color='darkgreen', edgecolor='black', s=80)
z = np.polyfit(data_plot['Día del Mes'], data_plot['Importe Promedio de Venta'], 1)
p = np.poly1d(z)
ax_scatter.plot(data_plot['Día del Mes'], p(data_plot['Día del Mes']),
                color='red', linestyle='--', linewidth=2)
promedio_general = importe_promedio_dia['importe_promedio'].mean()
ax_scatter.axhline(promedio_general, color='blue', linestyle=':', linewidth=1.2)
ax_scatter.set_title('Correlación: Importe Promedio de Venta Única vs Día del Mes', fontsize=12, fontweight='bold')
ax_scatter.set_xlabel('Día del Mes')
ax_scatter.set_ylabel('Importe Promedio de Venta Única')
st.pyplot(fig_scatter)
plt.close(fig_scatter)

fuerza = ("MUY DÉBIL" if abs(correlacion) < 0.1 else
          "DÉBIL" if abs(correlacion) < 0.3 else
          "MODERADA" if abs(correlacion) < 0.5 else
          "FUERTE")

st.markdown(f"""
<div class="analisis-box">
<b>Coeficiente de Correlación (Pearson):</b> {correlacion:.4f} — <b>{fuerza}</b><br>
Interpretación rápida: {'Hay una tendencia a gastar más a principios de mes.' if correlacion < 0 else 'El gasto tiende a subir hacia fines de mes.' if correlacion > 0 else 'No se observa tendencia lineal clara.'}
<br>Conclusión: usá este hallazgo como indicio (no prueba) — considerar segmentar por tipo de cliente o promociones para validar el efecto día de pago.
</div>
""", unsafe_allow_html=True)

# =============================================================
# --- MAPA INTERACTIVO DE VENTAS POR CIUDAD ---
# =============================================================
st.markdown("---")
st.subheader("🗺️ Mapa Interactivo de Ventas por Ciudad")

ventas_por_ciudad = df.groupby('ciudad')['id_venta'].nunique().reset_index()
ventas_por_ciudad.rename(columns={'id_venta': 'numero_ventas'}, inplace=True)

coordenadas_ciudades = {
    'Rio Cuarto': [-33.1227, -64.3248],
    'Alta Gracia': [-31.6521, -64.4273],
    'Cordoba': [-31.4201, -64.1888],
    'Carlos Paz': [-31.4234, -64.5043],
    'Villa Maria': [-32.4073, -63.2433],
    'Mendiolaza': [-31.2667, -64.3167],
}

ventas_por_ciudad['latitud'] = ventas_por_ciudad['ciudad'].map(lambda x: coordenadas_ciudades.get(x, [0, 0])[0])
ventas_por_ciudad['longitud'] = ventas_por_ciudad['ciudad'].map(lambda x: coordenadas_ciudades.get(x, [0, 0])[1])

centro_mapa = [-31.4201, -64.1888]
mapa_ventas = folium.Map(location=centro_mapa, zoom_start=8)

for _, row in ventas_por_ciudad.iterrows():
    folium.CircleMarker(
        location=[row['latitud'], row['longitud']],
        radius=max(5, row['numero_ventas'] * 0.4),
        popup=f"<b>{row['ciudad']}</b><br>Ventas: {row['numero_ventas']}",
        color='blue',
        fill=True,
        fill_color='steelblue',
        fill_opacity=0.6
    ).add_to(mapa_ventas)

st_folium(mapa_ventas, width=700, height=450)

# =============================================================
# --- FOOTER ---
# =============================================================
st.markdown("""
<footer>
    © 2025 Tienda Aurelion | Dashboard desarrollado por <b>Gabriela Coronel</b>
</footer>
""", unsafe_allow_html=True)
