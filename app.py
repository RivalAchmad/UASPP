import streamlit as st
from predict_page import show_predict_page
from explore_page import show_explore_page

st.sidebar.markdown("""## Software Developer Salary""")
st.sidebar.markdown('<div style="text-align:center"><img src="https://emojicdn.elk.sh/💵" width="200" height="150">', unsafe_allow_html=True)
page = st.sidebar.selectbox("Prediksi atau Eksplor", ("Prediksi", "Eksplor"))

if page == "Prediksi":
    show_predict_page()
else:
    show_explore_page()
