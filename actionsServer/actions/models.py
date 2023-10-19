import requests
import json
from typing import List, Any

def callGpt(
        userText: str,
        messages: List[Any],
        temperature: float = 0.3,
        max_tokens: int = 250
    ) -> str:
    url: str = f"https://model.hsueh.tw/callapi/chatGPT?temperature={temperature}&max_tokens={max_tokens}&top_p=1&purpose=none"
    payload = json.dumps(messages)
    headers = {
        'Content-Type': 'application/json',
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    try:
        return str(response.json()['choices'][0]['message']['content'])
    except:
        return "ERROR:"+str(response.text)


def callGPT_finetuneQuestion(userText: str) -> str:
        return callGpt(userText, [
                {
                    "role": "system",
                    "content": """
                    你唯一要做的事是優化使用者的問題，你負責將使用者的問題優化為另一個問題，請理解使用者的問題後提出更明確的問題，記住不要對使用者的問題進行回答。
                    例如，使用者輸入"光合作用"，優化為"植物如何進行光合作用?"
                    """
                },
                {"role": "user", "content": "蜘蛛 八隻腳"},
                {"role": "assistant", "content": "請問蜘蛛是八隻腳嗎"},
                {"role": "user", "content": userText}
        ],0.3)

def callGPT_AnswerQuestion(userText: str) -> str:
        return callGpt(userText, [
                {
                    "role": "system",
                    "content": """
                    我們是一個自然科的討論課程，你是這堂課的教師，你負責回應學生的問題，請理解學生的問題後提出明確的。
                    切記我們不提出自然以外的內容，所有確保回應維持在自然領域之中，並在200個字內回答問題。
                    """
                },
                {"role": "user", "content": "請問蜘蛛是八隻腳嗎"},
                {"role": "assistant", "content": "不是，大多數的蜘蛛是六隻腳"},
                {"role": "user", "content": userText}
        ],0.7)

def callGPT_CheckQuestion(userText: str) -> str:
        return callGpt(userText, [
                {
                    "role": "system",
                    "content": """
                    你唯一要做的事情是判斷使用者的訊息是否為「問題」，若是使用者的訊息不是「問題」，只回覆「否」即可，不回覆其他訊息；若是使用者的訊息是「問題」，只回覆「是」即可，不回覆其他訊息。
                    """
                },
                {"role": "user", "content": userText}
        ],0.7, 1)

def callGPT_CheckTopic(userText: str) -> str:
        return callGpt(userText, [
                {
                    "role": "system",
                    "content": """
                    你只知道關於「植物」的知識，你唯一要做的事情是判斷使用者的提問是否與「植物」有關係，若是使用者提出與「植物」無關的內容，只回覆「否」即可，不回覆其他訊息；若是使用者提出與「植物」相關的內容，只回覆「是」即可，不回覆其他訊息。
                    例如當使用者提出「昆蟲有幾隻腳?」，因為與「植物」無關，所以回覆「否」；當使用者提出「維管束是什麼?」，因為與「植物」有關，所以回覆「是」。
                    """
                },
                {"role": "user", "content": userText}
        ],0.7, 1)