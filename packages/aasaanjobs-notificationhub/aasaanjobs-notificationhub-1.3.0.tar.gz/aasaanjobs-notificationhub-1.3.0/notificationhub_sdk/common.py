from .proto import notification_hub_pb2 as pb


class MessageType:
    MARKETING = 0
    TRANSACTIONAL = 1
    OTP = 2


class WaterfallMode:
    AUTO = 0
    OVERRIDE = 1


class Platform:
    Waahjobs = 0
    OLXPeople = 1


class ClientPlatform:
    ANDROID = 0
    IOS = 1
    WEB = 2

class Waterfall:
    """
    Initiates Waterfall object
    The priority of the channel in the task
    The time offset in seconds after which the notification should be triggered after the previous channel
    """

    def __init__(self, priority: int = 0, offset_time: int = 0):
        self._waterfall = pb.Waterfall()
        self._waterfall.priority = priority
        self._waterfall.offsetTime = offset_time

    @property
    def proto(self) -> pb.Waterfall:
        return self._waterfall


class ChatbotType:
    JOBSEARCH = 0


class AccountType:
    HSM = 0
    TWOWAY = 1


class MessageContentType:
    TEXTTYPE = 0
    HSMTYPE = 1
   
 
class DataEnconding:
    TEXTDATA = 0
    UNICODETEXTDATA = 1
