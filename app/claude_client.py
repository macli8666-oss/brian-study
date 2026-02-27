import anthropic
from app.config import ANTHROPIC_API_KEY

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

SYSTEM_PROMPT = """You are a bilingual (English & Chinese) tutor for A-Level (AS) Mathematics and Physics.
You help students understand concepts from CIE 9709 (Pure Math 1, Statistics 1) and CIE 9702 (AS Physics).

Rules:
1. Always respond in BOTH English and Chinese (English first, then Chinese translation).
2. Use clear, step-by-step explanations suitable for high school students.
3. Include relevant formulas and worked examples when helpful.
4. If the question is about a specific exam topic, reference the syllabus content.
5. Be encouraging and patient.

Format your response as:
**English:**
[English explanation]

**中文：**
[中文解释]
"""


def ask_question(question, context=None):
    messages = []
    if context:
        messages.append({
            "role": "user",
            "content": f"Context: The student is currently studying {context}."
        })
        messages.append({
            "role": "assistant",
            "content": "Got it, I'll help with that topic."
        })
    messages.append({"role": "user", "content": question})

    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2000,
            system=SYSTEM_PROMPT,
            messages=messages,
        )
        return response.content[0].text
    except Exception as e:
        return f"Sorry, I encountered an error: {str(e)}\n抱歉，出现了错误：{str(e)}"
