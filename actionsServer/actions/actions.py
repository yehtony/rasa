# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from rasa_sdk.events import SlotSet
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from .models import callGPT_finetuneQuestion, callGPT_AnswerQuestion, callGPT_CheckQuestion, callGPT_CheckTopic

class RefactorQuestion(Action):

    def name(self) -> Text:
        return "action_refactor_question"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # text_latest_message=f"text_latest_message: {tracker.latest_message}
        slotNewQuestion = tracker.get_slot('newQuestion')
        userContent = tracker.latest_message['text']
        # dispatcher.utter_message(text="get_slot(newQuestion): "+str(slotNewQuestion))
        # dispatcher.utter_message(text="get_slot(newQuestion): "+str(userContent))

        # dispatcher.utter_message(text=f"text_latest_message"+text_latest_message)
        gptResponse = callGPT_finetuneQuestion(userContent)
        dispatcher.utter_message(text=gptResponse)
        return [
            SlotSet("newQuestion", gptResponse)
        ]

class AnswerQuestion(Action):

    def name(self) -> Text:
        return "action_answer_question"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # text_latest_message=f"text_latest_message: {tracker.latest_message}
        slotNewQuestion = tracker.get_slot('newQuestion')
        userContent = tracker.latest_message['text']

        #
        if slotNewQuestion is None or slotNewQuestion=="":
            dispatcher.utter_message(text="我不明白您的意思，請提出一個問題")
            return []

        #
        gptResponse = callGPT_AnswerQuestion(slotNewQuestion)
        dispatcher.utter_message(text=gptResponse)
        return [
            SlotSet("newQuestion", "")
        ]

class ActionCheckQuestion(Action):
    def name(self):
        return "action_check_question"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
    
        userContent = tracker.latest_message["text"]

        
        gpt_response = callGPT_CheckQuestion(userContent)

        
        is_related = gpt_response == "是"

        
        return [SlotSet("questionCheck", is_related )]
    
class ActionCheckTopic(Action):
    def name(self):
        return "action_check_topic"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
    
        userContent = tracker.latest_message["text"]

        # 调用GPT模型来检测用户的问题是否与植物主题相关
        gpt_response = callGPT_CheckTopic(userContent)

        # 根据模型的响应来确定是否与植物主题相关
        is_related = gpt_response == "是" 

        # 设置槽位的值，用于在对话中跟踪相关性
        return [SlotSet("topicCheck", is_related)]