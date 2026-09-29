"""副本随机事件与隐藏房间系统"""
import random
import time
from dataclasses import dataclass, field

# 每种副本类型有独立的事件池和触发概率，保证不同副本触发不同事件
EVENT_POOLS = {
    "fire_dungeon": [
        ("flame_trap", 0.4),
        ("lava_treasure", 0.35),
        ("ember_merchant", 0.25),
    ],
    "ice_dungeon": [
        ("frost_trap", 0.4),
        ("frozen_treasure", 0.35),
        ("ice_merchant", 0.25),
    ],
}
DEFAULT_POOL = [
    ("treasure", 0.34),
    ("trap", 0.33),
    ("merchant", 0.33),
]

# 隐藏房间的隐晦入口提示：裂缝 / 暗门 / 特殊NPC
HIDDEN_ROOM_HINTS = {
    "cracked_wall": "墙面上有一道细微的裂缝，似乎透着微风。",
    "hidden_door": "火把的光影在墙上投出一道不自然的门缝轮廓。",
    "mysterious_npc": "一位行踪诡秘的旅人欲言又止，似乎知道某条密道。",
}

# 事件选择的不同后果：奖励 / 惩罚 / 剧情分支
CHOICE_CONSEQUENCES = {
    "fight": {"reward": 200, "hp_loss": 30, "branch": "combat"},
    "flee": {"reward": 0, "hp_loss": 0, "branch": "escape"},
    "negotiate": {"reward": 100, "hp_loss": 0, "branch": "dialogue"},
    "default": {"reward": 0, "hp_loss": 10, "branch": "timeout"},
}

# 秘密通道触发条件：道具 / 技能 / 属性
SECRET_ROOM_CONDITION = {
    "required_item": "ancient_key",
    "required_skill": "detect_secret",
    "min_perception": 15,
}

# 隐藏房间奖励按房间类型区分
HIDDEN_ROOM_REWARDS = {
    "treasure": {"gold": 1000, "gems": 5},
    "boss": {"gold": 3000, "epic_item": "boss_trophy"},
    "shrine": {"buff": "blessing", "exp": 500},
}

BASE_TIME_LIMIT = 30.0  # 事件倒计时（秒），超时自动选择默认选项


class EventSystem:
    def __init__(self, seed=42):
        self.rng = random.Random(seed)
        self.events: list = ["treasure", "trap", "merchant"]
        self.hidden_room_hint: bool = True

    def _weighted_choice(self, pool) -> str:
        roll = self.rng.random()
        cumulative = 0.0
        for name, weight in pool:
            cumulative += weight
            if roll < cumulative:
                return name
        return pool[-1][0]

    def trigger_event(self, dungeon_type: str) -> str:
        # 按副本类型的事件池和概率随机触发，每次进本结果不同
        pool = EVENT_POOLS.get(dungeon_type, DEFAULT_POOL)
        return self._weighted_choice(pool)

    def has_hidden_room_hint(self, room_id: str) -> bool:
        # 有隐晦入口提示的房间返回 True
        return room_id in HIDDEN_ROOM_HINTS

    def get_hint_text(self, room_id: str) -> str:
        return HIDDEN_ROOM_HINTS.get(room_id, "")

    def get_choice_consequence(self, choice: str) -> dict:
        # 不同选择有不同后果（奖励/惩罚/剧情分支）
        return dict(CHOICE_CONSEQUENCES.get(choice, CHOICE_CONSEQUENCES["default"]))

    def get_event_time_limit(self) -> float:
        # 事件有倒计时限制
        return BASE_TIME_LIMIT

    def resolve_choice(self, choice: str, elapsed: float) -> dict:
        # 超时自动选择默认选项
        if elapsed > self.get_event_time_limit():
            choice = "default"
        return self.get_choice_consequence(choice)

    def get_secret_room_condition(self) -> dict:
        # 秘密通道需要特定条件（道具/技能/属性）才能触发
        return dict(SECRET_ROOM_CONDITION)

    def can_enter_secret_room(self, items=None, skills=None, attributes=None) -> bool:
        items = items or []
        skills = skills or []
        attributes = attributes or {}
        cond = SECRET_ROOM_CONDITION
        return (
            cond["required_item"] in items
            and cond["required_skill"] in skills
            and attributes.get("perception", 0) >= cond["min_perception"]
        )

    def get_event_difficulty(self, dungeon_level: int, player_gs: int) -> int:
        # 难度按副本等级和玩家装等动态调整
        return max(1, dungeon_level + player_gs // 1000)

    def get_hidden_room_reward(self, room_type: str, difficulty: int = 1) -> dict:
        # 奖励按房间类型和难度区分
        base = HIDDEN_ROOM_REWARDS.get(room_type, {"gold": 100})
        reward = dict(base)
        if "gold" in reward:
            reward["gold"] = reward["gold"] * max(1, difficulty)
        return reward

    def get_skip_penalty(self) -> dict:
        # 跳过事件有惩罚：失去奖励并触发负面事件
        return {"lose_reward": True, "negative_event": "ambush", "hp_loss": 20}
