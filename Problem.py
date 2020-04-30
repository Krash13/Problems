import requests
import constants
import json
import datetime
import time

def make_request(command,data,headers):
    url=constants.server+constants.commands[command]
    if command=="read":
        req=requests.get(url,params=data, headers=headers)
    else:
        req=requests.post(url,headers=headers,data=data)
    return req.json()

class ProblemSituation():
    def __init__(self,file_name):
        try:
            with open(file_name, "r") as read_file:
                    self.problem = json.load(read_file)
        except:
            print("Файл не найден")
            exit()
        self.headers = {"Authorization": self.problem["token"]}
        self.control = {}
        for c in self.problem["case"]["controllable"]:
            self.control[c["parameter"]["tag"]]=c
        rd = []
        for c in self.problem["case"]["controllable"]:
            rd.append(c["parameter"]["tag"])

        self.modif = self.problem["case"]["modifiable"]
        self.str_rd = '['
        for i in range(len(rd)):
            self.str_rd += '"' + rd[i] + '"'
            if i != len(rd) - 1:
                self.str_rd += ","
        self.str_rd += "]"
        self.changes = []
        for param in self.modif:
            for change in param["changes"]:
                self.changes.append(
                    {"tag": param["parameter"]["tag"], "value": change["value"], "time": change["last_time"]})

    def play(self,tim):
        self.date_start=(datetime.datetime.now()-datetime.timedelta(hours=3)).strftime("%d.%m.%Y_%H:%M:%S")
        make_request("start",{"start":self.date_start},self.headers)
        sec=0
        while (sec/60<tim):
            time.sleep(1)
            sec+=1
            ch=[{"tag":change["tag"],"value":change["value"]} for change in self.changes if change["time"]==sec]
            make_request("write", json.dumps(ch),self.headers)
            req=make_request("read",{"tags":self.str_rd},self.headers)
            print(req)
            for r in req:
                if r["value"]>=self.control[r["tag"]]["bottom"] and r["value"]<=self.control[r["tag"]]["top"]:
                    pass
                else:
                    print(self.control[r["tag"]]["fail_message"])
        self.date_end = (datetime.datetime.now() - datetime.timedelta(hours=3)).strftime("%d.%m.%Y_%H:%M:%S")
        make_request("end", {"end": self.date_end}, self.headers)