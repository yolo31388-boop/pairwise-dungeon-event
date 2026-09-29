"""副本随机事件与隐藏房间系统 - 红态测试"""
import pytest, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dungeon.event import EventSystem

class TestEventVariety:
    def test_different_dungeons_trigger_different_events(self):
        es = EventSystem(seed=42)
        e1 = es.trigger_event("fire_dungeon")
        e2 = es.trigger_event("ice_dungeon")
        assert e1 != e2

class TestHiddenRoomHint:
    def test_some_rooms_have_hints(self):
        es = EventSystem()
        assert es.has_hidden_room_hint("cracked_wall") == True

class TestChoiceConsequence:
    def test_different_choices_have_different_consequences(self):
        es = EventSystem()
        c1 = es.get_choice_consequence("fight")
        c2 = es.get_choice_consequence("flee")
        assert c1 != c2

class TestTimeLimit:
    def test_event_has_time_limit(self):
        es = EventSystem()
        limit = es.get_event_time_limit()
        assert limit < float("inf")

class TestSecretRoomCondition:
    def test_secret_room_needs_condition(self):
        es = EventSystem()
        cond = es.get_secret_room_condition()
        assert cond != {}

class TestEventDifficulty:
    def test_high_level_dungeon_harder_events(self):
        es = EventSystem()
        d1 = es.get_event_difficulty(1, 100)
        d2 = es.get_event_difficulty(50, 10000)
        assert d2 > d1

class TestHiddenRoomReward:
    def test_different_room_types_different_rewards(self):
        es = EventSystem()
        r1 = es.get_hidden_room_reward("treasure")
        r2 = es.get_hidden_room_reward("boss")
        assert r1 != r2

class TestSkipPenalty:
    def test_skipping_event_has_penalty(self):
        es = EventSystem()
        penalty = es.get_skip_penalty()
        assert penalty != {}
