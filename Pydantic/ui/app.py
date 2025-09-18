import streamlit as st
import requests
import json
import pandas as pd

# FastAPI backend URL
API_URL = "http://localhost:8000"

st.set_page_config(
    page_title="User Registration",
    page_icon="👤",
    layout="wide"
)

st.title("👤 User Registration System")
st.markdown("---")

# Create two columns
col1, col2 = st.columns([1, 1])

with col1:
    st.header("📝 Register New User")
    
    with st.form("user_form"):
        full_name = st.text_input("Full Name", placeholder="Enter your full name")
        email = st.text_input("Email", placeholder="Enter your email address")
        phone = st.text_input("Phone", placeholder="Enter your phone number")
        
        submitted = st.form_submit_button("Register User", type="primary")
        
        if submitted:
            if full_name and email and phone:
                # Prepare user data
                user_data = {
                    "full_name": full_name,
                    "email": email,
                    "phone": phone
                }
                
                try:
                    # Send POST request to FastAPI
                    response = requests.post(f"{API_URL}/users/", json=user_data)
                    
                    if response.status_code in (200, 201):
                        st.success("🎉 User registered successfully! ✅")
                        st.balloons()
                        # Clear form by rerunning
                        st.rerun()
                    else:
                        error_detail = response.json().get("detail", "Unknown error")
                        st.error(f"Registration failed: {error_detail}")
                        
                except requests.exceptions.ConnectionError:
                    st.error("🔌 Cannot connect to the API. Please make sure the FastAPI server is running on http://localhost:8000")
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
            else:
                st.warning("⚠️ Please fill in all fields!")

with col2:
    st.header("👥 Registered Users")
    
    if st.button("🔄 Refresh Users List"):
        try:
            response = requests.get(f"{API_URL}/users/")
            if response.status_code == 200:
                users = response.json()
                if users:
                    for user in users:
                        with st.expander(f"👤 {user['full_name']}"):
                            st.write(f"📧 **Email:** {user['email']}")
                            st.write(f"📱 **Phone:** {user['phone']}")
                            st.write(f"📅 **Registered:** {user['created_at'][:10]}")
                else:
                    st.info("No users registered yet! 🤷‍♀️")
            else:
                st.error("Failed to fetch users")
        except requests.exceptions.ConnectionError:
            st.error("🔌 Cannot connect to the API. Please make sure the FastAPI server is running.")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

# st.markdown("---")
# st.markdown("### 🚀 How to run this application:")
# st.code("""
# 1. Start FastAPI server (from Pydantic folder):
#    uv run uvicorn api.main:app --reload

# 2. Start Streamlit app:
#    uv run streamlit run app.py
# """)

# st.write("Here's our first attempt at using data to create a table:")
# st.write(pd.DataFrame({
#     'first column': [1, 2, 3, 4],
#     'second column': [10, 20, 30, 40]
# }))

# Add a selectbox to the sidebar:
add_selectbox = st.sidebar.selectbox(
    'How would you like to be contacted?',
    ('Email', 'Home phone', 'Mobile phone')
)

# Add a slider to the sidebar:
add_slider = st.sidebar.slider(
    'Select a range of values',
    0.0, 100.0, (25.0, 75.0)
)

left_column, right_column = st.columns(2)
# You can use a column just like st.sidebar:
left_column.button('Press me!')

# Or even better, call Streamlit functions inside a "with" block:
with right_column:
    chosen = st.radio(
        'Sorting hat',
        ("Gryffindor", "Ravenclaw", "Hufflepuff", "Slytherin"))
    st.write(f"You are in {chosen} house!")