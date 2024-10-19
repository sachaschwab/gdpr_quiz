import streamlit as st
import json
import random

# Set page config at the very beginning
st.set_page_config(layout="wide", page_title="GDPR Quiz")

def load_quiz_data():
    with open('content/quizz_data.json', 'r') as file:
        return json.load(file)

def local_css():
    st.markdown("""
    <style>
    /* #MainMenu {visibility: hidden;} */
    /* header {visibility: hidden;} */
    .question-button {
        width: 60% !important;
        padding: 0.2rem 0.5rem;
        margin: 0.1rem 0;
        border-radius: 4px;
        border: 1px solid rgba(49, 51, 63, 0.2);
    }
    .icon-correct, .icon-incorrect {
        display: flex;
        align-items: center;
        justify-content: center;
        margin-top: 20px;
        height: 100%;
    }
    .icon-correct {
        color: #28a745;
    }
    .icon-incorrect {
        color: #dc3545;
    }
    .stRadio > label {
        width: 100%;
        padding: 10px;
        margin: 5px 0;
        background-color: rgba(49, 51, 63, 0.2);  # Changed this line
        border-radius: 4px;
        color: inherit;  # Added this line
    }
    .stRadio > div[role="radiogroup"] {
        display: flex;
        flex-direction: column;
        background-color: transparent;  # Added this line
    }
    .stApp {
        margin-top: -80px;
    }
    .question-row {
        display: flex;
        align-items: center;
        margin: 0.1rem 0;
    }
    .question-button-col {
        flex-grow: 1;
    }
    .question-icon-col {
        width: 30px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .stButton button {
        padding: 0.25rem 0.5rem;
        font-size: 0.8rem;
    }
    .next-quiz-round-btn {
        background-color: #90EE90; /* Light green background */
        color: #006400; /* Dark green text */
        font-weight: bold; /* Bold text */
        /* Add any other existing styles here */
    }
    #nextQuizzRoundBtn {
        background-color: #90EE90 !important; /* Light green background */
        color: #006400 !important; /* Dark green text */
        font-weight: bold !important; /* Bold text */
        padding: 10px 20px; /* Add some padding for better appearance */
        border: none; /* Remove default button border */
        cursor: pointer; /* Change cursor to pointer on hover */
    }
    </style>
    """, unsafe_allow_html=True)

def get_new_quiz_round(all_questions, num_questions=10):
    return random.sample(all_questions, min(num_questions, len(all_questions)))

def find_next_unanswered_question(quiz_data):
    for i, _ in enumerate(quiz_data):
        if i not in st.session_state.answered_questions:
            return i
    return len(quiz_data)  # If all questions are answered

def get_answer_data(question, answer_data):
    if isinstance(answer_data, bool):
        is_correct = answer_data
        # Reconstruct the answer based on the correct solution
        correct_solution = question["correct_solution"].upper()
        user_answer = correct_solution
    elif isinstance(answer_data, tuple) and len(answer_data) == 2:
        is_correct, user_answer = answer_data
        user_answer = user_answer[0].upper()  # Extract just the letter
    else:
        is_correct = False
        user_answer = "?"
    return is_correct, user_answer

def display_question(question):
    st.subheader(f" ")
    st.subheader(f"Question {st.session_state.current_question + 1}")
    st.write(question['question'])

    options = [
        f"A) {question['option_a']}",
        f"B) {question['option_b']}",
        f"C) {question['option_c']}",
        f"D) {question['option_d']}"
    ]
    
    if st.session_state.current_question in st.session_state.answered_questions:
        # Display options as text instead of radio buttons
        st.write("Options:")
        for option in options:
            st.write(option)

        correct_solution = question["correct_solution"].upper()
        correct_answer = f"{correct_solution}) {question[f'option_{correct_solution.lower()}']}"
        
        answer_data = st.session_state.answered_questions[st.session_state.current_question]
        is_correct, user_answer = get_answer_data(question, answer_data)
        
        if is_correct:
            st.success(f"Your answer ({user_answer}) was correct!")
        else:
            st.error(f"Your answer ({user_answer}) was incorrect.")
            st.write(f"The correct answer is: {correct_answer}")
        
        st.write("Explanation:")
        st.write(question['explanation'])
        
        # Check if there are any unanswered questions
        next_question = find_next_unanswered_question(st.session_state.current_quiz_round)
        if next_question < len(st.session_state.current_quiz_round):
            # Add "Next Question" button only if there are unanswered questions
            if st.button("Next Question"):
                st.session_state.current_question = next_question
                st.rerun()
    else:
        selected_option = st.radio("Select your answer:", options, index=None, key="answer")

        if st.button("Submit"):
            if selected_option is None:
                st.warning("Please select an answer before submitting.")
            else:
                correct_solution = question["correct_solution"].upper()
                correct_answer = f"{correct_solution}) {question[f'option_{correct_solution.lower()}']}"
                is_correct = selected_option[0].upper() == correct_solution

                if is_correct:
                    st.success(f"Your answer ({selected_option[0].upper()}) was correct!")
                else:
                    st.error(f"Your answer ({selected_option[0].upper()}) was incorrect.")
                    st.write(f"The correct answer is: {correct_answer}")
                
                st.write("Explanation:")
                st.write(question['explanation'])

                st.session_state.answered_questions[st.session_state.current_question] = (is_correct, selected_option[0].upper())
                st.rerun()

def display_cookie_consent():
    if 'cookie_consent_given' not in st.session_state:
        st.session_state.cookie_consent_given = False

    if not st.session_state.cookie_consent_given:
        st.markdown(
            """
            <style>
            .cookie-box {
                display: flex;
                align-items: center;
                padding: 10px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                margin-bottom: 20px;
            }
            .cookie-text {
                margin-right: 10px;
            }
            .consent-button {
                background-color: orange;
                color: white;
                border: none;
                padding: 8px 16px;
                cursor: pointer;
                border-radius: 4px;
            }
            .accept-button {
                background-color: #006400;  /* Dark green background */
                color: white;  /* White text */
                font-weight: bold;  /* Bold text */
                border: none;
                padding: 8px 16px;
                cursor: pointer;
                border-radius: 4px;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <div class="cookie-box">
                <div class="cookie-text">We use cookies</div>
                <a href="https://streamlit.io/privacy-policy" target="_blank">
                    <button class="consent-button">Read Privacy & Cookies policy</button>
                </a>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Add the dark green "Accept Privacy & Cookie policy" button using Streamlit
        if st.button("Accept Privacy & Cookie policy", key="accept_cookies", type="primary"):
            st.session_state.cookie_consent_given = True
            st.rerun()

def main():
    local_css()
    display_cookie_consent()

    # Load all quiz data
    all_quiz_data = load_quiz_data()
    
    # Initialize session state
    if 'current_quiz_round' not in st.session_state:
        st.session_state.current_quiz_round = get_new_quiz_round(all_quiz_data)
    if 'current_question' not in st.session_state:
        st.session_state.current_question = -1  # -1 indicates the welcome screen
    if 'answered_questions' not in st.session_state:
        st.session_state.answered_questions = {}

    # Sidebar
    with st.sidebar:
        st.title("GDPR Quiz")
        for i in range(len(st.session_state.current_quiz_round)):
            col1, col2 = st.columns([4, 1])
            with col1:
                # Disable the button if cookie consent is not given
                if st.button(f"Question {i+1}", key=f"q_{i}", use_container_width=True, disabled=not st.session_state.cookie_consent_given):
                    st.session_state.current_question = i
                    st.rerun()  # Changed from st.experimental_rerun()
            with col2:
                if i in st.session_state.answered_questions:
                    is_correct, _ = get_answer_data(st.session_state.current_quiz_round[i], st.session_state.answered_questions[i])
                    icon = "✅" if is_correct else "❌"
                    st.markdown(f'<div style="display: flex; justify-content: center; align-items: center; height: 100%; position: relative; top: 8px;">{icon}</div>', unsafe_allow_html=True)
        
        # Add "Next Quiz Round" button if all questions are answered
        if len(st.session_state.answered_questions) == len(st.session_state.current_quiz_round):
            if st.sidebar.button(
                "Next Quiz Round",
                key="next_quiz_round",
                type="primary",
                use_container_width=True,
                help="Click to proceed to the next quiz round",
            ):
                st.session_state.current_quiz_round = get_new_quiz_round(all_quiz_data)
                st.session_state.current_question = -1
                st.session_state.answered_questions = {}
                st.rerun()  # Changed from st.experimental_rerun()

    # Main content
    if st.session_state.current_question == -1:
        st.title("Welcome to the GDPR Quiz")
        st.write("This app is not made for certification test preparation, but can be used to test your knowledge on GDPR.")
        st.write("The quiz generates a set of random 10 questions out of the 250 questions in the database.")
        st.write("Note that the certification tests are much harder. The questions were AI generated but curated by a human expert.")
        st.write("Have fun!")
        # Disable the "Start Quiz" button if cookie consent is not given
        if st.button("Start Quiz", disabled=not st.session_state.cookie_consent_given):
            st.session_state.current_question = 0
            st.rerun()  # Changed from st.experimental_rerun()
    elif st.session_state.current_question < len(st.session_state.current_quiz_round):
        display_question(st.session_state.current_quiz_round[st.session_state.current_question])
    else:
        st.success("Congratulations! You've completed this quiz round.")

if __name__ == "__main__":
    main()
