import openai
import streamlit as st
from streamlit_pills import pills

openai.api_key="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"

st.subheader("AI Assistant: Streamlit + OpenAI: 'stream' *argument*")
selected = pills("",["NO Streaming", "Streaming"],["xxx-0", "xxx-1"])

user_input = st.text_input("You:", placeholder = "Ask me anything ...", key="input")



if st.button("Submit", type="primary"):
    st.markdown("----")
    res_box = st.empty()

    if selected == "Streaming":
        None

    else:
        completions = openai.Completion.create(mode='txt-davinci-003',
                                               prompt=user_input,
                                               max_tokens=120,
                            
                                               temperature=0.5,)
