import json
import logging
import os.path
from pathlib import Path

import click

""" Este programa é um conversor de arquivos CSV para JSON ou de JSON para CSV.
    Caso os pararâmetro passados forem referentes um ou vparios arquivo CSV ele 
        converterá-los par JSON;
    Caso os pararâmetro passados forem referentes um ou vário arquivo JSON ele 
        converterá-los para CSV;
    Caso o parametro passado se revira a um diretório apenas, 
    o programa irá escanear a pasta em busca de arquivos CSV 
    para convertê-los e JSON e 
    buscará por arquivos JSON e converterá-los para CSV.
    
    
    É necessário que as extensões dos arquivos tratados pelo programa esteja corretas!!!
"""
#
logging.basicConfig(level="DEBUG", format="'%(asctime)s - %(name)s - %(levelname)s - %(message)s'")
logger = logging.getLogger(__name__)
#
@click.command()
@click.option(
    "--input",
    "-i",
    default="./",
    help="Path where to read the files for conversion.",
    type=str,
)
@click.option(
    "--output",
    "-o",
    default="./",
    help="Path where the converted files will be saved.",
    type=str,
)
@click.option(
    "--delimiter",
    "-d",
    default=";",
    help="Separator used to split csv files",
    type=str,
)
@click.option(
    "--prefix",
    "-prefix",
    prompt=True,
    prompt_required=False,
    default="f",
    help="Enter with prefix.",
    type=str,
)
#
def converter(input: str = "./", output: str = "./", delimiter: str = ";", prefix: str = None):
    """Convert single file or list of csv to json"""

    input_path = Path(input)
    output_path = Path(output)
    logger.info("Input path: %s", input_path)
    logger.info("Input path: %s", output_path)

    for p in [input_path, output_path]:
        if not (p.is_file() or p.is_dir()):
            raise TypeError("Not a valid path or filename.")
    if input_path.is_file():  #'Tratar arquivo unico...'
        A = os.path.join(input_path).split(".")
        ext = A[len(A) - 1]

        nomearq = A[0].split("\\")[len(A[0].split("\\")) - 1]
        nomearq = str(prefix) + "_" + nomearq

        if ext.upper() == "CSV":  # se arquivos = csv
            dados = ler_csv_file(input_path, delimiter)

            salvar_json(dados, nomearq + ".json", output)

        elif ext.upper() == "JSON":  # se arquivos = json
            dados = ler_json_file(input_path)

            salvar_csv(dados, delimiter, nomearq + ".csv", output)

    elif input_path.is_dir():  #'Tratar diretório [vários arquivos]...'
        for B in os.listdir(input_path):
            if Path(os.path.join(input_path, B)).is_file():
                A = (os.path.join(input_path, B)).split(".")
                ext = A[len(A) - 1]

                nomearq = A[0].split("\\")[len(A[0].split("\\")) - 1]
                nomearq = str(prefix) + "_" + nomearq

                if ext.upper() == "CSV":  # se arquivos = csv
                    dados = ler_csv_file(Path(os.path.join(input_path, B)), delimiter)

                    salvar_json(dados, nomearq + ".json", output)

                elif ext.upper() == "JSON":  # se arquivos = json
                    dados = ler_json_file(Path(os.path.join(input_path, B)))
                    salvar_csv(dados, delimiter, nomearq + ".csv", output)


#
def ler_csv_file(path, delimiter) -> tuple:
    arq = open(
        path, "r", encoding="UTF-8"
    )  # Criar uma nova versão que descobre atomaticamente o código de página

    lista = []
    for line in arq:
        list_line = line.split(delimiter)
        for lline in range(0, len(list_line)):

            if list_line[lline][0] == '"':
                list_line[lline] = list_line[lline][1 : len(list_line[lline]) - 1]

            list_line[lline] = list_line[lline].rstrip("\n")  # remove eventuais quebras de linha
        lista.append(list_line)

    arq.close
    return tuple(lista)


#
def ler_json_file(path) -> tuple:
    arq = open(
        path, "r", encoding="UTF-8"
    )  # Criar uma nova versão que descobre atomaticamente o código de página
    entrada_json = ""
    for linha in arq:
        entrada_json += linha

    arq.close()
    dados_json = json.loads(entrada_json)

    return tuple(dados_json)


#
def salvar_csv(dados, delimiter, nomearq, output):
    csv = ""
    for coluna in dados[0].keys():
        csv += '"' + coluna + '";'
    csv = csv[0 : len(csv) - 1] + "\n"

    for linha in range(0, len(dados)):
        for coluna in dados[linha].keys():
            if str(dados[linha][coluna]).isnumeric():
                csv += str(dados[linha][coluna]) + delimiter
            else:
                csv += '"' + str(dados[linha][coluna]) + '"' + delimiter
        csv = csv[0 : len(csv) - 1] + "\n"
    arq = open((os.path.join(output, nomearq)), "w", encoding="UTF-8")
    arq.write(csv)
    arq.close()


#
def salvar_json(dados, nomearq, output):
    cab = dados[0]

    json = add_line_json(cab, dados)

    arq = open((os.path.join(output, nomearq)), "w", encoding="UTF-8")
    arq.write(json)
    arq.close()


#
def add_line_json(cab, dado):
    #
    saida = "  {\n"
    for ln_dado in dado:
        if ln_dado != cab:

            for i in range(0, len(ln_dado)):  # compõe cada linha json de acordo com o tipo do dado
                if ln_dado[i] == "":
                    saida = saida + '      "' + cab[i] + '": null, \n'
                    pass
                elif ln_dado[i][0] == '"':
                    saida = saida + '      "' + cab[i] + '": ' + ln_dado[i] + " ,\n"
                elif ln_dado[i].isnumeric():
                    saida = saida + '      "' + cab[i] + '": ' + ln_dado[i] + ",\n"
                elif True:
                    saida = saida + '      "' + cab[i] + '": "' + ln_dado[i] + '",\n'

            saida = saida[0 : len(saida) - 2]
            saida = saida + "\n  },\n  {"

    saida = "[\n" + saida[0 : len(saida) - 5] + "\n]"
    return saida


#
if __name__ == "__main__":
    converter()
