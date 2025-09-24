import subprocess
import os
import copy

class BaseExecutor:

    def execute_ai_instruction(self, url: str, cache_id: str, instruction: str):
        """
        调用外部 TS 脚本来执行 AI 驱动的 UI 操作，并启用缓存。
        """
        ts_executor_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'ts_executor'))
        runner_script_path = os.path.join(ts_executor_path, 'runner.ts').replace('\\', '/')

        # 使用完整的 npx 路径
        command = ["C:\\Program Files\\nodejs\\npx.cmd", "tsx", runner_script_path, url, cache_id, instruction]

        # 核心：设置 MIDSCENE_CACHE=1 环境变量来启用缓存
        env = copy.deepcopy(os.environ)
        env["MIDSCENE_CACHE"] = "1"

        print(f"\n[CACHE ENABLED] Executing Command: {' '.join(command)}")
        print(f"Working directory: {ts_executor_path}")

        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=True,
                cwd=ts_executor_path, # 必须在 TS 项目目录下运行
                encoding='utf-8',
                env=env
            )
            print(f"Midscene Output: {result.stdout}")
        except subprocess.CalledProcessError as e:
            print(f"Error executing AI action: {e}")
            print(f"Stderr: {e.stderr}")
            raise
        except FileNotFoundError as e:
            print(f"File not found error: {e}")
            print("Please check if Node.js and npx are installed and in your PATH")
            raise