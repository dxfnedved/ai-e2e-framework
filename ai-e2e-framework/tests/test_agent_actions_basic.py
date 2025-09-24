import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from ai_actions.agent_page_actions import AgentPageActions

def test_agent_actions_basic():
    """测试AgentPageActions的基本功能"""
    print("AgentPageActions基本功能测试开始")

    # 使用一个真实的URL
    base_url = "https://example.com"

    # 创建AgentPageActions实例
    actions = AgentPageActions(base_url=base_url)

    # 验证actions实例已创建
    assert actions is not None
    print("AgentPageActions实例创建成功")

    # 验证所有方法都存在
    methods_to_check = [
        'enter_any_agent_detail',
        'run_workflow_agent',
        'run_chatflow_agent',
        'view_and_post_comment',
        'submit_bug_feedback',
        'check_text_visible'
    ]

    for method_name in methods_to_check:
        assert hasattr(actions, method_name), f"方法 {method_name} 不存在"
        print(f"方法 {method_name} 存在")

    print("AgentPageActions基本功能测试完成")

if __name__ == "__main__":
    test_agent_actions_basic()