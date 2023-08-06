import logging
from os import F_OK, path, read, replace
from typing import List
from click.decorators import pass_context
from abc import abstractproperty
from pathlib import Path

from click.termui import prompt

import click


logging.basicConfig(
    level='DEBUG',
    format = "'%(asctime)s - %(name)s - %(levelname)s - %(message)s'"
)


log = logging.getLogger(__name__)

@click.command()
@click.option(
    "--input",
    "-i",
    default= './',
    help="Caminho para identificar o arquivo a ser convertido",
    type=str
)
@click.option(
    "--output",
    "-o",
    default= './',
    help="Local para salvar o arquivo convertido",
    type=str
)
@click.option(
    "--delimiter",
    "-d",
    default= ';',
    help="Informe o delimitador a ser considerado",
    type=str
)
@click.option(
    "--prefix",
    "-p",
    prompt=True,
    prompt_required = False,
    default='file',
    help = (
        "Informe o nome a ser salvo do arquivo convertido"
        
    )
)   

def conversor_de_csv_para_json(input:str='./', output: str ="./", prefix: str= None, delimiter: str =","):
    
    "Função que converter arquivo no formato CSV para JSON"
    "Necessita ser informado o caminho de entrada e saida, nome do arquivo e delimitador"
    
    c_saida = Path(output)
    c_entrada = Path(input)
    
    log.info("Input Path: %s", c_entrada)
    log.info("Output Path: %s", c_saida)

    for c in [c_saida,c_entrada]:
        if not(c.is_file() or c.is_dir()):
            raise TypeError("Variaveis informadas para caminho de entrada e saida invalidos!")
    
    #Aqui começa rodar o codigo da função conversor
    dados = read_csv(caminho = input, demiliter=delimiter)
    dados_json = parse_csv_to_json(dados)
    white_json_data(dados_json, output, prefix)

def read_csv(caminho:Path,demiliter: str=",") -> list:
    
    """ Carregar o arquivo CSV do computador.
    Parametros: 
        caminho: corresponde ao local do arquivo;
        demiliter: corresponde a string delimitadora;
    Saída:
        Dict: Como saida tem-se um dicionario;"""

    if caminho.is_file():
        data = read_File_single_arch(caminho, demiliter)
        return data
    for name in caminho.iterdir():
        data = read_File_path(caminho, demiliter,name)
        return data 


def read_File_path(source:Path, delimiter:str, name) -> list:
    """Read archives from an Path"""
    with open(name,"r") as file:
      line = file.readlines()
      
    data_list = [lines.strip().split(delimiter) for lines in line]
    return data_list 
   
def read_File_single_arch(source:Path, delimiter:str) -> list:
    
    with open(source,'r') as file:
        line = file.readlines()
    
    data_list = [lines.strip().split(delimiter) for lines in line]
    return data_list 



def parse_csv_to_json(data: list) -> list:
    "Transforma o arquivo em dict de Json"
    column = data[0]
    lines = data[1:]
    return [dict(zip(column, line)) for line in lines]

def write_line(line: tuple, io, append_comma: bool):
    key, value = line
    if append_comma:
        io.write(f'\t\t"{key}": "{value}",\n')
    else:
        io.write(f'\t\t"{key}": "{value}"\n')
        io.write("\t}\n")

def write_dictionary(data:dict,io,append_comma:True):
    io.write("\t{\n")
    items = tuple(data.items())
    for line in items[:-1]:
        write_line(line, io,append_comma=True)
    write_line(items[-1],io,append_comma=False)
    
    if append_comma:
        io.write("\t,\n")
    

def white_json_data(data: list,output_path:Path, nome:str):
    '''escreve um dicionario json em disco no endereco'''
    name = output_path.joinpath(f"{nome}.json")
    
    with open(name,mode="w") as file:
        file.write("[\n")
        for i in data[:-1]:
            #print("Aqui tem o {} valor".format(d))
            write_dictionary(i, file, append_comma=True)
        write_dictionary(data[-1], file, append_comma=False)
        file.write("]\n")

@click.command()
@click.option(
    "--input",
    "-i",
    default= './',
    help="Caminho para identificar o arquivo a ser convertido",
    type=str
)
@click.option(
    "--output",
    "-o",
    default= './',
    help="Local para salvar o arquivo convertido",
    type=str
)
@click.option(
    "--delimiter",
    "-d",
    default= ';',
    help="Informe o delimitador a ser considerado",
    type=str
)
@click.option(
    "--prefix",
    "-p",
    prompt=True,
    prompt_required = False,
    default='file',
    help = (
        "Informe o nome a ser salvo do arquivo convertido"
        
    )
)
    
def conversor_de_json_para_csv(input:str='./', output: str ="./", prefix: str= None, delimitador: str =","):
    "Função que conveter arquivo no formato JSON para CSV"
    "Necessita ser informado o caminho de entrada e saida, nome do arquivo e delimitador"
    
    c_saida = Path(output)
    c_entrada = Path(input)

    for c in [c_saida,c_entrada]:
        if not(c.is_file() or c.is_dir()):
            raise TypeError("Variaveis informadas para caminho de entrada e saida invalidos!")
    
    #Aqui começa rodar o codigo da função conversor
    data = read_json(caminho = input)
    json_data = parse_json_to_csv(data)
    write_csv_data(json_data, output, prefix)

def read_json(caminho:Path) -> list:
    """ Carregar o arquivo JSON do computador.
    Parametros: 
        caminho: corresponde ao local do arquivo;
        demiliter: corresponde a string delimitadora;
    Saída:
        Dict: Como saida tem-se um dicionario;"""
    
    if caminho.is_file():
        
        data_json = read_json_File_single_arch(caminho)
        return data_json

    
    for name in caminho.iterdir():
        data = read_json_File_path(caminho)
        return data

def read_json_File_path(source:Path) -> list:
    """Read archives from an Path"""
    files = [*source.iterdir()]


def read_json_File_single_arch(source:Path) -> list:
    """Read a single archive csv."""
    with open(source,'r') as file:
        data = file.readlines()
    return data

def read_arquivos_json_path(source:Path)-> list:
    """Read archives from an Path"""
    files = [*source.iterdir()]



def parse_json_to_csv(data: list) -> list:
    ''' converte list de dados de csv para formato json'''
    list_header = []
    list_header_body = []
    string = ""
    parsed_data = [line.strip() for line in data]
    
    for i,line in enumerate(parsed_data):
        
        if(line != "[" and line != "{" and line != "," and line != "]"):
            string = string + line
    for index_s,s in enumerate(string.split("}")):
        if(i < (len(s) - 1)):
           for i,data_split in enumerate(s.split(",")):
               data_split = data_split.replace('"',"")
               header, body = data_split.split(":")
               if(index_s ==0):
                list_header.append(header)
               if(i==0):
                list_body = []
               list_body.append(body)    
           list_header_body.append(list_body)
    list_header_body.append(list_header)
    return list_header_body


#parse_json_to_csv(data)  
def write_csv_data(data: list,output_path:Path, nome_arquivo:str):
    nome = output_path.joinpath(f"{nome_arquivo}.csv")
    string = ""
    string_body = ""
    with open(nome,mode="w") as outfile:
        for i,datas1 in enumerate(data):
            if(i == (len(data) -1)):
                for index_d,d in enumerate(datas1):
                    if(index_d < (len(datas1)-1)):
                        string = string + d + "," 
                    else:
                        string = string + d;   
        outfile.write(string + "\n")     

        for i,datas2 in enumerate(data):
            if(i != (len(data) -1)):
                for index_body,body in enumerate(datas2):
                    if(index_body < (len(datas2)- 1)):
                        string_body = string_body.strip() + body + ","
                    else:
                        string_body = string_body.strip() + body
                        outfile.write(string_body + "\n")
                        string_body = ""
