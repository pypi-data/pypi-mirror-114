from time import*
from sys import*
from datetime import*
def printf(a):
    for b in a:
        sleep(0.1)
        print(b, end = '', flush=True)
    print()
def clean():
    print("\033[2J\033[00H",end="")
def logo(color):
    for x in range(len(color)):
        if color[x]=="0":
            print("\033[40m ",end="")
        elif color[x]=="1":
            print("\033[41m ",end="")
        elif color[x]=="2":
            print("\033[42m ",end="")
        elif color[x]=="3":
            print("\033[43m ",end="")
        elif color[x]=="4":
            print("\033[44m ",end="")
        elif color[x]=="5":
            print("\033[45m ",end="")
        elif color[x]=="6":
            print("\033[46m ",end="")
        elif color[x]=="7":
            print("\033[47m ",end="")
        else:
            print(color[x],end="")
    print("\033[0m")
def hello():
    h=datetime.now().hour
    if h==6 or h==7 or h==8:
        return "早上好！"
    elif h==9 or h==10:
        return "上午好！"
    elif h==11 or h==12:
        return "中午好！"
    elif h==13 or h==14 or h==15 or h==16:
        return "下午好！"
    elif h==17 or h==18:
        return "傍晚好！"
    else:
        return "晚上好！"
def works(id):
    import requests,json,time
    r=requests.get("https://code.xueersi.com/api/compilers/v2/{}?id={}".format(id,id))
    r.encoding="utf-8"
    r=r.json()
    data={
        "作品id":r["data"]["id"],
        "作者id":r["data"]["user_id"],
        "作品名":r["data"]["name"],
        "作品语言":r["data"]["lang"],
        "发布时间":r["data"]["created_at"],
        "更新时间":r["data"]["updated_at"],
        "点赞":r["data"]["likes"],
        "点踩":r["data"]["unlikes"],
        "浏览":r["data"]["views"],
        "评论":r["data"]["comments"],
        "热度":r["data"]["popular_score"]
    }
    return data
def help():
    print("Printf is used to output word by word.")
    print("Clean is used to clear terminals.")
    print("Logo is used to do logo.")
    print("Hello is used to say hello.")
    print("Works is used to find xes works.")
    print("Help is used to help you.")