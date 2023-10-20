import time
import streamlit as st
import random
import json
import openai
import os
from dotenv import load_dotenv

load_dotenv()

openai.api_type = os.getenv("OPENAI_API_TYPE")
openai.api_base = os.getenv("OPENAI_API_BASE")
openai.api_version = os.getenv("OPENAI_API_VERSION")
openai.api_key = os.getenv("OPENAI_API_KEY")

with open('mbti.json') as file:
  file_contents = file.read()
mbti_desc = json.loads(file_contents)

mbti_list = mbti_desc.keys()
mbti_upper = [mbti.upper() for mbti in mbti_list]

st.set_page_config(
    page_title="MBTI Solver!",
    page_icon="🔮",
    layout="centered",
)

st.markdown('## MBTI 人生难题 解决器！')
st.markdown(""" 
> 本网站**仅供娱乐**，所有的结果都是随机生成的，我们强烈建议用户不要受其内容的影响来做出任何决策。  
> 本网站只是为了测试和娱乐，不允许用于商业用途，所有的内容都不能当作真实的，未成年人请勿使用。请各位用户理性对待，保持娱乐的心态，不要依赖或深信其结果。  
> 为保证可用性和成本限制，每次只能提问**一个问题**，请谨慎提问   
            
🥺   
试试作者的 [其他作品](https://kaiyi.cool)   
玩的开心记得点个 star 呀 [网站源代码](https://github.com/RealKai42/mbti-solver)         
""")

if "disable_input" not in st.session_state:
    st.session_state.disable_input = False

def disable():
    st.session_state["disable_input"] = True

def add_message(role, content, delay=0.05):
     with st.chat_message(role):
        message_placeholder = st.empty()
        full_response = ""

        for chunk in list(content):
            full_response += chunk + ""
            time.sleep(delay)
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)

with st.form("my_form"):
    mbti = st.selectbox('请输入您的类型', mbti_upper, disabled=st.session_state.disable_input)
    action = st.selectbox('请问您需要',['情感支持', '解决方案'], disabled=st.session_state.disable_input)
    question = st.text_input('请输入您的疑问', disabled=st.session_state.disable_input)

    submitted = st.form_submit_button("Submit", on_click=disable())

if submitted and mbti and action and question:
    with st.spinner('加载解读中，请稍等 ......'):
        fixed_text = "作为一名专业的MBTI（迈尔斯-布里格斯性格类型指标）心理医生，你的任务是根据来访者的性格类型和特点给出建议，"
        if action == '情感支持':
            variable_text = "主要提供情感支持，关注来访者的情绪需求，而不只是解决问题。"
        else:
            variable_text = "在主要提供解决方案的同时，也要注意给予来访者适当的情感支持。"
        ending_text = "你的回答需要专业、有深度，同时富有情感价值，能够引导来访者积极面对问题。"
        prompt = f"{fixed_text} {variable_text} {ending_text}"

        desc = mbti_desc[mbti.lower()]

        response = openai.ChatCompletion.create(
            engine="gpt35",
            messages = [{"role":"system","content":prompt},
                        {"role":"user","content":f"""
                        我的性格类型是：{mbti},
                        这种类型的性格特点是:{desc},
                        我遇到问题是:{question}"""},
                        ],
            temperature=0.7,
            max_tokens=800,
            top_p=0.95,
            frequency_penalty=0.5,
            presence_penalty=0.1,
            stop=None)

    add_message("assistant", response.choices[0].message.content)
    time.sleep(0.1)

    add_message("assistant", """感谢使用，   
                🥺    
试试作者的 [其他作品](https://kaiyi.cool)   
玩的开心记得点个 star 呀 [网站源代码](https://github.com/RealKai42/mbti-solver)     
                """, 0.01)
