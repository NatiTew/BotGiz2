# from replit import db
# keys = db.keys()
# for row in keys:
#   del db[row]

import os
import numpy as np
import random
import discord
import collections
import time
from os import system
from itertools import repeat
from time import sleep
from keepAlive import keep_alive
from discord.ext import commands
from replit import db
from discord.ext.commands import has_permissions, MissingPermissions

my_secret = os.environ['Token']

listA1 = []
listB1 = []
listC1 = []

listA2 = []
listB2 = []
listC2 = []

client = commands.Bot(command_prefix='+')

chKeyPub = False
keys = db.keys()
for row in keys:
  if row == "supply":
    chKeyPub = True

pubNum = 1
if chKeyPub == True:
  pubNum = db["supply"]
valueArr = random.sample(range(pubNum), pubNum)


@client.event
async def on_ready():
    print(f'Successfully logged in as {client.user}')

def chData(name:str):
  keys = db.keys()
  for row in keys:
    if row == name:
      return True
  return False

@client.command()
async def info(ctx):
  async for message in ctx.channel.history(limit=1):
    await message.delete()
  await ctx.send("❈────────•✦•กระดานคำสั่ง•✦•────────❈\n"
                  "(ทุกคนสามารถใช้ได้ทุกคน)\n\n"
                  "+show   → เช็ค point ตัวเอง\n"
                  "+s <@name>   → เช็ค point คนอื่น\n"
                  "+douby   → เปิด LeaderBoard 25 อันดับแรก\n\n"
                  "+gacha   → เปิด LeaderBoard 25 อันดับแรก\n\n"
                  "❈────────•✦•❅•✦•────────❈\n")

def sort_list(list1, list2):
 
    zipped_pairs = zip(list2, list1)
 
    z = [x for _, x in sorted(zipped_pairs)]
     
    return z

def cal_board1():
  global listA1
  global listB1
  global listC1

  listA1 = []
  listB1 = []
  listC1 = []
  
  keys = db.keys()
  for row in keys:
    if row != 'item':
      value = db[row]
      # ch = isinstance(value[1],int)
      ch = 'player' in value
      if ch == True:
        listA1.append(row)
        listB1.append(value[0])
  # print(listA)
  # print(listB)
  listC1 = sort_list(listA1, listB1)
  listC1.reverse()
  
def cal_board2():
  global listA2
  global listB2
  global listC2

  listA2 = []
  listB2 = []
  listC2 = []
  
  keys = db.keys()
  for row in keys:
    if row != 'item':
      value = db[row]
      # ch = isinstance(value[1],int)
      ch = 'player' in value
      if ch == True:
        listA2.append(row)
        listB2.append(value[1])
  # print(listA)
  # print(listB)
  listC2 = sort_list(listA2, listB2)
  listC2.reverse()
  
@client.command()
@has_permissions(administrator = True)
async def add1(ctx, player: discord.Member, input: int):
  sPlayer = str(player.id)
  np = 'n' + str(player.id)
  nPlayer = str(player.name)
  check = False
  keys = db.keys()
  for row in keys:
    if row == sPlayer:
      check = True
      # print(check)
      break
  if check == True:
    value = db[sPlayer]
    value[1] = (value[1] + input)
    # print(value[0])
    db[sPlayer] = value
    db[np] = nPlayer
  else:
    db[np] = nPlayer
    arr = ['player',0,0]
    arr[1] = input
    # print(arr[0])
    db[sPlayer] = arr
  # print('<@'+ sPlayer +'> add '+ str(input) +'♚DouCoin')
  await ctx.channel.send('<@'+ sPlayer +'> add '+ str(input) +'♚DouCoin')


@add1.error
async def add1_error(ctx, error):
  if isinstance(error, MissingPermissions):
    text = "Sorry {}, you do not have permissions to do that!".format(ctx.message.author)
    await ctx.send(text)

@client.command()
@has_permissions(administrator = True)
async def add2(ctx, player: discord.Member, input: int):
  sPlayer = str(player.id)
  np = 'n' + str(player.id)
  nPlayer = str(player.name)
  check = False
  keys = db.keys()
  for row in keys:
    if row == sPlayer:
      check = True
      break
  if check == True:
    value = db[sPlayer]
    value[2] = (value[2] + input)
    db[sPlayer] = value
    db[np] = nPlayer
  else:
    db[np] = nPlayer
    arr = ['player',0,0]
    arr[2] = input
    db[sPlayer] = arr
  await ctx.channel.send('<@'+ sPlayer +'> add '+ str(input) +'🎮lotto')


@add2.error
async def add2_error(ctx, error):
  if isinstance(error, MissingPermissions):
    text = "Sorry {}, you do not have permissions to do that!".format(ctx.message.author)
    await ctx.send(text)

@client.command()
@has_permissions(administrator = True)
async def cut1(ctx, player: discord.Member, input: int): 
  
  sPlayer = str(player.id)
  np = 'n' + str(player.id)
  nPlayer = str(player.name)
  check = False
  keys = db.keys()
  for row in keys:
    if row == sPlayer:
      check = True
      break
  if check == True:
    value = db[sPlayer]
    print(value)
    value[1] = value[1] - input
    if value[1] < 0:
      await ctx.channel.send('Error คะแนนติดลบ')
    else:
      db[sPlayer] = value
      db[np] = nPlayer
      await ctx.channel.send('<@'+ sPlayer +'> del '+ str(input) +'♚DouCoin')
  else:
    await ctx.channel.send('<@'+ sPlayer +'> Not Found')

@cut1.error
async def cut1_error(ctx, error):
  if isinstance(error, MissingPermissions):
    text = "Sorry {}, you do not have permissions to do that!".format(ctx.message.author)
    await ctx.send(text)

@client.command()
@has_permissions(administrator = True)
async def cut2(ctx, player: discord.Member, input: int): 
  
  sPlayer = str(player.id)
  np = 'n' + str(player.id)
  nPlayer = str(player.name)
  check = False
  keys = db.keys()
  for row in keys:
    if row == sPlayer:
      check = True
      break
  if check == True:
    value = db[sPlayer]
    value[2] = value[2] - input
    if value[2] < 0:
      await ctx.channel.send('Error คะแนนติดลบ')
    else:
      db[sPlayer] = value
      db[np] = nPlayer
      await ctx.channel.send('<@'+ sPlayer +'> del '+ str(input) +'🎮lotto')
  else:
    await ctx.channel.send('<@'+ sPlayer +'> Not Found')

@cut2.error
async def cut2_error(ctx, error):
  if isinstance(error, MissingPermissions):
    text = "Sorry {}, you do not have permissions to do that!".format(ctx.message.author)
    await ctx.send(text)

@client.command()
async def show(ctx):
  sPlayer = str(ctx.author.id)
  np = 'n' + str(ctx.author.id)
  nPlayer = str(ctx.author.name)
  check = False
  keys = db.keys()
  for row in keys:
    if row == sPlayer:
      check = True
      break
  if check == True:
    value = db[sPlayer]
    db[np] = nPlayer
    print(sPlayer)
    await ctx.channel.send('<@'+ sPlayer +'> have '+ str(value[1]) +' ♚DouCoin, '+ str(value[2]) +' 🎮lotto')
  else:
    await ctx.channel.send('Not Found')
   
@client.command()
async def s(ctx, player: discord.Member):
  sPlayer = str(player.id)
  np = 'n' + str(player.id)
  nPlayer = str(player.name)
  check = False
  keys = db.keys()
  for row in keys:
    if row == sPlayer:
      check = True
      break
  if check == True:
    value = db[sPlayer]
    db[np] = nPlayer
    await ctx.channel.send(nPlayer +' have '+ str(value[1]) +' ♚DouCoin ,'+ str(value[2]) +' 🎮lotto')
  else:
    await ctx.channel.send('Not Found')

@client.command()
async def douby(ctx):
  async for message in ctx.channel.history(limit=1):
    await message.delete()
  cal_board1()
  print(listC1)
  embed = discord.Embed(title=f"{'----------<Leader Board>----------'}", description=('แสดง Top25'),color=discord.Color.red())
  num = 0
  while num < len(listC1):
    value = db[listC1[num]]
    nameDis = str(listC1[num])
    embed.add_field(name=str(value[1]) + ' DouCoin' , value=f"{'<@'+nameDis+'>'}")
    num += 1
  await ctx.send(embed=embed)

@client.command()
async def gacha(ctx):
  async for message in ctx.channel.history(limit=1):
    await message.delete()
  cal_board2()
  print(listC2)
  embed = discord.Embed(title=f"{'----------<Leader Board>----------'}", description=('แสดง Top25'),color=discord.Color.red())
  num = 0
  while num < len(listC2):
    value = db[listC2[num]]
    nameDis = str(listC2[num])
    embed.add_field(name=str(value[2]) + ' Lotto', value=f"{'<@'+nameDis+'>'}")
    num += 1
  await ctx.send(embed=embed)

@client.command()
async def b(ctx):
  await ctx.channel.send('ขอเวลาบอทคิดแปปนึง')
  cal_board1()
  #print(listC)
  output = " ----------<Leader Board>---------- \n"
  output = output + " ถ้าชื่อใครไม่ขึ้นให้ใช้คำสั่ง +show ก่อนแล้วมาลองใหม่ \n"
  num = 0
  while num < len(listC1):
    value = db[listC1[num]]
    nameDis = str(listC1[num])
    np = 'n' + nameDis
    #print(np)
    keys = db.keys()
    #print(keys)
    check = False
    for row in keys:
      if row == np:
        check = True
        break
    if check == True:
      nameDis = db[np]
      output = output + ''+ str(value[1]) + '★Star ของ ' +nameDis + ' \n'
    else:
      output = output + ''+str(value[1]) + '★Star ของ ' + '<@'+nameDis+'> \n'
    num += 1
    if num%25 == 0:
      await ctx.send('```' + output + '```' )
      output = " ----------<Leader Board>---------- \n"
      output = output + " ถ้าชื่อใครไม่ขึ้นให้ใช้คำสั่ง +show ก่อนแล้วมาลองใหม่ \n"
    elif num == len(listC1):
      await ctx.send('```' + output + '```' )
      output = " ----------<Leader Board>---------- \n"
      output = output + " ถ้าชื่อใครไม่ขึ้นให้ใช้คำสั่ง +show ก่อนแล้วมาลองใหม่ \n"

@client.command(pass_context = True)
@has_permissions(administrator = True)
async def whoami(ctx):
  await ctx.send('คุณเป็น administrator')

@whoami.error
async def whoami_error(ctx, error):
  if isinstance(error, MissingPermissions):
    text = "Sorry {}, you do not have permissions to do that!".format(ctx.message.author)
    await ctx.send(text)

@client.command()
# @has_permissions(administrator = True)
async def สร้าง(ctx, name:str, num:int):
  global valueArr
  keys = db.keys()
  check = False
  for row in keys:
    if row == 'create':
      check = True
      break
      
  if check != True:
    db["create"] = False
    
  status = db["create"]
  if status == False:
    db["name"] = name
    db["supply"] = num
    db["create"] = True
    valueArr = random.sample(range(num), num)
    np.random.shuffle(valueArr)
    db["valueArr"] = valueArr
    await ctx.send(name + ' Gacha กำลังเริ่ม มีของทั้งหมด ' + str(num) + 'รายการ')
  else:
    await ctx.send(' Gacha ถูกสร้างไปแล้ว')

@client.command()
# @has_permissions(administrator = True)
async def เพิ่ม(ctx, name:str, num:int, linkUrl:str):
  status = db["create"]
  if status == True:
    if chData("item") == False:
      db["item"] = []
      db["pic"] = []
      db["emo"] = []
      
    t = db['item']
    countArr = [item for item, count in collections.Counter(t).items() if count > 0]
    print(len(countArr))
    ch = chr(ord('a') + len(countArr))
    url = db['pic']
    supply = db["supply"]
    emo = db["emo"]
    chEmo = ":regional_indicator_"+ch+":"
    if (len(t)+num) <= supply :
      t.extend(repeat(name,num))
      url.extend(repeat(linkUrl,num))
      emo.extend(repeat(chEmo,num))
      db['item'] = t
      db["pic"] = url
      db["emo"] = emo
      # for arr in range(num):
      #   t = db['item']
        # t.append(name)
        # db['item'] = t
        # print(name)
      await ctx.send(chEmo + ' เพิ่ม ' + name + ' ลงในGacha จำนวน ' +  str(num) + ' ชิ้น\n'
                     'ตอนนี้เหลือพื้นที่ '+ str(supply - len(t)))
    else:
      await ctx.send(' Gacha ใส่ไม่พอ พื้นที่เหลือ ' + str(supply - len(t)))
  else:
    await ctx.send(' Gacha ยังไม่ถูกสร้าง')

@client.command()
# @has_permissions(administrator = True)
async def ล้าง(ctx):
  user_id = str(ctx.author)
  db["item"] = []
  db["pic"] = []
  db["emo"] = []
  db["name"] = ''
  db["supply"] = 0
  db["create"] = False
  await ctx.send(user_id + ' ได้ทำการล้างรายการใน Gacha')

@client.command()
async def สลับ(ctx):
  global valueArr
  await ctx.send('ช้านิดนึงนะ พอดีเซิฟเวอร์ของฟรี')
  tmp = db["valueArr"]
  for arr in range(len(tmp)):
    valueArr[arr] = tmp[arr]
  np.random.shuffle(valueArr)
  # print(valueArr)
  db["valueArr"] = valueArr
  # db["item"] = t
  print('สลับที่เรียบร้อย')
  await ctx.send('สลับที่เรียบร้อย')

@client.command()
async def เปิด(ctx):
  global valueArr
  status = db["create"]
  if status == True:
    name = db["name"]
    num = db["supply"]
    db["statusLotto"] = True
    await ctx.send('เริ่ม ' + name + ' มีจำนวน: ' + str(num))
  else:
    await ctx.send('Gacha ยังไม่ได้สร้าง')

@client.command()
async def ปิด(ctx):
  status = db["create"]
  if status == True:
    name = db["name"]
    num = db["supply"]
    db["statusLotto"] = False
    await ctx.send('ปิด ' + name + ' มีจำนวน: ' + str(num))
  else:
    await ctx.send('Gacha ยังไม่ได้สร้าง')

@client.command()
async def โชค(ctx):
  global valueArr
  statusLotto = db["statusLotto"]
  if statusLotto == True:
    t = db["item"]
    pic = db["pic"]
    emo = db["emo"]
    # valueArr = random.sample(range(len(t)), len(t))
    # print(t)
    if len(t) > 0:
      user_id = str(ctx.author)
      sPlayer = str(ctx.author.id)
      np = 'n' + str(ctx.author.id)
      nPlayer = str(ctx.author.name)
      check = False
      keys = db.keys()
      for row in keys:
        if row == sPlayer:
          check = True
          break
      if check == True:
        valueGacha = db[sPlayer]
        db[np] = nPlayer
        print(sPlayer)
        if valueGacha[2] > 0:
          x = random.randint(0,len(t)-1)
          valueArr = db["valueArr"]
          tmp = valueArr[x]
          print(str(x))
          print(str(len(t)))
          print(str(len(valueArr)))
          print(str(tmp))
          await ctx.send(" :white_large_square: "+":white_large_square: "+':arrow_down_small: '+":white_large_square: "+":white_large_square: ")
          message1 = await ctx.send("Loading:")
          numran = random.randint(10,15)
          for i in range(numran):
            # print(i)
            time.sleep(0.5)
            await message1.edit(content="\r " + emo[valueArr[(x+i-2) % len(valueArr)]] + " " + emo[valueArr[(x+i-1) % len(valueArr)]] + " " + emo[valueArr[(x+i) % len(valueArr)]] + " " + emo[valueArr[(x+i+1) % len(valueArr)]] + " " + emo[valueArr[(x+i+2) % len(valueArr)]])
            if i == (numran-1):
              await ctx.send(user_id + ' ได้รับ ||' + t[valueArr[(x+i) % len(valueArr)]] +'|| \nเหลือของในlotto อีก ' + str(len(t)-1))
              if pic[valueArr[(x+i) % len(valueArr)]] != "no":
                await ctx.send('|| '+pic[valueArr[(x+i) % len(valueArr)]]+' ||')
              print('||' + user_id + ' ได้รับ ' + t[valueArr[(x+i) % len(valueArr)]] +'||')
              t.pop(valueArr[(x+i) % len(valueArr)])
              pic.pop(valueArr[(x+i) % len(valueArr)])
              emo.pop(valueArr[(x+i) % len(valueArr)])
              # valueArr.pop((x+i) % len(valueArr))
              
              db["item"] = t
              db["pic"] = pic
              db["emo"] = emo
              valueArr = random.sample(range(len(t)), len(t))
              db["valueArr"] = valueArr
              valueGacha[2] = valueGacha[2] - 1
              db[sPlayer] = valueGacha
              # value = random.sample(range(len(t)), len(t))
        else:
          await ctx.channel.send('ตั๋วของคุณไม่พอ')
      else:
        await ctx.channel.send('Not Found')
        
      
    else:
      await ctx.send('Gacha หมดแล้วจ้าาา')
  else:
    await ctx.send('Gacha ยังไม่ได้เปิดจ้า')

@client.command()
async def แสดง(ctx):
  name = db["name"]
  t = db["item"]
  emo = db["emo"]
  
  arr = [item for item, count in collections.Counter(t).items() if count > 0]
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


@client.command()
async def restart(ctx): 
  await ctx.channel.send('Test Restart')
  print("\n\nRESTARTING NOW\n\n\n")
  await ctx.channel.send('kill process')
  print('kill')
  system('kill 1')
  await ctx.channel.send('sleep')
  print('sleep')
  sleep(7)
  await ctx.channel.send('restart')
  print('restart')
  system("python main.py")

keep_alive()
try:
    client.run(my_secret)
except discord.errors.HTTPException:
  print("\n\n\nBLOCKED BY RATE LIMITS\nRESTARTING NOW\n\n\n")
  system("python restarter.py")
  
  
  