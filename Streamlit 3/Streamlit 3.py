import streamlit as st
import pandas as pd
from streamlit_authenticator import Authenticate
from streamlit_option_menu import option_menu

# Charger les données des utilisateurs depuis le CSV
df = pd.read_csv('users.csv')

# Préparer les données pour Streamlit Authenticator
users_data = {
    'usernames': {row['name']: {
        'name': row['name'],
        'password': row['password'],
        'email': row['email'],
        'failed_login_attempts': row['failed_login_attempts'],
        'logged_in': row['logged_in'],
        'role': row['role']
    } for _, row in df.iterrows()}
}

# Initialiser Streamlit Authenticator
authenticator = Authenticate(
    users_data, 
    "cookie_name", 
    "cookie_key", 
    30
)

# Authentification
auth_status = authenticator.login("Login", "main")

# Page d'accueil après connexion
def accueil():
    st.title("Bienvenue sur le contenu réservé aux utilisateurs connectés")
    st.write(f"Bienvenue {st.session_state['name']} !")

# Page d'album photo
def photo_album():
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Un chat")
        st.image("https://static.streamlit.io/examples/cat.jpg")
    with col2:
        st.header("Un chien")
        st.image("https://static.streamlit.io/examples/dog.jpg")
    with col3:
        st.header("Un hibou")
        st.image("https://static.streamlit.io/examples/owl.jpg")

# Menu de navigation
def menu():
    selection = option_menu(
        menu_title=None,
        options=["Accueil", "Album Photo"]
    )
    return selection

# Si l'utilisateur est connecté
if auth_status:
    # Menu dans la sidebar
    with st.sidebar:
        authenticator.logout("Logout")
        st.sidebar.write(f"Bienvenue {st.session_state['name']}")
    
    # Navigation
    page = menu()
    if page == "Accueil":
        accueil()
    elif page == "Album Photo":
        photo_album()

# Si l'utilisateur n'est pas authentifié
elif auth_status is False:
    st.error("Nom d'utilisateur ou mot de passe incorrect")

# Si les champs sont vides
else:
    st.warning("Les champs nom d'utilisateur et mot de passe doivent être remplis")
