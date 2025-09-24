# 使用说明

## 1. 环境准备

### 安装Node.js依赖
```bash
cd ts_executor
npm install
```

### 安装Python依赖
```bash
pip install -r requirements.txt
```

### 安装浏览器驱动
```bash
playwright install
```

## 2. 配置AI模型

在 `ts_executor/.env` 文件中配置您的AI模型参数：
```env
# OpenAI配置示例
OPENAI_API_KEY="sk-..."
OPENAI_BASE_URL="https://api.openai.com/v1"

# 阿里云千问配置示例
QWEN_API_KEY="your-qwen-api-key"
```

## 3. 配置测试URL

更新 `tests/test_agent_journey.py` 文件中的URL配置：
```python
BASE_URL = "https://your-app-base-url.com"
WORKFLOW_AGENT_URL = "https://your-app-base-url.com/workflow-agent"
CHATFLOW_AGENT_URL = "https://your-app-base-url.com/chatflow-agent"
```

## 4. 运行测试

### 运行所有测试
```bash
pytest tests/
```

### 运行特定测试
```bash
# 运行P0优先级测试
pytest tests/ -m p0

# 运行特定测试文件
pytest tests/test_agent_journey.py

# 运行特定测试函数
pytest tests/test_agent_journey.py::test_main_user_journey
```

## 5. 查看缓存

执行测试后，缓存文件将生成在 `ts_executor/midscene_run/cache` 目录下。

## 6. 扩展框架

### 添加新的AI操作

1. 在 `ai_actions/agent_page_actions.py` 中添加新方法：
```python
def new_action(self, url: str, param: str):
    self.execute_ai_instruction(
        url,
        "unique_cache_id",
        f"Natural language description of the action with {param}"
    )
```

### 添加新的测试用例

1. 在 `tests/test_agent_journey.py` 中添加新测试函数：
```python
@pytest.mark.p1
def test_new_feature(actions: AgentPageActions):
    actions.new_action("https://your-url.com", "parameter")
    actions.check_text_visible("https://your-url.com", "check_new_feature", "Expected text")
```