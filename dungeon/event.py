"""副本随机事件与隐藏房间系统"""
import random
from dataclasses import dataclass, field


class EventSystem:
    # 每种副本类型有独立的事件池，保证不同副本触发不同事件
    EVENT_POOLS = {
        "fire_dungeon": ["lava_eruption", "fire_elemental", "burning_chest"],
        "ice_dungeon": ["frost_trap", "ice_wraith", "frozen_cache"],
    }
    DEFAULT_POOL = ["treasure", "trap", "merchant", "ambush", "shrine"]

    # 隐晦的隐藏房间入口提示
    HIDDEN_ROOM_HINTS = {
        "cracked_wall": "crack",
        "loose_brick": "hidden_door",
        "mysterious_npc": "special_npc",
    }

    # 事件选择的不同后果
    CHOICE_CONSEQUENCES = {
        "fight": {"reward": 100, "hp_cost": 20, "branch": "combat"},
        "flee": {"reward": 0, "hp_cost": 0, "branch": "escape"},
        "negotiate": {"reward": 50, "hp_cost": 0, "branch": "dialogue"},
    }

    EVENT_TIME_LIMIT = 30.0  # 秒，超时自动选择默认选项

    # 秘密通道触发条件
    SECRET_ROOM_CONDITION = {
        "required_item": "lockpick",
        "required_skill": "detect_secret",
        "min_perception": 15,
    }

    # 隐藏房间奖励按房间类型区分
    HIDDEN_ROOM_REWARDS = {
        "treasure": {"gold": 1000, "gems": 5},
        "boss": {"gold": 3000, "epic_item": 1},
        "shrine": {"blessing": 1, "exp": 500},
    }

    # 跳过事件的惩罚
    SKIP_PENALTY = {"lose_reward": True, "negative_event": "ambush", "exp_loss": 50}

    def __init__(self, seed=42):
        self.rng = random.Random(seed)
        self.events: list = list(self.DEFAULT_POOL)
        self.hidden_room_hint: bool = True

    def trigger_event(self, dungeon_type: str) -> str:
        pool = self.EVENT_POOLS.get(dungeon_type, self.DEFAULT_POOL)
        return self.rng.choice(pool)

    def has_hidden_room_hint(self, room_id: str) -> bool:
        return room_id in self.HIDDEN_ROOM_HINTS

    def get_choice_consequence(self, choice: str) -> dict:
        return dict(self.CHOICE_CONSEQUENCES.get(choice, {"reward": 0, "branch": "none"}))

    def get_event_time_limit(self) -> float:
        return self.EVENT_TIME_LIMIT

    def get_secret_room_condition(self) -> dict:
        return dict(self.SECRET_ROOM_CONDITION)

    def get_event_difficulty(self, dungeon_level: int, player_gs: int) -> int:
        return max(1, dungeon_level + player_gs // 1000)

    def get_hidden_room_reward(self, room_type: str) -> dict:
        return dict(self.HIDDEN_ROOM_REWARDS.get(room_type, {"gold": 100}))

    def get_skip_penalty(self) -> dict:
        return dict(self.SKIP_PENALTY)
