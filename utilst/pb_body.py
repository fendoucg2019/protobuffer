#coding=utf-8
class pb_bodys:
    def pbbody(pbclass,data:dict):
        pb_msg=pbclass(**data)
        return pb_msg
