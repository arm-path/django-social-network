from .models import Chat


def create_chat(users):
    if len(users) != 2:
        raise ValueError(f'create_chat() takes exactly two argument ({self.users})')
    chat = Chat.objects.create()
    chat.users.set(users)
    chat.save()
    return chat
