#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import time
import random
from datetime import datetime
import requests
import threading
from proxymanager import ProxyManager
from discord_webhook import DiscordEmbed, DiscordWebhook

headers= {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'}
proxy_manager = ProxyManager('proxies.txt')

webhookUrl = '' #Webhook To Post Pings 
logWebhookurl = '' #Webhook To store Monitor Logs
delay = '' #Number 1-10


def post_discord(imageUrl,title,status,styleColor,publishType,exclusiveAccess,hardLaunch,price,availability,method,Name,sizes):
    info = (f'Method: {method}   |   Type: {publishType}   |\n Price: {price}   |   Hard Launch: {hardLaunch}   |')
    webhook = DiscordWebhook(url=webhookUrl,content='')
    embed = DiscordEmbed(title=f'{title} [ {status} ]',url='https://www.nike.com/launch/t/'+str(title), color=0x36393F, description=f' {Name} - {styleColor}\n  |  Avilable: {str(availability)}  | Exclusive: {exclusiveAccess}')
    embed.add_embed_field(name='Info', value=info)
    embed.add_embed_field(name='Stock', value='\n'.join(sizes),inline=False)
    embed.set_author(name='@zyx898',icon_url='https://pbs.twimg.com/profile_images/1118878674642714624/lNXTIWNT_400x400.jpg',url='https://twitter.com/zyx898')
    embed.set_thumbnail(url=imageUrl)
    embed.set_footer(text=Name+' | SkrNotify', icon_url='https://pbs.twimg.com/profile_images/1134245182738718721/N12NVkrt_400x400.jpg')
    embed.set_timestamp()
    webhook.add_embed(embed)
    webhook.execute()

def post_log(message,Name):
    webhook = DiscordWebhook(url=webhookUrl,content='')
    embed = DiscordEmbed(title=Name,url='https://www.nike.com/launch/t/', color=0x36393F, description='')
    embed.add_embed_field(name='Message', value=message)
    embed.set_author(name='@zyx898',icon_url='https://pbs.twimg.com/profile_images/1118878674642714624/lNXTIWNT_400x400.jpg',url='https://twitter.com/zyx898')
    embed.set_footer(text=Name+' | SkrNotify', icon_url='https://pbs.twimg.com/profile_images/1134245182738718721/N12NVkrt_400x400.jpg')
    embed.set_timestamp()
    webhook.add_embed(embed)
    webhook.execute()

def scrpaeSlugs(url):
    apiReq = requests.get(url,headers=headers,proxies=proxy_manager.random_proxy().get_dict())
    apiInfo = json.loads(apiReq.text)
    apiObjects =  apiInfo['objects']
    objectSlugs = []
    for item in apiObjects:
        objectSlugs.append(item['publishedContent']['properties']['seo']['slug'])
    return objectSlugs

def hitApi(url):
    apiReq = requests.get(url,headers=headers,proxies=proxy_manager.random_proxy().get_dict())
    apiInfo = json.loads(apiReq.text)
    apiObjects =  apiInfo['objects']
    return apiObjects

def main(API,Name):
    old_slugs = scrpaeSlugs(API)
    post_log(f'{Name} Monitor has started.',Name)
    while True:
        try:
            apiObjects = hitApi(API)
            new_slugs = []
            for item in apiObjects:
                new_slugs.append(item['publishedContent']['properties']['seo']['slug'])
            differnces = set(new_slugs) - set(old_slugs)
            if differnces:
                for difference in differnces:
                    for item in apiObjects:
                        if item['publishedContent']['properties']['seo']['slug'] == difference:
                            imageUrl = item['publishedContent']['properties']['coverCard']['properties']['squarishURL']
                            title = item['publishedContent']['properties']['seo']['slug'].upper()
                            try:
                                status = item['productInfo'][0]['merchProduct']['status']
                            except Exception as e:
                                print('Error Parsing Status')
                                status = 'Null'
                                
                            try:
                                styleColor = item['productInfo'][0]['merchProduct']['styleColor']
                            except Exception as e:
                                print('Error Parsing Style Color')
                                styleColor = 'Null'
                                
                            try:
                                publishType = item['productInfo'][0]['merchProduct']['publishType']
                            except Exception as e:
                                print('Error Parsing Publish Type')
                                publishType = 'Null'
                                
                            try:
                                exclusiveAccess = item['productInfo'][0]['merchProduct']['exclusiveAccess']
                            except Exception as e:
                                print('Error Parsing Exclusive Access')
                                exclusiveAccess = 'Null'
                                
                            try:
                                hardLaunch = item['productInfo'][0]['merchProduct']['hardLaunch']
                            except Exception as e:
                                print('Error Parsing hard Launching')
                                hardLaunch = 'Null'
                            
                            try:
                                price = str(item['productInfo'][0]['merchPrice']['fullPrice']) +' USD'
                            except Exception as e:
                                print('Error Parsing Price')
                                price = 'Nulll'
                            
                            try:
                                availability = str(item['productInfo'][0]['availability']['available'])
                            except Exception as e:
                                print('Error Parsing Aviabality')
                                availability = 'Null'
                                
                                
                            try:
                                method = item['productInfo'][0]['launchView']['method']
                            except Exception as e:
                                print('Error Parsing Method')
                                method = 'Null'
                                
                            sizes = []
                            try:

                                for size,stock in zip(item['productInfo'][0]['skus'],item['productInfo'][0]['availableSkus']):
                                    sizes.append(size['countrySpecifications'][0]['localizedSize'] +' '+ str(stock['level']))
                                    
                            except Exception as e:
                                print('Error Getting Size and Stock')
                                sizes = ['NUll']
                                
                            post_discord(imageUrl,title,status,styleColor,publishType,exclusiveAccess,hardLaunch,price,availability,method,Name,sizes)

                            
                            old_slugs = new_slugs
            else:
                print(str(datetime.now())+ f' ------------------- Monitoring [ {Name} ]')
                time.sleep(int(delay))
        except Exception as e:
            post_log(str(e),Name)
            print(str(datetime.now()) + f' ----------------------Error Requesting to {Name}')

            
if __name__ == "__main__":
    APIS = ['https://api.nike.com/product_feed/threads/v2?filter=marketplace(US)&filter=language(en)&filter=channelId(008be467-6c78-4079-94f0-70e2d6cc4003)&fields=id&fields=lastFetchTime&fields=productInfo&fields=publishedContent.properties','https://api.nike.com/product_feed/threads/v2?filter=marketplace(CN)&filter=language(zh-Hans)&filter=channelId(008be467-6c78-4079-94f0-70e2d6cc4003)&fields=id&fields=lastFetchTime&fields=productInfo&fields=publishedContent.properties','https://api.nike.com/product_feed/threads/v2?filter=marketplace(GB)&filter=language(en-gb)&filter=channelId(008be467-6c78-4079-94f0-70e2d6cc4003)&fields=id&fields=lastFetchTime&fields=productInfo&fields=publishedContent.properties','https://api.nike.com/product_feed/threads/v2?filter=marketplace(JP)&filter=language(ja)&filter=channelId(008be467-6c78-4079-94f0-70e2d6cc4003)&fields=id&fields=lastFetchTime&fields=productInfo&fields=publishedContent.properties']
    for API in APIS:
        if 'US' in API:
            apiName = 'SNKRS US'
        elif 'CN' in API:
            apiName = 'SNKRS CN'
        elif 'GB' in API:
            apiName = 'SNRKS GB'
        elif 'JP' in API:
            apiName = 'SNKRS JP'
        threading.Thread(target=main,args=(API,apiName,)).start()
