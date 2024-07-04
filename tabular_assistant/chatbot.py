import streamlit as st
import pandas as pd
from streamlit_extras.add_vertical_space import add_vertical_space
from langchain_experimental.agents.agent_toolkits import create_csv_agent
from langchain_community.llms import Ollama


with st.sidebar:
    st.title("Chat with your csv")
    st.markdown('''
        Menu
    ''')
    csv = st.file_uploader("Upload your csv here", type='csv')
    add_vertical_space(5)

def main():
    st.header('Chat with your csv')
    model = Ollama(model="llama3")

    if csv is not None:
        agent = create_csv_agent(model,csv,verbose=True,allow_dangerous_code=True,max_iterations=10)
        if 'messages' not in st.session_state:
            st.session_state.messages = []

        def add_message(role, content):
            st.session_state.messages.append({"role": role, "content": content})

        df_query = st.chat_input("Enter your Query here")
        if df_query:
            add_message("user", df_query)
            try:
                response = agent.run(df_query)
                print(response)
                if response:
                    add_message("assistant", response)
                else:
                    add_message("assistant", "unable to generate output from the query")
            except Exception as e:
                print(e)
                add_message("assistant", str(e))
        
            for message in st.session_state.messages:
                if message["role"] == "user":
                    st.markdown(f"**User:** {message['content']}")
                else:
                    st.markdown(f"**Assistant:** {message['content']}")

if __name__=='__main__':
    main()
