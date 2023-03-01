

SERVER_CONFIG = {
    "ip": "192.168.0.18",
    "port": 8088
}
# 配置用户内容
USER_LIST = [{'admin': 'admin'}, {'root': 'root'}, {"test": 'test'}]

# token过期时间 分钟
ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8

# 生成token的加密算法
ALGORITHM: str = "HS256"

# 生产环境保管好 SECRET_KEY
SECRET_KEY: str = 'cetc'
# 权限相关配置
WHITE_URL = ['/login', '/user/login']
ALLOW_LIST = ['admin', 'root']
# openai的key
AI_KEY = "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"
