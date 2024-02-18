import streamlit as st

st.set_page_config(page_title="About Us", page_icon="📈")

st.sidebar.header("About Us")

st.title("About Us")

st.write("Welcome to our team's Streamlit app! We are a group of four IT students studying at the University of Camerino. "
            "Here's a brief introduction to each team member:")

# Team Members
team_members = [
    {"name": "John Doe", "role": "Team Lead", "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit."},
    {"name": "Jane Smith", "role": "Developer", "description": "Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."},
    {"name": "Bob Johnson", "role": "Designer", "description": "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris."},
    {"name": "Alice Brown", "role": "Tester", "description": "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur."}
]

# Display team members
for member in team_members:
    st.markdown(f"### {member['name']} - {member['role']}")
    st.write(member['description'])
    st.write("")