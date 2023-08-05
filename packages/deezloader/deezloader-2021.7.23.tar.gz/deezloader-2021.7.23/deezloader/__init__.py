#!/usr/bin/python3

from .__dee_api__ import API
from .__easy_spoty__ import Spo
from .__deegw_api__ import API_GW

from .models import (
	Track, Album, Playlist,
	Preferences, Smart
)

from .__download__ import (
	DW_TRACK, DW_ALBUM, DW_PLAYLIST,
	Download_JOB
)

from .exceptions import (
	InvalidLink, TrackNotFound,
	NoDataApi, AlbumNotFound
)

from .__utils__ import (
	create_zip, get_ids, link_is_valid,
	what_kind, convert_to_date
)

from .__others_settings__ import (
	stock_output, stock_quality,
	stock_recursive_quality, stock_recursive_download,
	stock_not_interface, stock_zip, method_save
)

class Login:
	def __init__(self, arl):
		self.__api = API()
		self.__gw_api = API_GW(arl)
		self.__gw_api.am_I_log()
		self.__spo = Spo()
		self.__download_job = Download_JOB(self.__gw_api, self.__api)

	def download_trackdee(
		self, link_track,
		output_dir = stock_output,
		quality_download = stock_quality,
		recursive_quality = stock_recursive_quality,
		recursive_download = stock_recursive_download,
		not_interface = stock_not_interface,
		method_save = method_save
	) -> Track:

		link_is_valid(link_track)
		ids = get_ids(link_track)

		try:
			song_metadata = self.__api.tracking(ids)
		except NoDataApi:
			infos = self.__gw_api.get_song_data(ids)
			ids = infos['FALLBACK']['SNG_ID']
			song_metadata = self.__api.tracking(ids)

		preferences = Preferences()

		preferences.link = link_track
		preferences.song_metadata = song_metadata
		preferences.quality_download = quality_download
		preferences.output_dir = output_dir
		preferences.ids = ids
		preferences.recursive_quality = recursive_quality
		preferences.recursive_download = recursive_download
		preferences.not_interface = not_interface
		preferences.method_save = method_save

		track = DW_TRACK(self.__download_job, preferences).dw()

		return track

	def download_albumdee(
		self, link_album,
		output_dir = stock_output,
		quality_download = stock_quality,
		recursive_quality = stock_recursive_quality,
		recursive_download = stock_recursive_download,
		not_interface = stock_not_interface,
		make_zip = stock_zip,
		method_save = method_save
	) -> Album:

		link_is_valid(link_album)
		ids = get_ids(link_album)

		try:
			album_json = self.__api.get_album(ids)
		except NoDataApi:
			raise AlbumNotFound(link_album)

		song_metadata = {
			"music": [],
			"artist": [],
			"tracknum": [],
			"discnum": [],
			"bpm": [],
			"duration": [],
			"isrc": [],
			"gain": [],
			"album": album_json['title'],
			"label": album_json['label'],
			"year": convert_to_date(album_json['release_date']),
			"upc": album_json['upc'],
			"nb_tracks": album_json['nb_tracks']
		}

		genres = []

		if "genres" in album_json:
			for a in album_json['genres']['data']:
				genres.append(a['name'])

		song_metadata['genre'] = " & ".join(genres)
		ar_album = []

		for a in album_json['contributors']:
			if a['role'] == "Main":
				ar_album.append(a['name'])

		song_metadata['ar_album'] = " & ".join(ar_album)

		for track in album_json['tracks']['data']:
			c_ids = track['id']
			detas = self.__api.tracking(c_ids, True)

			for key, item in song_metadata.items():
				if type(item) is list:
					song_metadata[key].append(detas[key])

		preferences = Preferences()

		preferences.link = link_album
		preferences.song_metadata = song_metadata
		preferences.quality_download = quality_download
		preferences.output_dir = output_dir
		preferences.ids = ids
		preferences.recursive_quality = recursive_quality
		preferences.recursive_download = recursive_download
		preferences.not_interface = not_interface
		preferences.method_save = method_save
		preferences.make_zip = make_zip

		album = DW_ALBUM(self.__download_job, preferences).dw()

		return album

	def download_playlistdee(
		self, link_playlist,
		output_dir = stock_output,
		quality_download = stock_quality,
		recursive_quality = stock_recursive_quality,
		recursive_download = stock_recursive_download,
		not_interface = stock_not_interface,
		make_zip = stock_zip,
		method_save = method_save
	) -> Playlist:

		link_is_valid(link_playlist)
		ids = get_ids(link_playlist)

		song_metadata = []
		playlist_json = self.__api.get_playlist(ids)['tracks']['data']

		for track in playlist_json:
			c_ids = track['id']

			try:
				c_song_metadata = self.__api.tracking(c_ids)
			except NoDataApi:
				infos = self.__gw_api.get_song_data(c_ids)
				c_ids = infos['FALLBACK']['SNG_ID']
				c_song_metadata = self.__api.tracking(c_ids)
			
			song_metadata.append(c_song_metadata)

		preferences = Preferences()

		preferences.link = link_playlist
		preferences.song_metadata = song_metadata
		preferences.quality_download = quality_download
		preferences.output_dir = output_dir
		preferences.ids = ids
		preferences.recursive_quality = recursive_quality
		preferences.recursive_download = recursive_download
		preferences.not_interface = not_interface
		preferences.method_save = method_save
		preferences.make_zip = make_zip

		playlist = DW_PLAYLIST(self.__download_job, preferences).dw()

		return playlist

	def download_artisttopdee(
		self, link_artist,
		output_dir = stock_output,
		quality_download = stock_quality,
		recursive_quality = stock_recursive_quality,
		recursive_download = stock_recursive_download,
		not_interface = stock_not_interface
	) -> list[Track]:

		link_is_valid(link_artist)
		ids = get_ids(link_artist)

		playlist_json = self.__api.get_artist_top_tracks(ids)['data']

		names = [
			self.download_trackdee(
				track['link'], output_dir,
				quality_download, recursive_quality,
				recursive_download, not_interface
			)

			for track in playlist_json
		]

		return names

	def convert_spoty_to_dee_link_track(self, link_track):
		link_is_valid(link_track)
		ids = get_ids(link_track)

		track_json = self.__spo.get_track(ids)
		isrc = f"isrc:{track_json['external_ids']['isrc']}"

		track_json_dee = self.__api.get_track(isrc)
		track_link_dee = track_json_dee['link']
		return track_link_dee

	def download_trackspo(
		self, link_track,
		output_dir = stock_output,
		quality_download = stock_quality,
		recursive_quality = stock_recursive_quality,
		recursive_download = stock_recursive_download,
		not_interface = stock_not_interface,
		method_save = method_save
	) -> Track:

		track_link_dee = self.convert_spoty_to_dee_link_track(link_track)

		track = self.download_trackdee(
			track_link_dee,
			output_dir = output_dir,
			quality_download = quality_download,
			recursive_quality = recursive_quality,
			recursive_download = recursive_download,
			not_interface = not_interface,
			method_save = method_save
		)

		return track

	def convert_spoty_to_dee_link_album(self, link_album):
		link_is_valid(link_album)
		ids = get_ids(link_album)
		link_dee = None

		tracks = self.__spo.get_album(ids)

		try:
			#print(tracks['external_ids']['upc'])
			upc = f"0{tracks['external_ids']['upc']}"

			while upc[0] == "0":
				upc = upc[1:]

				try:
					upc = f"upc:{upc}"
					url = self.__api.get_album(upc)
					link_dee = url['link']
					break
				except NoDataApi:
					if upc[0] != "0":
						raise AlbumNotFound
		except AlbumNotFound:
			tot = tracks['total_tracks']
			tracks = tracks['tracks']['items']
			tot2 = None

			for track in tracks:
				track_link = track['external_urls']['spotify']
				track_info = self.__spo.get_track(track_link)

				try:
					isrc = f"isrc:{track_info['external_ids']['isrc']}"
					track_data = self.__api.get_track(isrc)
					album_ids = track_data['album']['id']
					album_json = self.__api.get_album(album_ids)
					tot2 = album_json['nb_tracks']

					if tot == tot2:
						link_dee = album_json['link']
						break
				except NoDataApi:
					pass

			if tot != tot2:
				raise AlbumNotFound(link_album)

		return link_dee

	def download_albumspo(
		self, link_album,
		output_dir = stock_output,
		quality_download = stock_quality,
		recursive_quality = stock_recursive_quality,
		recursive_download = stock_recursive_download,
		not_interface = stock_not_interface,
		make_zip = stock_zip,
		method_save = method_save
	) -> Album:

		link_dee = self.convert_spoty_to_dee_link_album(link_album)

		album = self.download_albumdee(
			link_dee, output_dir,
			quality_download, recursive_quality,
			recursive_download, not_interface,
			make_zip, method_save
		)

		return album

	def download_playlistspo(
		self, link_playlist,
		output_dir = stock_output,
		quality_download = stock_quality,
		recursive_quality = stock_recursive_quality,
		recursive_download = stock_recursive_download,
		not_interface = stock_not_interface,
		make_zip = stock_zip,
		method_save = method_save
	) -> Playlist:

		link_is_valid(link_playlist)
		ids = get_ids(link_playlist)
		playlist_json = self.__spo.get_playlist(ids)
		playlist_tracks = playlist_json['tracks']['items']
		playlist = Playlist()
		tracks = playlist.tracks

		for track in playlist_tracks:
			link_track = track['track']['external_urls']['spotify']

			try:
				track = self.download_trackspo(
					link_track,
					output_dir = output_dir,
					quality_download = quality_download,
					recursive_quality = recursive_quality,
					recursive_download = recursive_download,
					not_interface = not_interface,
					method_save = method_save
				)
			except (TrackNotFound, NoDataApi):
				info = track['track']
				artist = info['artists'][0]['name']
				song = info['name']
				track = f"{song} - {artist}"

			tracks.append(track)

		if make_zip:
			playlist_name = playlist_json['name']
			zip_name = f"{output_dir}playlist {playlist_name}.zip"
			create_zip(tracks, zip_name = zip_name)
			playlist.zip_path = zip_name

		return playlist

	def download_name(
		self, artist, song,
		output_dir = stock_output,
		quality_download = stock_quality,
		recursive_quality = stock_recursive_quality,
		recursive_download = stock_recursive_download,
		not_interface = stock_not_interface,
		method_save = method_save
	) -> Track:
		query = f"track:{song} artist:{artist}"
		search = self.__spo.search(query)
		items = search['tracks']['items']

		if len(items) == 0:
			msg = f"No result for {query} :("
			raise TrackNotFound(message = msg)

		link_track = items[0]['external_urls']['spotify']

		track = self.download_trackspo(
			link_track,
			output_dir = output_dir,
			quality_download = quality_download,
			recursive_quality = recursive_quality,
			recursive_download = recursive_download,
			not_interface = not_interface,
			method_save = method_save
		)

		return track

	def download_smart(
		self, link,
		output_dir = stock_output,
		quality_download = stock_quality,
		recursive_quality = stock_recursive_quality,
		recursive_download = stock_recursive_download,
		not_interface = stock_not_interface,
		make_zip = stock_zip,
		method_save = method_save
	) -> Smart:

		link_is_valid(link)
		link = what_kind(link)
		smart = Smart()

		if "spotify.com" in link:
			source = "https://spotify.com"

		elif "deezer.com" in link:
			source = "https://deezer.com"

		smart.source = source

		if "track/" in link:
			if "spotify.com" in link:
				func = self.download_trackspo

			elif "deezer.com" in link:
				func = self.download_trackdee
				
			else:
				raise InvalidLink(link)

			track = func(
				link,
				output_dir = output_dir,
				quality_download = quality_download,
				recursive_quality = recursive_quality,
				recursive_download = recursive_download,
				not_interface = not_interface,
				method_save = method_save
			)

			smart.type = "track"
			smart.track = track

		elif "album/" in link:
			if "spotify.com" in link:
				func = self.download_albumspo

			elif "deezer.com" in link:
				func = self.download_albumdee

			else:
				raise InvalidLink(link)

			album = func(
				link,
				output_dir = output_dir,
				quality_download = quality_download,
				recursive_quality = recursive_quality,
				recursive_download = recursive_download,
				not_interface = not_interface,
				make_zip = make_zip,
				method_save = method_save
			)

			smart.type = "album"
			smart.album = album

		elif "playlist/" in link:
			if "spotify.com" in link:
				func = self.download_playlistspo

			elif "deezer.com" in link:
				func = self.download_playlistdee

			else:
				raise InvalidLink(link)

			playlist = func(
				link,
				output_dir = output_dir,
				quality_download = quality_download,
				recursive_quality = recursive_quality,
				recursive_download = recursive_download,
				not_interface = not_interface,
				make_zip = make_zip,
				method_save = method_save
			)

			smart.type = "playlist"
			smart.playlist = playlist

		return smart