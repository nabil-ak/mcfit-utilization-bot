import discord
import requests
import os
from base64 import b64encode,b64decode
from datetime import datetime
from dotenv import load_dotenv
import dateutil.parser

load_dotenv()

EMAIL = os.environ['EMAIL']
PASSWORD = os.environ['PASSWORD']
STUDIO = {"hash":os.environ['STUDIO'], "int":(b64decode(os.environ['STUDIO'].encode("utf-8"))).decode("utf-8").split(":")[1]}
SESSION = os.environ['SESSION']
S = requests.Session()
if len(SESSION) > 8:
    S.cookies.set('SESSION', SESSION)

# API_HOST = "my.mcfit.com"
API_HOST = "mein.fitx.de"
PUBLIC_FACILITY_GROUP = "FITXDE-7B7DAC63E1744DE797245D6E314CD8F6"
TENANT = "fitx"
UTILIZATION_VERSION = 2

try:
    res = requests.get("https://" + API_HOST + "/whitelabelconfigs/web")
    res.raise_for_status()
    PUBLIC_FACILITY_GROUP = res.json()["publicFacilityGroup"]
    TENANT = res.json()["tenantName"]
except Exception as e:
    print(e)
    print("FitX api has changed, please raise an issue on github")
    exit()

try:
    res = requests.get("https://" + API_HOST + "/sponsorship/v1/public/studios/"+STUDIO["hash"],
        headers={
            "x-public-facility-group": PUBLIC_FACILITY_GROUP
        }
    )
    res.raise_for_status()
    NAME = res.json()["name"]
except Exception as e:
    print(e)
    print("Your Studio ID is wrong")
    exit()

print(f"Studio: {NAME}")
bot = discord.Bot() 

async def login():
    if EMAIL == "ENTER_EMAIL":
        print("Set an email and password in the .env file")
        exit()
    headers = {
        'authority': API_HOST,
        'accept': '*/*',
        'accept-language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7',
        'authorization': f'Basic {(b64encode((EMAIL+":"+PASSWORD).encode("utf-8"))).decode("utf-8")}',
        'origin': 'https://' + API_HOST,
        'referer': 'https://' + API_HOST + '/login-register',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
        'x-nox-client-type': 'WEB',
        'x-public-facility-group': PUBLIC_FACILITY_GROUP,
        'x-tenant': TENANT,
    }
    
    json_data = {
        'username': EMAIL,
        'password': PASSWORD,
    }

    r = S.post('https://' + API_HOST + '/login', headers=headers, json=json_data)
    r.raise_for_status()
    print("Session after login: " + S.cookies.get('SESSION'))

async def get_util_v1():
    headers = {
        'authority': API_HOST,
        'accept': '*/*',
        'accept-language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7',
        'content-type': 'application/json',
        'referer': 'https://' + API_HOST + '/studio/'+STUDIO["hash"],
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
        'x-public-facility-group': PUBLIC_FACILITY_GROUP,
        'x-tenant': TENANT,
    }
    r = S.get(f'https://{API_HOST}/nox/v1/studios/{STUDIO["int"]}/utilization', headers=headers)
    if r.status_code != 200:
        await login()
        r = S.get(f'https://{API_HOST}/nox/v1/studios/{STUDIO["int"]}/utilization', headers=headers)
    r.raise_for_status()
    return r.json()

async def get_util_v2():
    headers = {
        'authority': API_HOST,
        'accept': '*/*',
        'accept-language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7',
        'content-type': 'application/json',
        'referer': 'https://' + API_HOST + '/studio/'+STUDIO["hash"],
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
        'x-ms-web-context': '/studio/'+STUDIO["hash"],
        'x-nox-client-type': 'WEB',
        'x-nox-web-context': '',
        'x-public-facility-group': PUBLIC_FACILITY_GROUP,
        'x-tenant': TENANT,
    }
    r = S.get(f'https://{API_HOST}/nox/v1/studios/{STUDIO["int"]}/utilization/v2/today', headers=headers)
    if r.status_code != 200:
        await login()
        r = S.get(f'https://{API_HOST}/nox/v1/studios/{STUDIO["int"]}/utilization/v2/today', headers=headers)
    r.raise_for_status()
    return r.json()

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

@bot.slash_command(description="Show the current Utilization")
async def util(ctx):
    try:
        if UTILIZATION_VERSION == 1:
            info = await get_util_v1()
        elif UTILIZATION_VERSION == 2:
            info = await get_util_v2()
        embed = discord.Embed(title=f"{NAME} Utilization", color=16774219) 
        time = ""
        status = ""

        isCurrentStr = "current"
        if UTILIZATION_VERSION == 1:
            info = info["items"]
            isCurrentStr = "isCurrent"
        for item in info:
            start = dateutil.parser.parse(item['startTime'], fuzzy=True).strftime("%H:%M")
            end = dateutil.parser.parse(item['endTime'], fuzzy=True).strftime("%H:%M")
            time += f"{start} -> {end}\n"
            if item['percentage'] > 80:
                status+=f"🔴 {item['percentage']}%\n"
            elif item['percentage'] > 40:
                status+=f"🟡 {item['percentage']}%\n"
            else:
                status+=f"🟢 {item['percentage']}%\n"
            
            if item[isCurrentStr]:
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


