from ai_actions.base_executor import BaseExecutor

class AgentPageActions(BaseExecutor):
    def __init__(self, base_url: str):
        self.base_url = base_url

    # 每个方法都调用 execute_ai_instruction，并传入独特的 cache_id

    def enter_any_agent_detail(self):
        self.execute_ai_instruction(
            self.base_url,
            "enter_agent_detail",
            "Locate any Agent card visible on the current page and click on it to navigate to the agent details page. If multiple agent cards are present, select the first one."
        )

    def run_workflow_agent(self, agent_url: str):
        # 注意: 文件上传依然是AI难以处理的，我们让AI点击按钮，再用Playwright(Python)精确上传
        # （这是一个高级混合模式，此处为简化，我们假设AI可以描述整个流程）
        self.execute_ai_instruction(
            agent_url,
            "run_workflow_excel",
            "Find and click the file upload button on the page. Then, locate and select the Excel file at 'test_data/sample_excel.xlsx'. After the file is selected, identify any required parameter input fields and fill them with appropriate test values. Finally, locate and click the '执行' (Execute) button to run the workflow."
        )

    def run_chatflow_agent(self, agent_url: str, message: str):
        self.execute_ai_instruction(
            agent_url,
            "run_chatflow_agent",
            f"Locate the chat input text area on the page. Type the message '{message}' into this chat input field. Then, find and click the send button (usually an arrow or paper plane icon) to submit the message."
        )

    def view_and_post_comment(self, agent_url: str, comment: str):
        self.execute_ai_instruction(
            agent_url,
            "view_and_post_comment",
            f"First, find and click on the '评论' (Comments) tab to switch to the comments section. Then, locate the comment input text area and type '{comment}' into it. Next, find the star rating control and select the 5-star rating option. Finally, locate and click the '发送' (Send) button to submit the comment."
        )

    def submit_bug_feedback(self, agent_url: str, content: str):
        self.execute_ai_instruction(
            agent_url,
            "submit_bug_feedback",
            f"First, find and click on the '反馈' (Feedback) tab to switch to the feedback section. Then, locate the feedback type selection control and choose the 'BUG' option. Next, find the main content text area and type '{content}' into it. Finally, locate and click the '发送' (Send) button to submit the feedback."
        )

    def check_text_visible(self, url: str, cache_id: str, text: str):
        self.execute_ai_instruction(
            url,
            cache_id,
            f"Verify that the text '{text}' is visible on the current page. Scan the entire page content including all sections, tabs, and scrollable areas to confirm the presence of this text."
        )