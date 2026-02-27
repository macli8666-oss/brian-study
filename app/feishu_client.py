import httpx
import time
import json
from app.config import FEISHU_APP_ID, FEISHU_APP_SECRET, FEISHU_BASE_URL

_token_cache = {"token": None, "expire": 0}


def get_tenant_access_token():
    now = time.time()
    if _token_cache["token"] and now < _token_cache["expire"]:
        return _token_cache["token"]

    resp = httpx.post(
        f"{FEISHU_BASE_URL}/auth/v3/tenant_access_token/internal",
        json={
            "app_id": FEISHU_APP_ID,
            "app_secret": FEISHU_APP_SECRET,
        },
    )
    data = resp.json()
    token = data.get("tenant_access_token", "")
    _token_cache["token"] = token
    _token_cache["expire"] = now + data.get("expire", 7200) - 300
    return token


def _headers():
    return {
        "Authorization": f"Bearer {get_tenant_access_token()}",
        "Content-Type": "application/json; charset=utf-8",
    }


def send_card(open_id, card):
    payload = {
        "receive_id": open_id,
        "msg_type": "interactive",
        "content": json.dumps(card),
    }
    resp = httpx.post(
        f"{FEISHU_BASE_URL}/im/v1/messages?receive_id_type=open_id",
        headers=_headers(),
        json=payload,
        timeout=10,
    )
    return resp.json()


def reply_card(message_id, card):
    payload = {
        "msg_type": "interactive",
        "content": json.dumps(card),
    }
    resp = httpx.post(
        f"{FEISHU_BASE_URL}/im/v1/messages/{message_id}/reply",
        headers=_headers(),
        json=payload,
        timeout=10,
    )
    return resp.json()


def send_text(open_id, text):
    payload = {
        "receive_id": open_id,
        "msg_type": "text",
        "content": json.dumps({"text": text}),
    }
    resp = httpx.post(
        f"{FEISHU_BASE_URL}/im/v1/messages?receive_id_type=open_id",
        headers=_headers(),
        json=payload,
        timeout=10,
    )
    return resp.json()


def update_card(message_id, card):
    payload = {
        "content": json.dumps(card),
    }
    resp = httpx.patch(
        f"{FEISHU_BASE_URL}/im/v1/messages/{message_id}",
        headers=_headers(),
        json=payload,
        timeout=10,
    )
    return resp.json()
