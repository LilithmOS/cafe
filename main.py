import streamlit as st
from authlib.integrations.requests_client import OAuth2Session
from urllib.parse import urlencode, parse_qs
import os
st.set_page_config(layout="wide")

# Your Google Client ID and Secret
GOOGLE_CLIENT_ID = "1069951594102-320ob1rirp8k3ovnaj4icenggbf44k8s.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET = "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"
REDIRECT_URI = "http://localhost:8501"

# OAuth endpoints
AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN_URL = "https://oauth2.googleapis.com/token"
USERINFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"

# Step 1: Create Auth URL
params = {
    "client_id": GOOGLE_CLIENT_ID,
    "response_type": "code",
    "redirect_uri": REDIRECT_URI,
    "scope": "openid email profile",
    "access_type": "offline",
    "prompt": "consent"
}

auth_url = f"{AUTH_URL}?{urlencode(params)}"

# Handle redirect back from Google
query_params = st.query_params
if "code" in query_params:
    code = query_params["code"]
    
    client = OAuth2Session(
    GOOGLE_CLIENT_ID,
    GOOGLE_CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    client_auth_method='client_secret_post'  # <- This forces client_secret in POST body only
)
    print(f"Recieved auth code: {code}")
    try:
        token = client.fetch_token(
            TOKEN_URL,
            code=code,
            redirect_uri=REDIRECT_URI,
        )
    except Exception as e:
        st.error(f"Error fetching token: {e}")
        st.stop()  
    resp = client.get(USERINFO_URL)
    user_info = resp.json()
    st.session_state['user'] = user_info
    st.success(f"✅ Logged in as {user_info['email']}")
else:
    if "user" not in st.session_state:
        st.markdown(f"[🔐 Sign in with Google]({auth_url})")
        st.stop()
    else:
        st.sidebar.write(f"👤 {st.session_state['user']['name']}")
        if st.sidebar.button("Logout"):
            st.session_state.clear()
            st.rerun()

# Your menu display
st.title("🍽️ Weekly Menu")
menu = {
    "Monday": "Grilled Chicken with Vegetables",
    "Tuesday": "Pasta Primavera",
    "Wednesday": "Taco Bowl",
    "Thursday": "Beef Stir Fry",
    "Friday": "Margherita Pizza",
    "Saturday": "Fish and Chips",
    "Sunday": "Roast Turkey with Mashed Potatoes"
}

for day, meal in menu.items():
    st.write(f"**{day}**: {meal}")




st.session_state['menu_items'] = {"turkey_blt" : {"name" : "Turkey BLT",
                                                  "serving_size" : "1 sandwich",
                                                  "total_fat" : 20,
                                                  "saturated_fat" : 20,
                                                  "calories" : 3000,
                                                  "station" : "deli"},
                                  "cheese_pizza" : {"name" : "Cheese Pizza",
                                                    "calories" : 3000,
                                                    "station" : "pizza"},
                                  "sausage_pizza" : {"name" : "Sausage Pizza",
                                                    "calories" : 3000,
                                                     "station" : "pizza"},
                                  "cheeseburger" : {"name" : "Cheeseburger",
                                                    "calories" : 3000,
                                                    "station" : "grill"},
                                }
if 'menu_item' not in st.session_state:
    st.session_state['menu_item'] = ""
# allows menu item to actually be a button
st.markdown(
    """
    <style>
    button {
        background: none!important;
        border: none;
        padding: 0!important;
        text-decoration: none;
        cursor: pointer;
        border: none !important;
    }
    button:hover {
        text-decoration: none;
        color: orange !important;
    }
    button:focus {
        outline: none !important;
        box-shadow: none !important;
        color: orange !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title('Menu (Mock)')
st.write("---")

week1 = "This week" #week of 9/2
week2 = "Week of 9/9"
week3 = "Week of 9/16"

week = st.selectbox(
    "Select Week",
    (week1, week2, week3)
)

if week == week1:
    with st.container(border=True):
        st.write("Allergen Guide: put info here for vegan / gf etc")

    col1, col2 = st.columns(spec=[0.4, 0.6])

    # menu that doesn't change
    with col1:
        with st.container(border=True):
            st.subheader(":orange[Deli Station]")
            for key, item in st.session_state.menu_items.items():
                if item['station'] == "deli":
                    if st.button(item['name']):
                        st.session_state['menu_item'] = key
                        st.switch_page("pages/nutrition.py")

            # for item in station_map['deli']:
            #     if st.button(item['name']):
            #         st.session_state['menu_item'] = key
            #         st.switch_page("pages/nutrition.py")

        with st.container(border=True):
            st.subheader(":orange[Pizza Station]")
            for key, item in st.session_state.menu_items.items():
                if item['station'] == "pizza":
                    if st.button(item['name']):
                        st.session_state['menu_item'] = key
                        st.switch_page("pages/nutrition.py")
        with st.container(border=True):
            st.subheader(":orange[Grill Station]")
            for key, item in st.session_state.menu_items.items():
                if item['station'] == "grill":
                    if st.button(item['name']):
                        st.session_state['menu_item'] = key
                        st.switch_page("pages/nutrition.py")
    # weekly menu
    with col2:

        #day and menu
        st.subheader(":orange[Monday]")
        st.write("""
        **Sauté Station**
        <br>
        Teriyaki Chicken Stir Fry (S) or Fried Tofu (S)
        <br>
        Peas, Cabbage & Peppers
        <br>
        Steamed Jasmine Rice
        """, unsafe_allow_html=True)

        innercol1, innercol2 = st.columns(2)
        with innercol1:
            st.write("""
            **Vegetable**
            <br>
            **Sandwich**
            <br>
            **Salad Bar**
            <br>
            **Breakfast**
            """, unsafe_allow_html=True)
        with innercol2:
            st.write("""
            Greek Green Beans
            <br>
            Italian Beef with Peppers & Onions (G, W)
            <br>
            Rotating selection of Greens, Veggies, Proteins & Toppings
            <br>
            Eggs or Eggs & Chorizo (E), Jalapeno Breakfast Potatoes & Tortillas
            """, unsafe_allow_html=True)
        st.write("---")

        # tuesday
        st.subheader(":orange[Tuesday]")
        st.write("""
        **Sauté Station**
        <br>
        Teriyaki Chicken Stir Fry (S) or Fried Tofu (S)
        <br> 
        Peas, Cabbage & Peppers
        <br> 
        Steamed Jasmine Rice
        """, unsafe_allow_html=True)

        innercol1, innercol2 = st.columns(2)
        with innercol1:
            st.write("""
            **Vegetable**
            <br>
            **Sandwich**
            <br>
            **Salad Bar**
            <br>
            **Breakfast**
            """, unsafe_allow_html=True)
        with innercol2:
            st.write("""
            Greek Green Beans
            <br>
            Italian Beef with Peppers & Onions (G, W)
            <br>
            Rotating selection of Greens, Veggies, Proteins & Toppings
            <br>
            Eggs or Eggs & Chorizo (E), Jalapeno Breakfast Potatoes & Tortillas
            """, unsafe_allow_html=True)
        st.write("---")

        # wednesday
        st.subheader(":orange[Wednesday]")
        st.write("""
        **Sauté Station**
        <br>
        Teriyaki Chicken Stir Fry (S) or Fried Tofu (S)
        <br> 
        Peas, Cabbage & Peppers
        <br> 
        Steamed Jasmine Rice
        """, unsafe_allow_html=True)

        innercol1, innercol2 = st.columns(2)
        with innercol1:
            st.write("""
            **Vegetable**
            <br>
            **Sandwich**
            <br>
            **Salad Bar**
            <br>
            **Breakfast**
            """, unsafe_allow_html=True)
        with innercol2:
            st.write("""
            Greek Green Beans
            <br>
            Italian Beef with Peppers & Onions (G, W)
            <br>
            Rotating selection of Greens, Veggies, Proteins & Toppings
            <br>
            Eggs or Eggs & Chorizo (E), Jalapeno Breakfast Potatoes & Tortillas
            """, unsafe_allow_html=True)
        st.write("---")

        # thursday
        st.subheader(":orange[Thursday]")
        st.write("""
        **Sauté Station**
        <br>
        Teriyaki Chicken Stir Fry (S) or Fried Tofu (S)
        <br> 
        Peas, Cabbage & Peppers
        <br> 
        Steamed Jasmine Rice
        """, unsafe_allow_html=True)

        innercol1, innercol2 = st.columns(2)
        with innercol1:
            st.write("""
            **Vegetable**
            <br>
            **Sandwich**
            <br>
            **Salad Bar**
            <br>
            **Breakfast**
            """, unsafe_allow_html=True)
        with innercol2:
            st.write("""
            Greek Green Beans
            <br>
            Italian Beef with Peppers & Onions (G, W)
            <br>
            Rotating selection of Greens, Veggies, Proteins & Toppings
            <br>
            Eggs or Eggs & Chorizo (E), Jalapeno Breakfast Potatoes & Tortillas
            """, unsafe_allow_html=True)
        st.write("---")

        # friday
        st.subheader(":orange[Friday]")
        st.write("""
        **Sauté Station**
        <br>
        Teriyaki Chicken Stir Fry (S) or Fried Tofu (S)
        <br> 
        Peas, Cabbage & Peppers
        <br> 
        Steamed Jasmine Rice
        """, unsafe_allow_html=True)

        innercol1, innercol2 = st.columns(2)
        with innercol1:
            st.write("""
            **Vegetable**
            <br>
            **Sandwich**
            <br>
            **Salad Bar**
            <br>
            **Breakfast**
            """, unsafe_allow_html=True)
        with innercol2:
            st.write("""
            Greek Green Beans
            <br>
            Italian Beef with Peppers & Onions (G, W)
            <br>
            Rotating selection of Greens, Veggies, Proteins & Toppings
            <br>
            Eggs or Eggs & Chorizo (E), Jalapeno Breakfast Potatoes & Tortillas
            """, unsafe_allow_html=True)
        st.write("---")


elif week == week2:
    st.header("Coming soon!")

elif week == week3:
    st.header("Coming soon!")

def main():
    global_state = gsl.get_global_state()