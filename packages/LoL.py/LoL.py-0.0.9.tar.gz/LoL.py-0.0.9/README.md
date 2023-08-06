# LoL.py
A League Of Legends API Wrapper
```python
from LoL import LoL

api_key = "API TOKEN"

lol = LoL(api_key, "euw")

user_data = lol.get_summoner("summoner_name")

summonerId = user_data['id'] # grab summoner id
puuid = user_data['puuid'] # grab ppuid

matches = lol. get_matches_by_puuid(puuid)

single_match = matches[0]

print(lol.get_all_champions())

print(lol.get_summoner(accountId="acc_id"))

print(lol.get_summoner(puuid="puuid"))

print(lol.get_summoner(summonerid="summoner_id"))

print(lol.get_champion_rotations())

print(lol.get_champions_mastery_by_summonerId(summonerId))

print(lol.get_champion_mastery_by_summonerId_and_championId(summonerId,17))

print(lol. get_matches_by_puuid(puuid))

print(lol.get_match_by_matchid(single_match))
```