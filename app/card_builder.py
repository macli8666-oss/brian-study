"""Build Feishu interactive card JSON structures."""


def main_menu_card():
    return {
        "config": {"wide_screen_mode": True},
        "header": {
            "title": {"tag": "plain_text", "content": "AS Study Hub | AS 学习中心"},
            "template": "blue",
        },
        "elements": [
            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": "Welcome! Choose a subject to start.\n欢迎！请选择一个科目开始学习。",
                },
            },
            {"tag": "hr"},
            {
                "tag": "action",
                "actions": [
                    {
                        "tag": "button",
                        "text": {"tag": "plain_text", "content": "📐 Pure Math 1 | 纯数学 1"},
                        "type": "primary",
                        "value": {"action": "select_subject", "subject": "math_pure1"},
                    },
                    {
                        "tag": "button",
                        "text": {"tag": "plain_text", "content": "📊 Statistics 1 | 统计学 1"},
                        "type": "primary",
                        "value": {"action": "select_subject", "subject": "math_stats1"},
                    },
                    {
                        "tag": "button",
                        "text": {"tag": "plain_text", "content": "⚛️ AS Physics | AS 物理"},
                        "type": "primary",
                        "value": {"action": "select_subject", "subject": "physics_as"},
                    },
                ],
            },
            {"tag": "hr"},
            {
                "tag": "note",
                "elements": [
                    {
                        "tag": "plain_text",
                        "content": "Type any question to ask the AI tutor | 直接输入问题即可向AI导师提问",
                    }
                ],
            },
        ],
    }


def chapter_list_card(subject_name_en, subject_name_zh, chapters, subject_id):
    buttons = []
    for ch in chapters:
        buttons.append({
            "tag": "button",
            "text": {
                "tag": "plain_text",
                "content": f"{ch['title_en']} | {ch['title_zh']}",
            },
            "type": "default",
            "value": {
                "action": "select_chapter",
                "subject": subject_id,
                "chapter": ch["chapter_id"],
            },
        })

    # Split buttons into groups of 3 for layout
    action_groups = []
    for i in range(0, len(buttons), 3):
        action_groups.append({
            "tag": "action",
            "actions": buttons[i:i + 3],
        })

    elements = [
        {
            "tag": "div",
            "text": {
                "tag": "lark_md",
                "content": f"**{subject_name_en} | {subject_name_zh}**\nSelect a chapter | 请选择章节",
            },
        },
        {"tag": "hr"},
    ]
    elements.extend(action_groups)
    elements.append({"tag": "hr"})
    elements.append({
        "tag": "action",
        "actions": [
            {
                "tag": "button",
                "text": {"tag": "plain_text", "content": "⬅️ Back to Menu | 返回主菜单"},
                "type": "default",
                "value": {"action": "main_menu"},
            }
        ],
    })

    return {
        "config": {"wide_screen_mode": True},
        "header": {
            "title": {"tag": "plain_text", "content": f"{subject_name_en} | {subject_name_zh}"},
            "template": "indigo",
        },
        "elements": elements,
    }


def mode_select_card(subject_id, chapter_id, chapter_title_en, chapter_title_zh):
    return {
        "config": {"wide_screen_mode": True},
        "header": {
            "title": {
                "tag": "plain_text",
                "content": f"{chapter_title_en} | {chapter_title_zh}",
            },
            "template": "wathet",
        },
        "elements": [
            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": "Choose your mode | 请选择模式",
                },
            },
            {"tag": "hr"},
            {
                "tag": "action",
                "actions": [
                    {
                        "tag": "button",
                        "text": {"tag": "plain_text", "content": "📖 Learn | 学习"},
                        "type": "primary",
                        "value": {
                            "action": "start_learn",
                            "subject": subject_id,
                            "chapter": chapter_id,
                        },
                    },
                    {
                        "tag": "button",
                        "text": {"tag": "plain_text", "content": "📝 Test | 测试"},
                        "type": "danger",
                        "value": {
                            "action": "start_test",
                            "subject": subject_id,
                            "chapter": chapter_id,
                        },
                    },
                ],
            },
            {"tag": "hr"},
            {
                "tag": "action",
                "actions": [
                    {
                        "tag": "button",
                        "text": {"tag": "plain_text", "content": "⬅️ Back | 返回"},
                        "type": "default",
                        "value": {"action": "select_subject", "subject": subject_id},
                    }
                ],
            },
        ],
    }


def knowledge_point_card(subject_id, chapter_id, point, index, total,
                          chapter_title_en, chapter_title_zh):
    elements = [
        {
            "tag": "div",
            "text": {
                "tag": "lark_md",
                "content": f"**Chapter | 章节:** {chapter_title_en} | {chapter_title_zh}\n"
                           f"**Point | 知识点 {index + 1}/{total}:**",
            },
        },
        {"tag": "hr"},
        {
            "tag": "div",
            "text": {
                "tag": "lark_md",
                "content": f"**{point['title_en']} | {point['title_zh']}**",
            },
        },
        {
            "tag": "div",
            "text": {
                "tag": "lark_md",
                "content": f"**English:**\n{point['content_en']}",
            },
        },
        {"tag": "hr"},
        {
            "tag": "div",
            "text": {
                "tag": "lark_md",
                "content": f"**中文：**\n{point['content_zh']}",
            },
        },
        {"tag": "hr"},
    ]

    nav_buttons = []
    if index > 0:
        nav_buttons.append({
            "tag": "button",
            "text": {"tag": "plain_text", "content": "⬅️ Previous | 上一个"},
            "type": "default",
            "value": {
                "action": "learn_point",
                "subject": subject_id,
                "chapter": chapter_id,
                "index": index - 1,
            },
        })
    if index < total - 1:
        nav_buttons.append({
            "tag": "button",
            "text": {"tag": "plain_text", "content": "➡️ Next | 下一个"},
            "type": "primary",
            "value": {
                "action": "learn_point",
                "subject": subject_id,
                "chapter": chapter_id,
                "index": index + 1,
            },
        })
    else:
        nav_buttons.append({
            "tag": "button",
            "text": {"tag": "plain_text", "content": "📝 Start Test | 开始测试"},
            "type": "danger",
            "value": {
                "action": "start_test",
                "subject": subject_id,
                "chapter": chapter_id,
            },
        })

    nav_buttons.append({
        "tag": "button",
        "text": {"tag": "plain_text", "content": "📋 Menu | 菜单"},
        "type": "default",
        "value": {"action": "select_chapter", "subject": subject_id, "chapter": chapter_id},
    })

    elements.append({"tag": "action", "actions": nav_buttons})

    return {
        "config": {"wide_screen_mode": True},
        "header": {
            "title": {
                "tag": "plain_text",
                "content": f"📖 {point['title_en']} | {point['title_zh']}",
            },
            "template": "green",
        },
        "elements": elements,
    }


def quiz_card(subject_id, chapter_id, question, index, total,
              chapter_title_en, chapter_title_zh):
    option_lines = []
    for key in ["A", "B", "C", "D"]:
        option_lines.append(f"**{key}.** {question['options'][key]}")

    elements = [
        {
            "tag": "div",
            "text": {
                "tag": "lark_md",
                "content": f"**Question {index + 1}/{total} | 第 {index + 1}/{total} 题**\n"
                           f"Chapter | 章节: {chapter_title_en} | {chapter_title_zh}",
            },
        },
        {"tag": "hr"},
        {
            "tag": "div",
            "text": {
                "tag": "lark_md",
                "content": f"**{question['question_en']}**\n\n**{question['question_zh']}**",
            },
        },
        {"tag": "hr"},
        {
            "tag": "div",
            "text": {
                "tag": "lark_md",
                "content": "\n".join(option_lines),
            },
        },
        {"tag": "hr"},
        {
            "tag": "action",
            "actions": [
                {
                    "tag": "button",
                    "text": {"tag": "plain_text", "content": "A"},
                    "type": "default",
                    "value": {
                        "action": "answer",
                        "subject": subject_id,
                        "chapter": chapter_id,
                        "index": index,
                        "selected": "A",
                    },
                },
                {
                    "tag": "button",
                    "text": {"tag": "plain_text", "content": "B"},
                    "type": "default",
                    "value": {
                        "action": "answer",
                        "subject": subject_id,
                        "chapter": chapter_id,
                        "index": index,
                        "selected": "B",
                    },
                },
                {
                    "tag": "button",
                    "text": {"tag": "plain_text", "content": "C"},
                    "type": "default",
                    "value": {
                        "action": "answer",
                        "subject": subject_id,
                        "chapter": chapter_id,
                        "index": index,
                        "selected": "C",
                    },
                },
                {
                    "tag": "button",
                    "text": {"tag": "plain_text", "content": "D"},
                    "type": "default",
                    "value": {
                        "action": "answer",
                        "subject": subject_id,
                        "chapter": chapter_id,
                        "index": index,
                        "selected": "D",
                    },
                },
            ],
        },
    ]

    return {
        "config": {"wide_screen_mode": True},
        "header": {
            "title": {
                "tag": "plain_text",
                "content": f"📝 Quiz | 测试 - Q{index + 1}/{total}",
            },
            "template": "orange",
        },
        "elements": elements,
    }


def answer_result_card(subject_id, chapter_id, question, index, total,
                        selected, is_correct, chapter_title_en, chapter_title_zh):
    correct_answer = question["answer"]

    if is_correct:
        result_text = f"✅ **Correct! | 正确！** You selected **{selected}**."
        template = "green"
    else:
        result_text = (
            f"❌ **Incorrect | 错误** — You selected **{selected}**, "
            f"correct answer is **{correct_answer}**.\n"
            f"你选了 **{selected}**，正确答案是 **{correct_answer}**。"
        )
        template = "red"

    elements = [
        {
            "tag": "div",
            "text": {
                "tag": "lark_md",
                "content": f"**Question {index + 1}/{total} | 第 {index + 1}/{total} 题**",
            },
        },
        {"tag": "hr"},
        {
            "tag": "div",
            "text": {
                "tag": "lark_md",
                "content": f"{question['question_en']}\n{question['question_zh']}",
            },
        },
        {"tag": "hr"},
        {
            "tag": "div",
            "text": {"tag": "lark_md", "content": result_text},
        },
        {"tag": "hr"},
        {
            "tag": "div",
            "text": {
                "tag": "lark_md",
                "content": f"**Explanation | 解析:**\n\n"
                           f"**English:** {question['explanation_en']}\n\n"
                           f"**中文:** {question['explanation_zh']}",
            },
        },
        {"tag": "hr"},
    ]

    nav_buttons = []
    if index < total - 1:
        nav_buttons.append({
            "tag": "button",
            "text": {"tag": "plain_text", "content": "➡️ Next Question | 下一题"},
            "type": "primary",
            "value": {
                "action": "quiz_question",
                "subject": subject_id,
                "chapter": chapter_id,
                "index": index + 1,
            },
        })
    else:
        nav_buttons.append({
            "tag": "button",
            "text": {"tag": "plain_text", "content": "🏁 Finish | 完成"},
            "type": "primary",
            "value": {
                "action": "select_chapter",
                "subject": subject_id,
                "chapter": chapter_id,
            },
        })

    nav_buttons.append({
        "tag": "button",
        "text": {"tag": "plain_text", "content": "📋 Menu | 菜单"},
        "type": "default",
        "value": {"action": "main_menu"},
    })

    elements.append({"tag": "action", "actions": nav_buttons})

    return {
        "config": {"wide_screen_mode": True},
        "header": {
            "title": {
                "tag": "plain_text",
                "content": "✅ Correct! | 正确！" if is_correct else "❌ Review | 错题讲解",
            },
            "template": template,
        },
        "elements": elements,
    }
