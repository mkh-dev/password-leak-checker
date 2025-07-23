import streamlit as st
import re
from password_checker import pwned_api_check

# -------------------- CONFIGURATION DE LA PAGE --------------------
st.set_page_config(page_title="🔐 Vérificateur de mot de passe piraté", page_icon="🛡️")

# -------------------- LANGUE --------------------
lang = st.radio(
    label="🌐 Langue / Language",
    options=["Français", "English"],
    horizontal=True
)

# -------------------- TEXTES MULTILINGUES --------------------
texts = {
    "Français": {
        "title": "🔐 Ton mot de passe est-il piraté ?",
        "prompt": "Tape un mot de passe pour savoir s'il a été exposé dans des fuites de données.",
        "input_label": "Mot de passe",
        "found_msg": "🚨 Ce mot de passe a été trouvé **{} fois** dans des bases de données piratées. Change-le !",
        "not_found_msg": "✅ Ce mot de passe **n'a pas été trouvé** dans les fuites connues. Il semble sûr.",
        "strength_labels": ["Très faible", "Faible", "Moyen", "Fort", "Excellent"],
        "sidebar_title": "🛡️ Vérification sécurisée",
        "sidebar_text_1": "🔍 Ce site utilise l'API HaveIBeenPwned pour vérifier si ton mot de passe a fuité.",
        "sidebar_text_2": "🧠 Tu peux aussi voir la robustesse de ton mot de passe.",
        "footer": "🔗 Voir le projet sur GitHub : [mkh-dev](https://github.com/mkh-dev)"
    },
    "English": {
        "title": "🔐 Is your password leaked?",
        "prompt": "Type a password to check if it has been exposed in data breaches.",
        "input_label": "Password",
        "found_msg": "🚨 This password has been found **{} times** in breached databases. Change it!",
        "not_found_msg": "✅ This password was **not found** in known breaches. It seems safe.",
        "strength_labels": ["Very weak", "Weak", "Medium", "Strong", "Excellent"],
        "sidebar_title": "🛡️ Secure Check",
        "sidebar_text_1": "🔍 This site uses the HaveIBeenPwned API to check if your password has leaked.",
        "sidebar_text_2": "🧠 You can also check your password strength.",
        "footer": "🔗 View the project on GitHub: [mkh-dev](https://github.com/mkh-dev)"
    }
}

t = texts[lang]

# -------------------- BARRE LATERALE --------------------
with st.sidebar:
    st.markdown(f"## {t['sidebar_title']}")
    st.info(t['sidebar_text_1'])
    st.success(t['sidebar_text_2'])

# -------------------- TITRE + SAISIE --------------------
st.title(t["title"])
st.write(t["prompt"])
password = st.text_input(t["input_label"], type="password")

# -------------------- ANALYSE ROBUSTESSE --------------------
def password_strength(password):
    score = 0
    if len(password) >= 8:
        score += 1
    if re.search(r"[A-Z]", password):
        score += 1
    if re.search(r"[a-z]", password):
        score += 1
    if re.search(r"[0-9]", password):
        score += 1
    if re.search(r"[^a-zA-Z0-9]", password):
        score += 1
    return score

def strength_color(score):
    if score <= 1:
        return "🔴"
    elif score == 2:
        return "🟠"
    elif score == 3:
        return "🟡"
    elif score == 4:
        return "🟢"
    else:
        return "💚"

if password:
    score = password_strength(password)
    label = t["strength_labels"][score - 1 if score > 0 else 0]
    emoji = strength_color(score)

    st.markdown(f"### {emoji} **{label}** ({score}/5)")
    st.progress(score / 5)

    count = pwned_api_check(password)
    if count:
        st.error(t["found_msg"].format(count))
    else:
        st.success(t["not_found_msg"])

# -------------------- PIED DE PAGE --------------------
st.markdown("---")
st.markdown(t["footer"])
