import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os

st.set_page_config(page_title="Studio Dentistico", layout="wide")

CSV_PAZIENTI = "pazienti.csv"
CSV_APPUNTAMENTI = "appuntamenti.csv"

# Configurazione orari e durate
ORARI_LAVORO = {
    'inizio_mattina': 9,
    'fine_mattina': 13,
    'inizio_pomeriggio': 14,
    'fine_pomeriggio': 18,
}

DURATA_TRATTAMENTI = {
    'Igiene': 30,
    'Conservativa': 60,
    'Ortodonzia': 45,
    'Estrazione': 45,
    'Altro': 30
}

def calcola_slot_disponibili(data, tipo_trattamento, df_app):
    """Calcola gli slot liberi per una data considerando pause e sovrapposizioni"""
    durata = DURATA_TRATTAMENTI.get(tipo_trattamento, 30)
    slot_disponibili = []
    
    # Orari precisi per controlli esatti (evitano bug su fine giornata e pausa pranzo)
    inizio_pausa = pd.Timestamp(f"{data.strftime('%Y-%m-%d')} {ORARI_LAVORO['fine_mattina']:02d}:00")
    fine_pausa = pd.Timestamp(f"{data.strftime('%Y-%m-%d')} {ORARI_LAVORO['inizio_pomeriggio']:02d}:00")
    fine_lavoro = pd.Timestamp(f"{data.strftime('%Y-%m-%d')} {ORARI_LAVORO['fine_pomeriggio']:02d}:00")
    
    # Slot da 30 minuti
    for ora in range(ORARI_LAVORO['inizio_mattina'], ORARI_LAVORO['fine_pomeriggio']):
        for minuti in [0, 30]:
            dt_slot = pd.Timestamp(f"{data.strftime('%Y-%m-%d')} {ora:02d}:{minuti:02d}")
            dt_fine = dt_slot + timedelta(minutes=durata)
            
            # Regola 1: Nessuna sovrapposizione con la pausa pranzo
            if (dt_slot < fine_pausa) and (dt_fine > inizio_pausa):
                continue
                
            # Regola 2: Non sforare l'orario di chiusura
            if dt_fine > fine_lavoro:
                continue
            
            # Controllo sovrapposizione appuntamenti
            occupato = False
            if not df_app.empty and 'Data' in df_app.columns:
                appuntamenti_giorno = df_app[df_app['Data'].dt.date == data.date()]
                
                for _, app in appuntamenti_giorno.iterrows():
                    app_inizio = app['Data']
                    app_durata = DURATA_TRATTAMENTI.get(app['Tipo'], 30)
                    app_fine = app_inizio + timedelta(minutes=app_durata)
                    
                    # Controlla intersezione temporale
                    if (dt_slot < app_fine) and (dt_fine > app_inizio):
                        occupato = True
                        break
            
            if not occupato:
                slot_disponibili.append(dt_slot)
                
    return slot_disponibili

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

def carica_appuntamenti():
    if os.path.exists(CSV_APPUNTAMENTI):
        df = pd.read_csv(CSV_APPUNTAMENTI)
        # errors='coerce' previene eccezioni se il formato date varia leggermente
        df['Data'] = pd.to_datetime(df['Data'], errors='coerce') 
        # Scarta eventuali righe in cui la conversione ha fallito
        return df.dropna(subset=['Data'])
    else:
        df = pd.DataFrame({
            'Data': ['2026-05-01 09:00', '2026-05-05 10:30', '2026-05-10 14:00', '2026-05-15 11:00', '2026-05-20 15:30', '2026-05-25 09:30'],
            'Paziente ID': [1, 2, 1, 3, 4, 5],
            'Tipo': ['Igiene', 'Conservativa', 'Igiene', 'Ortodonzia', 'Estrazione', 'Igiene'],
            'Importo': [80, 150, 80, 200, 120, 80],
        })
        df['Data'] = pd.to_datetime(df['Data'])
        return df

def salva_pazienti(df):
    df.to_csv(CSV_PAZIENTI, index=False)

def salva_appuntamenti(df):
    df_da_salvare = df.copy()
    df_da_salvare['Data'] = pd.to_datetime(df_da_salvare['Data']).dt.strftime('%Y-%m-%d %H:%M')
    df_da_salvare.to_csv(CSV_APPUNTAMENTI, index=False)

# Caricamento Globale dei Dati
df_pazienti = carica_pazienti()
df_appuntamenti = carica_appuntamenti()

# Funzione Helper robusta per visualizzare nomi dei pazienti (evita IndexError)
def format_nome_paziente(paz_id):
    if df_pazienti.empty:
        return f"ID {paz_id}"
    match = df_pazienti[df_pazienti['ID'] == paz_id]
    if not match.empty:
        return f"{match.iloc[0]['Nome']} {match.iloc[0]['Cognome']}"
    return f"Sconosciuto (ID {paz_id})"

with st.sidebar:
    st.title("⚙️ Studio Dr. Rossi")
    st.write("Maggio 2026")
    if st.button("🔄 Ricarica"):
        st.rerun()

st.title("📊 Studio Dr. Rossi")
st.subheader("Dashboard KPI - Maggio 2026")

tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard", "👥 Pazienti", "📅 Appuntamenti", "⚙️ Gestione"])

# ===== TAB 1: DASHBOARD =====
with tab1:
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Appuntamenti maggio", len(df_appuntamenti), "+3 vs aprile")
    col2.metric("Incasso maggio", f"€{df_appuntamenti['Importo'].sum():.0f}", "+11% vs aprile")
    col3.metric("No-show questo mese", 4, "2 da contattare")
    col4.metric("Pazienti attivi", len(df_pazienti), "+2 questo mese")
    
    st.divider()
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📈 Incasso mensile 2026")
        dati_incasso = pd.DataFrame({
            'Mese': ['Gen', 'Feb', 'Mar', 'Apr', 'Mag'],
            'Incasso': [6800, 7200, 7900, 7800, 8640]
        })
        st.bar_chart(dati_incasso.set_index('Mese'), height=300)
    
    with col2:
        st.subheader("📊 Tipo di trattamento")
        dati_tipo = pd.DataFrame({
            'Tipo': ['Igiene', 'Conservativa', 'Ortodonzia', 'Estrazione'],
            'Count': [38, 29, 21, 12]
        })
        st.bar_chart(dati_tipo.set_index('Tipo'), height=300)
    
    st.divider()
    
    st.subheader("🔔 Pazienti da richiamare")
    st.write("*Ultimi appuntamenti > 3 mesi fa*")
    richiamare = pd.DataFrame({
        'Nome': ['Anna Ferretti', 'Marco Conti', 'Giulia Marini'],
        'Ultima visita': ['6 mesi fa', '4 mesi fa', '3.5 mesi fa'],
        'Telefono': ['320 123 4567', '335 987 6543', '340 555 1234'],
        'Priorità': ['⚠️ URGENTE', '⚠️ Da seguire', '⚠️ Da seguire']
    })
    st.dataframe(richiamare, use_container_width=True, hide_index=True)
    
    st.divider()
    
    st.subheader("❌ Cancellazioni e no-show")
    st.write("*Ultimi 30 giorni*")
    cancellazioni = pd.DataFrame({
        'Paziente': ['Roberto Gallo', 'Lisa Neri', 'Paolo Verdi'],
        'Data': ['2026-05-20', '2026-05-18', '2026-05-15'],
        'Tipo': ['Conservativa', 'Igiene', 'No-show'],
        'Telefono': ['333 222 1111', '345 666 7777', '328 999 0000'],
        'Note': ['Ha detto rimando', 'Non si è presentato', 'Non ha riconfermato']
    })
    st.dataframe(cancellazioni, use_container_width=True, hide_index=True)
    
    st.divider()
    
    st.subheader("📦 Forniture in esaurimento")
    st.write("*Ricordati di ordinare questi materiali*")
    forniture = pd.DataFrame({
        'Materiale': ['Dischi abrasivi 25mm', 'Detergente ultrasonico', 'Guanti nitrile taglia L', 'Mascherine FFP2', 'Frese diamantate set 5'],
        'Quantità residua': [5, 2, 1, 8, 3],
        'Livello minimo': [20, 5, 10, 20, 5],
        'Status': ['⚠️ Finire', '⚠️ Finire', '🔴 ORDINARE SUBITO', '✅ OK', '⚠️ Finire']
    })
    st.dataframe(forniture, use_container_width=True, hide_index=True)

# ===== TAB 2: PAZIENTI =====
with tab2:
    st.subheader("👥 Elenco pazienti")
    st.dataframe(df_pazienti, use_container_width=True, hide_index=True)
    
    st.divider()
    st.subheader("📋 Storico paziente")
    
    if not df_pazienti.empty:
        paziente_selezionato = st.selectbox(
            "Seleziona paziente",
            options=df_pazienti['ID'].tolist(),
            format_func=format_nome_paziente
        )
        
        storico = df_appuntamenti[df_appuntamenti['Paziente ID'] == paziente_selezionato]
        if len(storico) > 0:
            st.write(f"**Appuntamenti totali:** {len(storico)}")
            st.write(f"**Spesa totale:** €{storico['Importo'].sum():.0f}")
            df_storico_display = storico.copy()
            df_storico_display['Data'] = pd.to_datetime(df_storico_display['Data']).dt.strftime('%d/%m/%Y %H:%M')
            st.dataframe(df_storico_display[['Data', 'Tipo', 'Importo']], use_container_width=True, hide_index=True)
        else:
            st.info("Nessun appuntamento registrato")
    else:
        st.warning("Nessun paziente registrato nel database.")

# ===== TAB 3: APPUNTAMENTI =====
with tab3:
    st.subheader("📅 Elenco completo appuntamenti")
    
    if not df_appuntamenti.empty:
        df_app_completo = df_appuntamenti.merge(
            df_pazienti[['ID', 'Nome', 'Cognome']], 
            left_on='Paziente ID', 
            right_on='ID', 
            how='left'
        )
        # Gestione pazienti cancellati o non trovati
        df_app_completo['Nome'] = df_app_completo['Nome'].fillna("Sconosciuto")
        df_app_completo['Cognome'] = df_app_completo['Cognome'].fillna("")
        df_app_completo['Paziente'] = df_app_completo['Nome'] + ' ' + df_app_completo['Cognome']
        
        df_app_completo = df_app_completo.sort_values(by='Data', ascending=False)
        df_app_completo['Data Formattata'] = df_app_completo['Data'].dt.strftime('%d/%m/%Y %H:%M')
        
        df_visualizza = df_app_completo[['Data Formattata', 'Paziente', 'Tipo', 'Importo']].rename(
            columns={'Data Formattata': 'Data e Ora'}
        )
        st.dataframe(df_visualizza, use_container_width=True, hide_index=True)
    else:
        st.info("Nessun appuntamento in archivio.")

# ===== TAB 4: GESTIONE =====
with tab4:
    subtab1, subtab2 = st.tabs(["Registra paziente", "Registra appuntamento"])

    with subtab1:
        st.subheader("➕ Registra nuovo paziente")
        with st.form("form_paziente"):
            col1, col2 = st.columns(2)
            nome = col1.text_input("Nome")
            cognome = col2.text_input("Cognome")
            
            col1, col2 = st.columns(2)
            telefono = col1.text_input("Telefono")
            data_nascita = col2.date_input("Data di nascita", min_value=datetime(1900, 1, 1))
            
            submitted = st.form_submit_button("Registra paziente")
            
            if submitted and nome and cognome:
                nuovo_id = int(df_pazienti['ID'].max() + 1) if not df_pazienti.empty else 1
                
                nuovo = pd.DataFrame({
                    'ID': [nuovo_id],
                    'Nome': [nome.strip()],
                    'Cognome': [cognome.strip()],
                    'Telefono': [telefono.strip()],
                    'Data nascita': [data_nascita.strftime('%Y-%m-%d')]
                })
                
                df_pazienti = pd.concat([df_pazienti, nuovo], ignore_index=True)
                salva_pazienti(df_pazienti)
                st.success(f"✅ Paziente registrato: {nome} {cognome}")
                st.rerun()
            elif submitted:
                st.error("⚠️ Inserisci nome e cognome")

    with subtab2:
        st.subheader("➕ Registra nuovo appuntamento")
        
        if not df_pazienti.empty:
            col1, col2 = st.columns(2)
            paziente_id = col1.selectbox(
                "Paziente",
                options=df_pazienti['ID'].tolist(),
                format_func=format_nome_paziente
            )
            
            tipo = col2.selectbox("Tipo di trattamento", ['Igiene', 'Conservativa', 'Ortodonzia', 'Estrazione', 'Altro'])
            data_selezionata = st.date_input("Seleziona data", value=datetime.now() + timedelta(days=1))
            
            slot_disponibili = calcola_slot_disponibili(pd.Timestamp(data_selezionata), tipo, df_appuntamenti)
            
            if slot_disponibili:
                slot_labels = [s.strftime('%H:%M') for s in slot_disponibili]
                slot_selezionato = st.selectbox("Seleziona orario disponibile", range(len(slot_disponibili)), format_func=lambda i: slot_labels[i])
                
                importo = st.number_input("Importo (€)", min_value=0, value=100)
                
                if st.button("Registra appuntamento"):
                    dt_completo = slot_disponibili[slot_selezionato]
                    nuovo = pd.DataFrame({
                        'Data': [dt_completo],
                        'Paziente ID': [paziente_id],
                        'Tipo': [tipo],
                        'Importo': [importo]
                    })
                    df_appuntamenti = pd.concat([df_appuntamenti, nuovo], ignore_index=True)
                    salva_appuntamenti(df_appuntamenti)
                    st.success(f"✅ Appuntamento registrato: {dt_completo.strftime('%d/%m/%Y %H:%M')}")
                    st.rerun()
            else:
                st.warning("❌ Nessuno slot disponibile per questo trattamento nella data selezionata.")
        else:
            st.error("Devi prima registrare un paziente.")

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
