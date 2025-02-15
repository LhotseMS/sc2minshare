from sc2reader.events.base import Event
from sc2reader.utils import Length
from sc2reader.log_utils import loggable


@loggable
class MessageEvent(Event):
    """
    Parent class for all message events.
    """

    def __init__(self, frame, pid):
        #: The user id (or player id for older replays) of the person that generated the event.
        self.pid = pid

        #: The frame of the game this event was applied
        self.frame = frame

        #: The second of the game (game time not real time) this event was applied
        self.second = self.frame / 22.4 #frame >> 4

        #: Short cut string for event class name
        self.name = self.__class__.__name__
    
    def _str_prefix(self):
        return f"{Length(seconds=int(self.frame / 22.4))}\t "
        #player_name = self.player.name if getattr(self, "pid", 16) != 16 else "Global"
        #return f"{Length(seconds=int(self.frame / 22.4))}\t{player_name:<15} "

    def __str__(self):
        return self._str_prefix() + self.name


@loggable
class ChatEvent(MessageEvent):
    """
    Records in-game chat events.
    """

    def __init__(self, frame, pid, target, text):
        super().__init__(frame, pid)
        #: The numerical target type. 0 = to all; 2 = to allies; 4 = to observers.
        self.target = target

        #: The text of the message.
        self.text = text

        #: Flag marked true of message was to all.
        self.to_all = self.target == 0

        #: Flag marked true of message was to allies.
        self.to_allies = self.target == 2

        #: Flag marked true of message was to observers.
        self.to_observers = self.target == 4

    def __str__(self):
        return super().__str__() + ":" + self.text


@loggable
class ProgressEvent(MessageEvent):
    """
    Sent during the load screen to update load process for other clients.
    """

    def __init__(self, frame, pid, progress):
        super().__init__(frame, pid)

        #: Marks the load progress for the player. Scaled 0-100.
        self.progress = progress


@loggable
class PingEvent(MessageEvent):
    """
    Records pings made by players in game.
    """

    def __init__(self, frame, pid, target, x, y):
        super().__init__(frame, pid)

        #: The numerical target type. 0 = to all; 2 = to allies; 4 = to observers.
        self.target = target

        #: Flag marked true of message was to all.
        self.to_all = self.target == 0

        #: Flag marked true of message was to allies.
        self.to_allies = self.target == 2

        #: Flag marked true of message was to observers.
        self.to_observers = self.target == 4

        #: The x coordinate of the target location
        self.x = x

        #: The y coordinate of the target location
        self.y = y

        #: The (x,y) coordinate of the target location
        self.location = (self.x, self.y)
