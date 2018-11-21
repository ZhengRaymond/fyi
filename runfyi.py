import sys
import json
import os
from copy import copy
import subprocess

DIR = sys.path[0] + "/"
f = open(DIR + "messages", "w+")
filecontents = f.read()
if filecontents == "":
    filecontents = "{}"
contents = json.loads(filecontents)
f.close()

HELPMSG = """
\t <NO_ARGS> print all
\t fyi help
\t fyi add key key ... key value
\t fyi add_group
\t fyi key key ... key
"""

def process():
    args = sys.argv
   
    if len(args) == 1:
        process_fetch([])
    elif args[1] == "help":
        print(HELPMSG)
    elif args[1] == '-x' or args[1] == '--execute':
        process_execute(args)
    elif args[1] == "add":
        process_add(args[2:])
    elif args[1] == "addgroup":
        process_add_group(args[2:])
    elif args[1] == "del":
        process_del(args[2:])
    elif args[1] == "delgroup":
        process_del_group(args[2:])
    else:
        process_fetch(args[1:])
    messageFiles = filter(lambda f: f[:8] == "messages" and f != "messages", os.listdir(DIR))
    messageFiles = [(int(messageFile[messageFile.find(".") + 1:]), messageFile) for messageFile in messageFiles]
    messageFiles = list(reversed(sorted(messageFiles)))[-100:]
    for fileNum, messageFile in messageFiles:
        newMessageFile = "messages." + str(fileNum + 1)
        os.rename(DIR + messageFile, DIR + newMessageFile)
    os.rename(DIR + "messages", DIR + "messages.1")

    w = open(DIR + "messages", 'w')
    w.write(json.dumps(contents))
    w.close()

def process_add_group(keys):
    current = contents
    for key in keys:
        if key not in current:
            current[key] = {}
            current[key]["messages"] = []
        current = current[key]
    return 0

def process_add(keys):
    current = contents
    for key in keys[:-1]:
        current = current[key]
    current["messages"].append(keys[-1])
    return 0

def process_del_group(keys):
    current = contents
    for key in keys[:-1]:
        current = current[key]
    if len(key[current]["messages"]) != 0:
        print("Could not delete key {}, key.messages contains {} messages.".format(key, len(key[current]["messages"])))
    else:
        del key[current]
    return 0

def process_del(keys):
    current = contents
    for key in keys[:-1]:
        current = current[key]
    msgIndx = int(keys[-1])
    current["messages"] = current["messages"][:msgIndx] + current["messages"][msgIndx + 1:]
    return 0

def process_fetch(keys):
    current = contents
    if len(keys) > 0 and keys[-1].isdigit():
        msgIndx = int(keys[-1])
        for key in keys[:-1]:
            current = current[key]
        msg = current["messages"][msgIndx]
        print(msg)
        return msg
    else:
        for key in keys:
            current = current[key]
        print(json.dumps(current, indent = 4, sort_keys = True))
        return None
    
def process_execute(args):
    msg = process_fetch(args[2:])
    process = subprocess.Popen(msg.split())

process()

