from libs.st_components.sidebar import SideBarBase
from libs.portal_transparencia.viagens import Viagens
import streamlit as st
import numpy as np
import plotly.express as px
import pandas as pd
import locale
locale.setlocale(locale.LC_ALL,'')


class App(SideBarBase):
    def __init__(self) -> None:
        self.config_app()
        super().__init__()
        self.viagens = Viagens()
        self.op = self.viagens.dados_disponiveis
        self.config_sidebar()
        self.graph_metricas(df:=self.get_df(self.chosed_year))
        self.graph_bublle(df)

    def config_app(self):
        st.set_page_config(
            page_title='Viagens - Portal da Transparência',
            page_icon='🛫',
            layout='wide',
            initial_sidebar_state="collapsed"
        )
        self.sidebar_title = 'Viagens - Portal da Transparência.'
    
    def config_sidebar(self) -> None:
        self.sidebar_description = '''
Dash Board sobre informações de viagens contidas no [Portal da Transparência](https://portaldatransparencia.gov.br/download-de-dados).
        '''
        st.sidebar.markdown('''# Escolha um Período.''')
        st.sidebar.markdown('Ao escolher um ano, serão coletados dados do ano escolhido até o presente momento')
        self.chosed_year = st.sidebar.selectbox(
            'Ano',
            self.op[::-1],
            index=0,
            )
        ##TODO - Inserir pediodo contemplado no DF
        self.qr_code_addrs_into = True
        self.badge_in_sidebar = True

    @st.cache_data
    def get_df(_self, year:int):
        _self.viagens.year = year
        return _self.viagens.get_data_dfs()
    
    @st.experimental_fragment
    def graph_bublle(self, df:pd.DataFrame):
        '''Gráfico de Órgãos que mais gastam com viagens'''
        df = df[['Nome Órgão Solicitante','Número Diárias','Valor']] 
        df = (df.groupby('Nome Órgão Solicitante', observed=False).
              sum().
              sort_values('Valor',ascending=False)[:100].reset_index())
        fig = px.scatter(
            df,
            x='Número Diárias', y='Valor', size='Valor', 
            color='Valor',
            hover_name='Nome Órgão Solicitante', 
            log_x=True, size_max=60
            )
        fig.update_layout(
            title_text="Gastos com Diárias por Órgão".upper(),
            title_x=0.5
            )
        st.plotly_chart(fig)
    
    @st.experimental_fragment
    def graph_metricas(self, df:pd.DataFrame):
        '''Grafico com os principais destinos'''
        df = df [['Valor Diárias','Valor Passagens','Valor Outros Gastos']]
        col = st.columns((1,1,1,1,1),gap='small')
        with col[0]:
            conteiner = st.container(border=True)
            conteiner.metric(
                label="Total de Viagens", 
                value=self.abreviar_numero(tot_viagens:=len(df.index), moeda=False),
                help='Total de viagem realizadas no período')
        
        with col[1]:
            conteiner = st.container(border=True)
            conteiner.metric(
            label="Total Gasto em Diárias", 
            value=self.abreviar_numero(
                tot_diarias := df['Valor Diárias'].sum()),
            help='Total de Gasto em Diárias no período')
        
        with col[2]:
            conteiner = st.container(border=True)
            conteiner.metric(
            label="Total Gasto em Passagens", 
            value=self.abreviar_numero(
                tot_passagens :=df['Valor Passagens'].sum()
                ), 
            help='Total de Gasto em Passagens no período')
        
        with col[3]:
            conteiner = st.container(border=True)
            conteiner.metric(
            label="Total de Outros Gastos", 
            value=self.abreviar_numero((tot_outros :=df['Valor Outros Gastos'].sum())), 
            # delta="1.2 °F",
            help='Total de Gasto com Outros Gastos no período')
        
        with col[4]:
            conteiner = st.container(border=True)
            conteiner.metric(
            label="Custo Médio por Viagem", 
            value=self.abreviar_numero((tot_diarias + tot_passagens + tot_outros) / tot_viagens), 
            help='Total de Gasto com Outros Gastos no período')
    
    def abreviar_numero(self,numero:int|float, moeda:bool=True):
        # Define os sufixos para cada ordem de magnitude
        sufixos = ['', 'K', 'M', 'B', 'T', 'P', 'E', 'Z', 'Y']
        # Converte o número para float para operações de divisão
        numero = float(numero)
        # Itera sobre os sufixos, dividindo o número por 1000 a cada passo
        for i, sufixo in enumerate(sufixos):
            if abs(numero) < 1000:
                return (locale.currency(
                    numero,
                    grouping=True
                    ) if moeda else str(numero)) + sufixo
            numero /= 1000
        return (locale.currency(
                    numero,
                    grouping=True
                    ) if moeda else str(numero)) + 'Y'  # Caso o número seja extremamente grande
        


    