from datetime import datetime, timedelta
from libs.portal_transparencia.utils.files import download_file_from_url, unzip_content
import os
from pathlib import Path 
import pandas as pd
import numpy as np

class Viagens:
    '''Portal da Transparência - Dados de Viagens'''
    _max_year = 2011
    _url_base = 'https://dadosabertos-download.cgu.gov.br/PortalDaTransparencia/saida/viagens/'

    def __init__(self) -> None:
        self._year = ((ano_atual := datetime.now().year) - 1)
        self.url = ''
        self.dados_disponiveis = list(range(self._max_year,ano_atual ))
        self.temp_folder:Path = Path()
        self.set_temp_folder()

    @property
    def year(self):
        return self._year
    @year.setter
    def year(self, value:int):
        if value > (ano_anterior := datetime.now().year - 1):
            value = ano_anterior
        self._year = self._max_year if value < self._max_year else value
        self.set_temp_folder()

    def set_temp_folder(self):
        self.temp_folder = Path(__file__).parent.parent.parent.parent / 'tmp_gov' /f'tmp_{self._year}'

    
    def url_valida(self):
        '''Encontra a URL Valida mais Atual dos últimos 60 dias'''
        data = datetime.now()
        dia = timedelta(days=1)
        cont = 0
        while cont<60:
            cont += 1
            url = f'{self._url_base}{self.year}'
            url_final = (f'_{data.year}' +
            f'{self._return_dois_digitos_num(data.month)}' +
            f'{self._return_dois_digitos_num(data.day)}_Viagens.zip')
            url = url + url_final
            data = data - dia
            try:
                r = download_file_from_url(url).raise_for_status()
                return url_final
            except:
                pass    

        raise ValueError('Não foi possível encontrar a URL.')

    def _return_dois_digitos_num(self, num:int) -> str:
        if len(str(num)) == 1:
            return f'0{num}'
        return str(num)
    
    def get_url(self):
        if self.url == '':
            self._url_final = self.url_valida()
        self.url = f'{self._url_base}{self.year}' + self._url_final


    def _download_and_extract(self):
        '''Baixa e extrai arquivos da URL'''
        self.get_url()
        print(f'Realizando download de : {self.url}')
        resp = download_file_from_url(self.url)
        unzip_content(resp,self.temp_folder.as_posix())
    
    def _clear_temp_folder(self):
        if not self.temp_folder.exists():
            return
        for file in self.temp_folder.iterdir():
            os.remove(file)
    
    def load_files_as_df(self):
        '''Carregando arquivos como df'''
        dicionario = {
            'Código Do Órgão Superior':(lambda x:x['Código Do Órgão Superior'].astype(np.int32)),
            'Codigo Do Órgão Pagador':(lambda x:x['Codigo Do Órgão Pagador'].astype(np.int32)),
            'Nome Da Unidade Gestora Pagadora': lambda x:x['Nome Da Unidade Gestora Pagadora'].astype('category'),
            'Tipo De Pagamento': lambda x:x['Tipo De Pagamento'].astype('category'),
            'Nome Do Órgão Superior': lambda x:x['Nome Do Órgão Superior'].astype('category'),
            'Nome Do Órgao Pagador': lambda x:x['Nome Do Órgao Pagador'].astype('category'),
            'Código Da Unidade Gestora Pagadora': lambda x:x['Código Da Unidade Gestora Pagadora'].astype('category'),
            'Valor': lambda x:x['Valor'].apply(lambda x : x.replace(',','.')).astype(np.float32),
            'Meio De Transporte': lambda x:x['Meio De Transporte'].astype('category'),
            'País - Origem Ida': lambda x:x['País - Origem Ida'].astype('category'),
            'Uf - Origem Ida': lambda x:x['Uf - Origem Ida'].astype('category'),
            'Cidade - Origem Ida': lambda x:x['Cidade - Origem Ida'].astype('category'),
            'País - Destino Ida': lambda x:x['País - Destino Ida'].astype('category'),
            'Uf - Destino Ida': lambda x:x['Uf - Destino Ida'].astype('category'),
            'Cidade - Destino Ida': lambda x:x['Cidade - Destino Ida'].astype('category'),
            'País - Origem Volta': lambda x:x['País - Origem Volta'].astype('category'),
            'Uf - Origem Volta': lambda x:x['Uf - Origem Volta'].astype('category'),
            'Cidade - Origem Volta': lambda x:x['Cidade - Origem Volta'].astype('category'),
            'Pais - Destino Volta': lambda x:x['Pais - Destino Volta'].astype('category'),
            'Uf - Destino Volta': lambda x:x['Uf - Destino Volta'].astype('category'),
            'Cidade - Destino Volta': lambda x:x['Cidade - Destino Volta'].astype('category'),
            'Valor Da Passagem': lambda x:x['Valor Da Passagem'].apply(lambda x : x.replace(',','.')).astype(np.float32),
            'Taxa De Serviço': lambda x:x['Taxa De Serviço'].apply(lambda x : x.replace(',','.')).astype(np.float32),
            'Sequência Trecho': lambda x:x['Sequência Trecho'].astype(np.int8),
            'Origem - País': lambda x:x['Origem - País'].astype('category'),
            'Origem - Uf': lambda x:x['Origem - Uf'].astype('category'),
            'Origem - Cidade': lambda x:x['Origem - Cidade'].astype('category'),
            'Destino - País': lambda x:x['Destino - País'].astype('category'),
            'Destino - Uf': lambda x:x['Destino - Uf'].astype('category'),
            # 'Destino - Cidade': lambda x:x['Destino - Cidade'].astype('category'),
            'Número Diárias': lambda x:x['Número Diárias'].apply(lambda x : x.replace(',','.')).astype(np.float32),
            'Missao?': lambda x:x['Missao?'].astype('category'),
            'Valor Outros Gastos': lambda x:x['Valor Outros Gastos'].apply(lambda x : x.replace(',','.')).astype(np.float32),
            'Valor Devolução': lambda x:x['Valor Devolução'].apply(lambda x : x.replace(',','.')).astype(np.float32),
            'Valor Passagens': lambda x:x['Valor Passagens'].apply(lambda x : x.replace(',','.')).astype(np.float32),
            'Valor Diárias': lambda x:x['Valor Diárias'].apply(lambda x : x.replace(',','.')).astype(np.float32),
            'Motivo': lambda x:x['Motivo'].astype('category'),
            'Destinos': lambda x:x['Destinos'].astype('category'),
            'Descrição Função': lambda x:x['Descrição Função'].astype('category'),
            'Função': lambda x:x['Função'].astype('category'),
            'Cargo': lambda x:x['Cargo'].astype('category'),
            'Nome Órgão Solicitante': lambda x:x['Nome Órgão Solicitante'].astype('category'),
            
            'Período - Data De Fim': lambda x:x['Período - Data De Fim'].apply(lambda x:datetime.strptime(x,'%d/%m/%Y')),
            'Período - Data De Início': lambda x:x['Período - Data De Início'].apply(lambda x:datetime.strptime(x,'%d/%m/%Y')),
            'Origem - Data': lambda x:x['Origem - Data'].apply(lambda x:datetime.strptime(x,'%d/%m/%Y')),
            'Destino - Data': lambda x:x['Destino - Data'].apply(lambda x:datetime.strptime(x,'%d/%m/%Y')),
            'Data Da Emissão/Compra': lambda x:x['Data Da Emissão/Compra'].apply(lambda x:datetime.strptime(x,'%d/%m/%Y')),
            
                      }
        
        if not self.temp_folder.exists():
            self._download_and_extract()
             
        for file in self.temp_folder.iterdir():
            df = pd.DataFrame()
            if file.name.endswith('csv'):

                for chunck in pd.read_csv(
                    file,
                    sep=';',
                    encoding='ISO-8859-1',
                    chunksize=500_000,
                    low_memory=False
                           ):
                    
                    df = pd.concat([df,chunck])
                df.rename(
                    columns={column:column.strip().title() for column in df.columns },
                    inplace=True)
                
                for key, value in dicionario.items():
                    try:
                        df[key] = value(df)
                    except:
                        pass
            os.remove(file)#apaga arquivo
            yield df
        return 
    
    def get_data_dfs(self)-> pd.DataFrame:
        '''Une os arquivos baixados e retorna um DataFrames'''
        if (data_frame := (self.temp_folder / f'{self.year}.pickle')).exists():
            return pd.read_pickle(data_frame)
        columns_to_delet = ['Codigo Do Órgão Pagador',
                            'Código Do Órgão Superior',
                            'Código Do Órgão Solicitante',
                            'Código Da Unidade Gestora Pagadora'
                            ]
        cont = 0
        df_final = pd.DataFrame()
        for df in self.load_files_as_df():
            if cont == 0:
                df_final = df
            else:
                df_final = df_final.join(df, rsuffix=f'_*_{cont}')
            for column in df_final.columns :
                if '_*_' in column or column in columns_to_delet:
                    df_final.drop(column, axis=1, inplace=True)

            cont += 1
        df_final.to_pickle(self.temp_folder / f'{self.year}.pickle')
        return df_final



if __name__== '__main__':
    a = Viagens()
    a.get_data_dfs()
    
    
    