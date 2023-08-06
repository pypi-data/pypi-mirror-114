class UserProfileList:
    def __init__(self, data):
        self.json = data

        self.userId = []
        self.username = []
        self.photo = []
        self.screenName = []
        self.isOnline = []

    @property
    def UserProfileList(self):
        for x in self.json:
            try: x = x["user"]
            except: pass
            try: self.userId.append(x["user_id"])
            except (KeyError, TypeError): self.userId.append(None)
            try: self.username.append(x["name"])
            except (KeyError, TypeError): self.username.append(None)
            try: self.photo.append(x["photo"])
            except (KeyError, TypeError): self.photo.append(None)
            try: self.screenName.append(x["screen_name"])
            except (KeyError, TypeError): self.screenName.append(None)
            try: self.isOnline.append(x["online"])
            except (KeyError, TypeError): self.isOnline.append(None)
        return self


class UserProfile:
    def __init__(self, data):
        self.json = data

        self.userId = None
        self.name = None
        self.photo = None
        self.screenName = None
        self.online = None

    @property
    def UserProfile(self):
        try: self.userId = self.json["user_id"]
        except (KeyError, TypeError): pass
        try: self.name = self.json["name"]
        except (KeyError, TypeError): pass
        try: self.photo = self.json["photo"]
        except (KeyError, TypeError): pass
        try:self.screenName = self.json["screen_name"]
        except (KeyError, TypeError): pass
        try:self.online = self.json["online"]
        except (KeyError, TypeError): pass
        return self


class Message:
    def __init__(self, data):
        self.json = data

        self.author: UserProfile = UserProfile(data["author"]).UserProfile
        self.messageId = None
        self.date = None
        self.text = None
        self.views = None

    @property
    def Message(self):
        try: self.messageId = self.json["message_id"]
        except (KeyError, TypeError): pass
        try: self.date = self.json["date"]
        except (KeyError, TypeError): pass
        try: self.text = self.json["text"]
        except (KeyError, TypeError): pass
        try: self.views = self.json["views"]
        except (KeyError, TypeError): pass
        return self


class Topic:
    def __init__(self, data):
        self.json = data

        self.topicId = None
        self.type = None
        self.membersCount = None
        self.title = None
        self.description = None
        self.photo = None
        self.link = None
        self.admin = None
        self.updated = None
        self.screenName = None

    @property
    def Topic(self):
        try: self.topicId = self.json["topic_id"]
        except (KeyError, TypeError): pass
        try: self.type = self.json["type"]
        except (KeyError, TypeError): pass
        try: self.membersCount = self.json["members_count"]
        except (KeyError, TypeError): pass
        try: self.title = self.json["name"]
        except (KeyError, TypeError): pass
        try: self.description = self.json["description"]
        except (KeyError, TypeError): pass
        try: self.photo = self.json["photo"]
        except (KeyError, TypeError): pass
        try: self.link = self.json["link"]
        except (KeyError, TypeError): pass
        try: self.admin = self.json["admin"]
        except (KeyError, TypeError): pass
        try: self.updated = self.json["updated"]
        except (KeyError, TypeError): pass
        try: self.screenName = self.json["screen_name"]
        except (KeyError, TypeError): pass
        return self


class MessagesInfo:
    def __init__(self, data):
        _author, _replyMessage = [], []
        self.json = data

        for y in data:
            try: _author.append(y["author"])
            except (KeyError, TypeError): _author.append(None)

        self.author: UserProfileList = UserProfileList(_author).UserProfileList
        self.messageId = []
        self.date = []
        self.text = []
        self.views = []

    @property
    def MessagesInfo(self):
        for x in self.json:
            try: self.messageId.append(x["message_id"])
            except (KeyError, TypeError): self.messageId.append(None)
            try: self.date.append(x["date"])
            except (KeyError, TypeError): self.date.append(None)
            try: self.text.append(x["text"])
            except (KeyError, TypeError): self.text.append(None)
            try:self.views.append(x["views"])
            except (KeyError, TypeError):self.views.append(None)
        return self


class PhotoList:
    def __init__(self, data):
        self.json = data

        self.photoId = []
        self.photo = []
        self.width = []
        self.height = []

    @property
    def PhotoList(self):
        for x in self.json:
            try:
                for x in x:
                    try: self.photoId.append(x["photo_id"])
                    except (KeyError, TypeError): self.photoId.append(None)
                    try: self.photo.append(x["photo"])
                    except (KeyError, TypeError): self.photo.append(None)
                    try: self.width.append(x["width"])
                    except (KeyError, TypeError): self.width.append(None)
                    try: self.height.append(x["height"])
                    except (KeyError, TypeError): self.height.append(None)
            except: pass
        return self


class MessageList:
    def __init__(self, data):
        _author, _replyMessage, _photos = [], [], []
        self.json = data

        for y in data:
            try: _author.append(y["author"])
            except (KeyError, TypeError): _author.append(None)
            try: _replyMessage.append(y["quoted"])
            except (KeyError, TypeError): _replyMessage.append(None)
            try: _photos.append(y["photos"])
            except (KeyError, TypeError): _photos.append(None)

        try:
            _photos, _replyMessage, _author = [], [], []
            for y in data:
                for y in y:
                    try: _photos.append(y["photos"])
                    except (KeyError, TypeError): _photos.append(None)
                    try: _author.append(y["author"])
                    except (KeyError, TypeError): _author.append(None)
                    try: _replyMessage.append(y["quoted"])
                    except (KeyError, TypeError): _replyMessage.append(None)
        except: pass

        self.author: UserProfileList = UserProfileList(_author).UserProfileList
        self.replyMessage: MessagesInfo = MessagesInfo(_replyMessage).MessagesInfo
        self.photos: PhotoList = PhotoList(_photos).PhotoList
        self.messageId = []
        self.date = []
        self.text = []
        self.views = []

    @property
    def MessageList(self):
        for x in self.json:
            try: self.messageId.append(x["message_id"])
            except (KeyError, TypeError): self.messageId.append(None)
            try: self.date.append(x["date"])
            except (KeyError, TypeError): self.date.append(None)
            try: self.text.append(x["text"])
            except (KeyError, TypeError): self.text.append(None)
            try: self.views.append(x["views"])
            except (KeyError, TypeError): self.views.append(None)
        return self


class TopicList:
    def __init__(self, data):
        _messages = []
        self.json = data

        for y in data:
            try: _messages.append(y["messages"])
            except (KeyError, TypeError): pass

        self.messages: MessageList = MessageList(_messages).MessageList
        self.topicId = []
        self.type = []
        self.membersCount = []
        self.title = []
        self.description = []
        self.photo = []
        self.link = []
        self.admin = []
        self.updated = []
        self.screenName = []
        self.role = []

    @property
    def TopicList(self):
        for x in self.json:
            try: x = x["topic"]
            except: pass
            try: self.topicId.append(x["topic_id"])
            except (KeyError, TypeError): self.topicId.append(None)
            try: self.type.append(x["type"])
            except (KeyError, TypeError): self.type.append(None)
            try: self.membersCount.append(x["members_count"])
            except (KeyError, TypeError): self.membersCount.append(None)
            try: self.title.append(x["name"])
            except (KeyError, TypeError): self.title.append(None)
            try: self.description.append(x["description"])
            except: self.description.append(None)
            try: self.photo.append(x["photo"])
            except (KeyError, TypeError): self.photo.append(None)
            try: self.link.append(x["link"])
            except (KeyError, TypeError): self.link.append(None)
            try: self.admin.append(x["admin"])
            except (KeyError, TypeError): self.admin.append(None)
            try: self.updated.append(x["updated"])
            except (KeyError, TypeError): self.updated.append(None)
            try: self.screenName.append(x["screen_name"])
            except (KeyError, TypeError): self.screenName.append(None)
            try: self.role.append(x["role"])
            except (KeyError, TypeError): self.role.append(None)
        return self


class NewAcc:
    def __init__(self, data):
        self.json = data

        self.token = None
        self.userId = None
        self.name = None
        self.photo = None
        self.screenName = None
        self.online = None
        self.new = None

    @property
    def NewAcc(self):
        try: self.token = self.json["token"]
        except (KeyError, TypeError): pass
        try: self.userId = self.json["user"]["user_id"]
        except (KeyError, TypeError): pass
        try: self.name = self.json["user"]["name"]
        except (KeyError, TypeError): pass
        try: self.photo = self.json["user"]["photo"]
        except (KeyError, TypeError): pass
        try: self.screenName = self.json["user"]["screen_name"]
        except (KeyError, TypeError): pass
        try: self.online = self.json["user"]["online"]
        except (KeyError, TypeError): pass
        try: self.new= self.json["new"]
        except (KeyError, TypeError): pass
        return self


class Notifications:
    def __init__(self, data):
        _topics, _messages = [], []
        self.json = data

        for y in data:
            try: _messages.append(y["message"])
            except (KeyError, TypeError): _messages.append(None)
            try: _topics.append(y["topic"])
            except (KeyError, TypeError): _topics.append(None)

        self.messages: MessagesInfo = MessagesInfo(_messages).MessagesInfo
        self.topics: TopicList = TopicList(_topics).TopicList

        self.notId = []
        self.type = []
        self.count = []
        self.date = []

    @property
    def Notifications(self):
        for x in self.json:
            try: self.notId.append(x["id"])
            except (KeyError, TypeError): self.notId.append(None)
            try: self.type.append(x["type"])
            except (KeyError, TypeError): self.type.append(None)
            try: self.count.append(x["count"])
            except (KeyError, TypeError): self.count.append(None)
            try: self.date.append(x["date"])
            except (KeyError, TypeError): self.date.append(None)
        return self
