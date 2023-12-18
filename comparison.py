import pandas as pd
from gedcom.element.individual import IndividualElement
from gedcom.parser import Parser

# Função para verificar se duas linhas de DataFrames são iguais
def are_rows_equal(row1, row2):
    return all(row1 == row2)

# Função para verificar se duas DataFrames são iguais
def are_dataframes_equal(df1, df2):
    return df1.equals(df2)

# Função para verificar se uma pessoa tem os mesmos dados que uma linha de DataFrame
def is_person_equal(person_data, df_row):
    return are_rows_equal(person_data, df_row)

# Initialize the parser
gedcom_parser = Parser()

# Ler dados do CSV do filho
son_df = pd.read_csv("filho.csv")

# Ler dados do CSV do pai
father_df = pd.read_csv("pai.csv")

# Ler dados do CSV da mãe
mother_df = pd.read_csv("mae.csv")

# Ler dados do GEDCOM do pai
father_gedcom = gedcom_parser.parse_file("arvore_pai.ged")

# Ler dados do GEDCOM da mãe
mother_gedcom = gedcom_parser.parse_file("arvore_mae.ged")

# Ler dados do CSV de outra pessoa
other_person_df = pd.read_csv("outra_pessoa.csv")

# Verificar se os campos RSID, CHROMOSOME, POSITION e RESULT são iguais entre os CSVs
are_son_and_father_equal = are_dataframes_equal(son_df, father_df)
are_son_and_mother_equal = are_dataframes_equal(son_df, mother_df)
are_son_and_other_person_equal = is_person_equal(other_person_df.iloc[0], son_df.iloc[0])

print("Os dados do filho são iguais aos dados do pai:", are_son_and_father_equal)
print("Os dados do filho são iguais aos dados da mãe:", are_son_and_mother_equal)
print("Os dados do filho são iguais aos dados da outra pessoa:", are_son_and_other_person_equal)

# Verificar se os dados do pai e mãe no GEDCOM são iguais aos dados dos CSVs
father_gedcom_data = father_gedcom.individuals[0].to_dict()
mother_gedcom_data = mother_gedcom.individuals[0].to_dict()

are_father_gedcom_and_father_equal = is_person_equal(father_gedcom_data, father_df.iloc[0])
are_mother_gedcom_and_mother_equal = is_person_equal(mother_gedcom_data, mother_df.iloc[0])

print("Os dados do pai no GEDCOM são iguais aos dados do pai no CSV:", are_father_gedcom_and_father_equal)
print("Os dados da mãe no GEDCOM são iguais aos dados da mãe no CSV:", are_mother_gedcom_and_mother_equal)
