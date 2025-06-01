
import streamlit as st
import random

st.title("🎲 ¡Adivina el número secreto!")
st.write("Estoy pensando en un número entre 1 y 100. ¿Puedes adivinarlo?")

if "secreto" not in st.session_state:
    st.session_state.secreto = random.randint(1, 100)
    st.session_state.intentos = 0
    st.session_state.terminado = False

if not st.session_state.terminado:
    numero = st.number_input("Ingresa tu número:", min_value=1, max_value=100, step=1)
    if st.button("Adivinar"):
        st.session_state.intentos += 1
        if numero < st.session_state.secreto:
            st.warning("🔻 Muy bajo")
        elif numero > st.session_state.secreto:
            st.warning("🔺 Muy alto")
        else:
            if st.session_state.intentos == 1:
                st.success("🎉 ¡Increíble! Lo adivinaste al primer intento.")
            else:
                st.success(f"✅ ¡Correcto! Adivinaste el número en {st.session_state.intentos} intentos.")
            st.session_state.terminado = True

        if st.session_state.intentos >= 10 and numero != st.session_state.secreto:
            st.error(f"❌ Lo siento, has superado los 10 intentos. El número era {st.session_state.secreto}.")
            st.session_state.terminado = True
else:
    if st.button("🔁 Jugar otra vez"):
        st.session_state.secreto = random.randint(1, 100)
        st.session_state.intentos = 0
        st.session_state.terminado = False
