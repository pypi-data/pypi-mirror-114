# coding=utf-8
# 尝试用requests获取到购物车列表，但是动态加载很烦,先不使用requests 2021-04-16
import requests

headers = {
    'authority': 'gma.alicdn.com',
    'cache-control': 'no-cache',
    'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36',
    'accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
    'sec-fetch-site': 'same-site',
    'sec-fetch-mode': 'no-cors',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'image',
    'referer': 'https://a1.alicdn.com/',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cookie': 't=9c4249a362a7567ff54490700617c0ca; xlly_s=1; thw=cn; cna=6UT8GGIdq0kCAXBAg2VSYHgZ; _samesite_flag_=true; cookie2=122c59e0073722ea70a887147a096ecf; _tb_token_=e3e38836d5bed; sgcookie=E100w%2B5heYpvWGMB796FZfaQ1JbuW9T2bwr9lYtEs5rMXbhInSCD2j7MY8O77ARl%2Fboz%2Bvfxh1wXIo1O3FD1UTA13A%3D%3D; unb=4286722913; uc3=lg2=UtASsssmOIJ0bQ%3D%3D&vt3=F8dCuwpnl0yrc4%2BJGyg%3D&nk2=F5RCYRiZq7FIMF0%3D&id2=Vy6wuiK%2BS0fkWw%3D%3D; csg=78b48096; lgc=tb743940389; cookie17=Vy6wuiK%2BS0fkWw%3D%3D; dnk=tb743940389; skt=9be306c41f340ccc; existShop=MTYxODU0MTU3OQ%3D%3D; uc4=id4=0%40VXkX0rZulCIxTBcvUj3yarFDqlej&nk4=0%40FY4Jj1fjy134mSEe8CjdnWHfThnusA%3D%3D; tracknick=tb743940389; _cc_=Vq8l%2BKCLiw%3D%3D; _l_g_=Ug%3D%3D; sg=937; _nk_=tb743940389; cookie1=U%2BJ4RwTGBOS7q2WhDFVS1zuEnBDdVCa8rH3wvCldIYk%3D; _m_h5_tk=5517bf0beb5723faa6c7189c7e7ef373_1618550580915; _m_h5_tk_enc=23d58d5205cffe9fde3f09a71de84d5f; mt=ci=4_1; uc1=cookie14=Uoe1iuWW1lLyNg%3D%3D&existShop=false&cookie16=V32FPkk%2FxXMk5UvIbNtImtMfJQ%3D%3D&cart_m=0&cookie15=UIHiLt3xD8xYTw%3D%3D&cookie21=W5iHLLyFe3xm&pas=0; l=eBgznlKcjwXjEw8vBOfwnurza77tsIRAguPzaNbMiOCPO4CH5etFW6a_WaLMCnGVh6JWR3yIziz8BeYBqC22sWRdUKaOYMkmn; tfstk=ckoRB2gS7IAl1t2xQ4LcdOA2k8vGZ5OLGTNhvLL9WhgOfAIdiBiiXVaMPJ18DKC..; isg=BG1tOleM8bWal5XWuQQRMus4fAnnyqGcC5WUE69yrIRxJo3Ydxh9bAn4EPrAprlU',
    'Referer': 'https://a1.alicdn.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36',
    'Origin': 'https://cart.taobao.com',
    'Pragma': 'no-cache',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Sec-WebSocket-Key': 'pgWIzG+W79r6suOOQTMNQQ==',
    'Upgrade': 'websocket',
    'Sec-WebSocket-Extensions': 'permessage-deflate; client_max_window_bits',
    'Cache-Control': 'no-cache',
    'Connection': 'Upgrade',
    'Sec-WebSocket-Version': '13',
    'if-none-match': 'W/"1efe-gibOP5kr+x7GzP3kayA6Wzcii4g"',
    'if-modified-since': 'Wed, 18 Jan 2017 08:06:30 GMT',
    'pragma': 'no-cache',
    'content-type': 'text/plain',
    'origin': 'https://cart.taobao.com',
}

params = (
    ('spm', 'a1z02.1.1997525049.1.U6BJfg'),
    ('from', 'mini'),
    ('ad_id', ''),
    ('am_id', ''),
    ('cm_id', ''),
    ('pm_id', '1501036000a02c5c3739'),
)

data = [
    ('{}', ''),
    ('{}', ''),
    ('data', '{"pageSize":20,"endTime":1618542900510}'),
]


def main():
    response = requests.post('https://cart.taobao.com/cart.htm', headers=headers, params=params, data=data)

    print(response.text)
