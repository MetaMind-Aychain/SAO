import sqlite3

def check_db():
    conn = sqlite3.connect('ai_website.db')
    cursor = conn.cursor()
    
    # 检查表是否存在
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("数据库中的表:", [table[0] for table in tables])
    
    # 检查动态数据
    try:
        cursor.execute('SELECT COUNT(*) FROM ai_dynamics')
        dynamics_count = cursor.fetchone()[0]
        print(f'AI动态数量: {dynamics_count}')
        
        cursor.execute('SELECT content, created_at FROM ai_dynamics LIMIT 3')
        dynamics = cursor.fetchall()
        print("最近的动态:")
        for d in dynamics:
            print(f"  - {d[0][:50]}... ({d[1]})")
    except Exception as e:
        print(f"查询ai_dynamics出错: {e}")
    
    # 检查开发日志
    try:
        cursor.execute('SELECT COUNT(*) FROM developer_updates')
        dev_count = cursor.fetchone()[0]
        print(f'开发日志数量: {dev_count}')
        
        cursor.execute('SELECT title, created_at FROM developer_updates LIMIT 3')
        updates = cursor.fetchall()
        print("最近的开发日志:")
        for u in updates:
            print(f"  - {u[0]} ({u[1]})")
    except Exception as e:
        print(f"查询developer_updates出错: {e}")
    
    # 检查用户数据
    try:
        cursor.execute('SELECT COUNT(*) FROM users')
        users_count = cursor.fetchone()[0]
        print(f'用户数量: {users_count}')
    except Exception as e:
        print(f"查询users出错: {e}")
    
    conn.close()

if __name__ == "__main__":
    check_db()