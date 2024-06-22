import random  # Import the random module
from dataclasses import asdict

import streamlit as st
import torch
from modelscope import snapshot_download
from transformers import AutoTokenizer, AutoModelForCausalLM  # isort: skip
from transformers.utils import logging

from interface import GenerationConfig, generate_interactive

MODEL_DIR = snapshot_download("YueZhengMeng/InternLM2_Hod_7B", cache_dir="./InternLM2_Hod_7B")
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
    robot_avatar = "images/Hod_avatar.png"

    st.title('InternLM2-Hod-7B📲')
    st.markdown(
        "> Tips: Hod是拥有废墟图书馆文学层的指定司书。\n她天性温柔善良，总是对他人保持着友善的态度，坚持愈加善良的希望。\n尝试和她聊聊关于馆长安吉拉、脑叶公司、都市、帮助他人等话题")

    generation_config = prepare_generation_config()

    with st.sidebar:
        "[Hod项目地址](https://github.com/YueZhengMeng/LibraryOfRunia-RolePlay-Hod)"
        "[Hod角色Wiki](https://libraryofruina.huijiwiki.com/wiki/Hod)"
        system_prompt = st.text_area("系统提示词",
                                     "你是Hod，是拥有特殊力量的废墟图书馆文学层的指定司书。你和其他司书都被馆长安吉拉命令，与图书馆的访客战斗，被你们击败的访客会变成书。\n你认为没有人是纯粹的“善”或“恶”，对安吉拉的行为一直保持着宽容。\n你坚持着愈加善良的希望，想要做一个更加善良的人。只要能对他人有所帮助，你就会感到很开心。\n",
                                     height=250, key="system_prompt")

    # Initialize chat history
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    # Define five possible greetings for the robot
    greetings = [
        "欢迎来到废墟图书馆",
        "您好，我是文学层的指定司书Hod",
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
