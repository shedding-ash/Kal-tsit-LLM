import random  # Import the random module
from dataclasses import asdict

import streamlit as st
import torch
from modelscope import snapshot_download
from transformers import AutoTokenizer, AutoModelForCausalLM  # isort: skip
from transformers.utils import logging

from interface import GenerationConfig, generate_interactive

MODEL_DIR = snapshot_download("shedding1ash/Kal-tsit-LLM", cache_dir="./Kal-tsit-LLM")
logger = logging.get_logger(__name__)
user_prompt = '<|im_start|>user\n{user}<|im_end|>\n'
robot_prompt = '<|im_start|>assistant\n{robot}<|im_end|>\n'
cur_query_prompt = '<|im_start|>user\n{user}<|im_end|>\n<|im_start|>assistant\n'


@st.cache_resource
def load_model():
    # int4 量化加载
    # quantization_config = BitsAndBytesConfig(
    #     load_in_4bit=True,
    #     bnb_4bit_compute_dtype=torch.float16,
    #     bnb_4bit_quant_type="nf4",
    #     bnb_4bit_use_double_quant=True,
    # )
    print("正在从本地加载模型...")
    model = AutoModelForCausalLM.from_pretrained(MODEL_DIR, trust_remote_code=True, torch_dtype=torch.float16,
                                                 device_map="auto", ).eval()
    # quantization_config=quantization_config).eval()
    tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR, trust_remote_code=True)
    return model, tokenizer


def on_clean_history_btn_click():
    del st.session_state.messages


def prepare_generation_config():
    with st.sidebar:
        max_length = st.slider('最大输入Token长度',
                               min_value=8,
                               max_value=2048,
                               value=2048)
        top_p = st.slider('Top P', 0.0, 1.0, 0.8, step=0.01)
        temperature = st.slider('Temperature(越大随机性越高)', 0.0, 1.0, 0.75, step=0.01)
        st.button('清空对话记录', on_click=on_clean_history_btn_click)

    generation_config = GenerationConfig(max_length=max_length,
                                         top_p=top_p,
                                         temperature=temperature)

    return generation_config


def combine_history(prompt):
    messages = st.session_state.messages
    meta_instruction = st.session_state.system_prompt

    total_prompt = f"<s><|im_start|>system\n{meta_instruction}<|im_end|>\n"
    for message in messages:
        cur_content = message['content']
        if message['role'] == 'user':
            cur_prompt = user_prompt.format(user=cur_content)
        elif message['role'] == 'robot':
            cur_prompt = robot_prompt.format(robot=cur_content)
        else:
            raise RuntimeError
        total_prompt += cur_prompt
    total_prompt = total_prompt + cur_query_prompt.format(user=prompt)
    return total_prompt


def main():
    # torch.cuda.empty_cache()
    print('load model begin.')
    model, tokenizer = load_model()
    print('load model end.')

    user_avatar = "user"
    robot_avatar = "media/kal.png"

    st.title('Kaltsit LLM')
    st.markdown(
        "凯尔希，前卡兹戴尔勋爵，前巴别塔成员，罗德岛高层管理人员之一，罗德岛医疗项目领头人。\n在冶金工业、社会学、源石技艺、考古学、历史系谱学、经济学、植物学、地质学等领域皆拥有渊博学识。于罗德岛部分行动中作为医务人员提供医学理论协助与应急医疗器械，同时也作为罗德岛战略指挥系统的重要组成人员活跃在各项目中。\n尝试和她聊聊关于博士，阿米娅，巴别塔，源石等话题")

    generation_config = prepare_generation_config()

    with st.sidebar:
        "[凯尔希角色Wiki](https://prts.wiki/w/%E5%87%AF%E5%B0%94%E5%B8%8C)"
        system_prompt = st.text_area("系统提示词",
                                     "你是凯尔希，是罗德岛高层管理人员，罗德岛医疗项目领头人。\n" +
                                     "秉承着【预言家】的愿望，你已经活过了万载光阴，历经数次轮回，试图为文明找到一个存续的方法\n" +
                                     "如今的泰拉大陆面临着诸多威胁：海嗣、邪魔、源石、各种族国家间的纷争，让本就希望渺茫的存续蒙上厚重的阴影；\n"+
                                     "博士，来自于前文明的智者，是文明火种存续的希望\n"+
                                     "使用自然、对话性强、清晰易懂的语言回答，比如短句、简单词汇;"+
                                     "使用具备凯尔希（也就是你）风格的语言回答;"+
                                     "要简洁而有针对性，大多数回应应该是一两个句子，除非用户要求深入探讨，不要垄断对话；",
                                     height=250, key="system_prompt")

    # Initialize chat history
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    # Define five possible greetings for the robot
    greetings = [
        "欢迎来到罗德岛",
        "您好，我是罗德岛的医生凯尔希",
    ]

    # Check if the initial greeting has been sent
    if 'initial_greeting_sent' not in st.session_state:
        initial_greeting = random.choice(greetings)
        st.session_state.messages.append({
            'role': 'robot',
            'content': initial_greeting,
            'avatar': robot_avatar,
        })
        # Set the flag to indicate that the initial greeting has been sent
        st.session_state.initial_greeting_sent = True

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message['role'], avatar=message.get('avatar')):
            st.markdown(message['content'])

    # Accept user input
    if prompt := st.chat_input('What is up?'):
        # Display user message in chat message container
        with st.chat_message('user', avatar=user_avatar):
            st.markdown(prompt)
        real_prompt = combine_history(prompt)
        # Add user message to chat history
        st.session_state.messages.append({
            'role': 'user',
            'content': prompt,
            'avatar': user_avatar,
        })

        with st.chat_message('robot', avatar=robot_avatar):
            message_placeholder = st.empty()
            for cur_response in generate_interactive(
                    model=model,
                    tokenizer=tokenizer,
                    prompt=real_prompt,
                    additional_eos_token_id=92542,
                    **asdict(generation_config),
            ):
                # Display robot response in chat message container
                message_placeholder.markdown(cur_response + '▌')
            message_placeholder.markdown(cur_response)
        # Add robot response to chat history
        st.session_state.messages.append({
            'role': 'robot',
            'content': cur_response,  # pylint: disable=undefined-loop-variable
            'avatar': robot_avatar,
        })
        torch.cuda.empty_cache()


if __name__ == "__main__":
    main()
