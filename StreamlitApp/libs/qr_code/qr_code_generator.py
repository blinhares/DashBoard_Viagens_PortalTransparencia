#type:ignore
import qrcode
from PIL import Image


def generate_qr_code(link, filename):
    qr = qrcode.QRCode(
        version=1,  # QR code version (1 to 40, higher means more data capacity)
        error_correction=qrcode.constants.ERROR_CORRECT_L,  # Error correction level ('L', 'M', 'Q', 'H')
        box_size=10,  # Pixel size of each box in the QR code
        border=4,  # Border size around the QR code (in boxes)
    )
    qr.add_data(link)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(filename)
    

def add_qr_code_to(
        _st,
        _link, 
        _filename,
        _caption="Generated QR Code",
        _use_column_width=True):
    """Adiciona um QR code gerado a um st ou  um st.sidebar
        st - st ou st.sidebar
        _link - endereco do qrcode gerado 
        _filename - nome do arquivo gerado que sera salvo
        _caption - legenda do qrcode
        _use_column_width - se o qrcode deve ser exibido com largura da coluna
    """
    
    generate_qr_code(
        _link,
        _filename)
    
    _st.image(
        Image.open(_filename) , 
        caption=_caption, 
        use_column_width=_use_column_width)


if __name__ == "__main__":
    generate_qr_code('asdasd','teste.png')