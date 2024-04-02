import streamlit as st
from langchain.chains import LLMChain
import cohere

# Initialize components

coherence = cohere('k9UV95uPtYxrklUp13NowufdqwmxWb9zvGvs4c23')
chain = LLMChain()
chat_history = []

# Build Streamlit interface
def app():
    st.title("My Talking Friend")
    user_input = st.text_input("Ask me anything!")
    
    if user_input:
        chat_history.append(user_input)
        # Use Langchain to analyze conversation and update context
        chain.update(user_input)
        # Generate response based on user input and conversation context
        response = coherence.generate(
            text=chain.get_prompt(),
            temperature=0.7,
            top_p=0.9,
        )["generations"][0]["text"]
        chat_history.append(response)
        
        # Display chat history
        for message in chat_history:
            st.write(message)

app()
