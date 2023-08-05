from ..common import AccountType, DataEnconding, MessageContentType
from ..proto import notification_hub_pb2 as pb


class ChatbotWhatsapp:
    def __init__(
            self,
            account_type: AccountType = AccountType.HSM,
            message_content_type: MessageContentType = MessageContentType.TEXTTYPE,
            is_hsm: bool = False,
            is_template: bool = False,
            button_url_param: str = "",
            data_encoding: DataEnconding = DataEnconding.TEXTDATA,
            message_id: str ="",
            extra_param: str = ""
    ):
        """
        Parameters:
            account_type (AccountType, optional): account type to be used to send the msg (defaults to AccountType.HSM; other options are TWOWAY)
            message_content_type (MessageContentType, optional): message content type (defaults to MessageContentType.TEXTTYPE)
            is_hsm (bool, optional): for HSM temaplte; (defaults to False)
            is_template (bool, optional): for templated message; (defaults to False)
            button_url_param (str, optional): buttom params to send
            data_encoding (DataEnconding, optional): (defaults to DataEnconding.TEXTDATA; set UNICODETEXTDATA for the Non-English chars or Emojis)
            message_format (MessageFormat, optional): format of the message; (defaults to MessageFormat.JSON; other options are TEXT and XML)
            message_id (str, optional): for a session id
            extra_params (str, optional): additional information to send
        """
        self._chatbot_whatsapp = pb.ChatbotWhatsapp()
        self._chatbot_whatsapp.accountType = account_type
        self._chatbot_whatsapp.messageContentType = message_content_type
        self._chatbot_whatsapp.isHSM = is_hsm
        self._chatbot_whatsapp.isTemplate = is_template
        self._chatbot_whatsapp.buttonUrlParam = button_url_param
        self._chatbot_whatsapp.dataEncoding = data_encoding
        self._chatbot_whatsapp.messageID = message_id
        self._chatbot_whatsapp.extraParam = extra_param

    @property
    def proto(self) -> pb.ChatbotWhatsapp:
        return self._chatbot_whatsapp
