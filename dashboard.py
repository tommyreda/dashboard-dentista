import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os

st.set_page_config(page_title="Studio Dentistico", layout="wide")

# File CSV dove salviamo gli appuntamenti
CSV_FILE = "appuntamenti.csv"

# Carica gli appuntamenti dal file se esiste
def carica_appuntamenti():
    if os.path.exists(CSV_FILE):
        return pd.read_csv(CSV_FILE)
    else:
        # Dati iniziali fittizi
        return pd.DataFrame({
            'Data': ['2026-05-01', '2026-05-05', '2026-05-10', '2026-05-15', '2026-05-20', '2026-05-25'],
            'Paziente': ['Marco Rossi', 'Anna Bianchi', 'Luca Verdi', 'Sara Neri', 'Giorgio Blu', 'Giulia Rosa'],
            'Tipo': ['Igiene', 'Conservativa', 'Igiene', 'Ortodonzia', 'Estrazione', 'Igiene'],
            'Importo': [80, 150, 80, 200, 120, 80],
        })

# Salva gli appuntamenti nel file
def salva_appuntamenti(df):
    df.to_csv(CSV_FILE, index=False)

# Carica i dati all'inizio
df_appuntamenti = carica_appuntamenti()
df_appuntamenti['Data'] = pd.to_datetime(df_appuntamenti['Data'], format='mixed')

# Sidebar
with st.sidebar:
    st.title("⚙️ Configurazione")
    st.write("Studio: Dr. Rossi")
    st.write("Mese: Maggio 2026")
    st.divider()
    if st.button("🔄 Ricarica dati"):
        st.rerun()

# Titolo
st.title("📊 Studio Dr. Rossi")
st.subheader("Dashboard KPI - Maggio 2026")

# --- KPI PRINCIPALI ---
st.subheader("📈 KPI Principali")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Appuntamenti maggio", len(df_appuntamenti), "+3 vs aprile")

with col2:
    st.metric("Incasso maggio", f"€{df_appuntamenti['Importo'].sum():.0f}", "+11% vs aprile")

with col3:
    st.metric("Media per appuntamento", f"€{df_appuntamenti['Importo'].mean():.0f}")

with col4:
    st.metric("Pazienti attivi", 312, "+8 questo mese")

st.divider()

# --- GRAFICI ---
st.subheader("📊 Andamento")
col1, col2 = st.columns(2)

with col1:
    st.write("Incasso mensile 2026")
    dati_incasso = pd.DataFrame({
        'Mese': ['Gen', 'Feb', 'Mar', 'Apr', 'Mag'],
        'Incasso': [6800, 7200, 7900, 7800, 8640]
    })
    st.bar_chart(dati_incasso.set_index('Mese'), height=300)

with col2:
    st.write("Tipo di trattamento")
    dati_trattamenti = pd.DataFrame({
        'Tipo': ['Igiene', 'Conservativa', 'Ortodonzia', 'Estrazione'],
        'Count': [38, 29, 21, 12]
    })
    st.bar_chart(dati_trattamenti.set_index('Tipo'), height=300)

st.divider()

# --- PAZIENTI DA RICHIAMARE ---
st.subheader("🔔 Pazienti da richiamare")
pazienti_richiamare = pd.DataFrame({
    'Nome': ['Anna Ferretti', 'Marco Conti', 'Giulia Marini'],
    'Ultimo appuntamento': ['6 mesi fa', 'Controllo non prenotato', 'Piano sospeso'],
    'Priorità': ['⚠️ URGENTE', '⚠️ Da seguire', '⚠️ Da seguire']
})
st.dataframe(pazienti_richiamare, use_container_width=True, hide_index=True)

st.divider()

# --- REGISTRA NUOVO APPUNTAMENTO ---
st.subheader("➕ Registra nuovo appuntamento")
with st.form("nuovo_appuntamento"):
    col1, col2 = st.columns(2)
    
    with col1:
        nome_paziente = st.text_input("Nome paziente")
        tipo_trattamento = st.selectbox("Tipo di trattamento", 
            ['Igiene', 'Conservativa', 'Ortodonzia', 'Estrazione', 'Altro'])
    
    with col2:
        data_appuntamento = st.date_input("Data appuntamento", value=datetime.now())
        importo = st.number_input("Importo (€)", min_value=0, value=100)
    
    submitted = st.form_submit_button("Registra appuntamento")
    
    if submitted:
        if nome_paziente and importo > 0:
            # Aggiungi il nuovo appuntamento al dataframe
            nuovo_app = pd.DataFrame({
                'Data': [data_appuntamento.strftime('%Y-%m-%d')],
                'Paziente': [nome_paziente],
                'Tipo': [tipo_trattamento],
                'Importo': [importo]
            })
            df_appuntamenti = pd.concat([df_appuntamenti, nuovo_app], ignore_index=True)
            salva_appuntamenti(df_appuntamenti)
            st.success(f"✅ Appuntamento registrato: {nome_paziente} - {tipo_trattamento} - €{importo}")
            st.rerun()
        else:
            st.error("⚠️ Riempi tutti i campi correttamente")

st.divider()

# --- ULTIMI APPUNTAMENTI REGISTRATI ---
st.subheader("📋 Ultimi appuntamenti registrati")
df_display = df_appuntamenti.copy()
df_display['Data'] = pd.to_datetime(df_display['Data']).dt.strftime('%d/%m/%Y')
st.dataframe(df_display, use_container_width=True, hide_index=True)

st.divider()

# --- DOWNLOAD DATI ---
st.subheader("📥 Scarica i dati")
csv = df_appuntamenti.to_csv(index=False).encode('utf-8')
st.download_button(
    label="Scarica appuntamenti in CSV",
    data=csv,
    file_name=f"appuntamenti_{datetime.now().strftime('%Y%m%d')}.csv",
    mime="text/csv"
)
