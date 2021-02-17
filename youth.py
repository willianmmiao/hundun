#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

# 此脚本参考 https://github.com/Sunert/Scripts/blob/master/Task/youth.js
from util import *
import traceback
import time
import re
import json
import sys
import os

p=os.path.dirname(os.path.dirname((os.path.abspath(__file__))))
if p not in sys.path:
    sys.path.append(p)
from util import send, requests_session
from datetime import datetime, timezone, timedelta

# YOUTH_HEADER 为对象, 其他参数为字符串，自动提现需要自己抓包
# 选择微信提现30元，立即兑换，在请求包中找到withdraw2的请求，拷贝请求body类型 p=****** 的字符串，放入下面对应参数即可
cookies1 = {
  'YOUTH_HEADER': '',
  'YOUTH_READBODY': '',
  'YOUTH_REDBODY': '',
  'YOUTH_READTIMEBODY': '',
  'YOUTH_WITHDRAWBODY': ''
}
cookies2 = {}

COOKIELIST = [cookies1,]  # 多账号准备

# ac读取环境变量
if "YOUTH_HEADER1" in os.environ:
  COOKIELIST = []
  for i in range(5):
    headerVar = 'YOUTH_HEADER{a)}'.format(a = str(i+1))
    readBodyVar = 'YOUTH_READBODY{a}'.format(a =str(i+1))
    redBodyVar = 'YOUTH_REDBODY{a}'.format(a =str(i+1))
    readTimeBodyVar = 'YOUTH_READTIMEBODY{a}'.format(a =str(i+1))
    withdrawBodyVar = 'YOUTH_WITHDRAWBODY{a}'.format(a =str(i+1))
    if headerVar in os.environ and os.environ[headerVar] and readBodyVar in os.environ and os.environ[readBodyVar] and redBodyVar in os.environ and os.environ[redBodyVar] and readTimeBodyVar in os.environ and os.environ[readTimeBodyVar]:
      globals()['cookies'+str(i + 1)]["YOUTH_HEADER"] = json.loads(os.environ[headerVar])
      globals()['cookies'+str(i + 1)]["YOUTH_READBODY"] = os.environ[readBodyVar]
      globals()['cookies'+str(i + 1)]["YOUTH_REDBODY"] = os.environ[redBodyVar]
      globals()['cookies' + str(i + 1)]["YOUTH_READTIMEBODY"] = os.environ[readTimeBodyVar]
      globals()['cookies' + str(i + 1)]["YOUTH_WITHDRAWBODY"] = os.environ[withdrawBodyVar]
      COOKIELIST.append(globals()['cookies'+str(i + 1)])
  print(COOKIELIST)

cur_path = os.path.abspath(os.path.dirname(__file__))
root_path = os.path.split(cur_path)[0]
sys.path.append(root_path)
YOUTH_HOST = "https://kd.youth.cn/WebApi/"

def get_standard_time():
  """
  获取utc时间和北京时间
  :return:
  """
  # <class 'datetime.datetime'>
  utc_datetime = datetime.utcnow().replace(tzinfo=timezone.utc)  # utc时间
  beijing_datetime = utc_datetime.astimezone(timezone(timedelta(hours=8)))  # 北京时间
  return beijing_datetime

def pretty_dict(dict):
    """
    格式化输出 json 或者 dict 格式的变量
    :param dict:
    :return:
    """
    return print(json.dumps(dict, indent=4, ensure_ascii=False))

def sign(headers):
  """
  签到
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = 'https://kd.youth.cn/TaskCenter/sign'
  try:
    response = requests_session().post(url=url, headers=headers, timeout=30).json()
    print('签到')
    print(response)
    if response['status'] == 1:
      return response
    else:
      return
  except:
    print(traceback.format_exc())
    return

def signInfo(headers):
  """
  签到详情
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = 'https://kd.youth.cn/TaskCenter/getSign'
  try:
    response = requests_session().post(url=url, headers=headers, timeout=30).json()
    print('签到详情')
    print(response)
    if response['status'] == 1:
      return response['data']
    else:
      return
  except:
    print(traceback.format_exc())
    return

def punchCard(headers):
  """
  打卡报名
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = '{b}PunchCard/signUp'.format(b = YOUTH_HOST)
  try:
    response = requests_session().post(url=url, headers=headers, timeout=30).json()
    print('打卡报名')
    print(response)
    if response['code'] == 1:
      return response
    else:
      return
  except:
    print(traceback.format_exc())
    return

def doCard(headers):
  """
  早起打卡
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = '{b}PunchCard/doCard'.format(b = YOUTH_HOST)
  try:
    response = requests_session().post(url=url, headers=headers, timeout=30).json()
    print('早起打卡')
    print(response)
    if response['code'] == 1:
      shareCard(headers=headers)
      return response['data']
    else:
      return
  except:
    print(traceback.format_exc())
    return

def shareCard(headers):
  """
  打卡分享
  :param headers:
  :return:
  """
  time.sleep(0.3)
  startUrl = '{b}PunchCard/shareStart'.format(b = YOUTH_HOST)
  endUrl = '{b}PunchCard/shareEnd'.format(b = YOUTH_HOST)
  try:
    response = requests_session().post(url=startUrl, headers=headers, timeout=30).json()
    print('打卡分享')
    print(response)
    if response['code'] == 1:
      time.sleep(0.3)
      responseEnd = requests_session().post(url=endUrl, headers=headers, timeout=30).json()
      if responseEnd['code'] == 1:
        return responseEnd
    else:
      return
  except:
    print(traceback.format_exc())
    return

def luckDraw(headers):
  """
  打卡分享
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = '{b}PunchCard/luckdraw'.format(b = YOUTH_HOST)
  try:
    response = requests_session().post(url=url, headers=headers, timeout=30).json()
    print('七日签到')
    print(response)
    if response['code'] == 1:
      return response['data']
    else:
      return
  except:
    print(traceback.format_exc())
    return

def shareArticle(headers):
  """
  分享文章
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = 'https://focu.youth.cn/article/s?signature=QqvZWbEKpA2yrNR1MnyjPetpZpz2TLdDDw849VGjJl8gXB5keP&uid=52242968&phone_code=4aa0b274198dafebe5c214ea6097d12b&scid=35438728&time=1609414747&app_version=1.8.2&sign=17fe0351fa6378a602c2afd55d6a47c8'
  readUrl = 'https://focus.youth.cn/article/s?signature=QqvZWbEKpA2yrNR1MnyjPetpZpz2TLdDDw849VGjJl8gXB5keP&uid=52242968&phone_code=4aa0b274198dafebe5c214ea6097d12b&scid=35438728&time=1609414747&app_version=1.8.2&sign=17fe0351fa6378a602c2afd55d6a47c8'
  try:
    response1 = requests_session().post(url=url, headers=headers, timeout=30)
    print('分享文章1')
    print(response1)
    time.sleep(0.3)
    response2 = requests_session().post(url=readUrl, headers=headers, timeout=30)
    print('分享文章2')
    print(response2)
    return
  except:
    print(traceback.format_exc())
    return

def openBox(headers):
  """
  开启宝箱
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = '{b}invite/openHourRed'.format(b = YOUTH_HOST)
  try:
    response = requests_session().post(url=url, headers=headers, timeout=30).json()
    print('开启宝箱')
    print(response)
    if response['code'] == 1:
      share_box_res = shareBox(headers=headers)
      return response['data']
    else:
      return
  except:
    print(traceback.format_exc())
    return

def shareBox(headers):
  """
  宝箱分享
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = '{b}invite/shareEnd'.format(b= YOUTH_HOST)
  try:
    response = requests_session().post(url=url, headers=headers, timeout=30).json()
    print('宝箱分享')
    print(response)
    if response['code'] == 1:
      return response['data']
    else:
      return
  except:
    print(traceback.format_exc())
    return

def friendList(headers):
  """
  好友列表
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = '{b}ShareSignNew/getFriendActiveList'.format(b = YOUTH_HOST)
  try:
    response = requests_session().get(url=url, headers=headers, timeout=30).json()
    print('好友列表')
    print(response)
    if response['error_code'] == '0':
      if len(response['data']['active_list']) > 0:
        for friend in response['data']['active_list']:
          if friend['button'] == 1:
            time.sleep(1)
            friendSign(headers=headers, uid=friend['uid'])
      return response['data']
    else:
      return
  except:
    print(traceback.format_exc())
    return

def friendSign(headers, uid):
  """
  好友签到
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = '{b}ShareSignNew/sendScoreV2?friend_uid={uid}'.format(b = YOUTH_HOST,c=uid)
  try:
    response = requests_session().get(url=url, headers=headers, timeout=30).json()
    print('好友签到')
    print(response)
    if response['error_code'] == '0':
      return response['data']
    else:
      return
  except:
    print(traceback.format_exc())
    return

def sendTwentyScore(headers, action):
  """
  每日任务
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = '{b}NewTaskIos/sendTwentyScore?{popo}&action={d}'.format(b = YOUTH_HOST,popo = headers["Referer"].split("?")[1],d=action)
  try:
    response = requests_session().get(url=url, headers=headers, timeout=30).json()
    print('每日任务 {}'.format(action))
    print(response)
    if response['status'] == 1:
      return response
    else:
      return
  except:
    print(traceback.format_exc())
    return

def watchAdVideo(headers):
  """
  看广告视频
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = 'https://kd.youth.cn/taskCenter/getAdVideoReward'
  headers['Content-Type'] = 'application/x-www-form-urlencoded;charset=utf-8'
  try:
    response = requests_session().post(url=url, data="type=taskCenter", headers=headers, timeout=30).json()
    print('看广告视频')
    print(response)
    if response['status'] == 1:
      return response
    else:
      return
  except:
    print(traceback.format_exc())
    return

def watchGameVideo(body):
  """
  激励视频
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = 'https://ios.baertt.com/v5/Game/GameVideoReward.json'
  headers = {'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'}
  try:
    response = requests_session().post(url=url, headers=headers, data=body, timeout=30).json()
    print('激励视频')
    print(response)
    if response['success'] == True:
      return response['items']
    else:
      return
  except:
    print(traceback.format_exc())
    return

def visitReward(body):
  """
  回访奖励
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = 'https://ios.baertt.com/v5/mission/msgRed.json'
  headers = {
    'User-Agent': 'KDApp/1.8.0 (iPhone; iOS 14.2; Scale/3.00)',
    'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'
  }
  try:
    response = requests_session().post(url=url, data=body, headers=headers, timeout=30).json()
    print('回访奖励')
    print(response)
    if response['success'] == True:
      return response['items']
    else:
      return
  except:
    print(traceback.format_exc())
    return

def articleRed(body):
  """
  惊喜红包
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = 'https://ios.baertt.com/v5/article/red_packet.json'
  headers = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
    'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'
  }
  try:
    response = requests_session().post(url=url, data=body, headers=headers, timeout=30).json()
    print('惊喜红包')
    print(response)
    if response['success'] == True:
      return response['items']
    else:
      return
  except:
    print(traceback.format_exc())
    return

def readTime(body):
  """
  阅读时长
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = 'https://ios.baertt.com/v5/user/stay.json'
  headers = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
    'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'
  }
  try:
    response = requests_session().post(url=url, data=body, headers=headers, timeout=30).json()
    print('阅读时长')
    print(response)
    if response['error_code'] == '0':
      return response
    else:
      return
  except:
    print(traceback.format_exc())
    return

def rotary(headers, body):
  """
  转盘任务
  :param headers:
  :return:
  """
  time.sleep(0.3)
  currentTime = time.time()
  url = '{b}RotaryTable/turnRotary?_={e}'.format(b= YOUTH_HOST,e = currentTime)
  try:
    response = requests_session().post(url=url, data=body, headers=headers, timeout=30).json()
    print('转盘任务')
    print(response)
    return response
  except:
    print(traceback.format_exc())
    return

def rotaryChestReward(headers, body):
  """
  转盘宝箱
  :param headers:
  :return:
  """
  time.sleep(0.3)
  currentTime = time.time()
  url = '{b}RotaryTable/getData?_={e}'.format(b= YOUTH_HOST,e = currentTime)
  try:
    response = requests_session().post(url=url, data=body, headers=headers, timeout=30).json()
    print('转盘宝箱')
    print(response)
    if response['status'] == 1:
      i = 0
      while (i <= 3):
        chest = response['data']['chestOpen'][i]
        if response['data']['opened'] >= int(chest['times']) and chest['received'] != 1:
          time.sleep(1)
          runRotary(headers=headers, body='{body}&num={ko}'.format(body = body,ko =i+1))
        i += 1
      return response['data']
    else:
      return
  except:
    print(traceback.format_exc())
    return

def runRotary(headers, body):
  """
  转盘宝箱
  :param headers:
  :return:
  """
  time.sleep(0.3)
  currentTime = time.time()
  url = '{b}RotaryTable/chestReward?_={e}'.format(b= YOUTH_HOST,e = currentTime)
  try:
    response = requests_session().post(url=url, data=body, headers=headers, timeout=30).json()
    print('领取宝箱')
    print(response)
    if response['status'] == 1:
      return response['data']
    else:
      return
  except:
    print(traceback.format_exc())
    return

def doubleRotary(headers, body):
  """
  转盘双倍
  :param headers:
  :return:
  """
  time.sleep(0.3)
  currentTime = time.time()
  url = '{b}RotaryTable/toTurnDouble?_={e}'.format(b= YOUTH_HOST,e = currentTime)
  try:
    response = requests_session().post(url=url, data=body, headers=headers, timeout=30).json()
    print('转盘双倍')
    print(response)
    if response['status'] == 1:
      return response['data']
    else:
      return
  except:
    print(traceback.format_exc())
    return

def incomeStat(headers):
  """
  收益统计
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = 'https://kd.youth.cn/wap/user/balance?{dd}'.format(dd=headers["Referer"].split("?")[1])
  try:
    response = requests_session().get(url=url, headers=headers, timeout=50).json()
    print('收益统计')
    print(response)
    if response['status'] == 0:
      return response
    else:
      return
  except:
    print(traceback.format_exc())
    return

def withdraw(body):
  """
  自动提现
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = 'https://ios.baertt.com/v5/wechat/withdraw2.json'
  headers = {
    'User-Agent': 'KDApp/1.8.0 (iPhone; iOS 14.2; Scale/3.00)',
    'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'
  }
  try:
    response = requests_session().post(url=url, headers=headers, data=body, timeout=30).json()
    print('自动提现')
    print(response)
    if response['success'] == True:
      return response['items']
    else:
      return
  except:
    print(traceback.format_exc())
    return

def bereadRed(headers):
  """
  时段红包
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = '{b}Task/receiveBereadRed'.format(b = YOUTH_HOST)
  try:
    response = requests_session().post(url=url, headers=headers, timeout=30).json()
    print('时段红包')
    print(response)
    if response['code'] == 1:
      return response['data']
    else:
      return
  except:
    print(traceback.format_exc())
    return

def run():
  title = '📚中青看点'
  content = ''
  result = ''
  beijing_datetime = get_standard_time()
  print('\n【中青看点】{gg}'.format(gg = beijing_datetime.strftime("%Y-%m-%d %H:%M:%S")))
  hour = beijing_datetime.hour
  for i, account in enumerate(COOKIELIST):
    headers = account['YOUTH_HEADER']
    readBody = account['YOUTH_READBODY']
    redBody = account['YOUTH_REDBODY']
    readTimeBody = account['YOUTH_READTIMEBODY']
    withdrawBody = account['YOUTH_WITHDRAWBODY']
    rotaryBody = '{eee}&{eeee}.format(eee=headers["Referer"].split("&")[15],eeee =headers["Referer"].split("&")[8])'
    sign_res = sign(headers=headers)
    if sign_res and sign_res['status'] == 1:
      content += '【签到结果】：成功 🎉 明日+{ii}青豆'.format(ii = sign_res["nextScore"])
    elif sign_res and sign_res['status'] == 2:
      send(title=title, content='【账户{po}】Cookie已过期，请及时重新获取'.format(po=i+1))
      continue

    sign_info = signInfo(headers=headers)
    if sign_info:
      content += '\n【账号】：{yu}'.format(yu = sign_info["user"]["nickname"])
      content += '\n【签到】：+{ac}青豆 已连签{aac}天'.format(ac = sign_info["sign_score"],aac = sign_info["total_sign_days"])
      result += '【账号】: {aj}'.format(aj = sign_info["user"]["nickname"])
    friendList(headers=headers)
    if hour > 12:
      punch_card_res = punchCard(headers=headers)
      if punch_card_res:
        content += '\n【打卡报名】：打卡报名{} ✅'.format(punch_card_res["msg"])
    if hour >= 5 and hour <= 8:
      do_card_res = doCard(headers=headers)
      if do_card_res:
        content += '\n【早起打卡】：{} ✅'.format(do_card_res["card_time"])
    luck_draw_res = luckDraw(headers=headers)
    if luck_draw_res:
      content += '\n【七日签到】：+{}青豆'.format(luck_draw_res["score"])
    visit_reward_res = visitReward(body=readBody)
    if visit_reward_res:
      content += '\n【回访奖励】：+{}青豆'.format(visit_reward_res["score"])
    shareArticle(headers=headers)
    open_box_res = openBox(headers=headers)
    if open_box_res:
      content += '\n【开启宝箱】：+{hji}青豆 下次奖励{hjij}分钟'.format(hji=open_box_res["score"],hjij =(open_box_res["time"])/60)
    watch_ad_video_res = watchAdVideo(headers=headers)
    if watch_ad_video_res:
      content += '\n【观看视频】：+{}个青豆'.format(watch_ad_video_res["score"])
    watch_game_video_res = watchGameVideo(body=readBody)
    if watch_game_video_res:
      content += '\n【激励视频】：{}个青豆'.format(watch_game_video_res["score"])
    # article_red_res = articleRed(body=redBody)
    # if article_red_res:
    #   content += f'\n【惊喜红包】：+{article_red_res["score"]}个青豆'
    read_time_res = readTime(body=readTimeBody)
    if read_time_res:
      content += '\n【阅读时长】：共计{}分钟'.format(int(read_time_res["time"]) // 60)
    if (hour >= 6 and hour <= 8) or (hour >= 11 and hour <= 13) or (hour >= 19 and hour <= 21):
      beread_red_res = bereadRed(headers=headers)
      if beread_red_res:
        content += '\n【时段红包】：+{}个青豆'.format(beread_red_res["score"])
    for i in range(0, 5):
      time.sleep(5)
      rotary_res = rotary(headers=headers, body=rotaryBody)
      if rotary_res:
        if rotary_res['status'] == 0:
          break
        elif rotary_res['status'] == 1:
          content += '\n【转盘抽奖】：+{rjs}个青豆 剩余{rjss}次'.format(rjs=rotary_res["data"]["score"],rjss =rotary_res["data"]["remainTurn"])
          if rotary_res['data']['doubleNum'] != 0 and rotary_res['data']['score'] > 0:
            double_rotary_res = doubleRotary(headers=headers, body=rotaryBody)
            if double_rotary_res:
              content += '\n【转盘双倍】：+{hth}青豆 剩余{htht}次'.format(hth = double_rotary_res["score"],htht=double_rotary_res["doubleNum"])

    rotaryChestReward(headers=headers, body=rotaryBody)
    for action in ['watch_article_reward', 'watch_video_reward', 'read_time_two_minutes', 'read_time_sixty_minutes', 'new_fresh_five_video_reward']:
      time.sleep(5)
      sendTwentyScore(headers=headers, action=action)
    stat_res = incomeStat(headers=headers)
    if stat_res['status'] == 0:
      for group in stat_res['history'][0]['group']:
        content += '\n【{grN}】：+{grM}青豆'.format(grN=group["name"],grM=group["money"])
      today_score = int(stat_res["user"]["today_score"])
      score = int(stat_res["user"]["score"])
      total_score = int(stat_res["user"]["total_score"])

      if score >= 300000 and withdrawBody:
        with_draw_res = withdraw(body=withdrawBody)
        if with_draw_res:
          result += '\n【自动提现】：发起提现30元成功'
          content += '\n【自动提现】：发起提现30元成功'
          send(title=title, content='【账号】: {} 发起提现30元成功'.format(sign_info["user"]["nickname"]))

      result += "\n【今日收益】：+{}".format(today_score / 10000)
      content += "\n【今日收益】：+{}".format(today_score / 10000)
      result += "\n【账户剩余】：{}".format(score / 10000)
      content += "\n【账户剩余】：{}".format(score / 10000)
      result += "\n【历史收益】：{}".format(total_score / 10000)
      content += "\n【历史收益】：{}".format(total_score / 10000)

  print(content)

  # 每天 23:00 发送消息推送
  if beijing_datetime.hour == 23 and beijing_datetime.minute >= 0 and beijing_datetime.minute < 5:
    send(title=title, content=result)
  elif not beijing_datetime.hour == 23:
    print('未进行消息推送，原因：没到对应的推送时间点\n')
  else:
    print('未在规定的时间范围内\n')

if __name__ == '__main__':
    run()
