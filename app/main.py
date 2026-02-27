"""Brian's AS Study Hub - Feishu Interactive Bot."""

import json
import hashlib
import logging
from fastapi import FastAPI, Request, Response
from app.database import init_db, set_user_state, get_user_state, save_quiz_result, get_quiz_stats
from app.feishu_client import send_card, send_text
from app.content_loader import (
    load_subject, get_all_subjects, get_chapters,
    get_chapter, get_knowledge_point, get_question,
)
from app.card_builder import (
    main_menu_card, chapter_list_card, mode_select_card,
    knowledge_point_card, quiz_card, answer_result_card,
)
from app.claude_client import ask_question
from app.config import FEISHU_APP_SECRET

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Brian AS Study Hub")

# Track processed event IDs to avoid duplicates
_processed_events = set()


@app.on_event("startup")
def startup():
    init_db()
    # Pre-load all content
    for sid in ["math_pure1", "math_stats1", "physics_as"]:
        data = load_subject(sid)
        if data:
            logger.info(f"Loaded {sid}: {len(data['chapters'])} chapters")
        else:
            logger.warning(f"Content not found for {sid}")


@app.get("/")
def health():
    return {"status": "ok", "service": "Brian AS Study Hub"}


@app.post("/callback")
async def callback(request: Request):
    """Handle Feishu event subscription callback."""
    body = await request.json()
    logger.info(f"Callback received: {json.dumps(body, ensure_ascii=False)[:500]}")

    # URL verification challenge
    if "challenge" in body:
        return {"challenge": body["challenge"]}

    # Schema v2 events
    schema = body.get("schema")
    header = body.get("header", {})
    event_type = header.get("event_type", "")
    event_id = header.get("event_id", "")

    # Deduplicate events
    if event_id in _processed_events:
        return {"code": 0}
    _processed_events.add(event_id)
    # Keep set size manageable
    if len(_processed_events) > 1000:
        _processed_events.clear()

    event = body.get("event", {})

    if event_type == "im.message.receive_v1":
        await handle_message(event)

    return {"code": 0}


@app.post("/card-action")
async def card_action(request: Request):
    """Handle Feishu card action callback."""
    body = await request.json()
    logger.info(f"Card action: {json.dumps(body, ensure_ascii=False)[:500]}")

    action = body.get("action", {})
    value = action.get("value", {})
    open_id = body.get("open_id", "")

    if not open_id:
        # Try to get from operator
        operator = body.get("operator", {})
        open_id = operator.get("open_id", "")

    if not value or not open_id:
        return {"code": 0}

    action_type = value.get("action", "")

    try:
        if action_type == "main_menu":
            card = main_menu_card()
            send_card(open_id, card)

        elif action_type == "select_subject":
            subject_id = value["subject"]
            data = load_subject(subject_id)
            if data:
                chapters = get_chapters(subject_id)
                card = chapter_list_card(
                    data["subject_name_en"], data["subject_name_zh"],
                    chapters, subject_id
                )
                send_card(open_id, card)

        elif action_type == "select_chapter":
            subject_id = value["subject"]
            chapter_id = value["chapter"]
            ch = get_chapter(subject_id, chapter_id)
            if ch:
                card = mode_select_card(
                    subject_id, chapter_id,
                    ch["title_en"], ch["title_zh"]
                )
                send_card(open_id, card)

        elif action_type == "start_learn":
            subject_id = value["subject"]
            chapter_id = value["chapter"]
            ch = get_chapter(subject_id, chapter_id)
            point, total = get_knowledge_point(subject_id, chapter_id, 0)
            if point and ch:
                set_user_state(open_id, subject_id, chapter_id, "learn", 0)
                card = knowledge_point_card(
                    subject_id, chapter_id, point, 0, total,
                    ch["title_en"], ch["title_zh"]
                )
                send_card(open_id, card)

        elif action_type == "learn_point":
            subject_id = value["subject"]
            chapter_id = value["chapter"]
            index = int(value["index"])
            ch = get_chapter(subject_id, chapter_id)
            point, total = get_knowledge_point(subject_id, chapter_id, index)
            if point and ch:
                set_user_state(open_id, subject_id, chapter_id, "learn", index)
                card = knowledge_point_card(
                    subject_id, chapter_id, point, index, total,
                    ch["title_en"], ch["title_zh"]
                )
                send_card(open_id, card)

        elif action_type == "start_test":
            subject_id = value["subject"]
            chapter_id = value["chapter"]
            ch = get_chapter(subject_id, chapter_id)
            question, total = get_question(subject_id, chapter_id, 0)
            if question and ch:
                set_user_state(open_id, subject_id, chapter_id, "test", 0)
                card = quiz_card(
                    subject_id, chapter_id, question, 0, total,
                    ch["title_en"], ch["title_zh"]
                )
                send_card(open_id, card)

        elif action_type == "quiz_question":
            subject_id = value["subject"]
            chapter_id = value["chapter"]
            index = int(value["index"])
            ch = get_chapter(subject_id, chapter_id)
            question, total = get_question(subject_id, chapter_id, index)
            if question and ch:
                set_user_state(open_id, subject_id, chapter_id, "test", index)
                card = quiz_card(
                    subject_id, chapter_id, question, index, total,
                    ch["title_en"], ch["title_zh"]
                )
                send_card(open_id, card)

        elif action_type == "answer":
            subject_id = value["subject"]
            chapter_id = value["chapter"]
            index = int(value["index"])
            selected = value["selected"]
            ch = get_chapter(subject_id, chapter_id)
            question, total = get_question(subject_id, chapter_id, index)
            if question and ch:
                is_correct = selected == question["answer"]
                save_quiz_result(
                    open_id, subject_id, chapter_id,
                    index, selected, question["answer"], int(is_correct)
                )
                card = answer_result_card(
                    subject_id, chapter_id, question, index, total,
                    selected, is_correct, ch["title_en"], ch["title_zh"]
                )
                send_card(open_id, card)

    except Exception as e:
        logger.error(f"Card action error: {e}", exc_info=True)
        send_text(open_id, f"Error | 出错了: {str(e)}")

    return {"code": 0}


async def handle_message(event):
    """Handle incoming messages — treat as questions for Claude."""
    message = event.get("message", {})
    sender = event.get("sender", {})
    open_id = sender.get("sender_id", {}).get("open_id", "")
    msg_type = message.get("message_type", "")

    if msg_type != "text" or not open_id:
        return

    content = json.loads(message.get("content", "{}"))
    text = content.get("text", "").strip()

    if not text:
        return

    # Check for menu commands
    lower = text.lower()
    if lower in ("menu", "菜单", "start", "开始", "/start", "hi", "hello", "你好"):
        card = main_menu_card()
        send_card(open_id, card)
        return

    if lower in ("stats", "统计", "成绩"):
        stats = get_quiz_stats(open_id)
        total = stats.get("total", 0) or 0
        correct = stats.get("correct", 0) or 0
        rate = (correct / total * 100) if total > 0 else 0
        send_text(
            open_id,
            f"📊 Your Stats | 你的成绩\n"
            f"Total questions | 总题数: {total}\n"
            f"Correct | 正确: {correct}\n"
            f"Accuracy | 正确率: {rate:.1f}%"
        )
        return

    # Otherwise, send to Claude for answering
    # Get context from user state
    context = None
    state = get_user_state(open_id)
    if state and state.get("current_subject"):
        data = load_subject(state["current_subject"])
        if data:
            ch = get_chapter(state["current_subject"], state.get("current_chapter", ""))
            if ch:
                context = f"{data['subject_name_en']} - {ch['title_en']}"

    send_text(open_id, "🤔 Thinking... | 正在思考...")
    answer = ask_question(text, context)
    send_text(open_id, answer)
