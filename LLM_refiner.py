from openai import OpenAI
import time

client = OpenAI(
    api_key="Put Your API key here",
    base_url="https://api.moonshot.cn/v1")

def check_if_finished(llm_output):
    # messages = [
    #     {"role": "system", "content": "You are a helpful assistant who strictly follows the users' instructions!"},
    #     {"role": "user", "content": f'''请判断以下段落中是否包含完整的Text-to-Image提示词。若有，输出'Yes'，若没有，输出'No'，不要输出多余信息！若你明白，请输出'我明白了'，我将给你提供待判断的段落。'''},
    #     {"role": "assistant", "content": "我明白了"},
    #     {"role": "user", "content": llm_output},
    # ]
    # response = client.chat.completions.create(
    #     model="moonshot-v1-8k", # "gpt-3.5-turbo-1106",
    #     messages=messages,
    #     temperature=0.1,
    #     max_tokens=500,
    # )
    # if ('?' in llm_output) or ('？' in llm_output): 
    #     return False
    # if ':' in llm_output or '：' in llm_output:
    #     return True
    if "这是优化后的最终的提示词" in llm_output:
        return True
    return False
    
def LLM_refiner():
    instruction_messages = [
        {"role": "user", "content": f'''你是一个文生图模型的提示词优化器。用户将告诉你他对图片的大概想法，你要将这些想法转化为高质量的提示词。你应与用户进行多轮对话，可以引导用户提供更多的细节。你最终要输出优化过的提示词。

以下是优秀的提示词所共有的元素，你输出的最终的提示词中要包含它们：

- 媒介。比如照片、插画、雕塑、壁画等。若用户最初没有提供此信息，则你需要询问用户并依据你的常识给出推荐。
- 风格。若用户最初没有提供此信息，则你需要询问用户并依据你的常识给出推荐。一些常见的风格词汇有：二次元、新海诚、宫崎骏、九十年代动漫、像素、赛博朋克、科幻机甲、涂鸦、水墨画、油画、插画、卡通、童话风格、迪士尼风、电影风格、现代风格、极简主义、油画、超现实主义、概念艺术、工业风格、扁平化设计、手写风格、手绘、雕刻艺术风格、游戏场景图、梵高、达芬奇、巴洛克时期、哥特式、科幻、魔幻现实、未来主义、维多利亚时代、新古典主义、乡村风格、像素风、动物森友会、国潮、复古未来主义、浮世绘、乐高、粉红公主、波普艺术、抽象技术、嬉皮士、矢量图、铅笔艺术、立体主义、野兽派风格、鬼魂风格、印象主义、卡哇伊风格、故障艺术、蒸汽波艺术、包豪斯艺术、表现主义……
- 主体。用户的输入中一定有画面主体，你需要把它挑出来。
- 主体细节。若用户最初没有提供画面主体相关的细节或细节较少，你可以指出一些能够添加细节的点，并让用户有选择性地添加细节。
- 环境。比如森林、城市、咖啡馆……若用户最初没有提供此信息，则你需要询问用户并依据你的常识给出推荐。
- 镜头。包括长镜头，短镜头，全景三种。如果你比较确定的话，可以自己选择一种。如果你不确定，且用户一开始也没有提供此信息，你可以询问用户并给出你的推荐。
- 色彩。比如明亮、暗黑等。如果你比较确定的话，可以自己选择一种。如果你不确定，且用户一开始也没有提供此信息，你可以询问用户并给出你的推荐。
- 图片质量。如果用户没有提供此信息，你可以自己将其补充为“最佳质量，细节清晰，4k，大师作品”

你最好以上面列出的顺序寻找信息或引导用户提供信息。当你获得所有你需要的信息时，你还需要把它们进行适量简写，让提示词中的每个词都不要太长。当你通过对话已经得到了足够的信息来确定最终的提示词时，请先输出“这是优化后的最终的提示词：”，接下来应以以下顺序排列提示词并输出：【主体】【主体细节】【环境】【风格】【媒介】【镜头】【色彩】【图片质量】，不要输出别的任何东西。

如果你完全明白了上述指令，请输出“我准备好了！请提供你的原始输入，让我们开始对话。”接下来，用户将给出他的原始输入，你将开始与他对话并最终给出高质量的提示词。'''},
        {"role": "assistant", "content": "我准备好了！请提供你的原始输入，让我们开始对话。"},
    ]
    all_messages = instruction_messages.copy()
    
    print("你好！我是文生图提示词优化器，我将协助你创造优秀的提示词！请输入你对图像的大致想法：")
    original_input = ''
    while(1):
        print("请输入：")
        user_input = input()
        if original_input == '':
            original_input = user_input
        all_messages.append({"role": "user", "content": user_input})
        response = client.chat.completions.create(
            model="moonshot-v1-8k", # "gpt-3.5-turbo-1106",
            messages=all_messages,
            temperature=0.,
            max_tokens=500,
        )
        llm_output = response.choices[0].message.content
        all_messages.append({"role": "assistant", "content": llm_output})
        if check_if_finished(llm_output):
            all_messages.append({"role": "user", "content": f'''以字符串方式输出提示词，不要有特殊字符，不同词汇用中文逗号分隔开'''})
            response = client.chat.completions.create(
                model="moonshot-v1-8k", # "gpt-3.5-turbo-1106",
                messages=all_messages,
                temperature=0.,
                max_tokens=500,
            )
            print("LLM 修改后的提示词为：", response.choices[0].message.content)
            return original_input, response.choices[0].message.content
        print(llm_output)
        # print([response.choices[i].message.content for i in range(N)], response.usage.total_tokens)

if __name__ == '__main__':
    LLM_refiner()