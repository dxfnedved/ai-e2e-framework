# Midscene.js + Playwright 集成指南

## 🎯 为什么选择 Playwright 集成模式？

基于您提供的 Midscene.js 官方文档，**Playwright 集成 + 缓存** 是构建 AI 驱动前端端到端自动化测试框架的最佳选择：

### 🚀 核心优势

1. **⚡ 性能优化**：缓存将执行时间从 51秒 降低到 28秒
2. **🔧 成熟生态**：利用 Playwright 完整的测试框架能力
3. **💰 成本控制**：大幅减少 AI 模型调用次数
4. **📊 丰富报告**：内置可视化测试报告
5. **🛠️ 调试友好**：强大的调试和开发工具
6. **🔄 并行执行**：支持多测试用例并行运行

## 🏗️ 架构设计

```
┌─────────────────────────────────────────────────────────────┐
│                    Playwright 测试框架                        │
├─────────────────────────────────────────────────────────────┤
│  测试用例 (TypeScript/JavaScript)                           │
│    ├── test.beforeEach() - 测试前置条件                     │
│    ├── test.step() - 测试步骤组织                           │
│    └── expect() - 断言验证                                   │
├─────────────────────────────────────────────────────────────┤
│  Midscene.js Fixture                                       │
│    ├── ai() - 通用 AI 交互                                  │
│    ├── aiTap() - AI 点击操作                                │
│    ├── aiInput() - AI 输入操作                              │
│    ├── aiQuery() - AI 数据提取                              │
│    ├── aiAssert() - AI 断言验证                             │
│    └── logScreenshot() - 截图记录                           │
├─────────────────────────────────────────────────────────────┤
│  缓存系统 (MIDSCENE_CACHE=1)                               │
│    ├── 任务规划结果缓存                                      │
│    ├── 元素定位 XPath 缓存                                   │
│    └── 自动缓存失效处理                                      │
├─────────────────────────────────────────────────────────────┤
│  AI 模型服务 (阿里云通义千问)                                │
│    ├── qwen-vl-max-latest                                  │
│    ├── 视觉理解能力                                          │
│    └── 中文指令优化                                          │
└─────────────────────────────────────────────────────────────┘
```

## 🚀 快速开始

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
# 在 js_driver 目录
cd js_driver
npm install @midscene/web @playwright/test playwright tsx

# 安装 Playwright 浏览器
npx playwright install chromium
```

### 3. 运行测试

```bash
# 基础运行
./run_playwright_tests.sh

# 不同运行模式
./run_playwright_tests.sh cache    # 缓存模式
./run_playwright_tests.sh headed   # 有头模式
./run_playwright_tests.sh debug    # 调试模式
./run_playwright_tests.sh p0       # P0 优先级测试
./run_playwright_tests.sh report   # 查看报告
```

## 📝 测试用例编写

### 基础结构

```typescript
import { test, expect } from './fixture';

test.beforeEach(async ({ page }) => {
  await page.setViewportSize({ width: 1280, height: 720 });
  await page.goto(process.env.BASE_URL!);
  await page.waitForLoadState('networkidle');
});

test.describe('功能模块', () => {
  test('具体测试场景', async ({
    ai,           // 通用 AI 交互
    aiQuery,      // AI 数据提取  
    aiAssert,     // AI 断言
    aiInput,      // AI 输入
    aiTap,        // AI 点击
    aiWaitFor,    // AI 等待
    logScreenshot // 截图记录
  }) => {
    // 启用缓存
    process.env.MIDSCENE_CACHE = '1';
    
    // 测试步骤
    await test.step('步骤1: 用户登录', async () => {
      await aiInput('admin', '用户名输入框');
      await aiInput('password', '密码输入框');
      await aiTap('登录按钮');
      await aiAssert('用户已成功登录');
    });
    
    // 记录关键状态
    await logScreenshot('登录成功', { content: '用户登录流程完成' });
  });
});
```

### 🎯 AI 指令最佳实践

```typescript
// ✅ 好的指令 - 具体明确
await ai('点击页面右上角的蓝色"登录"按钮');
await aiInput('测试数据', '标有"用户名"的输入框');
await aiAssert('页面显示"欢迎回来"的问候语');

// ❌ 避免的指令 - 模糊不清  
await ai('点击按钮');
await aiInput('数据', '输入框');
await aiAssert('页面正常');
```

### 📊 数据提取示例

```typescript
// 提取结构化数据
const products = await aiQuery<Array<{
  name: string;
  price: number;
  rating: number;
}>>('获取产品列表中所有商品的名称、价格和评分');

// 提取单个值
const totalPrice = await agent.aiNumber('购物车中的总金额是多少？');
const userName = await agent.aiString('当前登录用户的用户名是什么？');
const isLoggedIn = await agent.aiBoolean('用户是否已经登录？');
```

## 🗂️ 缓存策略详解

### 缓存内容

1. **任务规划结果**: `ai`、`aiAction` 方法的执行计划
2. **元素定位数据**: `aiTap`、`aiInput` 等方法的 XPath 信息
3. **不缓存内容**: `aiQuery`、`aiAssert`、`aiBoolean` 等查询类方法

### 缓存命中条件

```typescript
const agent = new PlaywrightAgent(page, {
  cacheId: 'my-test-cache', // 设置缓存标识
});

// 相同的指令 + 相同的页面状态 = 缓存命中
await agent.aiAction('点击搜索按钮'); // 第一次：调用 AI
await agent.aiAction('点击搜索按钮'); // 第二次：使用缓存
```

### 缓存文件位置

```
./midscene_run/cache/
├── my-test-cache.cache.yaml
├── agent-features-playwright.cache.yaml
└── ...
```

### 缓存性能对比

| 模式 | 执行时间 | AI 调用次数 | 成本 |
|------|----------|-------------|------|
| 无缓存 | 51秒 | 15次 | 高 |
| **缓存模式** | **28秒** | **3次** | **低** |

## 📊 测试报告

### 报告类型

1. **合并报告** (默认): 所有测试用例生成一个报告
2. **分离报告**: 每个测试用例独立报告

```typescript
// playwright.config.ts
reporter: [
  ['list'], 
  ['@midscene/web/playwright-reporter', { 
    type: 'merged' // 或 'separate'
  }]
]
```

### 报告内容

- 📸 每个步骤的页面截图
- 🤖 AI 操作的详细过程
- ⏱️ 执行时间和性能数据
- 🎯 缓存命中率统计
- ❌ 失败原因和调试信息

## 🛠️ 调试技巧

### 1. 启用调试模式

```bash
# 调试模式运行
./run_playwright_tests.sh debug

# 或者直接使用 Playwright
npx playwright test --debug
```

### 2. 查看缓存日志

```bash
export DEBUG=midscene:cache:*
./run_playwright_tests.sh
```

### 3. 手动清理缓存

```bash
# 删除所有缓存
rm -rf ./midscene_run/cache/

# 删除特定测试的缓存
rm ./midscene_run/cache/my-test-cache.cache.yaml
```

### 4. 性能分析

```typescript
test('性能测试', async ({ ai }) => {
  const startTime = Date.now();
  
  // 执行测试操作
  await ai('执行复杂操作');
  
  const endTime = Date.now();
  console.log(`执行时间: ${endTime - startTime}ms`);
});
```

## 🚨 常见问题排查

### 1. 缓存未生效

**原因**: 
- 未设置 `MIDSCENE_CACHE=1`
- 未设置 `cacheId`
- 页面结构发生变化

**解决**:
```bash
export MIDSCENE_CACHE=1
export DEBUG=midscene:cache:*
```

### 2. AI 模型调用失败

**原因**: API 密钥或配置错误

**解决**:
```bash
# 检查配置
echo $OPENAI_API_KEY
echo $OPENAI_BASE_URL

# 重新设置
export OPENAI_API_KEY="sk-your-key"
```

### 3. 元素定位失败

**原因**: 页面结构变化导致缓存失效

**解决**: 缓存会自动失效，AI 重新定位元素

### 4. 测试执行缓慢

**原因**: 
- 未启用缓存
- 页面加载缓慢
- AI 指令不够精确

**解决**:
- 启用缓存: `MIDSCENE_CACHE=1`
- 优化指令精确度
- 使用 `aiWaitFor` 等待页面就绪

## 🎯 最佳实践总结

1. **✅ 始终启用缓存**: `MIDSCENE_CACHE=1`
2. **✅ 设置缓存标识**: 使用有意义的 `cacheId`
3. **✅ 精确的 AI 指令**: 包含足够的上下文信息
4. **✅ 合理的测试组织**: 使用 `test.step()` 组织步骤
5. **✅ 关键状态截图**: 使用 `logScreenshot()` 记录
6. **✅ 适当的等待策略**: 使用 `aiWaitFor()` 而不是固定延时
7. **✅ 错误处理**: 使用 try-catch 处理异常情况

## 🔮 进阶功能

### 自定义操作

```typescript
import { defineAction } from '@midscene/core/device';

const customAction = defineAction({
  name: 'multiClick',
  description: '连续点击同一元素',
  paramSchema: z.object({
    locate: getMidsceneLocationSchema(),
    count: z.number()
  }),
  async call(param) {
    // 自定义实现
  }
});

const agent = new PlaywrightAgent(page, {
  customActions: [customAction]
});
```

### 并行测试

```typescript
// playwright.config.ts
export default defineConfig({
  fullyParallel: true,
  workers: process.env.CI ? 1 : 4, // 本地并行执行
});
```

这个基于 Playwright 集成的方案为您提供了一个完整、高效、可维护的 AI 驱动测试框架！🎉