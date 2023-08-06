import json
import uuid
import re

from .__agent__ import Agent
from .__stage__ import Stage, __USER_TEXT__, __SYS_REPLY__, StageStatus, SwitchStage, \
    __LOCAL_VAR_LABEL__, __LOCAL_VAR_VALUE__

__MOCK_STAGES_LABEL_1__ = "__MOCK_STAGES_LABEL_1__"


def mock_client_with_test(agent, says, tests):
    data = {}
    for s, t in zip(says, tests):
        data[__USER_TEXT__] = s
        reply_text, data = agent.run_all_stages(**data)
        assert t == reply_text


def mock_client(agent, says, show_data=True, show_user_text=True):
    data = {}
    for s in says:
        data[__USER_TEXT__] = s
        reply_text, data = agent.run_all_stages(**data)
        if show_user_text:
            print("\t用戶:", s)
        print("系統:", reply_text)
        if show_data:
            print("\t系統資料:", data)


def mock_client_human(agent):
    data = {}
    while True:
        s = input("請輸入：")
        data[__USER_TEXT__] = s
        if s == "exit":
            break
        reply_text, data = agent.run_all_stages(**data)
        print("系統:", reply_text)


def mock_client_once(agent: Agent, text: str, data: dict):
    data[__USER_TEXT__] = text
    return agent.run_all_stages(**data)


def to_bot(agent: Agent, text: str, data: dict):
    return mock_client_once(agent, text, data)


stage1 = Stage()
stage1.sys_reply_q1 = "s1_q1"
stage1.sys_reply_complete = "s1_complete"
stage2 = Stage()
stage2.sys_reply_q1 = "s2_q1"
stage2.sys_reply_complete = "s2_complete"
mock_client_with_test(Agent([stage1, stage2]), ["hi1", "hi2", "hi3"],
                      [
                          ['s1_q1'],
                          ['s1_complete', 's2_q1'],
                          ['s2_complete']
                      ])

# switch_stage = SwitchStage()
# mock_client_with_test(MultiAgent({
#     MultiAgent.__MAIN_STAGES__: [stage1, stage2, switch_stage],
#     "test": [stage1, stage2],
#     }),
#     ["hi1", "hi2", "hi3", "hi4", "hi5"],
#   [
#       ['s1_q1'],
#       ['s1_complete', 's2_q1'],
#       ['s2_complete', 'thanks for using.'],
#       ['thanks for using.'],
#       ['thanks for using.']
#   ])

stage3 = Stage()
stage3.sys_reply_q1 = "s3_q1"
stage3.sys_reply_complete = "s3_complete"
stage4 = Stage()
stage4.sys_reply_q1 = "s4_q1"
stage4.sys_reply_complete = "s4_complete"
switch_stage = SwitchStage(stages_filter=[
    (__LOCAL_VAR_LABEL__, __LOCAL_VAR_VALUE__, __MOCK_STAGES_LABEL_1__),
])
# mock_client_human(MultiAgent({
#     MultiAgent.__MAIN_STAGES__: [stage1, stage2, switch_stage],
#     __MOCK_SATGES_LABEL_1__: [stage3, stage4],
#     }))
