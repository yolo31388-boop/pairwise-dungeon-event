"""副本随机事件与隐藏房间系统 - 含8个bug"""
import random
from dataclasses import dataclass, field

class EventSystem:
    def __init__(self, seed=42):
        self.rng = random.Random(seed)
        self.events: list = ["treasure", "trap", "merchant"]  # bug1: 固定事件
        self.hidden_room_hint: bool = False  # bug2: 无提示

    def trigger_event(self, dungeon_type: str) -> str:
        # bug1: 固定触发
        return "treasure"

    def has_hidden_room_hint(self, room_id: str) -> bool:
        # bug2: 无提示
        return False

    def get_choice_consequence(self, choice: str) -> dict:
        # bug3: 无后果
        return {"reward": 100}

    def get_event_time_limit(self) -> float:
        # bug4: 无时间限制
        return float("inf")

    def get_secret_room_condition(self) -> dict:
        # bug5: 无条件
        return {}

    def get_event_difficulty(self, dungeon_level: int, player_gs: int) -> int:
        # bug6: 无难度区分
        return 1

    def get_hidden_room_reward(self, room_type: str) -> dict:
        # bug7: 固定奖励
        return {"gold": 1000}

    def get_skip_penalty(self) -> dict:
        # bug8: 无惩罚
        return {}
