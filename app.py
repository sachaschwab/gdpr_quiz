import streamlit as st

# Set page config at the very beginning
st.set_page_config(layout="wide", page_title="GDPR Quiz")

def main():
    st.title("GDPR Quiz Has Moved")
    
    st.markdown("""
    <div style='text-align: center; padding: 50px; font-size: 24px;'>
        The GDPR Quiz has moved to 
        <a href='https://www.aicrafters.ai' target='_blank'>www.aicrafters.ai</a>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
