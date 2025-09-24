import { chromium } from 'playwright';
import { PlaywrightAgent } from '@midscene/web/playwright';
import 'dotenv/config'; // 用于读取 .env 中的模型配置

// 从命令行参数获取指令
// 调用格式: tsx runner.ts "URL" "CACHE_ID" "INSTRUCTION"
const url = process.argv[2];
const cacheId = process.argv[3];
const instruction = process.argv[4];

if (!url || !cacheId || !instruction) {
  console.error('Usage: tsx runner.ts <url> <cacheId> <instruction>');
  process.exit(1);
}

(async () => {
  const browser = await chromium.launch({ headless: false }); // Headless in CI
  const page = await browser.newPage();
  await page.goto(url);

  // 初始化 PlaywrightAgent，并传入 cacheId 来激活缓存
  const agent = new PlaywrightAgent(page, { cacheId });

  try {
    console.log(`Executing AI action with cacheId='${cacheId}': "${instruction}"`);
    await agent.aiAction(instruction);
    console.log('Action completed successfully.');
  } catch (error) {
    console.error(`Error executing action: ${error}`);
    process.exit(1);
  } finally {
    await browser.close();
  }
})();