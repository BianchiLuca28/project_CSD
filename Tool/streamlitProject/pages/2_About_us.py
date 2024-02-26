import streamlit as st

st.set_page_config(page_title="About Us", page_icon="📈")

st.sidebar.header("About Us")

st.title("About Us")

st.write("Welcome to our team's: **T-Sentry!**")
st.write("We are a group of four IT students studying Computer Science at the University of Camerino. "
            "Here's a brief introduction to each team member:")
st.write("")

# Team Members
team_members = [
    {"name": "Francesco Finucci", "email": "francesco.finucci@studenti.unicam.it" , "description": "I am a 25 year old with an interest for data, data analysis and machine learning. My two passions are mathematics (especially statistics and probability) and informatics and my dream is to be able work by combining them into the data analysis and artificial intelligence fields. I'm always eager to learn and i give my all for what i'm passionate about."},
    {"name": "Stanislav Teghipco", "email": "stanislav.teghipco@studenti.unicam.it", "description": "A Computer Science Master's student at the University of Camerino who is passionate about the new emerging technologies and who has a soft spot for Humanities related topics."},
    {"name": "Fabio Michele De Vitis", "email": "fabiomichele.devitis@studenti.unicam.it", "description": "Computer Science student at Unicam with a passion for Data Science. Equipped with a strong programming foundation and practical experience, I'm dedicated to making a positive impact in the dynamic realm of Data Science. Committed to continuous learning and growth at the intersection of technology and data."},
    {"name": "Luca Bianchi", "email": "luca.bianchi@studenti.unicam.it", "description": "I am a dedicated computer science student with a profound fascination for the realms of coding and Artificial Intelligence. As an perpetual learner, I am actively engaged in both academic studies and hands-on projects, constantly seeking ways to enhance my skills. My goal is to reach a point where I can seamlessly apply my knowledge to real-world challenges, fueling my passion for technology and pushing the boundaries of my interests."}
]

# Display team members
for member in team_members:
    st.markdown(f"### {member['name']}")
    st.write(f"Email: {member['email']}")
    st.write(member['description'])
    st.write("")