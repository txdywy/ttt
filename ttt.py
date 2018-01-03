import requests
import json
import time
from Crypto.Cipher import AES
import base64
import random
game_data = dict(seed=1514949494604, action=[], musicList=[], touchList=[], version=1)
total = 10
start = 0
for i in range(total+1):
    interval = random.randrange(40,100)
    press = random.randrange(interval)
    start += interval
    game_data['action'].append([press*0.01,start*0.01,False])
    game_data['musicList'].append(False)
    game_data['touchList'].append((276+random.randrange(50),298+random.randrange(50)))
action_data = {
    "score": total,
    "times": start+5,
    "game_data": json.dumps(game_data, separators=(',',':'))
}

"""
action_data = {
    "score": score,
    "times": int(score/5),
    "game_data": "{}" 
}
"""

session_id = "MKOEO5JyKFWwWjEC7y4zlVQxWHvUUvrFmW+ILYoDDDaMz2HphvDurRnjb8NMdeeLB1OfKCmFSWhC4J45lk11beciq8wrqQmQQM6bSQ+WbdFU2XB6joxq//breRPVtiAbb5l2DvPk/Q1kDROBUmTbdw\u003d\u003d"
 
#"fXTXtN/eD6bxCe93FVLZQYu7h3oscKcJ9dwHoaVCHBt6yNv/ITYh+mAhNHvDDiaCdCVs/8I0UZymW0vQPEEgQpZECGfAYl3ILbbDa4Gp4V4SZqrnQ+EIX/k0ZZ8mZmjwlD1kK8M8X5Lz41CTF81hFw=="
#"kPHXqRdD5VO2nVvhz0Xti2U382l0mY0+mDZUY5nvQHhLWesG2ECCdQHzQpSFbNXdkU/DO3l4Wprb8FjVrIislVpsp9UzdEmrdnagv8ZzDN1khKqqOrW9oxy69Q6cwf7In+JxYl1xBsRgS/elxOeXZA==" 

aes_key = session_id[0:16]
aes_iv  = aes_key

cryptor = AES.new(aes_key, AES.MODE_CBC, aes_iv)

str_action_data = json.dumps(action_data).encode("utf-8")
print("json_str_action_data ", str_action_data)

#Pkcs7
length = 16 - (len(str_action_data) % 16)
str_action_data += bytes([length])*length

cipher_action_data = base64.b64encode(cryptor.encrypt(str_action_data)).decode("utf-8")
print("action_data ", cipher_action_data)

post_data = {
  "base_req": {
    "session_id": session_id,
    "fast": 1,
  },
  "action_data": cipher_action_data
}

headers = {
    "charset": "utf-8",
    "Accept-Encoding": "gzip",
    "referer": "https://servicewechat.com/wx7c8d593b2c3a7703/3/page-frame.html",
    "content-type": "application/json",
    "User-Agent": "MicroMessenger/6.6.1.1200(0x26060130) NetType/WIFI Language/zh_CN",
    "Content-Length": "0",
    "Host": "mp.weixin.qq.com",
    "Connection": "Keep-Alive"
}

url = "https://mp.weixin.qq.com/wxagame/wxagame_settlement"


response = requests.post(url, json=post_data, headers=headers)
print(json.loads(response.text))
