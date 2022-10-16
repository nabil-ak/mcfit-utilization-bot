import discord
import requests
import os
from base64 import b64encode,b64decode
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

EMAIL = os.environ['EMAIL']
PASSWORD = os.environ['PASSWORD']
STUDIO = {"hash":os.environ['STUDIO'], "int":(b64decode(os.environ['STUDIO'].encode("utf-8"))).decode("utf-8").split(":")[1]}
S = requests.Session()

try:
    res = requests.get("https://my.mcfit.com/sponsorship/v1/public/studios/"+STUDIO["hash"],
        headers={
        "x-public-facility-group":"MCFIT-2DBEBDE87C264635B943F583D13156C0"
        }
    )
    res.raise_for_status()
    NAME=res.json()["name"]
except Exception as e:
    print(e)
    print("Your Studio ID is wrong")
    exit()

bot = discord.Bot() 

async def login():
    headers = {
        'authority': 'my.mcfit.com',
        'accept': '*/*',
        'accept-language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7',
        'authorization': f'Basic {(b64encode((EMAIL+":"+PASSWORD).encode("utf-8"))).decode("utf-8")}',
        'origin': 'https://my.mcfit.com',
        'referer': 'https://my.mcfit.com/login-register',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
        'x-nox-client-type': 'WEB',
        'x-public-facility-group': 'MCFIT-2DBEBDE87C264635B943F583D13156C0',
        'x-tenant': 'rsg-group',
    }
    
    json_data = {
        'username': EMAIL,
        'password': PASSWORD,
    }

    r = S.post('https://my.mcfit.com/login', headers=headers, json=json_data)
    r.raise_for_status()

async def get_util():
    headers = {
        'authority': 'my.mcfit.com',
        'accept': '*/*',
        'accept-language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7',
        'content-type': 'application/json',
        'referer': 'https://my.mcfit.com/studio/'+STUDIO["hash"],
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
        'x-ms-web-context': '/studio/'+STUDIO["hash"],
        'x-nox-client-type': 'WEB',
        'x-nox-web-context': 'v=1',
        'x-public-facility-group': 'MCFIT-2DBEBDE87C264635B943F583D13156C0',
        'x-tenant': 'rsg-group',
    }
    r = S.get(f'https://my.mcfit.com/nox/v1/studios/{STUDIO["int"]}/utilization', headers=headers)
    if r.status_code != 200:
        await login()
        r = S.get(f'https://my.mcfit.com/nox/v1/studios/{STUDIO["int"]}/utilization', headers=headers)
    r.raise_for_status()
    return r.json()

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

@bot.slash_command(description="Show the current Utilization")
async def util(ctx):
    try:
        info = await get_util()
        embed = discord.Embed(title="McFit Utilization", color=16774219) 
        time = ""
        status = ""
        for item in info["items"]:
            time+=f"{item['startTime']} -> {item['endTime']}\n"
            if item['percentage']>80:
                status+=f"🔴 {item['percentage']}%\n"
            elif item['percentage']>40:
                status+=f"🟡 {item['percentage']}%\n"
            else:
                status+=f"🟢 {item['percentage']}%\n"
            if item['isCurrent']:
                break

        embed.add_field(name="Location", value=f"```{NAME}```", inline=False)
        embed.add_field(name="Time", value=f"```{time}```")
        embed.add_field(name="Status", value=f"```{status}```")
        embed.set_footer(text=f"{datetime.now().strftime('%d.%m.%Y %H:%M:%S')}")
        await ctx.respond(embed=embed)
    except Exception as e:
        print(e)
        await ctx.respond(f"Error")

if __name__ == "__main__":       
  bot.run(os.environ['DISCORD_BOT_TOKEN'])


