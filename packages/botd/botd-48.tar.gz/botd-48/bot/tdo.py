# This file is in the Public Domain.

"todo lists"

import ob


def __dir__():
    return ("Todo", "dne", "tdo")


k = ob.kernel()


class Todo(ob.Object):
    def __init__(self):
        super().__init__()
        self.txt = ""


def dne(event):
    if not event.args:
        event.reply("dne <string>")
        return
    s = {"txt": event.args[0]}
    db = ob.Db()
    for fn, o in db.findname("todo", s):
        o._deleted = True
        o.save()
        event.reply("ok")
        break


def tdo(event):
    if not event.rest:
        event.reply("tdo <txt>")
        return
    o = Todo()
    o.txt = event.rest
    o.save()
    event.reply("ok")
