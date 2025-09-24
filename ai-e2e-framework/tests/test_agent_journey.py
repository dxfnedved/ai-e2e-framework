import pytest
import configparser
import os
from ai_actions.agent_page_actions import AgentPageActions

# 从配置文件读取URL
config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), '..', 'config.ini'))

BASE_URL = config.get('Environment', 'base_url')
WORKFLOW_AGENT_URL = config.get('Environment', 'workflow_agent_url')
CHATFLOW_AGENT_URL = config.get('Environment', 'chatflow_agent_url')

@pytest.fixture(scope="module")
def actions():
    """初始化AgentPageActions实例"""
    # 确保浏览器已安装
    # 在命令行先运行一次: playwright install
    return AgentPageActions(base_url=BASE_URL)

@pytest.mark.p0
def test_main_user_journey(actions: AgentPageActions):
    # --- 测试点: 进入Agent详情页 ---
    actions.enter_any_agent_detail()
    # 简单的页面跳转后，我们可以在Python端用Playwright验证URL，或让AI验证
    # 此处让AI验证，以保持一致性
    actions.check_text_visible(CHATFLOW_AGENT_URL, "check_detail_page_loaded", "运行")

    # --- 测试点: 发表评论 ---
    actions.view_and_post_comment(CHATFLOW_AGENT_URL, "This AI agent is fantastic!")
    actions.check_text_visible(CHATFLOW_AGENT_URL, "check_comment_posted", "This AI agent is fantastic!")

    # --- 测试点: 提交反馈 ---
    actions.submit_bug_feedback(CHATFLOW_AGENT_URL, "Found a minor display issue.")
    actions.check_text_visible(CHATFLOW_AGENT_URL, "check_feedback_submitted", "感谢您的反馈")

    # --- 测试点: 运行 Workflow型 Agent ---
    actions.run_workflow_agent(WORKFLOW_AGENT_URL)
    actions.check_text_visible(WORKFLOW_AGENT_URL, "check_workflow_success", "执行成功")

    # --- 测试点: 运行 Chatflow型 Agent ---
    actions.run_chatflow_agent(CHATFLOW_AGENT_URL, "Please summarize today's news.")
    actions.check_text_visible(CHATFLOW_AGENT_URL, "check_chatflow_history", "Please summarize today's news.")

@pytest.mark.p1
def test_info_and_help_tabs(actions: AgentPageActions):
    # 此处可以导航到一个详情页开始测试
    # 为简化，假设我们已在详情页
    actions.execute_ai_instruction(CHATFLOW_AGENT_URL, "view_info_tab", "Click on the '信息' tab")
    actions.check_text_visible(CHATFLOW_AGENT_URL, "check_info_visible", "应用简介")

    actions.execute_ai_instruction(CHATFLOW_AGENT_URL, "view_help_tab", "Click on the '帮助' tab")
    actions.check_text_visible(CHATFLOW_AGENT_URL, "check_help_visible", "使用指南")