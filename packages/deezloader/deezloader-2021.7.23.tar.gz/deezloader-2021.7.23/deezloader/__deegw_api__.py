#!/usr/bin/python3

from requests import Session
from .__download_utils__ import md5hex
from .exceptions import BadCredentials, TrackNotFound

from requests import (
	post as req_post,
	get as req_get
)

client_id = "172365"
client_secret = "fb0bec7ccc063dab0417eb7b0d847f34"

class API_GW:
	def __init__(self, arl):
		self.__arl = arl
		self.__token = "null"
		self.__req = Session()
		self.__req.cookies['arl'] = arl
		self.__get_lyric = "song.getLyrics"
		self.__get_song_data = "song.getData"
		self.__get_user_data = "deezer.getUserData"
		self.__get_album_data = "song.getListByAlbum"
		self.__get_playlist_data = "playlist.getSongs"
		self.__private_api_link = "https://www.deezer.com/ajax/gw-light.php"
		self.__song_server = "https://e-cdns-proxy-{}.dzcdn.net/mobile/1/{}"
		self.__get_media_url = "https://media.deezer.com/v1/get_url"
		self.__get_auth_token_url = "https://api.deezer.com/auth/token"
		self.__license_token = "AAAAAmD4joBhDFUA0fwVTPmQVTgWCccXkEE4deslOEqgk_NxFqiSUfaAORZ7EabILvle0ifjod2JybUjyONqIOWETqk6Tv_peYpYJDh7KlOjHrpjngVnOz6I5LBc70jql7kjJS53PFbbSoiCiZaaAw"
		self.__refresh_token()
		#self.__get_access_token()

	def __get_access_token(self):
		email = "yoheyar@bit-degree.com"
		password = "Guestpass1-"
		password = md5hex(password)

		request_hash = md5hex(
			"".join(
				[client_id, email, password, client_secret]
			)
		)

		params = {
			"app_id": client_id,
			"login": email,
			"password": password,
			"hash": request_hash
		}

		results = req_get(self.__get_auth_token_url, params = params).json()
		print(results)

	def __get_api(self, method, json_data = None):
		params = {
			"api_version": "1.0",
			"api_token": self.__token,
			"input": "3",
			"method": method
		}

		results = self.__req.post(
			self.__private_api_link,
			params = params,
			json = json_data
		).json()['results']

		if not results:
			self.__refresh_token()
			self.__get_api(method, json_data)

		return results

	def get_user(self):
		data = self.__get_api(self.__get_user_data)
		return data

	def __refresh_token(self):
		data = self.get_user()
		self.__token = data['checkForm']
		#self.__license_token = data['USER']['OPTIONS']['license_token']

	def am_I_log(self):
		data = self.get_user()
		user_id = data['USER']['USER_ID']

		if user_id == 0:
			raise BadCredentials(self.__arl)

	def get_song_data(self, ids):
		json_data = {
			"sng_id" : ids
		}

		infos = self.__get_api(self.__get_song_data, json_data)

		return infos

	def get_album_data(self, ids):
		json_data = {
			"alb_id": ids,
			"nb": -1
		}

		infos = self.__get_api(self.__get_album_data, json_data)

		return infos

	def get_lyric(self, ids):
		json_data = {
			"sng_id": ids
		}

		infos = self.__get_api(self.__get_lyric, json_data)

		return infos

	def get_playlist_data(self, ids):
		json_data = {
			"playlist_id": ids,
			"nb": -1
		}

		infos = self.__get_api(self.__get_playlist_data, json_data)

		return infos

	def song_exist(self, n, song_hash):
		song_url = self.__song_server.format(n, song_hash)
		print(song_url)
		crypted_audio = req_get(song_url)

		if len(crypted_audio.content) == 0:
			raise TrackNotFound

		return crypted_audio

	def get_url(self, tracks_token, quality):
		json_data = {
			"license_token": self.__license_token,
			"media": [
				{
					"type": "FULL",
					"formats": [
						{
							"cipher": "BF_CBC_STRIPE",
							"format": quality
						}
					]
				}
			],
			"track_tokens": tracks_token
		}

		infos = req_post(
			self.__get_media_url,
			json = json_data
		).json()

		medias = infos['data']

		return medias