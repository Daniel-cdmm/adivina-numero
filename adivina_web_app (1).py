import streamlit as st
import random
import pandas as pd
import os
import re

st.title("🎯 ¡Adivina el Número Secreto!")

# Estado inicial
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
if "entrada_numero" not in st.session_state:
    st.session_state.entrada_numero = ""

# Pantalla de inicio
if not st.session_state.juego_iniciado:
    st.subheader("🎮 Ingresa tu nombre para comenzar:")
    nombre_input = st.text_input("Nombre del jugador", value=st.session_state.nombre)

    if st.button("✅ Jugar"):
        if nombre_input.strip() != "":
            if re.match("^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$", nombre_input):
                st.session_state.nombre = nombre_input
                st.session_state.juego_iniciado = True
                st.session_state.numero_secreto = random.randint(1, 100)
                st.session_state.intentos = 0
                st.session_state.mensaje = ""
                st.session_state.ganador = False
                st.session_state.entrada_numero = ""
            else:
                st.warning("⚠️ El nombre solo debe contener letras.")
        else:
            st.warning("⚠️ Por favor, ingresa tu nombre antes de jugar.")

# Juego en curso
if st.session_state.juego_iniciado and not st.session_state.ganador:
    st.write(f"👤 Jugador: {st.session_state.nombre}")
    st.write(f"🔢 Intento #{st.session_state.intentos + 1} / 10")

    with st.form("formulario_juego"):
        entrada = st.text_input(
            "Adivina el número secreto (1 a 100)",
            value=st.session_state.entrada_numero,
            max_chars=3
        )
        enviar = st.form_submit_button("🚀 Intentar")

    if enviar:
        if entrada.isdigit():
            numero = int(entrada)
            if 1 <= numero <= 100:
                st.session_state.intentos += 1
                if numero < st.session_state.numero_secreto:
                    st.session_state.mensaje = "🔽 Muy bajo."
                    st.session_state.entrada_numero = ""
                elif numero > st.session_state.numero_secreto:
                    st.session_state.mensaje = "🔼 Muy alto."
                    st.session_state.entrada_numero = ""
                else:
                    st.session_state.ganador = True
                    st.session_state.entrada_numero = ""
                    if st.session_state.intentos == 1:
                        st.balloons()
                        st.success("🎉 ¡Increíble! Adivinaste el número en el primer intento.")
                    else:
                        st.success(f"✅ ¡Correcto! Adivinaste en {st.session_state.intentos} intentos.")

                    # SONIDO de éxito
                    st.markdown(
                        """
                        <audio autoplay>
                            <source src="https://www.soundjay.com/human/sounds/applause-8.mp3" type="audio/mpeg">
                        </audio>
                        """,
                        unsafe_allow_html=True
                    )

                    # Guardar resultado
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
            else:
                st.warning("⚠️ El número debe estar entre 1 y 100.")
        else:
            st.warning("⚠️ Solo se permiten números.")

    if st.session_state.intentos >= 10 and not st.session_state.ganador:
        st.error("❌ Has alcanzado el máximo de 10 intentos. El número era: " + str(st.session_state.numero_secreto))
        st.session_state.ganador = True

        # SONIDO de fallo
        st.markdown(
            """
            <audio autoplay>
                <source src="https://www.soundjay.com/button/beep-07.wav" type="audio/wav">
            </audio>
            """,
            unsafe_allow_html=True
        )

    st.write(st.session_state.mensaje)

# Mostrar ranking y botón para volver a jugar
if st.session_state.ganador:
    st.subheader("🏆 Ranking de Ganadores (Menos intentos primero)")
    if os.path.exists("ranking.csv"):
        ranking = pd.read_csv("ranking.csv")
        st.dataframe(ranking.head(10))

    if st.button("🔁 Jugar otra vez"):
        st.session_state.juego_iniciado = False
        st.session_state.numero_secreto = random.randint(1, 100)
        st.session_state.intentos = 0
        st.session_state.mensaje = ""
        st.session_state.ganador = False
        st.session_state.entrada_numero = ""
