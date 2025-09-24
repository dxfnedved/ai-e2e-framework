# AI 驱动端到端测试框架 (Midscene.js + Playwright + 缓存)

## 🎉 项目概述

这是一个基于 **Midscene.js + Playwright 集成 + 智能缓存** 的革命性 AI 驱动前端测试框架。

### 🚀 框架优势

- **🎭 Playwright 集成**: 利用成熟的 Playwright 测试生态系统
- **🤖 AI 驱动操作**: 使用自然语言控制浏览器交互
- **⚡ 智能缓存**: 大幅减少 AI 调用，执行效率提升50% (51s → 28s)
- **📊 可视化报告**: 内置 Midscene 测试报告和截图
- **🔄 并行执行**: 支持多测试用例并行运行
- **🎯 中文优化**: 适配阿里云通义千问，完美支持中文指令

### 🎨 双模式支持

1. **🌉 桥接模式**: 控制桶面Chrome浏览器，复用现有状态
2. **🎭 Playwright 集成模式**: 完整的测试框架能力（推荐）

## 架构图

```
Python 测试用例 → subprocess → Node.js 脚本 → Midscene.js → 浏览器操作
    ↓                                                           ↑
 断言验证 ←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←
```

## 安装步骤

### 1. 安装 Python 依赖

```bash
pip install -r requirements.txt
playwright install chromium
```

### 2. 安装 Node.js 依赖

```bash
cd js_driver
npm install
```

### 3. 配置 Midscene.js Chrome 插件（桥接模式）

1. 在 Chrome 应用商店安装 [Midscene 浏览器插件](https://chromewebstore.google.com/detail/midscene/gbldofcpkknbggpkmbdaefngejllnief)
2. 启动 Chrome 并激活 Midscene 插件
3. 切换到插件的 'Bridge Mode' 标签页
4. 点击 "Allow connection" 按钮

**环境变量配置：**
```bash
# 配置阿里云通义千问 API
export OPENAI_BASE_URL="https://dashscope.aliyuncs.com/compatible-mode/v1"
export OPENAI_API_KEY="your-api-key-here"
export MIDSCENE_MODEL_NAME="qwen-vl-max-latest"
export MIDSCENE_USE_QWEN_VL=1
```

**注意：** 桥接模式不需要下载和解压插件文件，直接从 Chrome 应用商店安装即可。

### 4. 配置应用 URL

编辑 `ai_actions/agent_actions.py` 文件，将 `YOUR_AGENT_HOMEPAGE_URL` 替换为您的实际应用地址。

## 🚀 快速开始（推荐：Playwright 集成模式）

### 1. 环境配置

```bash
# 设置环境变量
export OPENAI_BASE_URL="https://dashscope.aliyuncs.com/compatible-mode/v1"
export OPENAI_API_KEY="your-api-key"
export MIDSCENE_MODEL_NAME="qwen-vl-max-latest"
export MIDSCENE_USE_QWEN_VL=1
export MIDSCENE_CACHE=1  # 启用缓存
export BASE_URL="https://your-app.com"
```

### 2. 安装依赖

```bash
# 安装 Node.js 依赖
cd js_driver
npm install
npx playwright install chromium
```

### 3. 运行测试

```bash
# Playwright 集成模式（推荐）
./run_playwright_tests.sh cache     # 缓存模式
./run_playwright_tests.sh headed    # 有头模式
./run_playwright_tests.sh p0        # P0 测试
./run_playwright_tests.sh report    # 查看报告

# 桥接模式（替代方案）
pytest -m bridge tests/
```

## 项目结构

```
ai-driven-e2e-tests/
├── js_driver/                  # Midscene.js 驱动脚本
│   ├── package.json           # Node.js 依赖配置
│   └── midscene_runner.js     # AI 操作执行器
├── ai_actions/                # Python AI 操作封装
│   ├── __init__.py
│   ├── base_actions.py        # 基础操作类
│   └── agent_actions.py       # Agent 业务操作封装
├── tests/                     # Pytest 测试用例
│   ├── __init__.py
│   └── test_agent_features.py # 主要测试用例
├── test_data/                 # 测试数据
│   └── sample_excel.csv       # 示例数据文件
├── midscene_extension/        # Chrome 插件目录 (需手动配置)
├── conftest.py               # Pytest 配置
├── requirements.txt          # Python 依赖
└── README.md                # 项目文档
```

## 核心组件说明

### BaseActions 类
- 提供 `do(instruction)` 方法，将自然语言指令转换为 Midscene.js 操作
- 处理 Python 与 Node.js 之间的通信
- 负责错误处理和日志输出

### AgentActions 类
- 继承 BaseActions，封装 Agent 应用的具体业务操作
- 包含页面导航、表单填写、文件上传等高级操作
- 提供语义化的断言方法

### 测试用例组织
- 使用 pytest 标记 (`@pytest.mark.p0`, `@pytest.mark.p1`) 区分测试优先级
- 每个测试方法专注于一个完整的用户旅程
- 包含详细的中文注释说明测试意图和预期结果

## 🌉 桥接模式详细说明

### 什么是桥接模式？

桥接模式允许您使用本地脚本控制桌面版本的 Chrome 浏览器。您的脚本可以连接到新标签页或当前已激活的标签页。

**优势：**
- 复用已有的 cookie、插件、页面状态等
- 与操作者互动，完成复杂任务
- 真实的用户环境测试

### 框架架构

```
Python 测试用例
    ↓
AgentActions 类
    ↓
BaseActions.do() 方法
    ↓
subprocess 调用 Node.js
    ↓
midscene_runner.js
    ↓
Midscene.js AgentOverChromeBridge
    ↓
Chrome 插件桥接
    ↓
桌面 Chrome 浏览器
```

### 使用示例

```python
# 创建 AgentActions 实例（桥接模式不需要 page 参数）
actions = AgentActions()

try:
    # 连接到桥接模式
    actions.setup_bridge_mode("https://example.com")
    
    # 执行 AI 操作
    actions.do("点击登录按钮")
    actions.do("在用户名输入框中输入 'admin'")
    actions.do("在密码输入框中输入 '123456'")
    actions.do("点击提交按钮")
    
    # 断言验证
    actions.assert_on_page("欢迎回来")
    
finally:
    # 清理连接
    actions.cleanup_bridge_mode()
```

1. **自然语言指令编写**
   - 使用清晰、具体的动作描述
   - 包含必要的元素标识信息
   - 示例：`"Click the '执行' button"` 而不是 `"Click button"`

2. **测试数据管理**
   - 将测试文件放在 `test_data/` 目录
   - 使用绝对路径引用测试文件
   - 考虑数据隔离和清理

3. **错误处理**
   - 框架会自动捕获和报告 Midscene.js 执行错误
   - 使用 AI 断言进行页面状态验证
   - 在测试失败时查看详细的执行日志

## 故障排除

### 常见问题

1. **Node.js 脚本执行失败**
   - 检查 Node.js 版本 (推荐 18+)
   - 确认 midscene 依赖安装成功
   - 验证工作目录和文件路径

2. **浏览器插件加载失败**
   - 确认插件文件完整性
   - 检查 Chrome/Chromium 版本兼容性
   - 验证插件目录权限

3. **远程调试连接问题**
   - 确认端口 9222 未被占用
   - 检查防火墙设置
   - 验证浏览器启动参数

## 扩展指南

### 添加新的业务操作
1. 在 `AgentActions` 类中添加新方法
2. 使用 `self.do()` 封装 AI 指令
3. 根据需要组合 Playwright 原生操作

### 创建新的测试套件
1. 在 `tests/` 目录创建新的测试文件
2. 使用适当的 pytest 标记
3. 遵循现有的命名和组织约定

### 支持其他应用
1. 创建新的 Actions 类继承 `BaseActions`
2. 封装应用特定的操作
3. 编写对应的测试用例

## 许可证

本项目基于 MIT 许可证开源。