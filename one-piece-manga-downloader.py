import requests
from bs4 import BeautifulSoup
import os
from PyPDF2 import PdfWriter, PdfReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from pdf2image import convert_from_path
from ebooklib import epub
from PIL import Image

print("\033[1;31m" + """
╔═╗┌┐┌┌─┐  ╔═╗┬┌─┐┌─┐┌─┐
║ ║│││├┤   ╠═╝│├┤ │  ├┤ 
╚═╝┘└┘└─┘  ╩  ┴└─┘└─┘└─┘
╔╦╗┌─┐┌┐┌┌─┐┌─┐  ╔╦╗┌─┐┬ ┬┌┐┌┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
║║║├─┤││││ ┬├─┤   ║║│ ││││││││  │ │├─┤ ││├┤ ├┬┘
╩ ╩┴ ┴┘└┘└─┘┴ ┴  ═╩╝└─┘└┴┘┘└┘┴─┘└─┘┴ ┴─┴┘└─┘┴└─
""" + "\033[0m")

print("\033[1;33m" + """
⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⡴⠖⠚⠉⠉⠉⢻⣓⠒⠤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢀⠞⠁⢀⣶⣾⣧⣤⣤⣴⣿⣧⡀⠈⠑⣄⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⣰⣁⣾⠟⠛⠉⠉⠁⠀⠀⠉⠈⠉⠉⠒⢶⡌⢦⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⢀⡔⢋⣥⠀⠀⢀⣠⣤⡤⣤⣤⣤⣀⣀⠠⢀⣀⣍⠺⣆⠀⠀⠀⠀⠀⠀
⠀⠀⠀⡴⢻⣿⣶⣿⣴⣶⡿⠋⠈⡇⠘⣿⣿⢻⣻⣿⣷⣿⣿⣶⡌⢣⡀⠀⠀⠀⠀
⠀⢀⠎⣀⠈⣡⣾⣿⣿⡟⠀⠀⠀⢹⠀⠘⣿⡀⠳⣿⣿⣿⣿⣅⠀⠀⠳⡀⠀⠀⠀
⠀⡞⡸⠿⣴⢋⣿⣿⣿⡠⠄⠢⠄⠀⠀⠀⠘⠏⠉⠉⢿⣿⣿⣿⣦⠀⠀⢣⠀⠀⠀
⠐⡇⡿⢿⣿⣿⣿⣿⠉⠀⣠⣤⣀⢀⡀⠀⠀⡴⠒⠲⢈⣾⣿⢿⣿⣷⣶⢾⠀⠀⠀
⠈⣿⠃⣰⣿⣟⡟⠷⣄⠘⠁⠀⠉⢰⡃⠀⠀⠳⠼⢞⣫⡞⣿⣿⢾⣿⡇⡼⠀⠀⠀
⠀⠸⠆⠹⣿⣿⢹⠀⢸⠙⠒⠢⡤⠤⠥⣤⠴⠒⠺⡉⠀⣱⣿⣿⣄⢻⡼⠁⠀⠀⠀
⠀⠀⠀⠘⢿⠙⣾⣓⠧⣄⣀⣸⠁⠀⠀⢸⣀⣀⠤⢷⠊⢁⣿⢟⣡⠋⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠻⢽⣦⡀⠀⣍⠉⠉⠉⠙⡅⠀⠀⢘⣦⣾⡛⠉⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠙⠻⢶⣿⣤⣤⣤⣴⣷⣶⣾⣿⣿⣿⣟⢳⣤⡀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢉⡝⠉⠀⠹⣿⣿⣿⣿⣿⣿⣯⠛⣤⠈⢦⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡜⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣧⠈⠳⡀⠳⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
""" + "\033[0m")

manga_chapters_input = input("\033[1;31mDigite os números dos capítulos que deseja baixar separados por espaço e pressione enter: \033[0m")
manga_chapters_array = manga_chapters_input.split()

for manga_chapter in manga_chapters_array:
    # URL do site
    url = f"https://mugiwarasoficial.com/manga/manga-one-piece/capitulo-{manga_chapter}/"

    # Pasta de destino para salvar as imagens
    destination_folder = f"one-piece-manga/capitulo-{manga_chapter}/"

    # Cria a pasta de destino se ela não existir
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # Faz a requisição HTTP para obter o conteúdo da página
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Encontra todas as divs com a classe "page-break"
    divs = soup.find_all("div", class_="page-break")

    print(f"\nBaixando imagens do capítulo {manga_chapter}...")

    # Itera sobre as divs encontradas
    for div in divs[:-1]:
        # Obtém o link da imagem dentro da div
        img_url = div.find("img")["data-src"]
        
        # Obtém o nome do arquivo da imagem
        nome_arquivo = img_url.split("/")[-1]
        
        # Faz o download da imagem
        response = requests.get(img_url)
        
        # Salva a imagem na pasta de destino
        with open(os.path.join(destination_folder, nome_arquivo), "wb") as arquivo:
            arquivo.write(response.content)

    print(f"Download das imagens do capítulo {manga_chapter} concluído!")

    print(f"Gerando PDF do capítulo {manga_chapter}...")

    # Nome do arquivo PDF a ser criado
    nome_pdf = f"{destination_folder}{url.split('/')[-2]}.pdf"

    # Caminho temporário para o PDF gerado pelo reportlab
    temp_pdf = os.path.join(destination_folder, "temp.pdf")

    # Cria um canvas do reportlab
    c = canvas.Canvas(temp_pdf, pagesize=A4)
    page_width, page_height = A4

    # Itera sobre os arquivos de imagem baixados
    for nome_arquivo in os.listdir(destination_folder):
        # Verifica se o arquivo é uma imagem
        if nome_arquivo.lower().endswith((".jpg", ".jpeg", ".png")):
            # Caminho completo da imagem
            image_path = os.path.join(destination_folder, nome_arquivo)
            # Desenha a imagem na página
            c.drawImage(image_path, 0, 0, page_width, page_height)
            c.showPage()  # Finaliza a página e inicia uma nova

    # Finaliza o PDF
    c.save()

    # Agora usamos PyPDF2 para qualquer manipulação adicional, se necessário
    pdf_writer = PdfWriter()

    # Lê o PDF temporário criado pelo reportlab
    with open(temp_pdf, "rb") as f:
        temp_pdf_reader = PdfReader(f)
        for page in temp_pdf_reader.pages:
            pdf_writer.add_page(page)

    # Salva o PDF final
    with open(nome_pdf, "wb") as pdf_file:
        pdf_writer.write(pdf_file)

    # Remove o arquivo PDF temporário
    os.remove(temp_pdf)

    print(f"PDF do capítulo {manga_chapter} criado: {nome_pdf}")

    print(f"Criando EPUB do capítulo {manga_chapter}...")

    # Converte o PDF em imagens
    pages = convert_from_path(nome_pdf, 300)

    # Função para comprimir imagens
    def compress_image(image, output_path, quality=85):
        image.save(output_path, 'JPEG', quality=quality)

    # Cria um arquivo EPUB
    book = epub.EpubBook()

    # Define o título e o autor do livro
    book.set_title(url.split('/')[-2])
    book.set_language('pt-br')

    # Adiciona as imagens ao EPUB
    for i, page in enumerate(pages):
        # Caminho para salvar a imagem comprimida
        img_path = os.path.join(destination_folder, f'page_{i}.jpg')
        # Comprime a imagem
        compress_image(page, img_path, quality=85)

        with open(img_path, 'rb') as img_file:
            img_content = img_file.read()

        # Cria um item de imagem para o EPUB
        img_item = epub.EpubItem(
            uid=f'image_{i}',
            file_name=f'image_{i}.jpg',
            media_type='image/jpeg',
            content=img_content
        )
        book.add_item(img_item)

        # Adiciona uma página ao EPUB com a imagem
        img_html = f'<html><body><img src="image_{i}.jpg" /></body></html>'
        img_chapter = epub.EpubHtml(
            uid=f'page_{i}',
            file_name=f'page_{i}.xhtml',
            content=img_html
        )
        book.add_item(img_chapter)
        book.spine.append(img_chapter)

    # Define a navegação do EPUB
    book.toc = [epub.Link(f'page_{i}.xhtml', f'Page {i + 1}', f'page_{i}') for i in range(len(pages))]
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    # Salva o arquivo EPUB
    epub_file = f"{destination_folder}{url.split('/')[-2]}.epub"
    epub.write_epub(epub_file, book, {})

    print(f"EPUB do capítulo {manga_chapter} criado: {epub_file}")

    # Deleta os arquivos de imagem da pasta de destino
    for nome_arquivo in os.listdir(destination_folder):
        if nome_arquivo.lower().endswith((".jpg", ".jpeg", ".png")):
            arquivo_path = os.path.join(destination_folder, nome_arquivo)
            os.remove(arquivo_path)
            
print("\033[1;31m" + "\nTodos os capítulos foram baixados e convertidos com sucesso!" + "\033[0m")
print("\033[1;31m" + "Aproveite sua aventura pirata!\n" + "\033[0m")
print("Pressione qualquer tecla para sair...")
input()
