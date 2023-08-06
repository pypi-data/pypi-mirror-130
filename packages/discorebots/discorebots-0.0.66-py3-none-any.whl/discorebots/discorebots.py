import discord
import json
from discord.ext import commands
import datetime
import time
import requests
import random
from .defines import *
from .__versions__ import packageVersion

version = packageVersion

class Database:
  def __init__(self, path: str=None):
    if path is not None:
      if path.endswith(".json"):
        self.path = path
      else:
        self.path = "variables.json"
    else:
      self.path = "variables.json"
      

  def createVar(self, key: str="key", value: str="value"):
    va = [key, value]
    with open(self.path, "r+", encoding = "utf-8") as f:
      try:
        data = json.load(f)
      except:
        data = {}

      if va[0] in data:
        print(f"createVar: Variable '{va[0]}' already exist")
      else:
        data[va[0]] = va[1]

        with open(self.path, "w+", encoding="utf-8") as f:
          json.dump(data, f, sort_keys=True, ensure_ascii=False, indent = 2)

  def getVar(self, key: str="key"):
    try:
      varname = key
      with open(self.path, "r+", encoding = "utf-8") as f:
        varsname = json.loads(f.read())
        return f"{str(varsname[varname])}"
    except:
      print(f"updateVar: Variable '{varname}' is not exist")

  def updateVar(self, key: str="key", new_value: str="new_value"):
    try:
      varname = [key, new_value]

      with open(self.path, "r+", encoding = "utf-8") as f:
        f_json = json.load(f)
        if varname[0] in f_json:
          f_json[varname[0]] += varname[1]

          with open(self.path, "r+", encoding = "utf-8") as f:
            json.dump(f_json, f, sort_keys=True, ensure_ascii=False, indent=2)
        else:
          print(f"updateVar: Variable '{varname[0]}' is not exist")
    except TypeError:
      pass

  def openAllVars(self):
    try:
      with open(self.path, "r+", encoding = "utf-8") as f:
        return f"```py\n{f.read()}```"
    except:
      print("openAllVars: error")

class commandloader:

  """
  Writes commands to a list for further storage
  """

  commandsToLoad = []

  def __init__(self, name: str = None, code: list = None):
    self.name = name
    self.code = code
    self.split = ";."

    commandloader.commandsToLoad.append(self)

class setupBot(commandloader):
  def __init__(self, intents: bool=False, prefix: str="", sharding: bool=False, shardsAmount: int=2, path: str=None):
    """
    create bot
    :param (bool) intents: enable intents
    :param (str) prefix: prefix to use bot
    """
    self.__intents = intents
    self.__prefix = prefix
    self.__sharding = sharding
    self.__shardsAmount = shardsAmount
    if path is not None:
      self.__database = Database(path)
    else:
      self.__database = Database("variables.json")
    if self.__intents is True:
      if self.__sharding is True:
        self.__clientUse = commands.AutoShardedBot(shard_count=self.__shardsAmount, command_prefix=self.__prefix, intents=discord.Intents.all())
      else:
        self.__clientUse = commands.Bot(command_prefix=self.__prefix, intents=discord.Intents.all())
    else:
      if self.__sharding is True:
        self.__clientUse = commands.AutoShardedBot(shard_count=self.__shardsAmount, command_prefix=self.__prefix)
      else:
        self.__clientUse = commands.Bot(command_prefix=self.__prefix)

  def logger(self, log=""):
    print(log)

  def onWebsocketResponse(self, to_console: str=None, status: str=None, text="discorebots.py lib", stream_url: str="https://discord.com"):
    @self.__clientUse.event
    async def on_ready():
      if to_console is not None:
        print(f"{to_console}")
      self.__status = status
      if status is not None:
        try:
          if self.__status == "game":
            await self.__clientUse.change_presence(activity=discord.Game(name=f"{text}"))
          elif self.__status == "watch":
            await self.__clientUse.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{text}"))
          elif self.__status == "listen":
            await self.__clientUse.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f"{text}"))
          elif self.__status == "stream":
            await self.__clientUse.change_presence(activity=discord.Streaming(name=f"{text}", url=stream_url))
          else:
            print("Status: Error set status (incorrect type)")
        except Exception as e:
          print(e)
      
      self.__start_time = time.time()

  def addCommand(self, name: str = None, code: list = None, prefix: str = None):
    """
    create a new command
    @param (str) name: commandName
    @param (list) code: code of your command
    """
    commandName = name
    commandCode = code
    if prefix is not None:
      commandPrefix = prefix
    else:
      commandPrefix = self.__prefix

    commandloader.commandsToLoad.append([commandName, commandCode, commandPrefix])

  def onClientMessage(self):
    """
    Allows the bot to use commands
    """
    commandloader.commandsToLoad = [*commandloader.commandsToLoad]

    @self.__clientUse.event
    async def on_message(message):
      
      if message.channel.type is not discord.ChannelType.private:
        if not message.author.bot:
            
          for commandinfo in commandloader.commandsToLoad:
            commandname = commandinfo[0]
            commandcode = commandinfo[1]
            prefix = commandinfo[2]

            if str(message.content).startswith(str(prefix + commandname)):
              
              
              channel = message.channel.id

              embed = discord.Embed()

              async def getMessage(index: int = None):
                try:
                  Msg = message.content.lstrip(f"{self.__prefix}{commandname} ")
                  if index:
                    return Msg.split()[index-1]
                  else:
                    return Msg
                except Exception as e:
                  print("message: Error find message")
                  return ""

              codestatus = {
                "addReactions": {
                  "enabled": False,
                  "reactions": []
                },
                "let": {}
              }
              
              while "$addCmdReactions[" in commandcode:
                reactions = commandcode.split("$addCmdReactions[")[1].split("]")[0]
                commandcode = commandcode.replace("$addCmdReactions[{}]".format(reactions), "")
                for react in reactions.split(";"):
                    await message.add_reaction(react)

              while "$addReactions[" in commandcode:
                reactions = commandcode.split("$addReactions[")[1].split("]")[0]
                commandcode = commandcode.replace("$addReactions[{}]".format(reactions), "")
                codestatus["addReactions"]["reactions"] = reactions.split(";")
                codestatus["addReactions"]["enabled"] = True

              while "$eval[" in commandcode:
                codetouse = commandcode.split("$eval[")[1].split("]")[0]
                commandcode = commandcode.replace(f"$eval[{codetouse}]", codetouse)
                break

              while "$message[" in commandcode:
                  index = int(commandcode.split("$message[")[1].split("]")[0])
                  commandcode = commandcode.replace(f"$message[{index}]", f"{await getMessage(index)}")

              while "$message" in commandcode:
                  commandcode = commandcode.replace("$message", f"{await getMessage()}")

              while "$authorID" in commandcode:
                commandcode = commandcode.replace("$authorID", str(message.author.id))
                break
                
              while "$createServerInvite[" in commandcode:
                invite_info = commandcode.split("$createServerInvite[")[1].split("]")[0]
                try:
                  link = await message.channel.create_invite(xkcd=True, max_age = int(invite_info), max_uses = 0)
                  commandcode = commandcode.replace(f"$createServerInvite[{invite_info}]", f"{link}")
                except Exception:
                  try:
                    link = await message.channel.create_invite(xkcd=True, max_age = 0, max_uses = 0)
                    commandcode = commandcode.replace(f"$createServerInvite[{invite_info}]", f"{link}")
                  except Exception:
                    commandcode = commandcode.replace(f"$createServerInvite[{invite_info}]", "createServerInvite: Failed to create invite")
                    break

              while "$serverName" in commandcode:
                commandcode = commandcode.replace("$serverName", f"{message.guild.name}")

              while "$authorName" in commandcode:
                commandcode = commandcode.replace("$authorName", str(message.author.name))
                break
              
              while "$ping" in commandcode:
                commandcode = commandcode.replace("$ping", f"{round(self.__clientUse.latency*1000)}")
                break

              while "$uptime" in commandcode:
                current_time = time.time()
                difference = int(round(current_time - self.__start_time))
                text = str(datetime.timedelta(seconds=difference))
                commandcode = commandcode.replace("$uptime", f"{text}")
                break

              while "$readyTimestamp" in commandcode:
                commandcode = commandcode.replace("$readyTimestamp", f"{int(self.__start_time)}")

              while "$channelID" in commandcode:
                commandcode = commandcode.replace("$channelID", str(message.channel.id))
                break

              while "$clientID" in commandcode:
                commandcode = commandcode.replace("$clientID", str(self.__clientUse.user.id))
                break

              while "$authorAvatar" in commandcode:
                commandcode = commandcode.replace("$authorAvatar",f"{message.author.avatar_url}")
                break

              while "$userTag[" in commandcode:
                try:
                  finduserid = commandcode.split("$userTag[")[1].split("]")[0]
                  kvas = await self.__clientUse.fetch_user(finduserid)
                  commandcode = commandcode.replace(f"$userTag[{finduserid}]", f"{kvas.name}#{kvas.discriminator}")
                except Exception as e:
                  commandcode = commandcode.replace(f"$userTag[{finduserid}]", f"```userTag: Incorrect UserID in $userTag[{finduserid}]```")
                  break

              while "$updateServerVar[" in commandcode:
                var = commandcode.split("$updateServerVar[")[1].split("]")[0].split(";")
                try:
                  var_key = var[0]
                  var_value = var[1]
                  commandcode = commandcode.replace(f"$updateServerVar[{var[0]};{var[1]}]", str(""))
                  try:
                    self.__database.updateVar(f"server_{var_key}_{message.guild.id}", f"{var_value}")
                    break
                  except Exception:
                    self.__database.updateVar(f"server_{var_key}_{message.guild.id}", f"{var_value}")
                    commandcode = commandcode.replace(f"$updateServerVar[{var[0]};{var[1]}]", str(""))
                    break
                except Exception:
                  print("updateServerVar: error values")
                  commandcode = commandcode.replace(f"$updateServerVar[{var[0]};{var[1]}]", f"updateServerVar: error values")
                  break

              while "$createServerVar[" in commandcode:
                var = commandcode.split("$createServerVar[")[1].split("]")[0].split(";")
                try:
                  var_key = var[0]
                  var_value = var[1]
                  commandcode = commandcode.replace(f"$createServerVar[{var[0]};{var[1]}]", str(""))
                  try:
                    server_id = message.guild.id
                    self.__database.createVar(f"server_{var_key}_{server_id}", f"{var_value}")
                    break
                  except Exception:
                    self.__database.createVar(f"server_{var_key}_{message.guild.id}", f"{var_value}")
                    commandcode = commandcode.replace(f"$createServerVar[{var[0]};{var[1]}]", str(""))
                    break
                except Exception:
                  print("createServerVar: error values")
                  commandcode = commandcode.replace(f"$createServerVar[{var[0]};{var[1]}]", f"createServerVar: error values")
                  break

              while "$getServerVar[" in commandcode:
                var = commandcode.split("$getServerVar[")[1].split("]")[0]
                try:
                  var_key = var
                  commandcode = commandcode.replace(f"$getServerVar[{var_key}]", str(""))
                  try:
                    server_id = message.guild.id
                    self.__database.getVar(f"server_{var_key}_{server_id}")
                    break
                  except Exception:
                    self.__database.getVar(f"server_{var_key}_{message.guild.id}")
                    commandcode = commandcode.replace(f"$getServerVar[{var_key}]", str(""))
                    break
                except Exception:
                  print("getServerVar: error values")
                  commandcode = commandcode.replace(f"$getServerVar[{var_key}]", f"getServerVar: error values")
                  break

              while "$createUserVar[" in commandcode:
                try:
                  keys = commandcode.split("$createUserVar[")[1].split("]")[0].split(";")
                  try:
                    user = discord.utils.get(message.guild.members, name=keys[2])
                    self.__database.createVar(f"user_{keys[0]}_{user.id}", str(f"{keys[1]}"))
                    commandcode = commandcode.replace(f"$createUserVar[{keys[0]};{keys[1]};{keys[2]}]", str(""))
                    break
                  except:
                    commandcode = commandcode.replace(f"$createUserVar[{keys[0]};{keys[1]};{keys[2]}]", str("createUserVar: Incorrect UserID"))
                    break
                except Exception:
                  print("createUserVar: error values")
                  commandcode = commandcode.replace(f"$createUserVar[{keys[0]};{keys[1]};{keys[2]}]", f"createUserVar: error values")
                  break

              while "$updateUserVar[" in commandcode:
                try:
                  keys = commandcode.split("$updateUserVar[")[1].split("]")[0].split(";")
                  try:
                    user = discord.utils.get(message.guild.members, name=keys[2])
                    self.__database.updateVar(f"user_{keys[0]}_{user.id}", str(f"{keys[1]}"))
                    commandcode = commandcode.replace(f"$updateUserVar[{keys[0]};{keys[1]};{keys[2]}]", str(""))
                    break
                  except:
                    commandcode = commandcode.replace(f"$updateUserVar[{keys[0]};{keys[1]};{keys[2]}]", str("updateUserVar: Incorrect UserID"))
                    break
                except Exception:
                  print("updateUserVar: error values")
                  commandcode = commandcode.replace(f"$updateUserVar[{keys[0]};{keys[1]};{keys[2]}]", f"updateUserVar: error values")
                  break

              while "$getUserVar[" in commandcode:
                try:
                  keys = commandcode.split("$getUserVar[")[1].split("]")[0].split(";")
                  try:
                    user = discord.utils.get(message.guild.members, name=keys[2])
                    self.__database.getVar(f"user_{keys[0]}_{user.id}")
                    commandcode = commandcode.replace(f"$getUserVar[{keys[0]};{keys[1]};{keys[2]}]", str(""))
                    break
                  except:
                    commandcode = commandcode.replace(f"$getUserVar[{keys[0]};{keys[1]};{keys[2]}]", str("getUserVar: Incorrect UserID"))
                    break
                except Exception:
                  print("getUserVar: error values")
                  commandcode = commandcode.replace(f"$getUserVar[{keys[0]};{keys[1]};{keys[2]}]", f"getUserVar: error values")
                  break

              while "$findUserID[" in commandcode:
                try:
                  finduserid = commandcode.split("$findUserID[")[1].split("]")[0]
                  strelkarak = discord.utils.get(message.guild.members, name=finduserid)
                  commandcode = commandcode.replace(f"$findUserID[{finduserid}]", f"{strelkarak.id}")
                except Exception as e:
                  commandcode = commandcode.replace(f"$findUserID[{finduserid}]", f"findUserID: Incorrect UserID in $findUserID[{finduserid}]")
                  setupBot.logger(f"$findUserID[{finduserid}]", f"findUserID: Incorrect UserID in $findUserID[{finduserid}]")
                  break
              
              while "$jsonRequest[" in commandcode:
                request = commandcode.split("$jsonRequest[")[1].split("]")[0].split(";")
                try:
                  commandcode = commandcode.replace(f"$jsonRequest[{request[0]};{request[1]};{request[2]}]", f'{json.dumps(requests.get(request[0]).json()[request[1]], indent = 2, ensure_ascii = False)}')
                except KeyError as e:
                  commandcode = commandcode.replace(f"$jsonRequest[{request[0]};{request[1]};{request[2]}]", f"{request[2]}")
                  setupBot.logger(f"$jsonRequest: {request[2]}")
                  break

              while "$round[" in commandcode:
                to_round = commandcode.split("$round[")[1].split("]")[0]
                try:
                  commandcode = commandcode.replace(f"$round[{to_round}]", f"{round(float(to_round))}")
                except Exception as e:
                  commandcode = commandcode.replace(f"$round[{to_round}]", f"round: Incorrect Number in $round[{to_round}]")
                  setupBot.logger(f"round: Incorrect Number in $round[{to_round}]")
                  break

              while "$shardID" in commandcode:
                if self.__sharding is True:
                  if self.__shardsAmount >= 2:
                    shard_id = message.guild.shard_id
                    commandcode = commandcode.replace("$shardID", f"{shard_id}")
                else:
                  commandcode = commandcode.replace("$shardID", f"shardID: Sharding disabled")
              
              while "$shardCount" in commandcode:
                if self.__sharding is True:
                  if self.__shardsAmount >= 2:
                    commandcode = commandcode.replace("$shardCount", f"{self.__shardsAmount}")
                  else:
                    commandcode = commandcode.replace("$shardCount", f"shardCount: Sharding error< shards count only >= 2")
                else:
                  commandcode = commandcode.replace("$shardCount", f"shardCount: Sharding disabled")

              while "$shardPing" in commandcode:
                if self.__sharding is True:
                  if self.__shardsAmount >= 2:
                    shard_id = message.guild.shard_id
                    shard = self.__clientUse.get_shard(shard_id)
                    shard_ping = shard.latency
                    commandcode = commandcode.replace("$shardPing", f"{round(shard_ping*1000)}")
                else:
                  commandcode = commandcode.replace("$shardPing", f"shardPing: Sharding disabled")
              
              while "$shardGuilds" in commandcode:
                if self.__sharding is True:
                  if self.__shardsAmount >= 2:
                    shard_id = message.guild.shard_id
                    shard = self.__clientUse.get_shard(shard_id)
                    shard_ping = shard.latency
                    shard_guilds = len([guild for guild in self.__clientUse.guilds if guild.shard_id == shard_id])
                    commandcode = commandcode.replace("$shardGuilds", f"{shard_guilds}")
                else:
                  commandcode = commandcode.replace("$shardGuilds", f"shardGuilds: Sharding disabled")

              while "$guildsCount" in commandcode:
                commandcode = commandcode.replace("$guildsCount", f"{len(self.__clientUse.guilds)}")
                break

              while "$guildID" in commandcode:
                commandcode = commandcode.replace("$guildID", f"{message.guild.id}")
                break

              while "$serverIcon" in commandcode:
                try:
                  icon_url = message.guild.icon_url
                  commandcode = commandcode.replace("$serverIcon", f"{icon_url}")
                except Exception as e:
                  commandcode = commandcode.replace("$serverIcon", str(""))

              while "$randomUserID" in commandcode:
                commandcode = commandcode.replace("$randomUserID", str(random.choice(message.guild.members).id))
                break

              while "$randomNumber[" in commandcode:
                randnumber = commandcode.split("$randomNumber[")[1].split("]")[0].split(";")
                try:
                  resrandnumber = random.randint(int(randnumber[0]),int(randnumber[1]))
                  commandcode = commandcode.replace(f"$randomNumber[{int(randnumber[0])};{int(randnumber[1])}]","{0}".format(resrandnumber))
                except:
                  commandcode = commandcode.replace(f"$randomNumber[{int(randnumber[0])};{int(randnumber[1])}]", f"```randomNumber: Error in $random[{int(randnumber[0])};{int(randnumber[1])}]```")
                  break

              while "$randomText[" in commandcode:
                randtext = commandcode.split("$randomText[")[1].split("]")[0]
                try:
                  rand = random.choice(randtext.split(";"))
                  commandcode = commandcode.replace(f"$randomText[{randtext}]", str(rand))
                except:
                  commandcode = commandcode.replace(f"$randomText[{randtext}]", f"```randomText: Error in $randomText[{randtext}]```")
                  break

              while "$remRole[" in commandcode:
                inde = commandcode.split("$remRole[")[1].split("]")[0].split(";")
                try:
                  commandcode = commandcode.replace(f"$remRole[{inde[0]};{inde[1]}]", f' ')
                  await self.__clientUse.get_user(int(inde[0])).remove_roles(id=discord.utils.get(message.guild.roles, id=int(inde[1])))
                except Exception as e:
                  commandcode = commandcode.replace(f"$remRole[{inde[0]};{inde[1]}]", f"remRole: Failed to add role")
                  break

              while "$addRole[" in commandcode:
                inde = commandcode.split("$addRole[")[1].split("]")[0].split(";")
                try:
                  commandcode = commandcode.replace(f"$addRole[{inde[0]};{inde[1]}]", f' ')
                  await self.__clientUse.get_user(int(inde[0])).add_roles(id=discord.utils.get(message.guild.roles, id=int(inde[1])))
                except Exception as e:
                  commandcode = commandcode.replace(f"$addRole[{inde[0]};{inde[1]}]", f"addRole: Failed to add role")
                  break

              while "$packageVersion" in commandcode:
                commandcode = commandcode.replace("$packageVersion", f"{version}")
                break

              while "$delMessage" in commandcode:
                try:
                  commandcode = commandcode.replace("$delMessage", f" ")
                  await message.delete()
                except Exception as e:
                  commandcode = commandcode.replace(f"$delMessage", "delMessage: Failed to delete message")
                  break

              if "$setTitle[" in commandcode:
                title = commandcode.split("$setTitle[")[1].split("]")[0]
                embed.title = title
                commandcode = commandcode.replace(f"$setTitle[{title}]", str(""))

              if "$setDescription[" in commandcode:
                descr = commandcode.split("$setDescription[")[1].split("]")[0]
                embed.description = descr
                commandcode = commandcode.replace(f"$setDescription[{descr}]", str(""))

              if "$setColor[" in commandcode:
                colour = commandcode.split("$setColor[")[1].split("]")[0]
                if colour == "random":
                  embed.color = discord.Color.random()
                  commandcode = commandcode.replace(f"$setColor[random]", str(""))
                else:
                  embed.color = eval(f"0x{str(colour)}")
                  commandcode = commandcode.replace(f"$setColor[{colour}]", str(""))



              if "$setFooter[" in commandcode:
                try:
                  fo = commandcode.split("$setFooter[")[1].split("]")[0].split(";")
                  if "$authorAvatar" in fo[1]:
                    commandcode = commandcode.replace(f"$setFooter[{fo[0]};$authorAvatar]", str(""))
                    embed.set_footer(text = fo[0], icon_url = message.author.avatar.url)
                  elif "$serverIcon" in fo[1]:
                    commandcode = commandcode.replace(f"$setFooter[{fo[0]};$serverIcon]", str(""))
                    embed.set_footer(text = fo[0], icon_url = message.guild.icon_url)
                  else:
                    commandcode = commandcode.replace(f"$setFooter[{fo[0]};{fo[1]}]", str(""))
                    embed.set_footer(text = fo[0], icon_url = fo[1])
                except Exception as e:
                  foer = commandcode.split("$setFooter[")[1].split("]")[0]
                  commandcode = commandcode.replace(f"$setFooter[{foer}]", str(""))
                  embed.set_footer(text = foer)

                  setupBot.logger(f"$setFooter: {e}")


              if "$setThumbnail[" in commandcode:
                thum = commandcode.split("$setThumbnail[")[1].split("]")[0]
                if "$authorAvatar" in thum:
                  commandcode = commandcode.replace(f"$setThumbnail[{thum}]", str(""))
                  embed.set_thumbnail(url = message.author.avatar.url)
                elif "$serverIcon" in thum:
                  commandcode = commandcode.replace(f"$setThumbnail[{thum}]", str(""))
                  embed.set_thumbnail(url = message.guild.icon_url)
                else:
                  commandcode = commandcode.replace(f"$setThumbnail[{thum}]", str(""))
                  embed.set_thumbnail(url = thum)


              if "$setAuthor[" in commandcode:
                try:
                  aut = commandcode.split("$setAuthor[")[1].split("]")[0].split(";")
                  if "$authorAvatar" in aut[1]:
                    commandcode = commandcode.replace(f"$setAuthor[{aut[0]};$authorAvatar]", str(""))
                    embed.set_author(name=aut[0], icon_url = message.author.avatar.url)
                  elif "$serverIcon" in aut[1]:
                    commandcode = commandcode.replace(f"$setAuthor[{aut[0]};$serverIcon]", str(""))
                    embed.set_author(name=aut[0], icon_url = message.guild.icon_url)
                  else:
                    commandcode = commandcode.replace(f"$setAuthor[{aut[0]};{aut[1]}]", str(""))
                    embed.set_author(name = aut[0], icon_url = aut[1])
                except:
                  aut = commandcode.split("$setAuthor[")[1].split("]")[0]
                  commandcode = commandcode.replace(f"$setAuthor[{aut}]", str(""))
                  embed.set_author(name = aut)

              if "$setImage[" in commandcode:
                url = commandcode.split("$setImage[")[1].split("]")[0]
                if "$authorAvatar" in url:
                  commandcode = commandcode.replace("$setImage[$authorAvatar]", str(""))
                  embed.set_image(url = message.author.avatar.url)
                elif "$serverIcon" in fo[1]:
                  commandcode = commandcode.replace(f"$setImage[$serverIcon]", str(""))
                  embed.set_image(url = message.guild.icon_url)
                else:
                  commandcode = commandcode.replace(f"$setImage[{url}]", str(""))
                  embed.set_image(url = url)

              if "$addTimestamp" in commandcode:
                try:
                  embed.timestamp = datetime.datetime.utcnow()
                  commandcode = commandcode.replace("$addTimestamp", str(""))
                except Exception:
                  commandcode = commandcode.replace("$addTimestamp", str(""))

              while "$addField[" in commandcode:
                field = commandcode.split("$addField[")[1].split("]")[0].split(";")
                embed.add_field(name=field[0], value=field[1])
                commandcode = commandcode.replace("$addField[{};{}]".format(field[0], field[1]), str(""))

              while "$let[" in commandcode:
                  let = commandcode.split("$let[")[1].split("]")[0].split(";")
                  commandcode = commandcode.replace("$let[{};{}]".format(let[0], let[1]), str(""))
                  if not let[0] in codestatus["let"]:
                      codestatus["let"][let[0]] = let[1]
                      
              while "$get[" in commandcode:
                  get = commandcode.split("$get[")[1].split("]")[0]
                  commandcode = commandcode.replace("$get[{}]".format(get), codestatus["let"][get])
              
              try:
                  msg = await message.channel.send(commandcode, embed=embed)
              except Exception:
                  try:
                      msg = await message.channel.send(commandcode)
                  except Exception:
                      pass

              if codestatus["addReactions"]["enabled"]:
                  for react in codestatus["addReactions"]["reactions"]:
                      try:
                          await msg.add_reaction(react)
                      except Exception:
                          pass

  def start(self, token):
    try:
      self.__clientUse.run(token)
    except Exception as e:
      print("An error connection occured while acessing to Discord!\n\n{0}".format(str(e)))