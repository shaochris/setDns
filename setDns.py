#!/usr/bin/env python3
import os, subprocess
import threading, time, concurrent.futures

hostip = [
            "208.67.222.222",           # Open DNS
            "208.67.220.220",
            "1.1.1.1",                  # CloudFlare
            "1.0.0.1",
            "8.8.8.8",                  # Google
            "8.8.4.4",
           # "199.85.126.10",            # Norton ConnectSafe
           # "199.85.127.10",
            "9.9.9.9",                  # Quad9
            "149.112.112.112",
            # "64.6.64.6",                # Verisign
            # "64.6.65.6",
            # "223.5.5.5",  # Ali
            # "223.6.6.6",

            # "119.29.29.29", # tencent
            # "119.28.28.28"
          ]


m = {}
m[hostip[0]] = hostip[1]
m[hostip[2]] = hostip[3]
m[hostip[4]] = hostip[5]
m[hostip[6]] = hostip[7]
# m[hostip[8]] = hostip[9]
# m[hostip[10]] = hostip[11]

# hostip_china = [  "223.5.5.5",  #Ali
#                   "223.6.6.6",
#                   "119.29.29.29", # tencent
#                   "119.28.28.28",
#                   "114.114.114.114", #
#                   "114.114.115.115"
#                 ]

# for i in m.keys():
# 	print(i)
comp = {}
def ping_host(ip):
  # global comp
  response = subprocess.check_output(['ping', '-c','10', '-q', ip])
  args = response.split()
  t = (args[-2].decode()).split('/')
  # print(t)
  comp[ip] = t[1]

with concurrent.futures.ThreadPoolExecutor() as executor:
  executor.map(ping_host, m.keys())

speed = []
sorted_x = sorted(comp.items(), key = lambda kv:kv[1])
for x in sorted_x[:3]:
  speed.append(x)


# print(speed)
# comp_china = {}
# # for ip in hostip_china:
# def ping_host_china(ip):
#   response = subprocess.check_output(['ping', '-c','10','-q', ip])
#   args = response.split()
#   t = (args[-2].decode()).split('/')
#   comp_china[ip] = t[1]

# with concurrent.futures.ThreadPoolExecutor() as executor:
#   executor.map(ping_host_china, hostip_china)

# sorted_x = sorted(comp_china.items(), key = lambda kv:kv[1])
# speed_china = []
# for x in sorted_x[:2]:
#   speed_china.append(x)
#



second_response = subprocess.check_output(['ping', '-c','1', '-q', m[speed[0][0]]])
second_args = second_response.split()
second_t = (second_args[-2].decode()).split('/')[1]


if float(speed[0][1]) < float(second_t):

  cmd = "networksetup -setdnsservers Wi-Fi " + str(speed[0][0]) + " " + str(m[speed[0][0]]) + " " + str(speed[1][0])

  if os.system(cmd) == 0:
    print("set primary dns server to " + str(speed[0][0]) + " response in " + str(speed[0][1]) + "ms")
    print("set secondary dns server to "+ str(m[speed[0][0]]) + " response in " + str(second_t) + "ms")
    print("set fallback dns server to "+ str(speed[1][0]) + " response in " + str(speed[1][1]) + "ms")
  else:
    print("fail to set dns")

else:
  cmd = "networksetup -setdnsservers Wi-Fi " + str(m[speed[0][0]]) + " " + str(speed[0][0]) + " " + str(speed[1][0])
  if os.system(cmd) == 0:
    print("set primary dns server to " +
          str(m[speed[0][0]]) + " response in " + str(second_t) + "ms")
    print("set secondary dns server to " +
          str(speed[0][0]) + " response in " + str(speed[0][1]) + "ms")
    print("set fallback dns server to " +
          str(speed[1][0]) + " response in " + str(speed[1][1]) + "ms")
  else:
    print("fail to set dns")

