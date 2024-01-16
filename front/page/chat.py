import streamlit as st
import requests
import json

def add_chat_message(data, draw: bool = True):
    st.session_state.history.append(data)
    if draw:
        st.chat_message(name=data['role']).markdown(data['content'])

def chat_page():
    st.title("💬 Text2Image Bot")
    with st.expander("用法说明", expanded=True):
        st.markdown("这是一个文本到图像的生成器。你可以在下面的输入框中输入你对图片的描述，随后根据语言模型的说明补充细节。在你对模型优化过的提示词满意且没有更多信息需要补充之后，点击“生成图片”按钮，即可生成图片。")
    
    if 'history' not in st.session_state or st.session_state['history'] == []:
        st.session_state['history'] = []
        add_chat_message({
            'role': 'assistant',
            'content': '你好，请输入你对图片的描述。'
        }, draw=False)
        
    for message in st.session_state['history']:
        st.chat_message(name=message['role']).markdown(message['content'])
    if 'is_end' not in st.session_state:
        st.session_state['is_end'] = False
    if st.session_state['is_end']:
        st.chat_message(name='assistant').markdown(':red[**LLM 已经完成提示词优化。如果您认为没有更多信息需要补充，可以点击下方的按钮生成图片。**]')
        
    if 'img_url' in st.session_state:
        # show the image using its url and its scale 200 * 200
        # st.markdown(f"![Generated Image]({st.session_state['img_url']})")
        st.write(f"<div style=\"text-align: center;\"><img src=\"{st.session_state['img_url']}\" style=\"zoom:35%;\" align=center /></div>", unsafe_allow_html=True)
        
    prompt = st.chat_input()
    if prompt:
        st.session_state['is_end'] = False
        add_chat_message({
            'role': 'user',
            'content': prompt
        })
        chatbot = ChatBot()
        response = chatbot.ask(prompt)
        print(response)
        if response[1]:
            st.session_state['is_end'] = True
            st.chat_message(name='assistant').markdown(f'这是您的提示词：{st.session_state["prompt"]}')
            add_chat_message({
                'role': 'assistant',
                'content': response[0]
            }, draw=False)
        else:
            add_chat_message({
                'role': 'assistant',
                'content': response[0]
            })
        st.rerun()
        
    if len(st.session_state.history) > 1 and st.button('结束对话生成图片'):
        chatbot = ChatBot()
        response = chatbot.finish()
        if response['img_generated']:
            st.session_state['img_url'] = response['img_url']
            # st.markdown(f"![Generated Image]({response['img_url']})")
            st.write(f"<div style=\"text-align: center;\"><img src=\"{st.session_state['img_url']}\" style=\"zoom:35%;\" align=center /></div>", unsafe_allow_html=True)
        else:
            st.session_state['is_end'] = True
            st.session_state['prompt'] = response['prompt']
            st.chat_message(name='assistant').markdown(f'这是您的提示词：{st.session_state["prompt"]}')
            add_chat_message({
                'role': 'assistant',
                'content': response['response']
            }, draw=False)
        st.rerun()
        
    # chatbot
    # (str, bool)
    # (str, bool)
    # button
    # draw image markdown
    
class ChatBot:
    def __init__(self):
        pass

    def ask(self, prompt: str) -> (str, bool):
        # response = ("This is a mock response.", False)
        data = {
            "history": st.session_state['history'][1:-1],
            "user_input": prompt,
        }
        data_str = json.dumps(data)
        response = requests.get("http://localhost:8080/chat/", data=data_str).json()
        st.session_state['prompt'] = response['prompt']
        return response['response'], response['is_end']
    
    def finish(self):
        data = {
            "history": st.session_state['history'][1:],
            "prompt": st.session_state['prompt'],
        }
        data_str = json.dumps(data)
        response = requests.get("http://localhost:8080/finish/", data=data_str).json()
        return response