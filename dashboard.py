import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os

st.set_page_config(page_title="Studio Dentistico", layout="wide")

# File CSV
CSV_PAZIENTI = "pazienti.csv"
CSV_APPUNTAMENTI = "appuntamenti.csv"

# Carica pazienti
def carica_pazienti():
    if os.path.exists(CSV_PAZIENTI):
        return pd.read_csv(CSV_PAZIENTI)
    else:
        return pd.DataFrame({
            'ID': [1, 2, 3, 4, 5],
            'Nome': ['Marco', 'Anna', 'Luca', 'Sara', 'Giorgio'],
            'Cognome': ['Rossi', 'Bianchi', 'Verdi', 'Neri', 'Blu'],
            'Telefono': ['320 123 4567', '335 987 6543', '340 555 1234', '333 222 1111', '345 666 7777'],
            'Data nascita': ['1985-03-15', '1990-07-22', '1988-11-30', '1992-01-10', '1980-05-20']
        })

# Carica appuntamenti
def carica_appuntamenti():
    if os.path.exists(CSV_APPUNTAMENTI):
        return pd.read_csv(CSV_APPUNTAMENTI)
    else:
        return pd.DataFrame({
            'Data': ['2026-05-01', '2026-05-05', '2026-05-10', '2026-05-15', '2026-05-20', '2026-05-25'],
            'Paziente ID': [1, 2, 1, 3, 4, 5],
            'Tipo': ['Igiene', 'Conservativa', 'Igiene', 'Ortodonzia', 'Estrazione', 'Igiene'],
            'Importo': [80, 150, 80, 200, 120, 80],
        })

def salva_pazienti(df):
    df.to_csv(CSV_PAZIENTI, index=False)

def salva_appuntamenti(df):
    df.to_csv(CSV_APPUNTAMENTI, index=False)

# Carica dati
df_pazienti = carica_pazienti()
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

st.title("📊 Studio Dr. Rossi")
st.subheader("Dashboard KPI - Maggio 2026")

# --- TABS ---
tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard", "👥 Pazienti", "📅 Appuntamenti", "⚙️ Gestione"])

# ============= TAB 1: DASHBOARD =============
with tab1:
    # KPI PRINCIPALI
    st.subheader("📈 KPI Principali")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Appuntamenti maggio", len(df_appuntamenti), "+3 vs aprile")
    
    with col2:
        st.metric("Incasso maggio", f"€{df_appuntamenti['Importo'].sum():.0f}", "+11% vs aprile")
    
    with col3:
        st.metric("No-show questo mese", 4, "2 da contattare")
    
    with col4:
        st.metric("Pazienti attivi", len(df_pazienti), "+2 questo mese")
    
    st.divider()
    
    # GRAFICI
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
    
    # PAZIENTI DA RICHIAMARE
    st.subheader("🔔 Pazienti da richiamare")
    pazienti_richiamare = pd.DataFrame({
        'Nome': ['Anna Ferretti', 'Marco Conti', 'Giulia Marini'],
        'Ultima visita': ['6 mesi fa', '4 mesi fa', '3.5 mesi fa'],
        'Telefono': ['320 123 4567', '335 987 6543', '340 555 1234'],
        'Priorità': ['⚠️ URGENTE', '⚠️ Da seguire', '⚠️ Da seguire']
    })
    st.dataframe(pazienti_richiamare, use_container_width=True, hide_index=True)
    
    st.divider()
    
    # CANCELLAZIONI E NO-SHOW
    st.subheader("❌ Cancellazioni e no-show")
    cancellazioni = pd.DataFrame({
        'Paziente': ['Roberto Gallo', 'Lisa Neri', 'Paolo Verdi'],
        'Data': ['2026-05-20', '2026-05-18', '2026-05-15'],
        'Tipo': ['Conservativa', 'Igiene', 'No-show'],
        'Telefono': ['333 222 1111', '345 666 7777', '328 999 0000'],
        'Note': ['Ha detto "rimando"', 'Non si è presentato', 'Non ha riconfermato']
    })
    st.dataframe(cancellazioni, use_container_width=True, hide_index=True)
    
    st.divider()
    
    # FORNITURE
    st.subheader("📦 Forniture in esaurimento")
    forniture = pd.DataFrame({
        'Materiale': ['Dischi abrasivi 25mm', 'Detergente ultrasonico', 'Guanti nitrile taglia L', 'Mascherine FFP2', 'Frese diamantate set 5'],
        'Quantità residua': [5, 2, 1, 8, 3],
        'Livello minimo': [20, 5, 10, 20, 5],
        'Status': ['⚠️ Finire', '⚠️ Finire', '🔴 ORDINARE SUBITO', '✅ OK', '⚠️ Finire']
    })
    st.dataframe(forniture, use_container_width=True, hide_index=True)

# ============= TAB 2: PAZIENTI =============
with tab2:
    st.subheader("👥 Elenco pazienti")
    
    # Mostra lista pazienti
    df_pazienti_display = df_pazienti.copy()
    st.dataframe(df_pazienti_display, use_container_width=True, hide_index=True)
    
    st.divider()
    
    # Storico paziente
    st.subheader("📋 Storico paziente")
    paziente_selezionato = st.selectbox("Seleziona paziente", 
        options=df_pazienti['ID'], 
        format_func=lambda x: f"{df_pazienti[df_pazienti['ID']==x]['Nome'].values[0]} {df_pazienti[df_pazienti['ID']==x]['Cognome'].values[0]}")
    
    # Mostra appuntamenti del paziente
    appuntamenti_paziente = df_appuntamenti[df_appuntamenti['Paziente ID'] == paziente_selezionato]
    if len(appuntamenti_paziente) > 0:
        st.write(f"**Appuntamenti totali:** {len(appuntamenti_paziente)}")
        st.write(f"**Spesa totale:** €{appuntamenti_paziente['Importo'].sum():.0f}")
        st.dataframe(appuntamenti_paziente[['Data', 'Tipo', 'Importo']], use_container_width=True, hide_index=True)
    else:
        st.info("Nessun appuntamento registrato per questo paziente")

# ============= TAB 3: APPUNTAMENTI =============
with tab3:
    st.subheader("📅 Ultimi appuntamenti")
    df_display = df_appuntamenti.copy()
    df_display['Data'] = pd.to_datetime(df_display['Data']).dt.strftime('%d/%m/%Y')
    
    # Aggiungi nome paziente
    df_display['Paziente'] = df_display['Paziente ID'].apply(
        lambda x: f"{df_pazienti[df_pazienti['ID']==x]['Nome'].values[0]} {df_pazienti[df_pazienti['ID']==x]['Cognome'].values[0]}"
    )
    
    st.dataframe(df_display[['Data', 'Paziente', 'Tipo', 'Importo']], use_container_width=True, hide_index=True)

# ============= TAB 4: GESTIONE =============
with tab4:
    st.subheader("➕ Registra nuovo paziente")
    with st.form("nuovo_paziente"):
        col1, col2 = st.columns(2)
        
        with col1:
            nome = st.text_input("Nome")
            cognome = st.text_input("Cognome")
        
        with col2:
            telefono = st.text_input("Telefono")
            data_nascita = st.date_input("Data di nascita")
        
        submitted_paziente = st.form_submit_button("Registra paziente")
        
        if submitted_paziente and nome and cognome:
            nuovo_id = df_pazienti['ID'].max() + 1 if len(df_pazienti) > 0 else 1
            nuovo_paziente = pd.DataFrame({
                'ID': [nuovo_id],
                'Nome': [nome],
                'Cognome': [cognome],
                'Telefono': [telefono],
                'Data nascita': [data_nascita.strftime('%Y-%m-%d')]
            })
            df_pazienti = pd.concat([df_pazienti, nuovo_paziente], ignore_index=True)
            salva_pazienti(df_pazienti)
            st.success(f"✅ Paziente registrato: {nome} {cognome}")
            st.rerun()
        elif submitted_paziente:
            st.error("⚠️ Inserisci almeno nome e cognome")
    
    st.divider()
    
    st.subheader("➕ Registra nuovo appuntamento")
    with st.form("nuovo_appuntamento"):
        col1, col2 = st.columns(2)
        
        with col1:
            # Dropdown di pazienti
            paziente_id = st.selectbox("Paziente", 
                options=df_pazienti['ID'],
                format_func=lambda x: f"{df_pazienti[df_pazienti['ID']==x]['Nome'].values[0]} {df_pazienti[df_pazienti['ID']==x]['Cognome'].values[0]}")
            
            tipo_trattamento = st.selectbox("Tipo di trattamento", 
                ['Igiene', 'Conservativa', 'Ortodonzia', 'Estrazione', 'Altro'])
        
        with col2:
            data_appuntamento = st.date_input("Data appuntamento", value=datetime.now())
            importo = st.number_input("Importo (€)", min_value=0, value=100)
        
        submitted_app = st.form_submit_button("Registra appuntamento")
        
        if submitted_app:
            nuovo_app = pd.DataFrame({
                'Data': [data_appuntamento.strftime('%Y-%m-%d')],
                'Paziente ID': [paziente_id],
                'Tipo': [tipo_trattamento],
                'Importo': [importo]
            })
            df_appuntamenti = pd.concat([df_appuntamenti, nuovo_app], ignore_index=True)
            salva_appuntamenti(df_appuntamenti)
            st.success(f"✅ Appuntamento registrato")
            st.rerun()
    
    st.divider()
    
    st.subheader("📥 Scarica i dati")
    col1, col2 = st.columns(2)
    
    with col1:
        csv_pazienti = df_pazienti.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Scarica pazienti in CSV",
            data=csv_pazienti,
            file_name=f"pazienti_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    
    with col2:
        csv_app = df_appuntamenti.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Scarica appuntamenti in CSV",
            data=csv_app,
            file_name=f"appuntamenti_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
