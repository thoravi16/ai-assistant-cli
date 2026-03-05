conversation = []

def add(role, content):
    conversation.append({"role": role, "content": content})


def get(limit=10):
    return conversation[-limit:]


def clear():
    conversation.clear()


def history():
    return conversation