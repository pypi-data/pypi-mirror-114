import json

from ..common import ChatbotType
from ..proto import notification_hub_pb2 as pb
from .chatbot_whatsapp import ChatbotWhatsapp


class Chatbot:
    def __init__(
            self,
            chatbot_type: ChatbotType = ChatbotType.JOBSEARCH,
            chatbot_whatsapp: ChatbotWhatsapp = None
    ):
        """
        Parameters:
            chatbot_type (ChatbotType): Type of chatbot; defaults to ChatbotType.JOBSEARCH
            chatbot_whatsapp (ChatbotWhatsapp): Additional information related whatsapp 
        """
        self._chatbot = pb.Chatbot()
        self._chatbot.chatbotType = chatbot_type
        self.__set_chatbot_whatsapp(chatbot_whatsapp)

    def __set_chatbot_whatsapp(self, value: ChatbotWhatsapp = None):
        if not value:
            value = ChatbotWhatsapp()
        self._chatbot.chatbotWhatsapp.CopyFrom(value.proto)

    @property
    def proto(self) -> pb.Chatbot:
        return self._chatbot
