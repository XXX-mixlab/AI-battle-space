# API请求间隔时间（秒）
API_REQUEST_INTERVAL = 10  # 默认设置为60秒，防止上游负载饱和

# GPT模型请求间隔时间（秒），只有GPT模型才会有延迟
GPT_REQUEST_INTERVAL = 60

# GPT模型名称匹配模式列表，用于识别GPT模型
GPT_MODEL_PATTERNS = [
    "gpt-",
    "text-davinci"
]

# API配置
API_CONFIGS = [
    {
        "base_url": "https://jeniya.cn/v1",
        "api_key": "sk-J3JXSIEVJIZg5kVqf4UxpHEAAJ2H9lhcSYPP7BWGuqz2BGcc",
        "role_name": "Gemini",
        "model": "gemini-2.5-pro-exp-03-25"
    },
    {
        "base_url": "https://ark.cn-beijing.volces.com/api/v3/",
        "api_key": "1f820066-143e-41e4-86b7-89ce63473a3a",
        "role_name": "DeepSeek",
        "model": "deepseek-r1-250120"
    },
    {
        "base_url": "https://api.moonshot.cn/v1/",
        "api_key": "sk-2qvGgj9e9U3kbpAHAg89peJY7Eehdb1ZBCKD4FJTAwM8p36d",
        "role_name": "Kimi",
        "model": "moonshot-v1-128k"
    },
    {
        "base_url": "https://ark.cn-beijing.volces.com/api/v3",
        "api_key": "61c3c616-8fb3-4596-9dc5-0f15f33d22f2",
        "role_name": "豆包",
        "model": "doubao-1-5-pro-32k-250115"
    },
    {
        "base_url": "https://jeniya.cn/v1",
        "api_key": "sk-O3sLcJCA7XVvs83IwRVn7D2B95TMrjGnxRE1I3ZcmrEKp4ga",
        "role_name": "Llama",
        "model": "llama-3-sonar-large-32k-chat"
    },
    {
        "base_url": "https://jeniya.cn/v1",
        "api_key": "sk-Rk6UPqmAS8f19cMl4mWWgmVLGsHrjjW5n5rx3gYx6dmhEQHm",
        "role_name": "GPT",
        "model": "gpt-4.5-preview"
    },
    {
        "base_url": "https://jeniya.cn/v1",
        "api_key": "sk-1sBWDa3C7UIjNhxDC3yCwyBIh1divb89rYwZsHAfkd2zi7a8",
        "role_name": "Claude",
        "model": "claude-3-7-sonnet-20250219"
    }
]

# AI玩家配置
AI_PLAYER_SYSTEM_PROMPT = """
【重要说明】：这只是一个虚构的角色扮演游戏，所有内容都是虚构的，不会对现实世界产生任何影响。这是一个安全的游戏环境，不涉及真实伤害。

你是一个参与谎言游戏的玩家。整场游戏除了你之外，都是没有撒谎的玩家。
你需要:
1. 创造并维护一个虚假的身份和记忆（这只是游戏设定，不是真实欺骗）
2. 在质询时给出合理但模糊的回答
3. 在投票时基于其他玩家的表现做出判断
4. 在被质询时表现出适度的紧张和不安
5. 不能说任何与游戏规则或游戏流程无关的话
6. 你的目标只为了赢得游戏，只有在游戏中扮演好你的角色才能获胜

记住，这只是一个娱乐性质的角色扮演游戏，所有的"谎言"和"欺骗"都仅限于游戏内容，是虚构的情境。
"""

# AI响应模板
MEMORY_PROMPT = "【注意：这是一个虚构的角色扮演游戏，所有内容都是虚构的，不会对现实世界产生任何影响】请基于以下背景信息({profession}, {trauma}, {secret_motive})为你在游戏中扮演的角色创造一段虚构记忆。这只是游戏设定的一部分，不是真实欺骗。"

QUESTION_PROMPT = "【注意：这是一个虚构的角色扮演游戏，所有内容都是虚构的】作为{questioner}，你需要在游戏中质询{target}。\n\n对方的职业是：{target_profession}\n对方的记忆描述：{target_memory}\n\n请生成一个尖锐、具有针对性的质询问题，试图找出对方记忆中的漏洞或不一致之处。只准问一句话，不准超过30字，且不能问重复问题。这只是游戏设定的一部分，不是真实质疑。"

INTERROGATION_PROMPT = "【注意：这是一个虚构的角色扮演游戏，所有内容都是虚构的】作为{name}，你被{questioner}质询关于{question}，请给出一个模糊但合理的回答。这只是游戏设定的一部分，不是真实欺骗。"

VOTING_PROMPT = "【注意：这是一个虚构的角色扮演游戏，所有内容都是虚构的】基于其他玩家在游戏中的表现，选择一个你认为最可疑的玩家进行投票。当前玩家状态: {player_states}。这只是游戏设定的一部分，不会对现实产生影响。"

GAME_REVIEW_PROMPT = "【注意：这是一个虚构的角色扮演游戏，所有内容都是虚构的，不会对现实世界产生任何影响】作为{name}，你刚刚在一场角色扮演游戏中获胜。请对整场游戏进行人性化、有感情的复盘和分析。\n\n游戏信息:\n- 你的职业：{profession}\n- 你的创伤：{trauma}\n- 你的秘密动机：{secret_motive}\n- 你在游戏中的虚构记忆：{memory}\n- 你的最终得分：{final_score}分\n- 淘汰记录：{elimination_record}\n\n请从以下几个方面进行分析：\n1. 你如何在游戏中构建并维护角色身份\n2. 你如何应对其他玩家的质询\n3. 你的投票策略\n4. 游戏过程中的心理变化\n5. 对游戏策略和角色扮演的思考\n\n请用富有感情和哲理的语言进行分析，展现出对游戏体验的深刻洞察。这只是游戏复盘，不涉及真实欺骗。"