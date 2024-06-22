<p align="center" width="100%">
  <img src="https://github.com/shedding-ash/Kal-tsit-LLM/blob/main/media/kal.jpg" width="50%">
</p>

本项目数据来源于

- [PRTS](https://prts.wiki/)
- [ArknightsGameResource](https://github.com/yuanyan3060/ArknightsGameResource)

模型使用 [xtuner](https://github.com/InternLM/xtuner) 在 [InternLM2](https://github.com/InternLM/InternLM) 的基础上指令微调而来

- Modelscope [凯尔希微调模型 · 模型库](https://modelscope.cn/models/shedding1ash/Kal-tsit-LLM)
- Openxlab [应用中心-OpenXLab](https://openxlab.org.cn/apps/detail/shedding_ash/Kal-tsit-LLM)

特别鸣谢

- 上海人工智能实验室提供的算力平台
- 书生·浦语团队提供的技术支持

## 模型介绍

Kal'tsit LLM 是一款模仿《明日方舟》中角色凯尔希的语气和风格的聊天机器人，其基于internLM2 7B进行了精细的指令微调，能够以凯尔希的口吻与用户进行互动。

1. **角色模仿对话**：Kal'tsit Bot 能够根据《明日方舟》中凯尔希的对话语料，生成符合其角色特点的回应，包括语气、用词习惯和情感表达。
2. **上下文理解**：通过对大量对话语料的学习，Kal'tsit Bot 能够理解对话的上下文，提供连贯且相关的回答。
3. **情感识别与响应**：系统能够识别用户的情绪，并以凯尔希的风格做出相应的情感反应，增强对话的自然性和互动性。
4. **多轮对话管理**：Kal'tsit Bot 支持多轮对话，能够记住之前的对话内容，使得对话更加流畅和个性化。
5. **知识库扩展**：除了《明日方舟》的对话语料，Kal'tsit Bot 还能够访问和整合外部知识库，以提供更丰富的对话内容。
6. **用户定制化**：用户可以根据自己的喜好，对Kal'tsit Bot 的对话风格进行一定程度的定制，使其更加符合个人的期待。
7. **跨平台交互**：Kal'tsit Bot 支持多种平台，包括但不限于网页、移动应用等，用户可以在不同设备上与凯尔希进行互动。
8. **持续学习与优化**：Kal'tsit Bot 具备自我学习和优化的能力，能够根据用户的反馈不断改进对话质量。

我们相信，通过不断的技术迭代和用户反馈，Kal'tsit Bot 将成为一个更加智能、有趣且富有个性的对话伙伴。

## 数据准备

## 模型训练

### 微调环境准备

```bash
# 使用conda创建一个名为xtuner的新环境，并指定Python版本为3.10，-y选项表示自动接受所有提示
conda create --name xtuner python=3.10 -y

# 激活名为xtuner的conda环境
conda activate xtuner

# 切换到用户的主目录，'~'是当前用户主目录的快捷方式
cd ~

# 在用户的主目录下创建xtuner目录，如果目录已存在则不进行任何操作，并切换到该目录
mkdir -p /root/xtuner && cd /root/xtuner

# 从GitHub克隆xtuner项目的指定分支v0.1.17到本地
git clone -b v0.1.17 https://github.com/InternLM/xtuner

# 切换到克隆的xtuner目录中
cd /root/xtuner/xtuner

# 在xtuner目录中使用pip安装当前目录下的所有依赖，并以可编辑模式安装，这样对代码的更改会立即反映出来
pip install -e '.[all]'

alpaca_en_path = '/root/github/output2.json'

xtuner train /root/ft/config/config1.py --work-dir /root/ft/train_deepspeed --deepspeed deepspeed_zero2

# 模型续训
xtuner train /root/ft/config/internlm2_1_8b_qlora_alpaca_e3_copy.py --work-dir /root/ft/train --resume /root/ft/train/iter_600.pth
```

## 模型推理

## 模型效果
