import streamlit as st
import random
import pandas as pd
import os
import time

st.title("🎯 ¡Adivina el Número Secreto!")

# Estado inicial
if "juego_iniciado" not in st.session_state:
    st.session_state.juego_iniciado = False
    st.session_state.nombre = ""
    st.session_state.numero_secreto = random.randint(1, 100)
    st.session_state.intentos = 0
    st.session_state.mensaje = ""
    st.session_state.ganador = False
    st.session_state.inicio_tiempo = 0
    st.session_state.tiempo_total = 0
    st.session_state.entrada_numero = ""

# Pantalla de inicio
if not st.session_state.juego_iniciado:
    st.subheader("📝 Ingresa tu nombre para comenzar:")
    nombre = st.text_input("Nombre del jugador")
    if st.button("🎮 Jugar"):
        if nombre.strip() != "":
            st.session_state.nombre = nombre.strip()
            st.session_state.juego_iniciado = True
            st.session_state.numero_secreto = random.randint(1, 100)
            st.session_state.intentos = 0
            st.session_state.mensaje = ""
            st.session_state.ganador = False
            st.session_state.inicio_tiempo = time.time()
            st.session_state.entrada_numero = ""
        else:
            st.warning("⚠️ Por favor, ingresa tu nombre.")

# Juego en curso
if st.session_state.juego_iniciado and not st.session_state.ganador:
    st.write(f"👤 Jugador: {st.session_state.nombre}")
    st.write(f"🔢 Intento #{st.session_state.intentos + 1} / 10")

    with st.form("formulario"):
        entrada = st.text_input("Adivina el número secreto (1 a 100)", max_chars=3, key="entrada_numero")
        enviar = st.form_submit_button("🚀 Intentar")

    if enviar:
        st.markdown("""
            <audio autoplay>
                <source src="https://www.soundjay.com/button/beep-01a.mp3" type="audio/mpeg">
            </audio>
        """, unsafe_allow_html=True)

        entrada = st.session_state.entrada_numero
        if entrada.isdigit():
            numero = int(entrada)
            if 1 <= numero <= 100:
                st.session_state.intentos += 1
                if numero < st.session_state.numero_secreto:
                    st.session_state.mensaje = "🔽 Muy bajo."
                    st.session_state.entrada_numero = ""
                    st.rerun()
                elif numero > st.session_state.numero_secreto:
                    st.session_state.mensaje = "🔼 Muy alto."
                    st.session_state.entrada_numero = ""
                    st.rerun()
                else:
                    st.session_state.ganador = True
                    st.session_state.tiempo_total = round(time.time() - st.session_state.inicio_tiempo, 2)
                    st.success(f"✅ ¡Correcto! Adivinaste en {st.session_state.intentos} intentos.")
                    st.success(f"⏱️ Tiempo total: {st.session_state.tiempo_total} segundos.")
                    st.balloons()
                    st.markdown("""
                        <audio autoplay>
                            <source src="https://www.soundjay.com/human/sounds/applause-8.mp3" type="audio/mpeg">
                        </audio>
                    """, unsafe_allow_html=True)

                    nuevo_registro = pd.DataFrame({
                        "Jugador": [st.session_state.nombre],
                        "Intentos": [st.session_state.intentos],
                        "Tiempo (segundos)": [st.session_state.tiempo_total]
                    })

                    if os.path.exists("ranking.csv"):
                        ranking = pd.read_csv("ranking.csv")
                        ranking = pd.concat([ranking, nuevo_registro], ignore_index=True)
                    else:
                        ranking = nuevo_registro
                    ranking.sort_values(by=["Intentos", "Tiempo (segundos)"], inplace=True)
                    ranking.to_csv("ranking.csv", index=False)
            else:
                st.warning("⚠️ El número debe estar entre 1 y 100.")
        else:
            st.warning("⚠️ Ingresa solo números válidos.")

    if st.session_state.intentos >= 10 and not st.session_state.ganador:
        st.error(f"❌ Has alcanzado el máximo de 10 intentos. El número era {st.session_state.numero_secreto}")
        st.session_state.ganador = True
        st.markdown("""
            <audio autoplay>
                <source src="https://www.soundjay.com/button/beep-07.wav" type="audio/wav">
            </audio>
        """, unsafe_allow_html=True)

    st.write(st.session_state.mensaje)

# Mostrar ranking
if st.session_state.ganador:
    st.subheader("🏆 Ranking de Ganadores (Menos intentos primero)")
    if os.path.exists("ranking.csv"):
        ranking = pd.read_csv("ranking.csv")
        st.dataframe(ranking.head(10))

    if st.button("🔁 Jugar otra vez"):
        st.session_state.juego_iniciado = False
        st.session_state.entrada_numero = ""
        st.rerun()
