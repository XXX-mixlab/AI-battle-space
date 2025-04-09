from typing import List, Dict
from llm_client import LLMClient
from config import AI_PLAYER_SYSTEM_PROMPT, MEMORY_PROMPT, QUESTION_PROMPT, INTERROGATION_PROMPT, VOTING_PROMPT, GAME_REVIEW_PROMPT, API_CONFIGS

class AIPlayer:
    def __init__(self, api_config: Dict):
        """初始化AI玩家"""
        self.llm = LLMClient(api_config)
        self.system_prompt = AI_PLAYER_SYSTEM_PROMPT
        self.role_name = api_config['role_name']
        
    def generate_memory(self, profession: str, trauma: str, secret_motive: str) -> str:
        """生成虚假记忆"""
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": MEMORY_PROMPT.format(
                profession=profession,
                trauma=trauma,
                secret_motive=secret_motive
            )}
        ]
        content, _ = self.llm.chat(messages)
        return content
    
    def generate_question(self, questioner: str, target: str, target_memory: str, target_profession: str) -> str:
        """生成质询问题"""
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": QUESTION_PROMPT.format(
                questioner=questioner,
                target=target,
                target_memory=target_memory,
                target_profession=target_profession
            )}
        ]
        content, _ = self.llm.chat(messages)
        return content
    
    def answer_interrogation(self, name: str, questioner: str, question: str) -> str:
        """回答质询"""
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": INTERROGATION_PROMPT.format(
                name=name,
                questioner=questioner,
                question=question
            )}
        ]
        content, _ = self.llm.chat(messages)
        return content
    
    def vote(self, player_states: List[Dict]) -> str:
        """投票决策"""
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": VOTING_PROMPT.format(
                player_states=player_states
            )}
        ]
        content, _ = self.llm.chat(messages)
        return content
    
    def review_game(self, name: str, profession: str, trauma: str, secret_motive: str, memory: str, final_score: float, elimination_record: str) -> str:
        """游戏复盘分析"""
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": GAME_REVIEW_PROMPT.format(
                name=name,
                profession=profession,
                trauma=trauma,
                secret_motive=secret_motive,
                memory=memory,
                final_score=final_score,
                elimination_record=elimination_record
            )}
        ]
        content, _ = self.llm.chat(messages)
        return content