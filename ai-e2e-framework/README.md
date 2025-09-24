# AI驱动的端到端测试框架

## 项目概述

这是一个结合了Python/Pytest和Midscene.js/Playwright的AI驱动测试框架，利用缓存机制大幅提升测试执行效率。该框架采用混合架构设计，充分发挥了Python在测试管理和报告生成方面的优势，以及Node.js/Midscene.js在AI驱动UI操作方面的强大能力。

## 核心特性

- **混合架构**: Python/Pytest负责测试管理，Node.js/Midscene.js负责AI执行
- **AI指令驱动**: 使用自然语言指令驱动UI操作，降低测试编写门槛
- **智能缓存**: 通过缓存机制大幅提升测试执行效率，节省50%以上时间
- **易于扩展**: 模块化设计，可轻松添加新的AI操作和测试用例
- **配置分离**: 环境配置与代码分离，便于维护和部署

## 项目结构

```
/ai-e2e-framework
|
|-- /ts_executor                # TypeScript AI执行层
|   |-- runner.ts               # 核心执行脚本
|   |-- package.json            # Node.js依赖配置
|   |-- tsconfig.json           # TypeScript配置
|   |-- .env                    # AI模型配置文件
|
|-- /ai_actions                 # Python端的AI操作封装
|   |-- __init__.py
|   |-- base_executor.py        # 调用TS驱动的核心方法
|   |-- agent_page_actions.py   # 封装Agent页面的所有AI操作
|
|-- /tests                      # Pytest测试用例
|   |-- __init__.py
|   |-- test_agent_journey.py   # 完整的测试流程
|
|-- /test_data                  # 测试数据
|   |-- sample_excel.xlsx       # 示例Excel文件
|
|-- config.ini                  # 环境配置文件
|-- pytest.ini                  # Pytest配置文件
|-- requirements.txt            # Python依赖
```

## 安装与设置

### 前提条件

- Node.js (版本14或更高)
- Python (版本3.7或更高)
- Git

### 安装步骤

1. **安装Node.js依赖**
   ```bash
   cd ts_executor
   npm install
   ```

2. **安装Python依赖**
   ```bash
   pip install -r requirements.txt
   ```

3. **安装浏览器驱动**
   ```bash
   playwright install
   ```

## 配置

### 配置AI模型参数

在 `ts_executor/.env` 文件中配置您的AI模型参数：

```env
# For Qwen (推荐)
OPENAI_BASE_URL="https://dashscope.aliyuncs.com/compatible-mode/v1"
OPENAI_API_KEY="your-qwen-api-key"
MIDSCENE_MODEL_NAME="qwen-vl-max-latest"
MIDSCENE_USE_QWEN_VL=1

# For OpenAI
# OPENAI_API_KEY="your-openai-api-key"
# OPENAI_BASE_URL="https://api.openai.com/v1"
```

### 配置测试环境URL

在项目根目录的 `config.ini` 文件中配置测试环境URL：

```ini
[Environment]
base_url = http://your-real-app-url.com
workflow_agent_url = http://your-real-app-url.com/workflow-agent
chatflow_agent_url = http://your-real-app-url.com/chatflow-agent
```

## 如何运行测试

### 基本运行命令

```bash
# 运行所有测试
python -m pytest

# 运行特定测试文件
python -m pytest tests/test_agent_journey.py

# 只运行P0优先级测试
python -m pytest -m p0

# 只运行P1优先级测试
python -m pytest -m p1
```

### 生成测试报告

```bash
# 生成HTML报告
python -m pytest --html=report.html

# 生成详细报告
python -m pytest -v --html=report.html
```

## 查看报告

### Pytest HTML报告

运行测试时使用 `--html=report.html` 参数生成的HTML报告将包含：
- 测试执行摘要
- 详细的测试结果
- 失败测试的错误信息
- 执行时间统计

### Midscene可视化报告

Midscene会自动生成可视化报告，位于：
- `ts_executor/midscene_run/report/` 目录下

### 缓存文件

缓存文件位于：
- `ts_executor/midscene_run/cache/` 目录下

## 最佳实践：编写高效的AI指令

为了确保AI能够准确理解和执行您的指令，请遵循以下最佳实践：

### 1. 使用明确的动词和动作描述

**推荐**:
```
"Locate any Agent card visible on the current page and click on it"
```

**不推荐**:
```
"Click on any Agent card"
```

### 2. 结构化多步骤指令

使用序数词使步骤更清晰：
```
"First, find and click on the '评论' tab
Then, locate the comment input text area
Next, find the star rating control
Finally, locate and click the '发送' button"
```

### 3. 添加视觉特征描述

帮助AI识别特定元素：
```
"Find and click the send button (usually an arrow or paper plane icon)"
```

### 4. 处理歧义情况

明确处理可能的歧义：
```
"If multiple agent cards are present, select the first one"
```

### 5. 明确操作目标

说明每步操作的目的：
```
"to navigate to the agent details page"
"to submit the message"
```

### 6. 全面检查要求

要求AI检查所有可能的区域：
```
"Scan the entire page content including all sections, tabs, and scrollable areas"
```

通过遵循这些最佳实践，您可以显著提高AI执行的准确性和成功率，从而提升测试的稳定性和效率。