import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="Studio Dentistico", layout="wide")
st.title("📊 Studio Dr. Rossi")
st.subheader("Dashboard KPI - Maggio 2026")

# KPI principali
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Appuntamenti questa settimana", 24, "+3")

with col2:
    st.metric("Incasso maggio", "8.640€", "+11%")

with col3:
    st.metric("No-show questo mese", 4, "2 da contattare")

with col4:
    st.metric("Pazienti attivi", 312, "+8 questo mese")

st.divider()

# Grafici
col1, col2 = st.columns(2)

with col1:
    st.subheader("Incasso mensile 2026")
    dati_incasso = pd.DataFrame({
        'Mese': ['Gen', 'Feb', 'Mar', 'Apr', 'Mag'],
        'Incasso': [6800, 7200, 7900, 7800, 8640]
    })
    st.bar_chart(dati_incasso.set_index('Mese'))

with col2:
    st.subheader("Tipo di trattamento")
    dati_trattamenti = pd.DataFrame({
        'Tipo': ['Igiene', 'Conservativa', 'Ortodonzia', 'Altro'],
        'Percentuale': [38, 29, 21, 12]
    })
    st.bar_chart(dati_trattamenti.set_index('Tipo'))

st.divider()

# Pazienti da richiamare
st.subheader("🔔 Pazienti da richiamare")
pazienti = pd.DataFrame({
    'Nome': ['Anna Ferretti', 'Marco Conti', 'Giulia Marini'],
    'Ultima visita': ['6 mesi fa', 'Controllo non prenotato', 'Piano ortodontico in sospeso'],
    'Priorità': ['⚠️ Urgente', '⚠️ Da seguire', '⚠️ Da seguire']
})
st.dataframe(pazienti, use_container_width=True, hide_index=True)
