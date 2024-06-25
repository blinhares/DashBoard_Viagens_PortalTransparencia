from typing import Any
import streamlit as st
from libs.qr_code.qr_code_generator import add_qr_code_to # type: ignore
from libs.ip.local_ip import get_local_ip


class SideBarBase:
    """``
    Sidebar base class
    """
    def __init__(self) -> None:
        self._sidebar_title:str = ''
        self._sidebar_description = ''
        self._qr_code_addrs_into = True
        self._badge_in_sidebar = True
        
    @property
    def sidebar_title(self):
        return self._sidebar_title
    @sidebar_title.setter
    def sidebar_title(self,title:str):
        self._sidebar_title = title
        self.set_sidebar_title()
    
    @st.cache_resource
    def set_sidebar_title(_self):
        st.sidebar.title(_self._sidebar_title)

    @property
    def sidebar_description(_self):
        return _self._sidebar_description
    @sidebar_description.setter
    def sidebar_description(self, description:str):
        self._sidebar_description = description
        self.set_sidebar_description()

    @st.cache_data
    def set_sidebar_description(_self):
        st.sidebar.markdown(_self.sidebar_description)

    @property
    def qr_code_addrs_into(self):
        return self._qr_code_addrs_into
    @qr_code_addrs_into.setter
    def qr_code_addrs_into(self, value:bool):
        self._qr_code_addrs_into = value
        if value:
            self.add_qrcode_adds_in_sidebar(st.sidebar)

    @property
    def badge_in_sidebar(self):
        return self._badge_in_sidebar
    @badge_in_sidebar.setter
    def badge_in_sidebar(self, value:bool):
        self._badge_in_sidebar = value
        if value:
            self.add_badge_in_sidebar()

    @st.cache_data
    def add_badge_in_sidebar(_self):
        st.sidebar.html(
            '''<p align="center"><img src="https://img.shields.io/badge/Blinhares-white?logo=github&logoColor=181717&style=for-the-badge&label=git" /><p align="center">
        ''')

    @st.cache_data
    def add_qrcode_adds_in_sidebar(_self,
        _st:Any,
        _caption:str='Leia Este QrCode Para ter Acesso em Outros Dispositivos Locais',
        _use_column_width:bool=True):
        """Adiciona um QR code gerado com o endereço local
         a um st ou  um st.sidebar
        _st - st ou st.sidebar
        _link - endereco do qrcode gerado 
        _filename - nome do arquivo gerado que sera salvo
        _caption - legenda do qrcode
        _use_column_width - se o qrcode deve ser exibido com largura da coluna
    """
        local_addrs =f"http://{get_local_ip()}:8501"

        add_qr_code_to(_st,
            local_addrs,
            'meu_ip_qr.png',
            _caption,
            _use_column_width)