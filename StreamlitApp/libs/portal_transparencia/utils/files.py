import requests
from zipfile import ZipFile 
from io import BytesIO

def download_file_from_url(url):
    '''Download conteudo de url'''
    response = requests.get(url, stream=True)
    return response

def unzip_content(response,path:str=''):
    '''Descompacta conteúdo zip'''
    ZipFile(BytesIO(response.content)).extractall(path)



if __name__ == '__main__':
    url = 'https://dadosabertos-download.cgu.gov.br/PortalDaTransparencia/saida/viagens/2022_20240519_Viagens.zip'
    r = download_file_from_url(url)
    r.raise_for_status()
    unzip_content(r)  # Descompacta conteúdo zip

