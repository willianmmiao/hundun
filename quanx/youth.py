#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

# 此脚本参考 https://github.com/Sunert/Scripts/blob/master/Task/youth.js

import traceback
import time
import re
import json
import sys
import os
from util import send, requests_session
from datetime import datetime, timezone, timedelta


# YOUTH_HEADER 为对象, 其他参数为字符串
# 选择微信提现30元，立即兑换，在请求包中找到withdraw2的请求，拷贝请求body类型 p=****** 的字符串，放入下面对应参数即可 YOUTH_WITHDRAWBODY
# 分享一篇文章，找到 put.json 的请求，拷贝请求体，放入对应参数 YOUTH_SHAREBODY
# 清除App后台，重新启动App，找到 start.json 的请求，拷贝请求体，放入对应参数 YOUTH_STARTBODY

cookies1 = {
  'YOUTH_HEADER': {"Accept-Encoding":"gzip, deflate, br","Cookie":"sensorsdata2019jssdkcross=%7B%22distinct_id%22%3A%2251638237%22%2C%22%24device_id%22%3A%221774e8f5b4f2a9-0f4b7eb478de918-754c1551-304704-1774e8f5b50bd9%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%2C%22first_id%22%3A%221774e8f5b4f2a9-0f4b7eb478de918-754c1551-304704-1774e8f5b50bd9%22%7D; Hm_lvt_268f0a31fc0d047e5253dd69ad3a4775=1610421104,1612602247,1612604421,1612604427; Hm_lvt_6c30047a5b80400b0fd3f410638b8f0c=1612602247,1612604421; sensorsdata2019jssdkcross=%7B%22distinct_id%22%3A%2251638237%22%2C%22%24device_id%22%3A%221774e8f5b4f2a9-0f4b7eb478de918-754c1551-304704-1774e8f5b50bd9%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%2C%22first_id%22%3A%221774e8f5b4f2a9-0f4b7eb478de918-754c1551-304704-1774e8f5b50bd9%22%7D","Connection":"keep-alive","Referer":"https://kd.youth.cn/h5/20190301taskcenter/ios/index.html?uuid=36cef368385ab4ef4666ce337c13a054&sign=ede6b3252e30c24089b6cef0f044ad7f&channel_code=80000000&uid=51638237&channel=80000000&access=WIfI&app_version=2.0.0&device_platform=iphone&cookie_id=45bc68c5cc54973f81289f0039a1ee3a&openudid=36cef368385ab4ef4666ce337c13a054&device_type=1&device_brand=iphone&sm_device_id=20201121232223d9287179b4ff550b9d00eabe7887e093014f1292b017b974&device_id=48404203&version_code=200&os_version=14.2&cookie=MDAwMDAwMDAwMJCMpN-w09Wtg5-Bb36eh6CPqHualq2jmrCarWOwt42zhnx-4K_eqmqXr6NthJl7mI-shMmXeqDau4StacS3o7GFonrfr8-iY4Gfn26EY2Ft&device_model=iPhone_6_Plus&subv=1.5.1&&cookie=MDAwMDAwMDAwMJCMpN-w09Wtg5-Bb36eh6CPqHualq2jmrCarWOwt42zhnx-4K_eqmqXr6NthJl7mI-shMmXeqDau4StacS3o7GFonrfr8-iY4Gfn26EY2Ft&cookie_id=45bc68c5cc54973f81289f0039a1ee3a","Accept":"*/*","Host":"kd.youth.cn","User-Agent":"Mozilla/5.0 (iPhone; CPU iPhone OS 14_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148","Accept-Language":"zh-cn","X-Requested-With":"XMLHttpRequest"},
  'YOUTH_READBODY': 'p=9NwGV8Ov71o%3DgW5NEpb6rjb84bkaCQyOq-myT0C-Ktb_pYgxM135XoUfaIpfBqAxRGnFAl1k71C_zMPfUdFlHJTcuxYW9LgBCdTzuda7fnA8r2K-D8AqSYWzt-6LIEcC8SPkaeAgjjv1iCeYI_yckjGbVxJEy1xSQc4qp-_g8cJecymP34l6mTfctKg7kaxHi0R1L2yQjkyBaLUFMP_XNY-r4XVI4Uuw4BDvreocGlOQbcwXrbVvGmLTa1CwlvXqjMUEscxbODycfzWESB3_HXxD2QEUJd5vli2ac_7GFHMPQlilA4rciHQ510Adm3_MwKoRM1FdjThzExuxl-dPaw4biRfbxotcRhHb4YZ4Sr8Xn3hWoB4yBcOa5sHhe_J2ihHKoIZJqzCFqUdK6h31sgpO-lGiBo6Yoc0dRVqlian4MUekcN-RfwsM9QUl2NG14dpqa1efmFJlf58Na2bYtEYz6Cr2E95zlJX94EG1SNBOvH7Ox3PUxldoVItNNWEmSUAkPQKbwSmgY-5KgdXQx4P5YPRJAw1gs770jX2FK7O4G65S6JoVpFOk1oskPCMCxA4slAoQ0lOOXVKf2SD8gRQtzA1V5KfcZ9PtadrAex3d_fupluGi_YMQMu7cWVvltoRt8TzwN89iES1nzPDZJppIoKPSKi05l7hxiRplbDiDqTYfJ8gKa4JgKFAVaPoaWMfE3IYf67dDs10a3ApLxA1gUIjnM3IHy50KrBhN1S1epKxrAbSvLJBSQnmpI57ePnzbnEcUjXq_pJf8oDcHdZ02IOJkgRkA8BhcwQHNDmKHxlz4RPB0VrHoMu8Da96ZOn8oXPFBdRwX_v3PNr4LRPifQqKlJVDIwA%3D%3D',
  'YOUTH_READTIMEBODY': 'p=9NwGV8Ov71o%3DgW5NEpb6rjb84bkaCQyOq-myT0C-Ktb_pYgxM135XoUfaIpfBqAxRGnFAl1k71C_zMPfUdFlHJTcuxYW9LgBCdTzuda7fnA8r2K-D8AqSYWzt-6LIEcC8SPkaeAgjjv1iCeYI_yckjGbVxJEy1xSQc4qp-_g8cJecymP34l6mTfctKg7kaxHi0R1L2yQjkyBaLUFMP_XNY-r4XVI4Uuw4BDvreocGlOQbcwXrbVvGmLTa1CwlvXqjMUEscxbODycfzWESB3_HXya2QP5E-GG3cLeCGj71mkVeUp_1loCX3IK4R2Eqz4w2OZDphqMIheLo0uEog3gAw4KGeGQMwov0dw0VlGdGeKAwHD_baPanAp89dntsM906ksC_aP0rJ7TcMrjmN4IwSFb0-FzTEVMD-yFg73ZduJRHd1PxufPAGCQyfDIUP-jo4hvosGT2HoVSmnDyqNcDyHhDoK7S85Wc6gp-bRZYYNlvCm48MluvRUiZOyfWwJYMjrd8CYqauom4HoNmRMyJZgUw6OEVZJY5LzDYKj9bPtMA7uVVLjHkeOkNfTjlGJrT3HOPZTmhsgyGK7zIoqmvySywmHSrx4F5_WHf7DjM9ZU18HclKaSW1aRNi_Q4DW2sqgJhdKWz9xsUyAE_8i04t4O7dujKbEww4zOHg5YlREQLHwrEHLGtMy9rCpzFgciv92gU3U49siL2n08AuEOnyFEvfBfZAX1uHz0DG1Jox56PghpYBKRArq3O6BXcwzZyXddG4nuPKGO7DT9H_xH13Jbd0QXjiBCRShzide-z_D5UCZyqtQShoHoQLjlLjVxpG_Gl3IHmNU0tEyu6PVvXj4%3D',
  'YOUTH_WITHDRAWBODY': 'p=9NwGV8Ov71o=gW5NEpb6rjb84bkaCQyOq-myT0C-Ktb_mEtDEGsOrBruuZzIpWlevTEf2n4e6SDtwtHI8jh7tGLFm1iscPtbZwlhO1--2rPMqEVay5SHQZ0Xa5om9y_QnFioIoDSg-ArtrfwznZt1IhRAOspLNm4F1Z4mRILDUTDM9AS-u45jBBrvAt-MgxpsBrVTNGrYGdkTVk7rTFgRbYXQdv-gZuNVQ7-N-bLkpNesNYnIVAfkzbd82Bj7SWS9lEb6uUctD-2eDvPs_pRQSsXA1N3eNQOtiJcmHuhXMnOjYzDaFkOz00mK9Tgwosq6SA_T4MoOtUySUErdnw-cEPhG9mIjUpKwjsjcwQA151Gvd9hA3v8zvrYxy_xpksi0UurnF6XuOnwMcLnqXvf335fBFHQdootakP7NV4pRj8XI5pZGZi4q8RxkE0-wk2lWQ4isva2i2wyirOgqLWQlVQ9Yr89TLRmQ01Y9JXB9XMfHB8STxmCVk2WbasfVVUPh-HUpYMzo2spKjQjDNtjyGJDqxxjkeCXBDh27xkzDR65JHOJ-aUFKVtr6WrPY4Ny7myVSJg9o0lSMLpFTOi5rL73Xl8dgifzDSjoESApYryZ90l2BLUqlTtXFzP6bEDuG_QwNuPk9uPKC6BFeyVxBJ1FNI2TK6OZQUooJJ3Xy9j3XzYC5X8guW4rFXxVJZD6-QAyCZLHT3PW09OGP7lyNnZtNOJUqyYU4IHmA2GntzxReds_a4MIQUWD3UVmm3k1jOSmsu3-WP5n8MYGvHYaL1QCgDfyNMLeeL2ben4L4AkinCHbICEywO5pQtWDDuTTayGKLbCBaJLEkuXnTJMez4Y=',
  'YOUTH_SHAREBODY': 'access=WIFI&app_version=2.0.2&article_id=36625696&channel=80000000&channel_code=80000000&cid=80000000&client_version=2.0.2&device_brand=iphone&device_id=48404203&device_model=iPhone&device_platform=iphone&device_type=iphone&from=0&is_hot=0&isnew=1&mobile_type=2&net_type=1&openudid=36cef368385ab4ef4666ce337c13a054&os_version=14.2&phone_code=36cef368385ab4ef4666ce337c13a054&phone_network=WIFI&platform=3&request_time=1614859605&resolution=828x1472&sign=93cbffe6aef9b697a1766cf2834cb665&sm_device_id=20201121232223d9287179b4ff550b9d00eabe7887e093014f1292b017b974&stype=WEIXIN&szlm_ddid=D2O2VAj6%2Bsc5sUzdGOd06cVcrxVZuSQf4Wt6UZzFTN47wX8e&time=1614859606&uid=51638237&uuid=36cef368385ab4ef4666ce337c13a054',
  'YOUTH_STARTBODY': 'access=WIFI&app_version=2.0.2&channel=80000000&channel_code=80000000&cid=80000000&client_version=2.0.2&device_brand=iphone&device_id=48404203&device_model=iPhone&device_platform=iphone&device_type=iphone&isnew=1&mobile_type=2&net_type=1&openudid=36cef368385ab4ef4666ce337c13a054&os_version=14.2&phone_code=36cef368385ab4ef4666ce337c13a054&phone_network=WIFI&platform=3&request_time=1614859867&resolution=828x1472&sm_device_id=20201121232223d9287179b4ff550b9d00eabe7887e093014f1292b017b974&szlm_ddid=D2O2VAj6%2Bsc5sUzdGOd06cVcrxVZuSQf4Wt6UZzFTN47wX8e&time=1614859868&token=b9dfc2a8149133d08a61fc966706d149&uid=51638237&uuid=36cef368385ab4ef4666ce337c13a054'
}
cookies2 = {
  'YOUTH_HEADER': {"Accept-Encoding":"gzip, deflate, br","Accept":"*/*","Connection":"keep-alive","Referer":"https://kd.youth.cn/h5/20190301taskcenter/ios/index.html?uuid=36cef368385ab4ef4666ce337c13a054&sign=a9dd01afca08df56ce717e6b9d77c487&channel_code=80000000&uid=54172453&channel=80000000&access=Wlan&app_version=2.0.2&device_platform=iphone&cookie_id=445fc8d0cd05929beeb3e8d269cfb6c9&openudid=36cef368385ab4ef4666ce337c13a054&device_type=1&device_brand=iphone&sm_device_id=20201121232223d9287179b4ff550b9d00eabe7887e093014f1292b017b974&device_id=48404203&version_code=202&os_version=14.2&cookie=MDAwMDAwMDAwMJCMpN-w09Wtg5-Bb36eh6CPqHualq2jmrCarWOxp3lshKKGl67eqmqXr6NthJl7mI-shMmXeqDau4StacS3o7GFonqWsKm6q4N5l7GEY2Ft&device_model=iPhone_6_Plus&subv=1.5.1&&cookie=MDAwMDAwMDAwMJCMpN-w09Wtg5-Bb36eh6CPqHualq2jmrCarWOxp3lshKKGl67eqmqXr6NthJl7mI-shMmXeqDau4StacS3o7GFonqWsKm6q4N5l7GEY2Ft&cookie_id=445fc8d0cd05929beeb3e8d269cfb6c9","Content-Type":"","Host":"kd.youth.cn","User-Agent":"Mozilla/5.0 (iPhone; CPU iPhone OS 14_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148","Accept-Language":"zh-cn","X-Requested-With":"XMLHttpRequest"},
  'YOUTH_READBODY': 'p=9NwGV8Ov71o=GvDnjwMsu_lk8V15hrmPeFtKCBAoDX5kqrLpJGAkdwV8gOpPHTnSbw8wHrILlLgcdQvtAfFybVIPGHf_XtQiAk56lw4qSSwPjMmFTlMb22L0Xzl3EpMENkDly_2RuJh3AmE2y6Bh4KV8wydXMOZiS2EPJ488sXFnHedaY6SaPcXt6JrA_eW5bx_9mf1RPPEvzdga6vgBIWz0Pi9AvG9xVEmNUUhitZfL3j3P9Z4osbgR05rSwLJoLa6h-jRl95ZG3T0yslw-1m-zsSPuVj_IH0O7kTmuFBRyR3c59YOfZdgCksgejcNGH4wEZkTdkIvQAyRjzocmqTXov47PyPZ527HV67dQsDARITDeW4kvIe1OYzYevDYpx0RzSHiEAZ88jAtHRKouckRs_hidLpSYtPXmRimzwg9gKTuL2IDSYszXba-_d2isX-fh_F2XQxtZQmw5NybuUto3Xp2_veVAdxUs83cYnIWUhM7ifHcKU1-zrGfTfrCyBTJMzWL7fIFTHeZ4FShRcLiUzKjsel2bw5lAZ3GM2DH0RrL2XKWnv2Q9pWvZ1oFO7snoCfyssUERm0Dxmybjt9p7ochHYIEsUcJu4bDtC_qmjF7Lr0NsMMbxvj2YI6gm6OmtcLsWELT4JDZGHh6WUQ6_lh037B_t9f523c7YY-i78ZcqRQDkoAk3tNJ1QQlAp-OUKwYuqVwhOoFdwJPs-6urQeXeq5nJrphBMA6f1tWxTdaR00Vz8IZBMUg5NZcU5nQE6nE8Nwdl74n9b6INFSNeWYab6GxEJ-qLVoIbrsF-zoQNta8nXIcYik0j-3fDn_G9PED3rc8RQnxsAtbMBI3ZgYnuuOBGC0R-7sO8uYTlIO2v_qwfHszogIPztyxGk0NvKl156BYa',
  'YOUTH_READTIMEBODY': 'p=9NwGV8Ov71o%3DGvDnjwMsu_ld4qx0YVkhCGSN79Nz9uYVd_6x03zS0fnS8kKdOyWyDMKSICaFBvwH5U4nsR_vvJsjHH2Z81CBL7eyJjtPmVfyM0x8EAsS-_ESh4-JImy11uTAadxMJCYAdD7P_w27pQt6_tIUTgtnDG7LOKwRL-IZbYYNciqqQLKQixTuL9vTgcEbgQW9NUdi_vjXlcCK9HIuTXo885cTj2oJ179vVPgA6OxXbKxeHdSBZQs4ZELQYJiDf3rEh3fMQuuBi3J0fqkIQn4TdqBEXlyYkgMeRW-JBrXjM1LmIT0LIrLi8czB-O-ujqiG-JDtEOQgVxkDhZZUR4nwSS-NmR8I0r_45WkdAOva8b_4dxy5DMsLKFi3SPgTZSwKW4mIawEBFfI754s_TfAVXpWU5i15TEoSHFnGwZdwY9bCs-YLv5CnfuOv9s60c0Rbv1rYkZYxig_4mdv5tGL3tfAbn-sW10iJZF9xkabD63l6uTEfdiYMwF0D1Rn6rZrh7qeKsT0DS8RpdVGApYvnn62i_HExxqh-0fRH2kqAu8Rn1upzC2oMOUwEdrKCn3pwbKUiukbhmHgtpOLyt_uLIdPjyiP2PbsEiOc8wnjEbhgcZUF_2DEF0QifmtFVG8ibepSky67oU2ZKMBJj42hTIm8DXsI_rUVDfOdHJr0GlTFU3rO8l3F01fFXrNf6tLc9syLYvd3Bl5frgo_KiCA-Gv0Ov-QzrQ2FkL9b0sEygPkKcna8fQ3x5AlEs1h5gLHEFofkENvI0wwCuhOB3M5o490EjnQjxIOQ7auGQjTfImxyXRz9NPlqDbQYb-LP2H15dqxB',
  'YOUTH_WITHDRAWBODY': 'p=9NwGV8Ov71o=GvDnjwMsu_ld4qx0YVkhCGSN79Nz9uYVd_6x03zS0fnS8kKdOyWyDMKSICaFBvwH5U4nsR_vvJsjHH2Z81CBL7eyJjtPmVfyM0x8EAsS-_ESh4-JImy11uTAadxMJCYAdD7P_w27pQt6_tIUTgtnDG7LOKwRL-IZbYYNciqqQLKQixTuL9vTgcEbgQW9NUdi_vjXlcCK9HIuTXo885cTj2oJ179vVPgA6OxXbKxeHdSBZQs4ZELQYJiDf3rEh3fMQuuBi3J0fqkIQn4TdqBEXlyYkgMeRW-JBrXjM1LmIT1KeZhWpm1JhWsgYBgdwG2MKaoCO9Ad8Od4nYp4DjmkjGPSCcmyc1UZU9ctMIZjRgCEayolZ-oNO-mQ470eBDbLHhRk5-KitkwLKCBwc7BU3Fv-nZIleE7mHW3PehFtmAKUL4qadLdtuYCrBFQCL3-v_-GcklkHRkuNlvzrCX9bsnOZkmPtGrE1HaaRE6qeZD_wCcceaYZB24DeQx7L0kQaZbx1e3QEIOnJ5lcus5pRjhE95khK3U20D14JBMyUDBQxhXAKORbX-KTWvgoW7Yh11PiFyYjHuMiMG8dpJWG74qsqzl40Jm84BDrpdnJHJVCFrlyU-nH9Xp9nVZoPEhucR0pBfEvS_DFHN3cCNM_gz0JrEXvQsYtaD_1919IndTC0Hevr-ha6-bCRGcDP7QE0fxfVc-74UgKbcCdXKKHGHJUsmkU3ITV3139ASKDeZtcNCJLklm9WuNEWBL-S7kB9aNOgF5nA0YY-bdxntwtOctBtJt2WJ9iL8FVss1MEnY4GrA0LpPTb-Xw8SHoq_4NYTmwPnss1GPs=',
  'YOUTH_SHAREBODY': 'access=4G&app_version=2.0.2&article_id=36607855&channel=80000000&channel_code=80000000&cid=80000000&client_version=2.0.2&device_brand=iphone&device_id=48404203&device_model=iPhone&device_platform=iphone&device_type=iphone&from=0&is_hot=0&isnew=1&mobile_type=2&net_type=2&openudid=36cef368385ab4ef4666ce337c13a054&os_version=14.2&phone_code=36cef368385ab4ef4666ce337c13a054&phone_network=4G&platform=3&request_time=1614866498&resolution=828x1472&sign=dd57f5254a8311e0a74184652e79fcc2&sm_device_id=20201121232223d9287179b4ff550b9d00eabe7887e093014f1292b017b974&stype=WEIXIN&szlm_ddid=D2O2VAj6%2Bsc5sUzdGOd06cVcrxVZuSQf4Wt6UZzFTN47wX8e&time=1614866498&uid=54172453&uuid=36cef368385ab4ef4666ce337c13a054',
  'YOUTH_STARTBODY': 'access=4G&app_version=2.0.2&channel=80000000&channel_code=80000000&cid=80000000&client_version=2.0.2&device_brand=iphone&device_id=48404203&device_model=iPhone&device_platform=iphone&device_type=iphone&isnew=1&mobile_type=2&net_type=2&openudid=36cef368385ab4ef4666ce337c13a054&os_version=14.2&phone_code=36cef368385ab4ef4666ce337c13a054&phone_network=4G&platform=3&request_time=1614866466&resolution=828x1472&sm_device_id=20201121232223d9287179b4ff550b9d00eabe7887e093014f1292b017b974&szlm_ddid=D2O2VAj6%2Bsc5sUzdGOd06cVcrxVZuSQf4Wt6UZzFTN47wX8e&time=1614866467&token=4bf5202964b368b154abd736f366c038&uid=54172453&uuid=36cef368385ab4ef4666ce337c13a054'
}
cookies3 = {
  'YOUTH_HEADER': {"Accept-Encoding":"gzip, deflate, br","Accept":"*/*","Connection":"keep-alive","Referer":"https://kd.youth.cn/h5/20190301taskcenter/ios/index.html?uuid=36cef368385ab4ef4666ce337c13a054&sign=237799dfc54c9482d55f31e3351182e4&channel_code=80000000&uid=54182047&channel=80000000&access=Wlan&app_version=2.0.2&device_platform=iphone&cookie_id=e8422beb84baec9880d574d8e5cc3b89&openudid=36cef368385ab4ef4666ce337c13a054&device_type=1&device_brand=iphone&sm_device_id=20201121232223d9287179b4ff550b9d00eabe7887e093014f1292b017b974&device_id=48404203&version_code=202&os_version=14.2&cookie=MDAwMDAwMDAwMJCMpN-w09Wtg5-Bb36eh6CPqHualq2jmrCarWOxp3lthKJ2lq_eqmqXr6NthJl7mI-shMmXeqDau4StacS3o7GFonqWsLmiqoKJjWqEY2Ft&device_model=iPhone_6_Plus&subv=1.5.1&&cookie=MDAwMDAwMDAwMJCMpN-w09Wtg5-Bb36eh6CPqHualq2jmrCarWOxp3lthKJ2lq_eqmqXr6NthJl7mI-shMmXeqDau4StacS3o7GFonqWsLmiqoKJjWqEY2Ft&cookie_id=e8422beb84baec9880d574d8e5cc3b89","Content-Type":"","Host":"kd.youth.cn","User-Agent":"Mozilla/5.0 (iPhone; CPU iPhone OS 14_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148","Accept-Language":"zh-cn","X-Requested-With":"XMLHttpRequest"},
  'YOUTH_READBODY': 'p=9NwGV8Ov71o=GvDnjwMsu_lk8V15hrmPeFtKCBAoDX5kqrLpJGAkdwV8gOpPHTnSb_cy0qkEPI1w9ZD8gyINaMzfgTSKQVGcghyQEsVkbvi8yYRARnhD2Rh0X7bT5o8Ay06SHY0NI1mqaR9o_88JsPp031v5geXkxQ1WAhFWmiaQgWP-tTKP8P3gcNzWQFhqEoemt0zu0W7ZBjvn9YZcvLlWeFyyaykJyALPiYFPb2UHEn7avD8dxJAHZrtgJlJ9OqR6uI11pFdl084GZaBarT_cFYqW_4DmstV0QqEe9rz4XagzDkFSxatpOO7-4WdIwaRP6u7Vq0cBr3zi2toBsiUuEkFnRPh0ocSoGgqi0RmHH6TI-YG2ZDEMD-l_LCx4bdIpM3-sjp_s2mnyY2QTbokoKWTgiOTOSONpl2uD2XEP-F5l-IyolG3fWB0ia53wzqM4IaBvkqEfKBNPWKekLmJc7K1teaLrIRED91wDsg0mI9dnz-Wox6Mb9gRz6wjFIf-aYszw7ceaZ7EEE8eo35ojYMBck7_vx2HOK70JE4vVM7gPeIKS7sWSYdlRdRHfDgEQastYiVrsRVDT9QPj4VBr0hTa_C3odel1hOI8hHHA2q5lsKOBYgRbEY4XV1rEEYk3HsIkodPGM0ZxMTdDpk6n2fhWPy5AE7R_xpFfYEUNjngZSIvInGYD4ubCPMMuPeoEvXpb8w0-FgVr1t3XsgD2wOAKY5ojKmGXi4Lpz8-ATyDKr4mZzMB-gzovihI5KsEb67oA75z8uEE63O8MUMmhjwbSSiU7UND8WD3RagcMESIYogdy_MH2MzEbsMNXEBtX4IymJhIUJBEQV6nQ53AVMLTPsAQ3mGXrimtTCzoWHcd-gUyTfcB9u9PHkyh0HNP4BpILt9Ms',
  'YOUTH_READTIMEBODY': 'p=9NwGV8Ov71o%3DGvDnjwMsu_ld4qx0YVkhCGSN79Nz9uYVd_6x03zS0fnS8kKdOyWyDMKSICaFBvwH5U4nsR_vvJsjHH2Z81CBL7eyJjtPmVfyM0x8EAsS-_ESh4-JImy11uTAadxMJCYAdD7P_w27pQt6_tIUTgtnDG7LOKwRL-IZbYYNciqqQLKQixTuL9vTgcEbgQW9NUdi_vjXlcCK9HIuTXo885cTj2oJ179vVPgA6OxXbKxeHdSBZQs4ZELQYJiDf3rEh3fMQuuBi3J0fqkIQn4TdqBEXlyYkgMeRW-JBrXjM1LmIT0LIrLi8czB-O-ujqiG-JDtEOQgVxkDhZZUR4nwSS-NmR8I0r_45WkdAOva8b_4dxy5DMsLKFi3SPgTZSwKW4mIawEBFfI754s_TfAVXpWU5i15TEoSHFnGwZdwY9bCs-YLv5CnfuOv9s60c0Rbv1rYkZYxig_4mdv5tGL3tfAbn-sW10iJZF9xkabD63l6uTEfdiYMwF0D1T-4xaw2R8AFhU1-7nR0nKbgt3OpUCwKvAkIxMItpEocJNkZ1dxvblP656sPJklaiTZcOUf4O8kMilybFfyjDdfHbxkQNFJHX6_gh6Gp9YhjQqYVI8uu5URPbtIx2fECX88mWv6-pjpv686nsYXQMc50g0yWUZvMjz38waC3BoB88iBtWxkfqDSQrxkIIJxVTaVurv4EGYFBFpVjiJ7DE6i2m1wsBOpuPqPtGx_qOm5Dey9nubIYLBfYAMt4dD9I5UcmXtRhrgz1-6-bfnIJGVLy4y_gWE9vhYxAKT8eOoq3EfAslUlZR5aQRu6wicLPh79zT42tVbOl',
  'YOUTH_WITHDRAWBODY': 'p=9NwGV8Ov71o=gW5NEpb6rjb84bkaCQyOq-myT0C-Ktb_mEtDEGsOrBruuZzIpWlevTEf2n4e6SDtwtHI8jh7tGLFm1iscPtbZwlhO1--2rPMqEVay5SHQZ0Xa5om9y_QnFioIoDSg-ArtrfwznZt1IhRAOspLNm4F1Z4mRILDUTDM9AS-u45jBBrvAt-MgxpsBrVTNGrYGdkTVk7rTFgRbYXQdv-gZuNVQ7-N-bLkpNesNYnIVAfkzbd82Bj7SWS9lEb6uUctD-2eDvPs_pRQSsXA1N3eNQOtiJcmHuhXMnOjYzDaFkOz00mK9Tgwosq6SA_T4MoOtUySUErdnw-cEPhG9mIjUpKwjsjcwQA151Gvd9hA3v8zvrYxy_xpksi0UurnF6XuOnwMcLnqXvf335fBFHQdootakP7NV4pRj8XI5pZGZi4q8RxkE0-wk2lWQ4isva2i2wyirOgqLWQlVQ9Yr89TLRmQ01Y9JXB9XMfHB8STxmCVk2WbasfVVUPh-HUpYMzo2spKjQjDNtjyGJ3Ee4kcKlY6UR7yvMlNGBEfdsB-42zuKQFBXx_uVPASj3oZ87hX5UzUsTU0q18ok0zsI3iV7QJcX1mkZD624QWAN7JbfobGVMCoHp1CRJPPhzVBL1tVsyvWcJ8_AZBsPhJTQlbMvG7DLPMP58T08jv2U5745u8R4RZRf1R5VQ1ekP4s28cCP9PNn2V6a1uWvR2LpnrG3VnfS1Y_n4pXD6IhbFtAaarN6zaMawVeRiv4Fc2Gl9UALCMMcY7vVaE1TkdhNlhGsIGWREVxn9wXjlx6A-p0diQPxypqjpqYChibNpPf-b-A4v8TB6ITjVUge8=',
  'YOUTH_SHAREBODY': 'access=4G&app_version=2.0.2&article_id=36634225&channel=80000000&channel_code=80000000&cid=80000000&client_version=2.0.2&device_brand=iphone&device_id=48404203&device_model=iPhone&device_platform=iphone&device_type=iphone&from=0&is_hot=0&isnew=1&mobile_type=2&net_type=2&openudid=36cef368385ab4ef4666ce337c13a054&os_version=14.2&phone_code=36cef368385ab4ef4666ce337c13a054&phone_network=4G&platform=3&request_time=1614901867&resolution=828x1472&sign=656b40dbbe921675622bc8cb00a62d54&sm_device_id=20201121232223d9287179b4ff550b9d00eabe7887e093014f1292b017b974&stype=WEIXIN&szlm_ddid=D2O2VAj6%2Bsc5sUzdGOd06cVcrxVZuSQf4Wt6UZzFTN47wX8e&time=1614901868&uid=54182047&uuid=36cef368385ab4ef4666ce337c13a054',
  'YOUTH_STARTBODY': 'access=4G&app_version=2.0.2&channel=80000000&channel_code=80000000&cid=80000000&client_version=2.0.2&device_brand=iphone&device_id=48404203&device_model=iPhone&device_platform=iphone&device_type=iphone&isnew=1&mobile_type=2&net_type=2&openudid=36cef368385ab4ef4666ce337c13a054&os_version=14.2&phone_code=36cef368385ab4ef4666ce337c13a054&phone_network=4G&platform=3&request_time=1614901833&resolution=828x1472&sm_device_id=20201121232223d9287179b4ff550b9d00eabe7887e093014f1292b017b974&szlm_ddid=D2O2VAj6%2Bsc5sUzdGOd06cVcrxVZuSQf4Wt6UZzFTN47wX8e&time=1614901834&token=1f089bc08bf73d6e20ff59ed342b73b9&uid=54182047&uuid=36cef368385ab4ef4666ce337c13a054'
}

COOKIELIST = [cookies1,cookies2,cookies3,]  # 多账号准备

# ac读取环境变量
if "YOUTH_HEADER1" in os.environ:
  COOKIELIST = []
  for i in range(5):
    headerVar = f'YOUTH_HEADER{str(i+1)}'
    readBodyVar = f'YOUTH_READBODY{str(i+1)}'
    readTimeBodyVar = f'YOUTH_READTIMEBODY{str(i+1)}'
    withdrawBodyVar = f'YOUTH_WITHDRAWBODY{str(i+1)}'
    shareBodyVar = f'YOUTH_SHAREBODY{str(i+1)}'
    startBodyVar = f'YOUTH_STARTBODY{str(i+1)}'
    if headerVar in os.environ and os.environ[headerVar] and readBodyVar in os.environ and os.environ[readBodyVar] and readTimeBodyVar in os.environ and os.environ[readTimeBodyVar]:
      globals()['cookies'+str(i + 1)]["YOUTH_HEADER"] = json.loads(os.environ[headerVar])
      globals()['cookies'+str(i + 1)]["YOUTH_READBODY"] = os.environ[readBodyVar]
      globals()['cookies' + str(i + 1)]["YOUTH_READTIMEBODY"] = os.environ[readTimeBodyVar]
      globals()['cookies' + str(i + 1)]["YOUTH_WITHDRAWBODY"] = os.environ[withdrawBodyVar]
      globals()['cookies' + str(i + 1)]["YOUTH_SHAREBODY"] = os.environ[shareBodyVar]
      globals()['cookies' + str(i + 1)]["YOUTH_STARTBODY"] = os.environ[startBodyVar]
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
  url = f'{YOUTH_HOST}PunchCard/signUp'
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
  url = f'{YOUTH_HOST}PunchCard/doCard'
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
  startUrl = f'{YOUTH_HOST}PunchCard/shareStart'
  endUrl = f'{YOUTH_HOST}PunchCard/shareEnd'
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
  url = f'{YOUTH_HOST}PunchCard/luckdraw'
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

def timePacket(headers):
  """
  计时红包
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = f'{YOUTH_HOST}TimePacket/getReward'
  try:
    response = requests_session().post(url=url, data=f'{headers["Referer"].split("?")[1]}', headers=headers, timeout=30).json()
    print('计时红包')
    print(response)
    return
  except:
    print(traceback.format_exc())
    return

def watchWelfareVideo(headers):
  """
  观看福利视频
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = f'{YOUTH_HOST}NewTaskIos/recordNum?{headers["Referer"].split("?")[1]}'
  try:
    response = requests_session().get(url=url, headers=headers, timeout=30).json()
    print('观看福利视频')
    print(response)
    return
  except:
    print(traceback.format_exc())
    return

def shareArticle(headers, body):
  """
  分享文章
  :param headers:
  :return:
  """
  url = 'https://ios.baertt.com/v2/article/share/put.json'
  headers['Content-Type'] = 'application/x-www-form-urlencoded;charset=utf-8'
  try:
    response = requests_session().post(url=url, data=body, headers=headers, timeout=30).json()
    print('分享文章')
    print(response)
    return
  except:
    print(traceback.format_exc())
    return

def threeShare(headers, action):
  """
  三餐分享
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = f'{YOUTH_HOST}ShareNew/execExtractTask'
  headers['Content-Type'] = 'application/x-www-form-urlencoded;charset=utf-8'
  body = f'{headers["Referer"].split("?")[1]}&action={action}'
  try:
    response = requests_session().post(url=url, data=body, headers=headers, timeout=30).json()
    print('三餐分享')
    print(response)
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
  url = f'{YOUTH_HOST}invite/openHourRed'
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
  url = f'{YOUTH_HOST}invite/shareEnd'
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
  url = f'{YOUTH_HOST}ShareSignNew/getFriendActiveList'
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
  url = f'{YOUTH_HOST}ShareSignNew/sendScoreV2?friend_uid={uid}'
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
  url = f'{YOUTH_HOST}NewTaskIos/sendTwentyScore?{headers["Referer"].split("?")[1]}&action={action}'
  try:
    response = requests_session().get(url=url, headers=headers, timeout=30).json()
    print(f'每日任务 {action}')
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
  url = f'{YOUTH_HOST}RotaryTable/turnRotary?_={currentTime}'
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
  url = f'{YOUTH_HOST}RotaryTable/getData?_={currentTime}'
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
          runRotary(headers=headers, body=f'{body}&num={i+1}')
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
  url = f'{YOUTH_HOST}RotaryTable/chestReward?_={currentTime}'
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
  url = f'{YOUTH_HOST}RotaryTable/toTurnDouble?_={currentTime}'
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
  url = f'https://kd.youth.cn/wap/user/balance?{headers["Referer"].split("?")[1]}'
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
  url = f'{YOUTH_HOST}Task/receiveBereadRed'
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

def startApp(headers, body):
  """
  启动App
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = 'https://ios.baertt.com/v6/count/start.json'
  headers = {
    'User-Agent': 'KDApp/1.8.0 (iPhone; iOS 14.2; Scale/3.00)',
    'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'
  }
  try:
    response = requests_session().post(url=url, headers=headers, data=body, timeout=30).json()
    print('启动App')
    print(response)
    if response['success'] == True:
      return response
    else:
      return
  except:
    print(traceback.format_exc())
    return

def run():
  title = f'📚中青看点'
  content = ''
  result = ''
  beijing_datetime = get_standard_time()
  print(f'\n【中青看点】{beijing_datetime.strftime("%Y-%m-%d %H:%M:%S")}')
  hour = beijing_datetime.hour
  for i, account in enumerate(COOKIELIST):
    headers = account.get('YOUTH_HEADER')
    readBody = account.get('YOUTH_READBODY')
    readTimeBody = account.get('YOUTH_READTIMEBODY')
    withdrawBody = account.get('YOUTH_WITHDRAWBODY')
    shareBody = account.get('YOUTH_SHAREBODY')
    startBody = account.get('YOUTH_STARTBODY')
    rotaryBody = f'{headers["Referer"].split("&")[15]}&{headers["Referer"].split("&")[8]}'

    if startBody:
      startApp(headers=headers, body=startBody)
    sign_res = sign(headers=headers)
    if sign_res and sign_res['status'] == 1:
      content += f'【签到结果】：成功 🎉 明日+{sign_res["nextScore"]}青豆'
    elif sign_res and sign_res['status'] == 2:
      send(title=title, content=f'【账户{i+1}】Cookie已过期，请及时重新获取')
      continue

    sign_info = signInfo(headers=headers)
    if sign_info:
      content += f'\n【账号】：{sign_info["user"]["nickname"]}'
      content += f'\n【签到】：+{sign_info["sign_score"]}青豆 已连签{sign_info["total_sign_days"]}天'
      result += f'【账号】: {sign_info["user"]["nickname"]}'
    friendList(headers=headers)
    if hour > 12:
      punch_card_res = punchCard(headers=headers)
      if punch_card_res:
        content += f'\n【打卡报名】：打卡报名{punch_card_res["msg"]} ✅'
    if hour >= 5 and hour <= 8:
      do_card_res = doCard(headers=headers)
      if do_card_res:
        content += f'\n【早起打卡】：{do_card_res["card_time"]} ✅'
    luck_draw_res = luckDraw(headers=headers)
    if luck_draw_res:
      content += f'\n【七日签到】：+{luck_draw_res["score"]}青豆'
    visit_reward_res = visitReward(body=readBody)
    if visit_reward_res:
      content += f'\n【回访奖励】：+{visit_reward_res["score"]}青豆'
    if shareBody:
      shareArticle(headers=headers, body=shareBody)
      for action in ['beread_extra_reward_one', 'beread_extra_reward_two', 'beread_extra_reward_three']:
        time.sleep(5)
        threeShare(headers=headers, action=action)
    open_box_res = openBox(headers=headers)
    if open_box_res:
      content += f'\n【开启宝箱】：+{open_box_res["score"]}青豆 下次奖励{open_box_res["time"] / 60}分钟'
    watch_ad_video_res = watchAdVideo(headers=headers)
    if watch_ad_video_res:
      content += f'\n【观看视频】：+{watch_ad_video_res["score"]}个青豆'
    watch_game_video_res = watchGameVideo(body=readBody)
    if watch_game_video_res:
      content += f'\n【激励视频】：{watch_game_video_res["score"]}个青豆'
    read_time_res = readTime(body=readTimeBody)
    if read_time_res:
      content += f'\n【阅读时长】：共计{int(read_time_res["time"]) // 60}分钟'
    if (hour >= 6 and hour <= 8) or (hour >= 11 and hour <= 13) or (hour >= 19 and hour <= 21):
      beread_red_res = bereadRed(headers=headers)
      if beread_red_res:
        content += f'\n【时段红包】：+{beread_red_res["score"]}个青豆'
    for i in range(0, 5):
      time.sleep(5)
      rotary_res = rotary(headers=headers, body=rotaryBody)
      if rotary_res:
        if rotary_res['status'] == 0:
          break
        elif rotary_res['status'] == 1:
          content += f'\n【转盘抽奖】：+{rotary_res["data"]["score"]}个青豆 剩余{rotary_res["data"]["remainTurn"]}次'
          if rotary_res['data']['doubleNum'] != 0 and rotary_res['data']['score'] > 0:
            double_rotary_res = doubleRotary(headers=headers, body=rotaryBody)
            if double_rotary_res:
              content += f'\n【转盘双倍】：+{double_rotary_res["score"]}青豆 剩余{double_rotary_res["doubleNum"]}次'

    rotaryChestReward(headers=headers, body=rotaryBody)
    for i in range(5):
      watchWelfareVideo(headers=headers)
    timePacket(headers=headers)
    for action in ['watch_article_reward', 'watch_video_reward', 'read_time_two_minutes', 'read_time_sixty_minutes', 'new_fresh_five_video_reward', 'first_share_article']:
      time.sleep(5)
      sendTwentyScore(headers=headers, action=action)
    stat_res = incomeStat(headers=headers)
    if stat_res['status'] == 0:
      for group in stat_res['history'][0]['group']:
        content += f'\n【{group["name"]}】：+{group["money"]}青豆'
      today_score = int(stat_res["user"]["today_score"])
      score = int(stat_res["user"]["score"])
      total_score = int(stat_res["user"]["total_score"])

      if score >= 300000 and withdrawBody:
        with_draw_res = withdraw(body=withdrawBody)
        if with_draw_res:
          result += f'\n【自动提现】：发起提现30元成功'
          content += f'\n【自动提现】：发起提现30元成功'
          send(title=title, content=f'【账号】: {sign_info["user"]["nickname"]} 发起提现30元成功')

      result += f'\n【今日收益】：+{"{:4.2f}".format(today_score / 10000)}'
      content += f'\n【今日收益】：+{"{:4.2f}".format(today_score / 10000)}'
      result += f'\n【账户剩余】：{"{:4.2f}".format(score / 10000)}'
      content += f'\n【账户剩余】：{"{:4.2f}".format(score / 10000)}'
      result += f'\n【历史收益】：{"{:4.2f}".format(total_score / 10000)}\n\n'
      content += f'\n【历史收益】：{"{:4.2f}".format(total_score / 10000)}\n'

  print(content)

  # 每天 23:00 发送消息推送
  if beijing_datetime.hour == 13 and beijing_datetime.minute >= 0 and beijing_datetime.minute < 5:
    send(title=title, content=result)
  elif not beijing_datetime.hour == 13:
    print('未进行消息推送，原因：没到对应的推送时间点\n')
  else:
    print('未在规定的时间范围内\n')

if __name__ == '__main__':
    run()
