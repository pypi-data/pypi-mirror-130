import logging
from pathlib import Path
from typing import Any, Dict, List
import click

logging.basicConfig(
    level="DEBUG", format="'%(asctime)s - %(name)s - %(levelname)s - %(message)s'"
)
logger = logging.getLogger(__name__)

@click.command()
@click.option("--input","-i", default="./", help="Path where to read files for conversion.", type=str,)
@click.option("--output","-o", default="./", help="Path where the converted files will be saved.", type=str,)
@click.option("--type_conversion","-t", default="csvtojson", help="Type of conversion, type 'csvtojson' or 'jsontocsv'.", type=str,)
@click.option("--delimiter","-d", default=",", help="Separator used to split the files.", type=str,)
@click.option("--prefix","-prefix", prompt=True, prompt_required=False, default='file',
              help=("Prefix used to prepend to the name of the converted file saved on disk."),)

def converter(input: str = "./", output: str = "./", type_conversion : str = 'csvtojson', delimiter: str = ",", prefix: str = None):
    """Convert single file or list of csv to json."""
    input_path = Path(input)
    output_path = Path(output)
    type = type_conversion
    logger.info("Input Path: %s", input_path)  
    logger.info("Output Path: %s", output_path)
    
    for p in [input_path, output_path]:
        if not (p.is_file() or p.is_dir()):
            raise (TypeError("Not a valid path or file name.", p))
    
    
    if type == 'csvtojson':        
    #included to read just one file and verify that the file has a .csv extension
        if input_path.is_file() and str((Path(input_path).suffix).lower()) == '.csv': 
            data = read_csv(input_path, delimiter=delimiter)
            json = parse_csv_to_json(data)
            name = Path(input_path).stem
            write_json_data(json,Path(output_path.joinpath(f'{name}_{prefix}.json')))

        #included for more than one file checking if the extension is csv
        if input_path.is_dir():       
            for arq in Path(input_path).glob("*.*"):
                if arq.is_file() and str((arq.suffix).lower()) == '.csv':
                    data = read_csv(arq, delimiter=delimiter)
                    json = parse_csv_to_json(data)
                    name = Path(arq).stem
                    write_json_data(json,Path(output_path.joinpath(f'{name}_{prefix}.json')))
    
    #conversion json to csv
    elif type == 'jsontocsv':
        json_csv(input, output)
   
    else:
        logger.error("Type of conversion invalid.")

    
#############File handling for CSV format
def read_csv(input_path: Path, delimiter: str = ","):
    """Load csv files"""
    with input_path.open(mode='r') as file:
        data = file.readlines()
    
    return [line.strip().split(delimiter) for line in data]


def parse_csv_to_json(data):
    """Convert CSV to JSON format. """
    column = data[0]
    lines = data[1:]
    return [dict(zip(column, line)) for line in lines]

def write_line(line: tuple, io, append_comma: bool):
    """Transforming the file to json format"""
    key, value = line
    if append_comma:
        io.write(f'\t\t"{key}": "{value}",\n')
    else:
        io.write(f'\t\t"{key}": "{value}"\n')
    
def write_dictionary(data: dict, io, append_comma: True):
    """Transforming the file to json format creating the dictionary"""
    io.write("\t{\n")
    items = tuple(data.items())
    for line in items[:-1]:
        write_line(line, io, append_comma=True)
    write_line(items[-1], io, append_comma=False)
    io.write("\t}")
    if append_comma:
        io.write(",\n")
    else:
        io.write("\n")

def write_json_data(data, output_path: Path):
    """writing file to disk. """
    with output_path.open(mode='w') as file:
        file.write("[\n")
        for d in data[:-1]:
            write_dictionary(d, file, append_comma=True) 
        write_dictionary(data[-1], file, append_comma=False)
        file.write("]\n")

 ####################################################################
 
 
 
 #############file handling for JSON format
def _parse_value(value_raw: Any) -> str:
    value = value_raw.strip()

    if value[0] == '"' and value[-1] == '"':
        return value[1:-1]

    if value == "null":
        return ""

    return value
    
#reading json files
def _read_json(file_name: str):

    with open(file_name, "r", encoding="utf-8") as f:
        all_lines = "".join(line.strip() for line in f.readlines())

    useful_lines = all_lines[1:-2]

    def _read_dictionary(dict_str: str) -> Dict[str, str]:
        dict_data_raw = dict_str.replace("{", "").split(",")
        dict_data = {}        
        for item in dict_data_raw:
            key, value = item.split(":")
            dict_data[_parse_value(key)] = _parse_value(value)

        return dict_data

    return [
        _read_dictionary(dict_str) for dict_str in useful_lines.split("},")
    ]

#converting convert files json to csv
def _convert_file(file_name: str, separator: str = ",") -> List[str]:

    json_list = _read_json(file_name)
    csv_list = []

    keys = list(json_list[0].keys())  
    header_line = separator.join(key for key in keys)
    header_line += "\n"
    csv_list.append(header_line)

    def write_data_line(json_dict: Dict[str, Any]) -> str:
        data_line = separator.join(json_dict[key] for key in keys)
        data_line += "\n"
        return data_line

    data_lines = [write_data_line(json_dict) for json_dict in json_list]
    csv_list.extend(data_lines)

    return csv_list

def input_path(input_path: str, extension: str):
    input_path_pos = Path(input_path)
    if input_path_pos.is_dir():
        file_names = list(input_path_pos.glob(f"*.{extension}"))
        logger.info("Converting all files in a folder")
    else:
        file_names = [input_path_pos]
        logger.info("Converting a single file")

    if not file_names:
        logger.warning("Folder has no %s files. Skipping.", extension)

    return file_names

#function to handle and save files
def json_csv(input: str = "./", output: str = "./", delimiter: str = ",", prefix: str = 'file'):
    input_path = Path(input)
    output_path = Path(output)

    file_names = input_path(input_path, "json")
     
    csvs = [
        _convert_file(file_name, ',')
        for file_name in file_names
    ]
    
    for file_name, csv_list in zip(file_names, csvs):
        csv_file_name = f"{output_path}/{prefix}_{file_name.stem}.csv"
        with open(csv_file_name, "w", encoding="utf-8") as f:
            f.writelines(csv_list)
           

    return csvs
    
 ####################################################################


