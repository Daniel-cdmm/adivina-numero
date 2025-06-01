import streamlit as st
import random
import pandas as pd
import os

# Título principal
st.title("🎯 ¡Adivina el Número Secreto!")

# Inicializar sesión de estado
if "nombre" not in st.session_state:
    st.session_state.nombre = ""
if "juego_iniciado" not in st.session_state:
    st.session_state.juego_iniciado = False
if "numero_secreto" not in st.session_state:
    st.session_state.numero_secreto = random.randint(1, 100)
if "intentos" not in st.session_state:
    st.session_state.intentos = 0
if "mensaje" not in st.session_state:
    st.session_state.mensaje = ""
if "ganador" not in st.session_state:
    st.session_state.ganador = False

# Registro del nombre
if not st.session_state.juego_iniciado:
    st.subheader("📝 Ingresa tu nombre para comenzar:")
    nombre_input = st.text_input("Nombre del jugador", value=st.session_state.nombre)

    if st.button("🎮 Jugar"):
        if nombre_input.strip() != "":
            st.session_state.nombre = nombre_input
            st.session_state.juego_iniciado = True
            st.session_state.numero_secreto = random.randint(1, 100)
            st.session_state.intentos = 0
            st.session_state.mensaje = ""
            st.session_state.ganador = False
        else:
            st.warning("⚠️ Por favor, ingresa tu nombre antes de jugar.")

# Juego
if st.session_state.juego_iniciado and not st.session_state.ganador:
    st.write(f"👤 Jugador: {st.session_state.nombre}")
    st.write(f"🔢 Intento #{st.session_state.intentos + 1} / 10")

    numero = st.number_input("Adivina el número secreto (1 a 100)", min_value=1, max_value=100, step=1)

    if st.button("🚀 Intentar"):
        st.session_state.intentos += 1
        if numero < st.session_state.numero_secreto:
            st.session_state.mensaje = "🔽 Muy bajo."
        elif numero > st.session_state.numero_secreto:
            st.session_state.mensaje = "🔼 Muy alto."
        else:
            st.session_state.ganador = True
            if st.session_state.intentos == 1:
                st.success("🎉 ¡Increíble! Adivinaste en el primer intento.")
            else:
                st.success(f"✅ ¡Correcto! Adivinaste en {st.session_state.intentos} intentos.")
            # Guardar en el ranking
            nuevo_registro = pd.DataFrame({
                "Jugador": [st.session_state.nombre],
                "Intentos": [st.session_state.intentos]
            })
            if os.path.exists("ranking.csv"):
                ranking = pd.read_csv("ranking.csv")
                ranking = pd.concat([ranking, nuevo_registro], ignore_index=True)
            else:
                ranking = nuevo_registro
            ranking.sort_values(by="Intentos", inplace=True)
            ranking.to_csv("ranking.csv", index=False)

    if st.session_state.intentos >= 10 and not st.session_state.ganador:
        st.error("❌ Has alcanzado el máximo de 10 intentos. El número era: " + str(st.session_state.numero_secreto))
        st.session_state.ganador = True

    st.write(st.session_state.mensaje)

# Ranking
if st.session_state.ganador:
    st.subheader("🏆 Ranking de Ganadores (Menos intentos primero)")
    if os.path.exists("ranking.csv"):
        ranking = pd.read_csv("ranking.csv")
        st.dataframe(ranking.head(10))  # Mostrar solo top 10

    if st.button("🔁 Jugar otra vez"):
        st.session_state.juego_iniciado = False
        st.session_state.numero_secreto = random.randint(1, 100)
        st.session_state.intentos = 0
        st.session_state.mensaje = ""
        st.session_state.ganador = False

    if st.button("🧹 Reiniciar todo"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.experimental_rerun()
