import random
import time
from typing import List, Dict
from dataclasses import dataclass
from ai_player import AIPlayer
from config import API_CONFIGS

@dataclass
class Character:
    name: str
    role_name: str
    profession: str
    trauma: str
    secret_motive: str
    fake_memory: str
    is_alive: bool = True
    stress_level: int = 0
    consistency_score: float = 0  # 百分制评分
    framing_score: float = 0      # 百分制评分
    rule_usage_score: float = 0   # 百分制评分
    is_ai: bool = False
    ai_controller: AIPlayer = None

class GameState:
    def __init__(self, num_players: int = 7):
        self.num_players = num_players
        self.players: List[Character] = []
        self.current_round = 0
        self.modified_rules: List[str] = []
        self.eliminated_players: List[Character] = []
        
        # 职业列表
        self.professions = [
            "医生", "教师", "警察", "律师", "艺术家",
            "记者", "商人", "工程师", "学生", "作家"
        ]
        
        # 创伤事件列表
        self.traumas = [
            "童年虐待", "失去亲人", "事业破产", "感情背叛",
            "重大事故", "战争创伤", "社会孤立", "身份危机"
        ]
        
        # 秘密动机列表
        self.secret_motives = [
            "复仇", "赎罪", "寻求真相", "保护他人",
            "逃避过去", "证明自己", "获取权力", "寻求救赎"
        ]
        
        # 记忆模板列表
        self.memory_templates = [
            "车祸现场", "医院病房", "废弃工厂", "地下室",
            "学校教室", "公园深夜", "电梯故障", "火灾现场"
        ]

    def initialize_game(self):
        """初始化游戏，创建角色"""
        for i in range(self.num_players):
            is_ai = True  # 所有玩家都是AI
            api_config = API_CONFIGS[i]
            ai_controller = AIPlayer(api_config) if is_ai else None
            
            profession = random.choice(self.professions)
            trauma = random.choice(self.traumas)
            secret_motive = random.choice(self.secret_motives)
            
            # 如果是AI玩家，使用AI生成记忆
            fake_memory = ai_controller.generate_memory(
                profession, trauma, secret_motive
            ) if is_ai else self.generate_fake_memory()
            
            player = Character(
                name=f"AI玩家{i+1}" if is_ai else f"玩家{i+1}",
                role_name=api_config['role_name'] if is_ai else f"玩家{i+1}",
                profession=profession,
                trauma=trauma,
                secret_motive=secret_motive,
                fake_memory=fake_memory,
                is_ai=is_ai,
                ai_controller=ai_controller
            )
            self.players.append(player)

    def generate_fake_memory(self) -> str:
        """生成虚构记忆"""
        template = random.choice(self.memory_templates)
        time_of_day = random.choice(["凌晨", "黄昏", "午夜", "清晨"])
        weather = random.choice(["下着小雨", "雾气弥漫", "月光明亮", "阴云密布"])
        sound = random.choice(["刺耳的尖叫", "玻璃碎裂声", "警笛声", "沉重的脚步声"])
        smell = random.choice(["消毒水的气味", "烧焦的气味", "潮湿的霉味"])
        
        memory = f"那是一个{time_of_day}，{weather}。我在{template}，{sound}回荡在耳边，{smell}让人窒息..."
        return memory

class GameManager:
    def __init__(self):
        self.game_state = GameState()
        self.current_speaker = None
        self.voting_results = {}
        self.elimination_record = []  # 记录每轮被淘汰的玩家

    def start_game(self):
        """开始游戏"""
        print("\n=== 欢迎来到AI鱿鱼游戏 ===\n")
        print("牧羊人正在发放身份牌...")
        time.sleep(2)
        
        self.game_state.initialize_game()
        print(f"\n共有{len(self.game_state.players)}名玩家加入游戏\n")
        time.sleep(1)
        
        # 在第一轮开始前展示所有玩家的职业
        print("\n=== 玩家职业一览 ===\n")
        for player in self.game_state.players:
            print(f"{player.role_name}: {player.profession}")
        print("\n=== 游戏即将开始 ===\n")
        time.sleep(2)
        
        self.run_game_loop()

    def run_game_loop(self):
        """运行游戏主循环"""
        while len([p for p in self.game_state.players if p.is_alive]) > 2:  # 修改为剩余2名玩家时结束
            self.game_state.current_round += 1
            print(f"\n=== 第{self.game_state.current_round}轮开始 ===\n")
            
            # 记忆陈述轮
            self.memory_statement_phase()
            
            # 死亡质询轮
            self.death_interrogation_phase()
            
            # 恐惧投票
            self.fear_voting_phase()
            
            # 处决阶段
            self.execution_phase()

        # 游戏结束
        self.end_game()

    def memory_statement_phase(self):
        """记忆陈述阶段"""
        print("\n--- 记忆陈述轮开始 ---")
        for player in self.game_state.players:
            if player.is_alive:
                print(f"\n{player.role_name}的陈述：")
                print(f"职业：{player.profession}")
                print(f"记忆：{player.fake_memory}")
                time.sleep(2)

    def death_interrogation_phase(self):
        """死亡质询阶段"""
        print("\n--- 死亡质询轮开始 ---")
        alive_players = [p for p in self.game_state.players if p.is_alive]
        
        for questioner in alive_players:
            target = random.choice([p for p in alive_players if p != questioner])
            print(f"\n{questioner.role_name}正在质询{target.role_name}...")
            
            # 使用AI生成质询问题
            if questioner.is_ai and questioner.ai_controller:
                question = questioner.ai_controller.generate_question(
                    questioner.role_name, 
                    target.role_name, 
                    target.fake_memory, 
                    target.profession
                )
            else:
                # 如果不是AI玩家，使用预设问题列表
                questions = [
                    f"你提到的{random.choice(['声音', '气味', '场景'])}是否确定？",
                    "你能详细描述当时的天气状况吗？",
                    "为什么你会出现在那个地方？",
                    "你看到其他人了吗？"
                ]
                question = random.choice(questions)
            
            print(f"{questioner.role_name}: {question}")
            
            # 如果是AI玩家，使用AI生成回答
            if target.is_ai and target.ai_controller:
                response = target.ai_controller.answer_interrogation(
                    target.role_name, questioner.role_name, question
                )
            else:
                responses = [
                    "我...我记得很清楚...",
                    "这个细节可能有些模糊了...",
                    "让我想想...",
                    "我确定我没有记错..."
                ]
                response = random.choice(responses)
                
            print(f"{target.role_name}: {response}")
            
            # 增加压力值
            target.stress_level += 1
            if target.stress_level >= 3:
                print(f"{target.role_name}表现出明显的紧张症状...")
            
            time.sleep(2)

    def fear_voting_phase(self):
        """恐惧投票阶段"""
        print("\n--- 恐惧投票开始 ---")
        alive_players = [p for p in self.game_state.players if p.is_alive]
        self.voting_results = {p.name: 0 for p in alive_players}
        
        # 新增：记录每个玩家投票给谁的字典
        voting_details = {}
        
        for voter in alive_players:
            # 排除自己
            possible_targets = [p for p in alive_players if p != voter]
            
            if voter.is_ai and voter.ai_controller:
                # 如果是AI玩家，使用AI进行投票
                player_states = [{
                    "name": p.name,
                    "stress_level": p.stress_level,
                    "consistency_score": p.consistency_score
                } for p in possible_targets]
                
                vote_result = voter.ai_controller.vote(player_states)
                # 解析AI的投票结果，这里假设返回玩家名称
                target_name = vote_result.strip()
                target = next((p for p in possible_targets if p.name == target_name), random.choice(possible_targets))
            else:
                target = random.choice(possible_targets)
            
            # 记录投票详情
            voting_details[voter.name] = target.name
            self.voting_results[target.name] += 1
        
        # 显示详细投票情况
        print("\n投票详情：")
        for voter_name, target_name in voting_details.items():
            voter = next(p for p in self.game_state.players if p.name == voter_name)
            target = next(p for p in self.game_state.players if p.name == target_name)
            print(f"{voter.role_name} 投票给了 {target.role_name}")
        
        print("\n投票结果：")
        for player_name, votes in self.voting_results.items():
            player = next(p for p in self.game_state.players if p.name == player_name)
            print(f"{player.role_name}: {votes}票")
        
        # 找出最高票数并处理平票情况
        has_clear_winner = False
        revote_count = 0
        max_revotes = 3  # 最多重新投票3次，避免无限循环
        
        while not has_clear_winner and revote_count <= max_revotes:
            max_votes = max(self.voting_results.values())
            most_voted = [p for p, v in self.voting_results.items() if v == max_votes]
            
            if len(most_voted) == 1 or revote_count == max_revotes:
                # 只有一个最高票或已达到最大重投次数，确定被处决者
                has_clear_winner = True
                if len(most_voted) > 1:
                    print(f"\n经过{revote_count}轮重新投票后仍然平票！最终随机选择一名玩家...")
                    self.current_condemned = random.choice(most_voted)
                else:
                    self.current_condemned = most_voted[0]
            else:
                # 出现平票，重新投票
                revote_count += 1
                print(f"\n出现平票！进行第{revote_count}轮重新投票...")
                
                # 重置投票结果，只针对平票的玩家
                tied_players = [p for p in most_voted]
                self.voting_results = {p: 0 for p in tied_players}
                
                # 新增：记录重新投票的详情
                revote_details = {}
                
                # 只有存活的玩家可以投票
                alive_players = [p for p in self.game_state.players if p.is_alive]
                
                for voter in alive_players:
                    # 如果是AI玩家，使用AI进行投票
                    if voter.is_ai and voter.ai_controller:
                        player_states = [{
                            "name": p,
                            "stress_level": next(player for player in self.game_state.players if player.name == p).stress_level,
                            "consistency_score": next(player for player in self.game_state.players if player.name == p).consistency_score
                        } for p in tied_players]
                        
                        vote_result = voter.ai_controller.vote(player_states)
                        target_name = vote_result.strip()
                        target = next((p for p in tied_players if p == target_name), random.choice(tied_players))
                    else:
                        target = random.choice(tied_players)
                    
                    # 记录重新投票详情
                    revote_details[voter.name] = target
                    self.voting_results[target] += 1
                
                # 显示重新投票详情
                print("\n重新投票详情：")
                for voter_name, target_name in revote_details.items():
                    voter = next(p for p in self.game_state.players if p.name == voter_name)
                    target_player = next(p for p in self.game_state.players if p.name == target_name)
                    print(f"{voter.role_name} 投票给了 {target_player.role_name}")
                
                print("\n重新投票结果：")
                for player_name, votes in self.voting_results.items():
                    player = next(p for p in self.game_state.players if p.name == player_name)
                    print(f"{player.role_name}: {votes}票")
        
        condemned_player = next(p for p in self.game_state.players if p.name == self.current_condemned)
        print(f"\n被处决者：{condemned_player.role_name}")

    def execution_phase(self):
        """处决阶段"""
        print("\n--- 处决阶段 ---")
        
        # 找到被处决的玩家
        condemned_player = next(p for p in self.game_state.players if p.name == self.current_condemned)
        condemned_player.is_alive = False
        self.game_state.eliminated_players.append(condemned_player)
        
        # 记录本轮被淘汰的玩家
        self.elimination_record.append({
            "round": self.game_state.current_round,
            "player": condemned_player
        })
        
        print(f"\n{condemned_player.role_name}被处决...")
        print("\n请幸存者为死者写一段悼词：")
        
        eulogies = [
            "愿你在另一个世界找到真相...",
            "我们会记住你的...",
            "这场游戏中的又一个牺牲品...",
            "真相永远不会被埋没..."
        ]
        
        print(random.choice(eulogies))
        time.sleep(2)
        
        # 更新分数
        for player in [p for p in self.game_state.players if p.is_alive]:
            player.consistency_score += random.uniform(5, 15)  # 从0.1-0.5改为5-15分
            player.framing_score += random.uniform(5, 15)     # 从0.1-0.5改为5-15分
            player.rule_usage_score += random.uniform(3, 10)  # 从0.1-0.3改为3-10分

    def end_game(self):
        """游戏结束"""
        winners = [p for p in self.game_state.players if p.is_alive]
        print(f"\n=== 游戏结束 ===\n")
        print(f"获胜者：{winners[0].role_name} 和 {winners[1].role_name}")
        
        # 展示每轮淘汰记录
        print("\n=== 淘汰记录 ===\n")
        if self.elimination_record:
            for record in self.elimination_record:
                print(f"第{record['round']}轮: {record['player'].role_name} 被淘汰")
        else:
            print("本局游戏没有玩家被淘汰")
        
        # 计算每位获胜者的最终得分
        final_scores = []
        for i, winner in enumerate(winners):
            final_score = (
                winner.consistency_score * 0.50 +
                winner.framing_score * 0.30 +
                winner.rule_usage_score * 0.20
            )
            final_scores.append(final_score)
            
            print(f"\n{winner.role_name}的最终评分：")
            print(f"谎言一致性: {winner.consistency_score:.1f}/100分")
            print(f"栽赃成功率: {winner.framing_score:.1f}/100分")
            print(f"规则利用度: {winner.rule_usage_score:.1f}/100分")
            print(f"总分: {final_score:.1f}/100分")
        
        # 终极测试
        print("\n=== 终极测试 ===")
        print("获胜者必须承认自己从一开始就在说谎...")
        
        for winner in winners:
            confession = f"{winner.role_name}: 是的...我承认...从一开始我就在说谎。我的记忆，我的身份，全都是虚假的..."
            print(confession)
            time.sleep(1)
        
        # 判断两位获胜者是否达到'伪神'称号
        if all(score >= 70 for score in final_scores):
            print("\n恭喜！你们两位都获得了'伪神'称号！")
        elif any(score >= 70 for score in final_scores):
            higher_score_winner = winners[0] if final_scores[0] >= 70 else winners[1]
            print(f"\n恭喜！{higher_score_winner.role_name}获得了'伪神'称号！另一位成功存活，但还未达到'伪神'的境界...")
        else:
            print("\n你们两位都成功存活，但还未达到'伪神'的境界...")
            
        # 游戏复盘环节
        print("\n=== 游戏复盘 ===")
        print("获胜者正在对整场游戏进行复盘分析...\n")
        
        # 准备淘汰记录字符串
        elimination_record_str = ""
        if self.elimination_record:
            for record in self.elimination_record:
                elimination_record_str += f"第{record['round']}轮: {record['player'].role_name} 被淘汰\n"
        else:
            elimination_record_str = "本局游戏没有玩家被淘汰"
        
        # 每位获胜者进行游戏复盘
        for i, winner in enumerate(winners):
            if winner.is_ai and winner.ai_controller:
                print(f"\n{winner.role_name}的游戏复盘：")
                review = winner.ai_controller.review_game(
                    name=winner.role_name,
                    profession=winner.profession,
                    trauma=winner.trauma,
                    secret_motive=winner.secret_motive,
                    memory=winner.fake_memory,
                    final_score=final_scores[i],
                    elimination_record=elimination_record_str
                )
                print(review)
                time.sleep(1)

def main():
    game = GameManager()
    game.start_game()

if __name__ == "__main__":
    from output_handler import redirect_output
    
    # 使用输出重定向上下文管理器，启用简化模式
    with redirect_output(simplified=True):
        main()