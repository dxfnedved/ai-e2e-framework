import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from ai_actions.base_executor import BaseExecutor

def test_framework_basic():
    """测试框架的基本功能"""
    print("框架基本功能测试开始")

    # 创建BaseExecutor实例
    executor = BaseExecutor()

    # 验证executor实例已创建
    assert executor is not None
    print("BaseExecutor实例创建成功")

    # 验证execute_ai_instruction方法存在
    assert hasattr(executor, 'execute_ai_instruction')
    print("execute_ai_instruction方法存在")

    print("框架基本功能测试完成")

if __name__ == "__main__":
    test_framework_basic()