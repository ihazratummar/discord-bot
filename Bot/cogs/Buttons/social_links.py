import discord

class SocialLinks(discord.ui.View):
    def __init__(self):
        super().__init__()

        self.add_item(discord.ui.Button(label="Discord", url="https://discord.gg/DhsEvqHyE9", emoji="<:discord:1243197853371859017>"))
        self.add_item(discord.ui.Button(label="Facebook", url="https://www.facebook.com/crazyforsurprise", emoji="<:facebook:1243197848498077716>"))
        self.add_item(discord.ui.Button(label="YouTube", url="https://www.youtube.com/crazyforsurprise", emoji="<:youtube:1243197856014139485>"))
        self.add_item(discord.ui.Button(label="Instagram", url="https://www.instagram.com/ummaroyin/", emoji="<:instagram:1243197850880446464>"))
        
