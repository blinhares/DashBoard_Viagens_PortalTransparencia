#makefile
all:
	@pip install poetry ; poetry install
build-app:
	@pyinstaller StreamlitApp/streamlit_app.spec --clean --noconfirm ; sudo rm -R build/
