import os
import json
import redis
from typing import List, Dict

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
SESSION_TTL = int(os.getenv("SESSION_TTL", "3600"))
SESSION_MAX_MESSAGES = int(os.getenv("SESSION_MAX_MESSAGES", "6"))

_r = None

def _get_redis():
    global _r
    if _r is None:
        _r = redis.from_url(REDIS_URL, decode_responses=True)
    return _r

def _key(user_id: int) -> str:
  return f"tg:ai:session:{user_id}"

def append_user_message(user_id: int, content: str):
    r = _get_redis()
    item = {"role": "user", "content": content}
    r.rpush(_key(user_id), json.dumps(item))
    # Trim length (keep last SESSION_MAX_MESSAGES*2 entries roughly)
    r.ltrim(_key(user_id), -SESSION_MAX_MESSAGES*2, -1)
    r.expire(_key(user_id), SESSION_TTL)

def append_assistant_message(user_id: int, content: str):
    r = _get_redis()
    item = {"role": "assistant", "content": content}
    r.rpush(_key(user_id), json.dumps(item))
    r.ltrim(_key(user_id), -SESSION_MAX_MESSAGES*2, -1)
    r.expire(_key(user_id), SESSION_TTL)

def get_session_messages(user_id: int, system_prompt: str = None) -> List[Dict]:
    r = _get_redis()
    raw = r.lrange(_key(user_id), 0, -1)
    msgs = []
    if system_prompt:
        msgs.append({"role": "system", "content": system_prompt})
    for item in raw:
        try:
            d = json.loads(item)
            msgs.append(d)
        except Exception:
            continue
    return msgs

def clear_session(user_id: int):
    r = _get_redis()
    r.delete(_key(user_id))
