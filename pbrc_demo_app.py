
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="PBRC Weight Loss Predictor", layout="centered")

st.title("Simulatore di Perdita di Peso - Modello PBRC (Demo)")

# Input utente
sesso = st.selectbox("Sesso", ["maschio", "femmina"])
eta = st.number_input("Età (anni)", min_value=10, max_value=100, value=35)
altezza = st.number_input("Altezza (cm)", min_value=100, max_value=250, value=175)
peso_iniziale = st.number_input("Peso iniziale (kg)", min_value=30.0, max_value=200.0, value=90.0)
kcal_giornaliere = st.number_input("Apporto calorico (kcal/die)", min_value=800, max_value=5000, value=1800)
pal = st.slider("Livello attività fisica (PAL)", 1.2, 2.5, 1.5)
peso_obiettivo = st.number_input("Peso obiettivo (kg)", min_value=30.0, max_value=200.0, value=75.0)
durata_settimane = st.slider("Durata simulazione (settimane)", 4, 156, 52)

# Calcolo BMR
if sesso == "maschio":
    bmr = 10 * peso_iniziale + 6.25 * altezza - 5 * eta + 5
else:
    bmr = 10 * peso_iniziale + 6.25 * altezza - 5 * eta - 161

# TDEE iniziale
tdee = bmr * pal

# Simulazione dinamica con adattamento
peso = peso_iniziale
pesi = [peso]
settimane = [0]

for week in range(1, durata_settimane + 1):
    deficit_giornaliero = tdee - kcal_giornaliere
    deficit_settimanale = deficit_giornaliero * 7
    perdita = deficit_settimanale / 7700
    peso -= perdita
    peso = max(peso, peso_obiettivo)

    # Adattamento metabolico (semplificato): -0.5% TDEE ogni 1.5 kg persi
    perdita_totale = peso_iniziale - peso
    tdee = bmr * pal * (1 - 0.005 * (perdita_totale / 1.5))

    pesi.append(peso)
    settimane.append(week)

# Grafico
fig, ax = plt.subplots()
ax.plot(settimane, pesi, label="Peso stimato")
ax.set_xlabel("Settimana")
ax.set_ylabel("Peso (kg)")
ax.set_title("Andamento della perdita di peso (modello PBRC semplificato)")
ax.grid(True)
st.pyplot(fig)

st.markdown("**Nota:** questa è una demo semplificata del modello PBRC per test preliminari. La versione finale includerà partizione massa grassa/magra e simulazione composizionale.")
