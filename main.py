# from replit import db
# keys = db.keys()
# for row in keys:
#   del db[row]

import os
import discord
import random
import numpy as np
import collections
from itertools import repeat
from keepAlive import keep_alive
from discord.ext import commands
from replit import db
from discord.ext.commands import has_permissions, MissingPermissions

my_secret = os.environ['Token']

listA = []
listB = []
listC = []

Admin = ['358984660342145025']

client = commands.Bot(command_prefix='+')

value = random.sample(range(300), 300)
np.random.shuffle(value)

@client.command(pass_context = True)
@has_permissions(administrator = True)
async def whoami(ctx):
  await ctx.send('คุณเป็น administrator')

def chData(name:str):
  keys = db.keys()
  for row in keys:
    if row == name:
      return True
  return False

@client.event
async def on_ready():
    print(f'Successfully logged in as {client.user}')

@client.command()
async def hello(ctx):
  user_id = str(ctx.author.id)
  sent_message = await ctx.send('<@'+ str(user_id)+ '>\n 555')
  await sent_message.add_reaction('\U0001F60E')
  print(sent_message.id)

@client.command()
@has_permissions(administrator = True)
async def create(ctx, name:str, num:int):
  global value
  status = db["create"]
  if status == False:
    db["name"] = name
    db["supply"] = num
    db["create"] = True
    value = random.sample(range(num), num)
    await ctx.send(name + ' Lotto กำลังเริ่ม มีของทั้งหมด ' + str(num) + 'รายการ')
  else:
    await ctx.send(' Lotto ถูกสร้างไปแล้ว')

@client.command()
@has_permissions(administrator = True)
async def add(ctx, name:str, num:int):
  status = db["create"]
  if status == True:
    if chData("item") == False:
      db["item"] = []
      
    t = db['item']
    supply = db["supply"]
    if (len(t)+num) <= supply :
      t.extend(repeat(name,num))
      db['item'] = t
      # for arr in range(num):
      #   t = db['item']
        # t.append(name)
        # db['item'] = t
        # print(name)
      await ctx.send('เพิ่ม ' + name + ' ลงในLotto จำนวน ' +  str(num) + ' ชิ้น\n'
                     'ตอนนี้เหลือพื้นที่ '+ str(supply - len(t)))
    else:
      await ctx.send(' Lotto ใส่ไม่พอ พื้นที่เหลือ ' + str(supply - len(t)))
  else:
    await ctx.send(' Lotto ยังไม่ถูกสร้าง')

@client.command()
@has_permissions(administrator = True)
async def reset(ctx):
  user_id = str(ctx.author)
  db["item"] = []
  db["name"] = ''
  db["supply"] = 0
  db["create"] = False
  await ctx.send(user_id + ' ได้ทำการล้างรายการใน Lotto')

@client.command()
async def s(ctx):
  global value
  await ctx.send('ช้านิดนึงนะ พอดีเซิฟเวอร์ของฟรี')
  np.random.shuffle(value)
  # t = db["item"]
  # arr1 = t
  # i = 0
  # while i<len(t):
  #   arr1[i] = t[i]
  #   i += 1
  # np.random.shuffle(arr1)
  print(value)
  # db["item"] = t
  await ctx.send('สลับที่เรียบร้อย')

@client.command()
async def open(ctx):
  status = db["create"]
  
  db["name"] = name
  db["supply"] = num
  db["statusLotto"] = True
  await ctx.send('สลับที่เรียบร้อย')
  
@client.command()
async def close(ctx):
  db["statusLotto"] = False
  
@client.command()
async def ran(ctx):
  global value
  statusLotto = db["statusLotto"]
  if statusLotto == True:
    t = db["item"]
    value = random.sample(range(len(t)), len(t))
    # print(t)
    if len(t) > 0:
      user_id = str(ctx.author)
      x = random.randint(0,len(t)-1)
      tmp = value[x]
      print(str(x))
      print(str(len(t)))
      print(str(len(value)))
      print(str(tmp))
      await ctx.send(user_id + ' ได้รับ ||' + t[tmp] +'|| \nเหลือของในlotto อีก ' + str(len(t)-1))
      print('||' + user_id + ' ได้รับ ' + t[tmp] +'||')
      t.pop(tmp)
      db["item"] = t
      value = random.sample(range(len(t)), len(t))
    else:
      await ctx.send('Lotto หมดแล้วจ้าาา')
  else:
    await ctx.send('Lotto ยังไม่ได้เปิดจ้า')

@client.command()
async def show(ctx):
  name = db["name"]
  t = db["item"]
  arr = [item for item, count in collections.Counter(t).items() if count > 1]
  num = 0
  text = ''
  await ctx.send(name)
  for i in arr:
    num = 0
    for j in t:
      if i == j:
        num+=1
    text = text + str(i) + ' มี ' + str(num) + '\n'
    
  await ctx.send(text)
        

  
@whoami.error
async def whoami_error(ctx, error):
  if isinstance(error, MissingPermissions):
    text = "Sorry {}, you do not have permissions to do that!".format(ctx.message.author)
    await ctx.send(text)

@create.error
async def create_error(ctx, error):
  if isinstance(error, MissingPermissions):
    text = "Sorry {}, you do not have permissions to do that!".format(ctx.message.author)
    await ctx.send(text)

@add.error
async def add_error(ctx, error):
  if isinstance(error, MissingPermissions):
    text = "Sorry {}, you do not have permissions to do that!".format(ctx.message.author)
    await ctx.send(text)

@reset.error
async def reset_error(ctx, error):
  if isinstance(error, MissingPermissions):
    text = "Sorry {}, you do not have permissions to do that!".format(ctx.message.author)
    await ctx.send(text)
  
  
keep_alive()

client.run(my_secret)