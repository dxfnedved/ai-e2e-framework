# Midscene.js 桥接模式使用指南

## 📋 准备工作清单

### ✅ 1. 环境配置

确保以下环境变量已配置：

```bash
export OPENAI_BASE_URL="https://dashscope.aliyuncs.com/compatible-mode/v1"
export OPENAI_API_KEY="your-api-key-here"
export MIDSCENE_MODEL_NAME="qwen-vl-max-latest"
export MIDSCENE_USE_QWEN_VL=1
```

### ✅ 2. Chrome 插件安装

1. 打开 Chrome 浏览器
2. 访问 [Midscene Chrome 插件](https://chromewebstore.google.com/detail/midscene/gbldofcpkknbggpkmbdaefngejllnief)
3. 点击"添加至 Chrome"安装插件
4. 安装完成后，点击浏览器工具栏中的 Midscene 图标
5. 切换到 "Bridge Mode" 标签页
6. 点击 "Allow connection" 按钮

### ✅ 3. 项目依赖

确保已安装所有依赖：

```bash
# Python 虚拟环境
source .venv/Scripts/activate  # Windows
source .venv/bin/activate      # Linux/Mac

# 安装 Python 依赖
pip install -r requirements.txt

# 安装 Node.js 依赖
cd js_driver
npm install
cd ..
```

## 🚀 快速开始

### 方法一：运行演示脚本

```bash
# 设置环境变量并运行演示
./demo_bridge.sh
```

### 方法二：运行测试用例

```bash
# 运行所有桥接模式测试
pytest -m bridge tests/

# 只运行 P0 优先级测试
pytest -m "bridge and p0" tests/

# 运行特定测试
pytest tests/test_agent_features.py::test_p0_features_journey_bridge_mode -v
```

### 方法三：手动使用 API

```python
from ai_actions.agent_actions import AgentActions

# 创建 AgentActions 实例
actions = AgentActions()

try:
    # 连接到桥接模式（打开新标签页）
    actions.setup_bridge_mode("https://www.bing.com")
    
    # 执行搜索操作
    actions.do("在搜索框中输入 'AI automation' 并按回车")
    
    # 验证结果
    actions.assert_on_page("搜索结果")
    
    print("✅ 测试成功完成！")
    
finally:
    # 清理连接
    actions.cleanup_bridge_mode()
```

## 🛠️ 故障排除

### 常见问题

#### 1. 连接失败："Connection failed"

**原因：**
- Chrome 插件未安装或未启用
- 插件未切换到 Bridge Mode
- 未点击 "Allow connection" 按钮

**解决方案：**
1. 检查 Chrome 扩展程序页面，确保 Midscene 插件已启用
2. 点击插件图标，确保在 "Bridge Mode" 标签页
3. 点击 "Allow connection" 按钮
4. 重新运行测试

#### 2. API 密钥错误

**错误信息：** `Error: Invalid API key`

**解决方案：**
```bash
# 检查环境变量
echo $OPENAI_API_KEY
echo $OPENAI_BASE_URL

# 重新设置环境变量
export OPENAI_API_KEY="sk-your-real-api-key"
```

#### 3. 模块导入错误

**错误信息：** `ModuleNotFoundError: No module named '@midscene/web'`

**解决方案：**
```bash
cd js_driver
npm install
```

#### 4. Node.js 版本不兼容

**要求：** Node.js 版本 >= 18.0.0

**解决方案：**
```bash
# 检查版本
node --version

# 如果版本过低，请更新 Node.js
```

### 调试技巧

#### 1. 开启详细日志

```bash
# 运行测试时显示详细输出
pytest -v -s tests/

# 查看 Node.js 脚本输出
cd js_driver
node midscene_runner.js connect "https://example.com"
```

#### 2. 手动测试连接

```bash
cd js_driver

# 测试连接到当前标签页
node midscene_runner.js connect current

# 测试连接到新标签页
node midscene_runner.js connect "https://www.bing.com"

# 执行简单操作
node midscene_runner.js action "assert that the page is loaded"

# 清理连接
node midscene_runner.js destroy
```

#### 3. 检查浏览器控制台

1. 打开 Chrome 开发者工具 (F12)
2. 查看 Console 标签页
3. 查找 Midscene 相关的错误信息

## 📝 使用提示

### 1. 最佳实践

- **总是使用 try-finally 结构**：确保连接在测试结束后被正确清理
- **一次只连接一个标签页**：避免多个连接冲突
- **使用描述性的 AI 指令**：越具体的指令，AI 执行越准确
- **在操作间添加适当等待**：让页面有时间加载

### 2. AI 指令编写技巧

```python
# ✅ 好的指令 - 具体明确
actions.do("点击页面右上角的蓝色'登录'按钮")
actions.do("在标有'用户名'的输入框中输入 'admin'")

# ❌ 避免的指令 - 模糊不清
actions.do("点击按钮")
actions.do("输入用户名")
```

### 3. 文件上传处理

桥接模式下文件上传需要手动处理：

```python
def run_workflow_agent(self):
    # 点击上传按钮
    self.do("点击文件上传按钮")
    
    # 提示用户手动上传
    print("⚠️ 请手动上传 test_data/sample_excel.xlsx 文件")
    input("上传完成后按回车键继续...")
    
    # 继续后续操作
    self.do("点击执行按钮")
```

## 🎯 下一步

1. **配置应用 URL**：在 `ai_actions/agent_actions.py` 中将 `YOUR_AGENT_HOMEPAGE_URL` 替换为实际的应用地址
2. **自定义测试用例**：根据您的应用功能编写特定的测试场景
3. **集成 CI/CD**：将桥接模式测试集成到持续集成流程中

## 🆘 获取帮助

如果遇到问题，请检查：

1. [Midscene.js 官方文档](https://midscenejs.com/)
2. [GitHub Issues](https://github.com/web-infra-dev/midscene.js/issues)
3. 项目 README.md 文件
4. 运行 `./setup_bridge_env.sh` 检查环境配置