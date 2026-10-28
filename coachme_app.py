import streamlit as st
import pandas as pd
import json

st.set_page_config(
    page_title="CoachMe™ Diagnostic Assessment Tool",
    page_icon="🎯",
    layout="wide"
)

st.title("CoachMe™ Self-Assessment Tool")
st.write("Discover your Person Code, Model Roles, Key Traits, and Caution Areas.")

# Definition of CVAs
CVA_INFO = {
    1: {"name": "Societal Change", "desc": "Influencing public opinion, advocating for justice, and driving systemic cultural shifts."},
    2: {"name": "Theoretical Discovery", "desc": "Answering complex questions, analyzing systems, and exploring underlying concepts."},
    3: {"name": "Strategic Decisions", "desc": "Managing operational plans, resource allocation, and organizational strategy."},
    4: {"name": "Human Development", "desc": "Mentoring, advising, pastoral care, and fostering individual growth."},
    5: {"name": "Entrepreneurial Challenge", "desc": "Pioneering new initiatives, taking calculated risks, and building fresh expressions."},
    6: {"name": "Production Efficiency", "desc": "Maintaining operational order, repeatable systems, and execution quality."},
    7: {"name": "Artistic Creativity", "desc": "Designing innovations, visual/narrative storytelling, and creative expression."},
    8: {"name": "Natural Appreciation", "desc": "Pattern recognition, contemplative balance, environmental connection, and sanctuary."},
    9: {"name": "Motivational Energy", "desc": "Energizing teams, building enthusiastic consensus, and dynamic engagement."}
}

MODEL_ROLES_MAP = {
    4: {"role": "The Advocate / Mentor", "desc": "Pleading for individual growth, interceding for outcasts, and forming safe spaces for self-discovery."},
    1: {"role": "The Culturalist / Defender", "desc": "Exegeting context, confronting institutional harm, and establishing protective sanctuary."},
    8: {"role": "The Contemplative Pattern-Finder", "desc": "Observing divine/natural connections, preserving balance, and resting in quiet discernment."},
    5: {"role": "The Pioneer / Builder", "desc": "Launching fresh expressions in third spaces and taking bold risks for community impact."},
    7: {"role": "The Storyteller / Innovator", "desc": "Communicating through visual media, pop culture parables, and creative narrative arts."},
    9: {"role": "The Catalyst / Energizer", "desc": "Inspiring collective action and building joyful, open-table community."}
}

st.sidebar.title("CoachMe™ Navigation")
page = st.sidebar.radio("Go to", ["Welcome & Overview", "Take Assessment", "View Results Dashboard", "Deployment Guide"])

if page == "Welcome & Overview":
    st.header("Welcome to CoachMe™")
    st.write("CoachMe™ is a diagnostic assessment platform designed to help anyone discover their Person Code, Model Roles, Key Traits, and Caution Areas.")
    st.info("Click **Take Assessment** in the sidebar to begin.")

elif page == "Take Assessment":
    st.header("CoachMe™ Diagnostic Questionnaire")
    st.write("Rate each scenario from 1 (Least Like Me) to 5 (Most Like Me).")
    
    with st.form("assessment_form"):
        q1 = st.slider("1. I feel most energized when helping individuals grow, heal, and discover their authentic identity.", 1, 5, 3)
        q2 = st.slider("2. I am driven to speak out against social injustices, institutional hypocrisy, or systemic gaps.", 1, 5, 3)
        q3 = st.slider("3. I find deep satisfaction in quiet reflection, observing patterns in nature, and protecting balance.", 1, 5, 3)
        q4 = st.slider("4. I love pioneering new projects, venturing into third-space environments, and taking risks.", 1, 5, 3)
        q5 = st.slider("5. I am naturally drawn to visual arts, creative storytelling, photography, or digital media.", 1, 5, 3)
        q6 = st.slider("6. I thrive when bringing high energy to groups, inspiring people, and creating enthusiasm.", 1, 5, 3)
        
        q7 = st.slider("7. People naturally come to me for individual coaching, pastoral care, or personal counsel.", 1, 5, 3)
        q8 = st.slider("8. I am skilled at reading cultural contexts, analyzing community needs, and advocating for outcasts.", 1, 5, 3)
        q9 = st.slider("9. I excel at subtle pattern recognition, seeing underlying connections others miss.", 1, 5, 3)
        
        submit = st.form_submit_button("Calculate My Profile")
        
        if submit:
            scores = {
                4: q1 + q7,
                1: q2 + q8,
                8: q3 + q9,
                5: q4 * 2,
                7: q5 * 2,
                9: q6 * 2
            }
            sorted_cvas = sorted(scores.items(), key=lambda x: x[1], reverse=True)
            st.session_state.person_code = [cva[0] for cva in sorted_cvas[:3]]
            st.session_state.scores = scores
            st.success("Assessment Complete! Navigate to 'View Results Dashboard' in the sidebar.")

elif page == "View Results Dashboard":
    st.header("Your CoachMe™ Profile Dashboard")
    if 'person_code' not in st.session_state:
        st.warning("Please complete the assessment under 'Take Assessment' first.")
    else:
        code = st.session_state.person_code
        code_str = " · ".join(map(str, code))
        primary_role = MODEL_ROLES_MAP.get(code[0], {"role": "Relational Developer"})["role"]
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Person Code (High Triad)", code_str)
        with col2:
            st.metric("Primary Model Role", primary_role)
            
        st.subheader("Core Value Areas (CVA) Energy Distribution")
        df_scores = pd.DataFrame([
            {"CVA": f"{k}. {CVA_INFO[k]['name']}", "Score": v} 
            for k, v in st.session_state.scores.items()
        ])
        st.bar_chart(df_scores.set_index("CVA"))

        col_a, col_b = st.columns(2)
        with col_a:
            st.subheader("🌟 Key Traits & Superpowers")
            st.write("• **Relational Empathy**: Creates deep psychological safety.")
            st.write("• **Pattern Recognition**: Uncovers systemic gaps and connections.")
            st.write("• **Open-Table Hospitality**: Fosters inclusive community.")

        with col_b:
            st.subheader("⚠️ Caution Areas & Grace Boundaries")
            st.write("• **The Messiah Trap**: Guard against taking over-responsibility.")
            st.write("• **Defensive Walls Under Friction**: Watch for emotional detachment.")
            st.write("• **Institutional Friction**: Balance non-hierarchical community with structure.")

elif page == "Deployment Guide":
    st.header("Online Deployment Guide")
    st.write("To deploy CoachMe™ online:")
    st.code("pip install streamlit pandas
streamlit run coachme_app.py")
