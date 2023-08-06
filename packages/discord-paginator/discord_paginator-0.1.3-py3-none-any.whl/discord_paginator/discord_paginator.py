import discord
from discord import Message,Embed
from discord_slash.model import ButtonStyle
from discord_slash.utils.manage_components import create_button, create_actionrow,create_select, create_select_option,wait_for_component
from discord_slash import SlashCommand
from discord.ext.commands import Bot
import asyncio
from typing import Union,Optional, List

class Page:
    def __init__(self,
                 message : Union[SlashCommand,Message],
                 bot : Bot,
                 embeds : Optional[List[Embed]] = None,
                 content : Optional[List[str]] = None,
                 timeout : Optional[int] = None,
                 hidden : Optional[bool] = False,
                 skipper : Optional[bool] = False):
        self.message=message
        self.bot=bot
        self.embeds=embeds
        self.content=content
        self.timeout=timeout
        self.hidden=hidden
        self.skipper=skipper
        if len(self.embeds)>len(self.content):
            self.length=len(self.embeds)
            while not len(self.embeds)==len(self.content):
                self.content.append(None)
        elif len(self.embeds)<len(self.content):
            self.length=len(self.content)
            while not len(self.embeds)==len(self.content):
                self.embeds.append(None)
        else:
            self.length=len(self.content)
    async def send(self):
        self.count=1
        if type(self.message)==SlashCommand:
            self.components=[create_actionrow(create_button(label="Back",style=ButtonStyle.gray,custom_id="Back",disabled=True),
                                            create_button(label="Page "+str(self.count)+"/"+str(self.length),disabled=True,style=ButtonStyle.gray),
                                            create_button(label="Next",custom_id="Next",style=ButtonStyle.gray))]
            msg = await self.message.send(content=self.content[self.count-1],embed=self.embeds[self.count-1],components=self.components,hidden=self.hidden)
            while True:
                try:
                    button_ctx : wait_for_component(client=self.bot,messages=msg,components=self.components,timeout=self.timeout)
                    if button_ctx.custom_id=="Next":
                        self.count=self.count+1
                    elif button_ctx.custom_id=="Back":
                        self.count=self.count-1
                    if self.count==1:
                        self.components = [create_actionrow(create_button(label="Back",style=ButtonStyle.gray,custom_id="Back",disabled=True),
                                                      create_button(label="Page "+str(self.count)+"/"+str(self.length),disabled=True,style=ButtonStyle.gray),
                                                      create_button(label="Next",custom_id="Next",style=ButtonStyle.gray))]
                    elif self.count==len(self.length):
                        self.components = [create_actionrow(create_button(label="Back",style=ButtonStyle.gray,custom_id="Back"),
                                                      create_button(label="Page "+str(self.count)+"/"+str(self.length),disabled=True,style=ButtonStyle.gray),
                                                      create_button(label="Next",custom_id="Next",style=ButtonStyle.gray,disabled=True))]
                    else:
                        self.components = [create_actionrow(create_button(label="Back",style=ButtonStyle.gray,custom_id="Back"),
                                                          create_button(label="Page "+str(self.count)+"/"+str(self.length),disabled=True,style=ButtonStyle.gray),
                                                          create_button(label="Next",custom_id="Next",style=ButtonStyle.gray))]
                    await button_ctx.edit_origin(content=self.content[self.count],embed=self.embeds[self.count],components=self.components)
                except:
                    self.components = [create_actionrow(create_button(label="Back",style=ButtonStyle.gray,custom_id="Back",disabled=True),
                                                          create_button(label="Page "+str(self.count)+"/"+str(self.length),disabled=True,style=ButtonStyle.gray),
                                                          create_button(label="Next",custom_id="Next",style=ButtonStyle.gray,disabled=True))]
                    await msg.edit(components=self.components)
                    break
        if type(self.message)==Message:
            self.components=[create_actionrow(create_button(label="Back",style=ButtonStyle.gray,custom_id="Back",disabled=True),
                                            create_button(label="Page "+str(self.count)+"/"+str(self.length),disabled=True,style=ButtonStyle.gray),
                                            create_button(label="Next",custom_id="Next",style=ButtonStyle.gray))]
            msg = await self.message.channel.send(content=self.content[self.count-1],embed=self.embeds[self.count-1],components=self.components)
            while True:
                try:
                    button_ctx : wait_for_component(client=self.bot,messages=msg,components=self.components,timeout=self.timeout)
                    if button_ctx.custom_id=="Next":
                        self.count=self.count+1
                    elif button_ctx.custom_id=="Back":
                        self.count=self.count-1
                    if self.count==1:
                        self.components = [create_actionrow(create_button(label="Back",style=ButtonStyle.gray,custom_id="Back",disabled=True),
                                                      create_button(label="Page "+str(self.count)+"/"+str(self.length),disabled=True,style=ButtonStyle.gray),
                                                      create_button(label="Next",custom_id="Next",style=ButtonStyle.gray))]
                    elif self.count==len(self.length):
                        self.components = [create_actionrow(create_button(label="Back",style=ButtonStyle.gray,custom_id="Back"),
                                                      create_button(label="Page "+str(self.count)+"/"+str(self.length),disabled=True,style=ButtonStyle.gray),
                                                      create_button(label="Next",custom_id="Next",style=ButtonStyle.gray,disabled=True))]
                    else:
                        self.components = [create_actionrow(create_button(label="Back",style=ButtonStyle.gray,custom_id="Back"),
                                                          create_button(label="Page "+str(self.count)+"/"+str(self.length),disabled=True,style=ButtonStyle.gray),
                                                          create_button(label="Next",custom_id="Next",style=ButtonStyle.gray))]
                    await button_ctx.edit_origin(content=self.content[self.count-1],embed=self.embeds[self.count-1],components=self.components)
                except:
                    self.components = [create_actionrow(create_button(label="Back",style=ButtonStyle.gray,custom_id="Back",disabled=True),
                                                          create_button(label="Page "+str(self.count)+"/"+str(self.length),disabled=True,style=ButtonStyle.gray),
                                                          create_button(label="Next",custom_id="Next",style=ButtonStyle.gray,disabled=True))]
                    await msg.edit(components=self.components)
                    break
