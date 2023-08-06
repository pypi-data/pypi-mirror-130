import logging  # print gurmetizado
from pathlib import Path
from typing import Tuple  # trabalha com os diretorios
import click
from numpy import record
import pandas as pd


logging.basicConfig(
    level="DEBUG", format="'%(asctime)s - %(name)s - %(levelname)s - %(message)s'"
)
logger = logging.getLogger(__name__)

@click.command() ## comandos no terminal
@click.option(
        "--input", 
        "-i", 
        default="./", 
        help="Caminho onde encontrar os arquivos CSV a serem convertidos em JSON.", 
        type= str,
) ## opcoes de comando
@click.option(
    "--output",
    "-o",
    default="./",
    help="Caminho onde os arquivos convertidos serão salvos.",
    type=str,
)
@click.option(
    "--delimiter",
    "-d",
    default=",",
    help="Separador usado para dividir os arquivos.",
    type=str,
)
@click.option(
    "--prefix",
    "-p",
    prompt=True,
    prompt_required=False,
    default="file",
    help=(
       "Prefixo usado para preceder o nome do arquivo convertido salvo no disco."
        "O sufixo será um número começando em 0. ge: file_0.json."
    ),
)
def converter(input: str = "./", output: str = "./", delimiter: str  = ",", prefix: str = None):
    input_path = Path(input)
    output_path = Path(output)
    logger.info("Input Path: %s", input_path)
    logger.info("Output Path: %s", output_path)

    for p in [input_path, output_path]:
        if  not p.is_file() or p.is_dir(): # verifica se é um arquivo ou diretorio existente
            raise TypeError("Arquivo ou diretorio não é valido")


    data = read_csv_file(source=input_path, delimiter=delimiter) #leitura de arquivo(s) csv e tranforma em tupla
    save_to_json_file(csvs=data, output_path= output_path, prefix=prefix) # sava como Json o(s) arquivo(s)


# lendo 1 ou diretorio contendo arquivos CSV
def read_csv_file(source: Path, delimiter: str = ",") -> tuple:
    """Carregue os arquivos csv do disco.

    Args:
        source (Path): Caminho de um único arquivo csv ou um diretório contendo arquivos csv.
        delimitador (str): Separador para colunas em csv.

    Retornar:
        tupla: tupla de DataFrames.
    """
    # verifica se oque esta sendo passado é arquivo CSV e faz a leitura
    if source.is_file():
        logger.info("Realiza a leitura de unico arquivo %s", source)
        return(pd.read_csv(filepath_or_buffer=source, delimiter=delimiter, index_col=False),
        )

    # caso não seja arquivo ele entende que se trata de um diretorio com arquivos CSV 
    # e realiza a interação dos arquivo e realiza a leitura
    logger.info("Realiza a leitura de todos os arquivos do diretorio %s", source)
    data = list()
    for i in source.iterdir():
       data.append(pd.read_csv(filepath_or_buffer=i, delimiter=delimiter, index_col=False))

    return tuple(data) # convert a lista em tupla

def save_to_json_file(csvs: tuple, output_path:Path, prefix: str = None):
    """Salvar dataframes no disco.

    Args:
        csvs (tupla): Tupla com dataframes que serão convertidos
        output_path (Path): Caminho onde salvar os arquivos json
        prefix (str): Nome dos arquivos. Se nada for dado, vai  como file_
    """
    i = 0
    while i < len(csvs):
        file_name = f"{prefix}_{i}.json" #monta a parte final do arquivo
        output = output_path.joinpath(file_name) # monta o nome completo do arquivo
        data: pd.DataFrame = csvs[i]
        logger.info("Savando o arquivo como: %s", output)
        data.to_json(path_or_buf=output_path, orient="records", indent=4) # tranforma o arquivo em um arquivo Json
        i += 1

