import streamlit as st
import time
import os
import json
import backend  # Assumes backend has disease prediction logic




# Function to load previous chat history from a file
def load_chat_history():
    if os.path.exists("chat_history.json"):
        with open("chat_history.json", "r") as file:
            return json.load(file)
    else:
        return []

# Function to save the chat history to a file
def save_chat_history():
    with open("chat_history.json", "w") as file:
        json.dump(st.session_state.messages, file)

# Function to format response as bullet points
def format_response_as_points(prompt):
    # Generate response from backend
    response = backend.GenerateResponse(prompt)
    
    # Ensure response is a string (convert list to string if needed)
    if isinstance(response, list):  
        response = " ".join(response)  # Convert list to a single string
    
    response = response.strip()  # Remove leading/trailing whitespace
    
    # Split response into points (delimiters: '.', ';', or newlines)
    points = [point.strip() for point in response.replace('\n', '.').split('.') if point.strip()]
    return points

# Sidebar for settings
st.sidebar.title("Chatbot Settings")

# Assigning a unique key to the radio button to prevent duplicate IDs
theme = st.sidebar.radio("Select Theme", ["Light", "Dark"], key="theme_selector")

# Apply selected theme using HTML/CSS
if theme == "Dark":
    st.markdown(""" 
    <style>
        body {
            background-color: #333;
            color: white;
        }
        .stChatMessage {
            background-color: #444;
            color: white;
        }
        .stTextInput input {
            background-color: #555;
            color: white;
        }
    </style>
    """, unsafe_allow_html=True)
else:
    st.markdown(""" 
    <style>
        body {
            background-color: white;
            color: black;
        }
        .stChatMessage {
            background-color: #f4f4f4;
            color: black;
        }
        .stTextInput input {
            background-color: #f9f9f9;
            color: black;
        }
    </style>
    """, unsafe_allow_html=True)

# Title of the app
st.title("Healthcare Chatbot")

# Clear chat button to reset history
if st.sidebar.button("Clear Chat"):
    st.session_state.messages.clear()
    save_chat_history()  # Save the cleared history to the file
    st.rerun()  # Reload the app to reflect changes

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = load_chat_history()  # Load chat history from file

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(
            f"<div style='background-color: "
            f"{'#f4f4f4' if message['role'] == 'assistant' else '#d1f1ff'}; "
            f"padding: 10px; border-radius: 5px;'>{message['content']}</div>",
            unsafe_allow_html=True,
        )

# Custom input form for healthcare-related data
st.sidebar.header("Enter Healthcare Information:")

# User inputs for symptoms, medications, diets, etc.
symptoms = st.sidebar.text_area("Enter symptoms (comma separated)")
description = st.sidebar.text_area("Describe the condition (optional)")
medications = st.sidebar.text_area("List any medications (optional)")
diet = st.sidebar.text_area("Any dietary preferences or restrictions (optional)")
precautions = st.sidebar.text_area("Any precautions you follow (optional)")
foods_to_avoid = st.sidebar.text_area("Foods to avoid (optional)")
foods_to_intake = st.sidebar.text_area("Foods to intake (optional)")

# Specialist consultation
specialist = st.sidebar.selectbox("Select Specialist to Consult", ["General Physician", "Dermatologist", "Cardiologist", "Neurologist", "Pediatrician", "Gynecologist"])

# Accept user input for healthcare suggestions
if st.sidebar.button("Get Healthcare Suggestions"):
    # Combine user input into a query
    prompt = f"Given the symptoms: {symptoms}, description: {description}, medications: {medications}, diet: {diet}, precautions: {precautions}, foods to avoid: {foods_to_avoid}, foods to intake: {foods_to_intake}, which disease can be predicted? What precautions, diet, foods to avoid and intake should be followed? Also, which specialist should be consulted?"

    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message in the chat
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate assistant response
    with st.chat_message("assistant"):
        with st.spinner("Predicting disease..."):
            # Format the response into points
            response_points = format_response_as_points(prompt)

            # Display each point as a bullet
            st.markdown("### Healthcare Suggestions:")
            for point in response_points:
                st.markdown(f"- {point}")

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": "\n".join(response_points)})

    # Save chat history to file
    save_chat_history()