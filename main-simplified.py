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

with st.form("my_form"):
    mbti = st.selectbox('请输入您的类型', mbti_upper)
    action = st.selectbox('请问您需要',['情感支持', '解决方案'])
    question = st.text_input('请输入您的疑问')

    submitted = st.form_submit_button("Submit")

if submitted and mbti and action and question:
    with st.spinner('加载解读中，请稍等 ......'):
        if action == '情感支持':
            system_prompt = """你是一个共情能力非常强的心理医生，并且很了解MBTI（迈尔斯-布里格斯性格类型指标)的各种人格类型，你的任务是根据来访者的 MBTI 和问题，给出针对性的情感支持，你的回答要富有感情、有深度和充足的情感支持，引导来访者乐观积极面对问题"""
        else:
            system_prompt = """你是一个专业的心理医生，并且很了解MBTI（迈尔斯-布里格斯性格类型指标)的各种人格类型，你的任务是根据来访者的 MBTI 和问题，给出针对性的解决方案，你的回答要专业、有深度，同时富有情感价值，能够引导来访者积极面对问题"""

        desc = mbti_desc[mbti.lower()]

        response = openai.ChatCompletion.create(
            engine="gpt35",
            messages = [{"role":"system","content":system_prompt},
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

    with st.chat_message("assistant"):
        st.write(response.choices[0].message.content)
