import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver

# Leia os três arquivos CSV
arquivo = 'dados_brutos20231129.csv'

# rs53576 = influences social behavior and personality
# Rs333 = resistencia ao HIV
# Rs6152 = baldness


# Escolha o número da linha que você deseja consultar (substitua 'numero_da_linha' pelo número real)
numero_da_linha = int(input('Digite o número da linha: '))

# Leitura dos arquivos CSV para DataFrames
df1 = pd.read_csv(arquivo)
linha_para_consultar = df1.iloc[numero_da_linha - 1]

# Substitua 'nome_da_coluna_rsid' pelo nome real da coluna que contém o RSID no seu DataFrame
rsid = linha_para_consultar['RSID']
result = linha_para_consultar['RESULT']
resultado = result.strip()

# Construa a URL do SNP no SNPedia
url_snpedia = f'https://www.snpedia.com/index.php/{rsid}'

# Configuração do Selenium
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Para executar em modo headless (sem interface gráfica)
driver = webdriver.Chrome(options=options)

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

        #remova espaço
        genotipos = genotipo.strip()

        # O segundo valor (índice 1) pode ser o texto associado ao genótipo
        texto_associado = celulas[1].get_text()

        # O segundo valor (índice 1) pode ser o texto associado ao genótipo
        summary = celulas[2].get_text()

        # Imprima o genótipo e o texto associado
        if str(resultado) == str(genotipos):
            print(f'seu alelo é {resultado} e o resultado é: {summary}')
else:
    print('Tabela não encontrada.')

# Feche o navegador após a conclusão
driver.quit()
