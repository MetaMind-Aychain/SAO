#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置恢复脚本
恢复完整配置，重新启用所有高级功能
"""

import os
import shutil

def restore_config():
    """恢复原始配置"""
    try:
        backup_path = "config.json.backup"
        
        if os.path.exists(backup_path):
            shutil.copy(backup_path, "config.json")
            print("✅ 配置已恢复到完整模式")
            print("💡 提示: 请确保网络连接正常，并配置有效的API密钥")
            return True
        else:
            print("❌ 未找到备份配置文件")
            return False
            
    except Exception as e:
        print(f"❌ 恢复配置失败: {e}")
        return False

if __name__ == "__main__":
    print("🔄 恢复NagaAgent完整配置")
    print("=" * 30)
    restore_config()