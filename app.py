import streamlit as st
from password_checker import pwned_api_check

st.set_page_config(page_title="🔐 Vérificateur de mot de passe piraté", page_icon="🛡️")

# Sélecteur de langue avec emoji drapeaux à droite
lang = st.radio(
    label="🌐 Langue / Language",
    options=["Français", "English"],
    horizontal=True
)

# Texte selon langue
if lang == "Français":
    title = "🔐 Ton mot de passe est-il piraté ?"
    prompt = "Tape un mot de passe pour savoir s'il a été exposé dans des fuites de données."
    input_label = "Mot de passe"
    found_msg = "🚨 Ce mot de passe a été trouvé **{} fois** dans des bases de données piratées. Change-le !"
    not_found_msg = "✅ Ce mot de passe **n'a pas été trouvé** dans les fuites connues. Il semble sûr."
else:
    title = "🔐 Is your password leaked?"
    prompt = "Type a password to check if it has been exposed in data breaches."
    input_label = "Password"
    found_msg = "🚨 This password has been found **{} times** in breached databases. Change it!"
    not_found_msg = "✅ This password was **not found** in known breaches. It seems safe."

st.title(title)
st.write(prompt)

password = st.text_input(input_label, type="password")

if password:
    count = pwned_api_check(password)
    if count:
        st.error(found_msg.format(count))
    else:
        st.success(not_found_msg)
