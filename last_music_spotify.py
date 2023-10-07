#Importação de Bibliotecas
import pandas as pd
import requests
from spotipy.oauth2 import SpotifyOAuth
import spotipy.util as util

#Função para criar Token de acesso de um usuário em específico: create_user_access_token()

def create_user_access_token(username,clientID,secret):
    '''Função que utiliza a biblioteca Spotipy para realizar a criação de
       um token específico para coleta de dados pessoais do usuário
    '''
    # Configurações do aplicativo Spotify
    CLIENT_ID = clientID
    CLIENT_SECRET = secret
    REDIRECT_URI = 'http://localhost:8888/callback' 
    USERNAME = username  

    # Escopo de permissões que você deseja obter
    SCOPE = 'user-read-recently-played user-read-private user-read-email user-top-read'  # Solicita acesso ao histórico de reprodução recente do usuário

    # Autorização do usuário
    token = util.prompt_for_user_token(username=USERNAME,
                                       scope=SCOPE,
                                       client_id=CLIENT_ID,
                                       client_secret=CLIENT_SECRET,
                                       redirect_uri=REDIRECT_URI)

    return 'Bearer '+token

#Função para coletar os dados mais recentes de execução

def query_recent(token):
    '''Função que realiza a consulta dos últimos registros do player do spotify.
       Esta função executa a create_user_access_token(), pois necessita de um escopo específico.
       O limite padrão é 150, mas pode ter como entrada outro valor.
    '''
    headers = {
        "Authorization":  token
            }

    # Definir URL para pesquisa
    recently_played_url = "https://api.spotify.com/v1/me/player/recently-played"

    # Definindo parâmetro de limite de resultado. Inicialmente definido para 50. Usar com parcimônia, pois o Spotify bloqueia consultas muito longas
    params = {
        "limit": 50
    }

    # Realizar o Request na API do Spotify
    response = requests.get(recently_played_url, headers=headers, params=params)
    recently_played_data = response.json()

    # Extrair dados da resposta
    tracks = []
    for item in recently_played_data.get("items", []):
        track = item.get("track")
        if track:
            track_info = {
                "Nome da Música": track.get("name"),
                "Nome do Artista": track.get("artists")[0].get("name"),
                "Nome do Álbum": track.get("album").get("name"),
                "Link da Música": track.get("uri"),
                "Data de Execução": item.get("played_at")
            }
            tracks.append(track_info)
    #Retorno da Função
    return tracks

#Criação de Token do Spotify.
#O Token tem validade de 60 minutos
#Username pode ser coletado diretamente do painel de gerenciamento da conta do usuário
#O Client ID e o Secret precisam ser criadas no Dashboard de API do Spotify
token = create_user_access_token('22rxsto4zfjdqqyfdhx27v3jq','7d486b31ccdc419798ea333e9aa9c91c','018d8dfeb158496b80452b6a4ccbe28d')

ultimas_musicas = pd.DataFrame.from_dict(query_recent(token))
print(ultimas_musicas)
with open('arquivo.json', 'w') as arquivo:
    json.dump(ultimas_musicas, arquivo)