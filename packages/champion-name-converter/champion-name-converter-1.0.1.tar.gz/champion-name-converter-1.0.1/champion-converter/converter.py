import requests as req

class Converter:
	def __init__(self):
		get_all_versions = req.get('https://ddragon.leagueoflegends.com/api/versions.json').json()
		self.latest_version = get_all_versions[0]

	def champion_to_id(self, champion_name):
		self.champion_name = champion_name.lower().capitalize().replace("'", "")
		if self.champion_name == "Reksai":
			self.champion_name = "RekSai"
		elif self.champion_name == "Kogmaw":
			self.champion_name = "KogMaw"
		champion_url = 'https://ddragon.leagueoflegends.com/cdn/{}/data/en_US/champion/{}.json'.format(self.latest_version, self.champion_name)
		get_champion_info = req.get(champion_url)
		if get_champion_info.status_code != 403:
			data = get_champion_info.json()["data"]
			champion_id = data[self.champion_name]["key"]
			return champion_id
		else:
			raise Exception("Invalid Champion Name")
