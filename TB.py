import json
import requests
import discord
import tb_config

url = 'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key='
key = tb_config.perspective_api_key



client = discord.Client()

@client.event
async def on_ready():
	try:
		print(f"We have logged in as {client.user}")
	except SSLCertVerification as e:
		print("Error handled")


@client.event
async def on_message(message):  
	if (message.author.id != tb_config.discord_bot_id): #makes sure that it does not read its own messages
		if "!logout" in message.content.lower():
			if (message.author.id in tb_config.admin_ids): 
			#checks if user is admin
				await message.channel.send("Bye bye!")
				await client.close()
			else:
				await message.channel.send("Umm, no!")

		if "!help" in message.content.lower():
			await message.channel.send("""```This bot checks the toxicity of messages and warns the user if message is too toxic.

Use !check followed by sentence to check the toxicity of that message.```""")

		payload = {'comment': {'text': message.content}, 'languages': ['en'], 'requestedAttributes': {'TOXICITY':{}} }
		r = requests.post(str(url+key), data = json.dumps(payload))


		tscore = float(r.json()["attributeScores"]["TOXICITY"]["summaryScore"]["value"])
		if message.content.startswith("!check"):
			await message.channel.send("""Message by {0.author.name} - ```{2}```Toxicity = {1}""".format(message, tscore, message.content[7:]))

		else:

			print(tscore)
			if ((tscore) >= 0.9):
				await message.channel.send("Please don't be toxic! {0.author.mention}".format(message))


		

client.run(tb_config.discord_bot_token)


