import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from src.libs.common.Logger.Logger import Logger
from src.libs.youtube_downloader.YouTubeDownloader import YouTubeDownloader

# Configura tus credenciales y permisos de Spotify
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id="TU_CLIENT_ID",
    client_secret="TU_CLIENT_SECRET",
    redirect_uri="http://localhost:8888/callback",
    scope="playlist-read-private"
))


class SpotifyDownloader:
    def __init__(self, logger):
        self.logger = logger
        self.youtube_downloader = YouTubeDownloader(logger)  # Instancia de YouTubeDownloader

    def download_playlist_from_spotify(self, playlist_name: str, download_path: str):
        # Buscar la lista de reproducción en la biblioteca del usuario
        playlists = sp.current_user_playlists()
        playlist_id = None
        for playlist in playlists['items']:
            if playlist['name'].lower() == playlist_name.lower():
                playlist_id = playlist['id']
                break

        if not playlist_id:
            self.logger.write_error(f"No se encontró la lista de reproducción: {playlist_name}")
            return

        # Obtener las pistas de la lista de reproducción
        tracks = sp.playlist_tracks(playlist_id)
        for item in tracks['items']:
            track = item['track']
            track_name = track['name']
            artist_name = track['artists'][0]['name']
            search_query = f"{track_name} {artist_name}"

            # Crear el path para la lista
            playlist_path = os.path.join(download_path, playlist_name)
            os.makedirs(playlist_path, exist_ok=True)

            self.logger.write_info(f"Descargando '{track_name}' de '{artist_name}' desde YouTube")
            self.youtube_downloader.download_video(
                url=f"ytsearch:{search_query}",
                path=playlist_path,
                keep_audio_only=True
            )

# Ejemplo de uso
logger = Logger()  # Asume que tienes una clase Logger implementada
spotify_downloader = SpotifyDownloader(logger)
spotify_downloader.download_playlist_from_spotify("Mi Lista de Spotify", "./descargas")
