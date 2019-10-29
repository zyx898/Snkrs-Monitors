#!/usr/bin/python
# -*- coding: utf-8 -*-


import requests,threading,random
import json
import re
import time
import datetime
import random
import pytz
from discord_webhook import DiscordEmbed, DiscordWebhook

webhook_url = '' # Put your discord Webhook


urls = ['https://api.nike.com/product_feed/threads/v2?filter=marketplace(US)&filter=language(en)&filter=channelId(008be467-6c78-4079-94f0-70e2d6cc4003)&fields=id&fields=lastFetchTime&fields=productInfo&fields=publishedContent.properties','https://api.nike.com/product_feed/threads/v2?filter=marketplace(CN)&filter=language(zh-Hans)&filter=channelId(008be467-6c78-4079-94f0-70e2d6cc4003)&fields=id&fields=lastFetchTime&fields=productInfo&fields=publishedContent.properties','https://api.nike.com/product_feed/threads/v2?filter=marketplace(GB)&filter=language(en-gb)&filter=channelId(008be467-6c78-4079-94f0-70e2d6cc4003)&fields=id&fields=lastFetchTime&fields=productInfo&fields=publishedContent.properties','https://api.nike.com/product_feed/threads/v2?filter=marketplace(JP)&filter=language(ja)&filter=channelId(008be467-6c78-4079-94f0-70e2d6cc4003)&fields=id&fields=lastFetchTime&fields=productInfo&fields=publishedContent.properties']

def gettime():
	now = str(datetime.datetime.now())
	
	now = now.split(' ')[1]
	
	threadname = threading.currentThread().getName()
	
	threadname = str(threadname).replace('Thread', 'Task')
	
	now = '[' + str(now) + ']' + '[' + str(threadname) + ']'

	return now

def message_post(webhook_url,title,image,restricrt,method,starttime):
	try:
		
		webhook = DiscordWebhook(url=webhook_url,content='')
		
		embed = DiscordEmbed(title=title, color=0x00fea9,url="https://nike.com/launch")
		
		
		embed.add_embed_field(name='**Product Infos：**',value='Access: '+restricrt +'\n\n'+'Start Time: '+starttime +'\n\n'+'Release Type: '+method)
		
		
		embed.set_thumbnail(url=image)
		
		embed.set_footer(text='@zyx898',icon_url='https://pbs.twimg.com/profile_images/1118878674642714624/lNXTIWNT_400x400.jpg')
		
		embed.set_timestamp()
		
		webhook.add_embed(embed)
		
		webhook.execute()
		
		print(gettime() + '[SUCCESS] --> Successfully sent success webhook!')
	except:
		print(gettime() + '[ERROR] --> Unable to send webhook')
		pass


def main(url):
	while True:
		try:
			if url == 'https://api.nike.com/product_feed/threads/v2?filter=marketplace(US)&filter=language(en)&filter=channelId(008be467-6c78-4079-94f0-70e2d6cc4003)&fields=id&fields=lastFetchTime&fields=productInfo&fields=publishedContent.properties':
				file1 = 'old_data_us.txt'
			elif url == 'https://api.nike.com/product_feed/threads/v2?filter=marketplace(CN)&filter=language(zh-Hans)&filter=channelId(008be467-6c78-4079-94f0-70e2d6cc4003)&fields=id&fields=lastFetchTime&fields=productInfo&fields=publishedContent.properties':
				file1 = 'old_data_cn.txt'
			elif url == 'https://api.nike.com/product_feed/threads/v2?filter=marketplace(GB)&filter=language(en-gb)&filter=channelId(008be467-6c78-4079-94f0-70e2d6cc4003)&fields=id&fields=lastFetchTime&fields=productInfo&fields=publishedContent.properties':
				file1 = 'old_data_gb.txt'
			elif url == 'https://api.nike.com/product_feed/threads/v2?filter=marketplace(JP)&filter=language(ja)&filter=channelId(008be467-6c78-4079-94f0-70e2d6cc4003)&fields=id&fields=lastFetchTime&fields=productInfo&fields=publishedContent.properties':
				file1 = 'old_data_jp.txt'

			ids = []
			response = requests.get(url)
			content = json.loads(response.text)
			for i in range(len(content['objects'])):
				id1 = content['objects'][i]['publishedContent']['properties']['seo']['slug']
				ids.append(id1)


			old_data = open(file1).read()

			difference = [c for c in ids if c not in old_data]

			for i in difference:
				for c in content['objects']:
					if c['publishedContent']['properties']['seo']['slug'] == i:
						try:
							restricrt = c['publishedContent']['properties']['custom']['restricted']
						except:
							restricrt = 'NONE'
						try:
							method = c['productInfo'][0]['launchView']['method']
						except:
							method ='NONE'
						try:
							starttime = c['productInfo'][0]['launchView']['startEntryDate']
						except:
							starttime = 'NONE' 

						if restricrt == False:

							restricrt = 'Not Exclusive'

						elif restricrt == True:

							restricrt = 'Exclusive'

						else:

							pass

						try:

							title = c['publishedContent']['properties']['seo']['title']

						except:

							title ='NONE'

						try:

							image = c['publishedContent']['properties']['coverCard']['properties']['squarishURL']

						except:

							image = 'https://pbs.twimg.com/profile_images/1118878674642714624/lNXTIWNT_400x400.jpg'


						message_post(webhook_url,title,image,restricrt,method,starttime)

			file = open(file1,'w+')

			file.write(str(ids))

			file.close()

			print(gettime() + "Monitoring>>>>>>>>>")

			time.sleep(2)

		except:

			time.sleep(2)


for i in range(len(urls)):
	(threading.Thread(target=main,args=(urls[i],))).start()