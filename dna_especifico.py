import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver

# Leia o arquivo CSV
arquivo = 'dados_brutos20231129.csv'
df = pd.read_csv(arquivo)

# RSIDs desejados
rsids_desejados = ['rs53576', 'Rs333', 'Rs6152']

# Configuração do Selenium
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Para executar em modo headless (sem interface gráfica)
driver = webdriver.Chrome(options=options)

# Itera sobre os RSIDs desejados
for rsid_desejado in rsids_desejados:
    # Filtra o DataFrame para o RSID desejado
    df_rsid = df[df['RSID'].str.lower() == rsid_desejado.lower()]

    if not df_rsid.empty:
        # Pega o primeiro resultado (pode haver mais de um)
        resultado = df_rsid.iloc[0]['RESULT'].strip()

        # Construa a URL do SNP no SNPedia
        url_snpedia = f'https://www.snpedia.com/index.php/{rsid_desejado}'

        # Acesse a página usando o Selenium
        driver.get(url_snpedia)

        # Aguarde alguns segundos para garantir que a tabela seja carregada
        driver.implicitly_wait(5)

        # Obtenha o conteúdo da página
        pagina_selenium = driver.page_source

        # Use o BeautifulSoup para fazer o parsing do HTML
        soup = BeautifulSoup(pagina_selenium, 'html.parser')

        # Encontre a tabela com a classe específica
        tabela = soup.find('table', class_='sortable smwtable jquery-tablesorter')

        # Verifique se a tabela foi encontrada
        if tabela:
            # Itere sobre as linhas da tabela (excluindo o cabeçalho)
            for linha in tabela.find_all('tr')[1:]:
                # Obtenha os valores das células na linha
                celulas = linha.find_all('td')

                # O primeiro valor (índice 0) pode ser o genótipo, por exemplo, "AA"
                g = celulas[0].get_text()

                # Remova parênteses
                gene = g.replace('(', '').replace(')', '')

                # Remova ponto e vírgula
                genotipo = gene.replace(';', '')

                # Remova espaço
                genotipos = genotipo.strip()

                # O segundo valor (índice 1) pode ser o texto associado ao genótipo
                texto_associado = celulas[1].get_text()

                # O segundo valor (índice 1) pode ser o texto associado ao genótipo
                summary = celulas[2].get_text()

                # Imprima o genótipo e o texto associado
                if str(resultado) == str(genotipos):
                    print(f'Para RSID {rsid_desejado}, seu alelo é {resultado} e o resultado é: {summary}')
        else:
            print(f'Tabela não encontrada para RSID {rsid_desejado}.')
    else:
        print(f'RSID {rsid_desejado} não encontrado no arquivo CSV.')

# Feche o navegador após a conclusão
driver.quit()
