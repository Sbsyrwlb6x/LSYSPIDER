import  redis
import json
r=redis.StrictRedis(host='localhost',port=6379,db=0)
username="xunkao973338@163.com"
password="js7105349"

SCF="Astt9vy4YqUSzeekuHDfvWMm2jtMKSRrDgR"
SSOLoginState="1493266316"
SUB="_2A250BfkADeThGeNH7FQQ8i7JyjyIHXVXCYdIrDV6PUJbkdBeLRjVkW1LupbTUcqlSan7p3cxn9oTCGyN-g.."
SUHB="0C1ScWyX0gSjex"
_T_WM="15925d9cfe4192a57ce63a4ba4d48c22"
temp={
      "SUB":SUB,
      "SUHB":SUHB,
      "_T_WM":_T_WM}
r.set("lsy_spider:Cookies:%s--%s" %  (username,password),json.dumps(temp))

username="rtt128512566@163.com"
password="eqh938ttul9"
SUB="_2A250Bfo0DeThGeNH7VUU-CzMwzWIHXVXCYZ8rDV6PUJbkdBeLVLlkW0GelGc-JSewLrV3Qb5HmQnM9G0yw.."
SUHB="0U1ZrS5uoBx9a-"
_T_WM="faaf7e742699f4c073fc2e8d90b93421"
temp={#"SCF":SCF,
      #"SSOLoginState":SSOLoginState,
      "SUB":SUB,
      #"SUBP":SUBP,
      "SUHB":SUHB,
      "_T_WM":_T_WM}
r.set("lsy_spider:Cookies:%s--%s" %  (username,password),json.dumps(temp))


username="17088529470"
password="hh001122"
SUB="_2A250Bfs0DeRhGeBP41YZ-SrFzjiIHXVXCYV8rDV6PUJbkdBeLUbekW0Cx5Vr9CjwOYcFi1wmirhHEsqFYw.."
SUHB="0sqBoTdlGP6Xq8"
_T_WM="709a05f7766dbbf8e058451a9508c8f0"
temp={#"SCF":SCF,
      #"SSOLoginState":SSOLoginState,
      "SUB":SUB,
      #"SUBP":SUBP,
      "SUHB":SUHB,
      "_T_WM":_T_WM}
r.set("lsy_spider:Cookies:%s--%s" %  (username,password),json.dumps(temp))

