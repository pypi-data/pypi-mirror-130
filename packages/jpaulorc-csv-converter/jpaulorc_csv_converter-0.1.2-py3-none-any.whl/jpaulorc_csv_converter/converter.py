import logging
import threading
import typing
from os import path
from pathlib import Path

import click
from click.termui import prompt

thread_local = threading.local()

logging.basicConfig(level="DEBUG", format="'%(asctime)s - %(name)s - %(levelname)s - %(message)s'")
logger = logging.getLogger(__name__)


@click.command()
@click.option(
    "--input", "-i", default="./", help="Path where to read the files for convertion.", type=str
)
@click.option(
    "--output", "-o", default="./", help="Path where the converted files will be saved.", type=str
)
@click.option(
    "--delimiter",
    "-d",
    default=",",
    help="Separator used to split the files. You can only use these symbols: comma and colon",
    type=str,
)
@click.option(
    "--prefix",
    "-prefix",
    prompt=True,
    prompt_required=False,
    default="file",
    help=(
        "Prefix used to prepend to the name of the converted file saved on disk."
        " The suffix will have a number starting from 0. eg: file_0.json."
    ),
)
def converter(input: str = "./", output: str = "./", delimiter: str = ",", prefix: str = ""):
    """Convert single file or list of files

    - If the file was a CSV then it will be converted to JSON.

    - If the file was a JSON then it will be converted to CSV."""
    input_path = Path(input)
    output_path = Path(output)

    logger.info("Input Path: %s", input_path)
    logger.info("Output Path: %s", output_path)

    for p in [input_path, output_path]:
        if not (p.is_file() or p.is_dir()):
            raise TypeError("Not a valid path or file name.")

    if delimiter not in [",", ":"]:
        raise TypeError("Not a valid symbol to delimiter.")

    if input_path.is_file():
        if check_extension(input_path) == ".json":
            logger.info("Reading Single JSON File %s", input_path)
            write_csv(
                data=[read_json(input_path=input_path)],
                delimiter=delimiter,
                output_path=output_path,
                prefix=prefix,
            )
        elif check_extension(input_path) == ".csv":
            logger.info("Reading Single CSV File %s", input_path)
            write_json(
                data=[read_csv(input_path=input_path, delimiter=delimiter)],
                output_path=output_path,
                prefix=prefix,
            )
    else:
        csv_data = list()  # type: list
        json_data = list()  # type: list
        logger.info("Reading all files for given path %s", input_path)
        for name in input_path.iterdir():
            if check_extension(name) == ".json":
                json_data.append(read_json(input_path=name))
            elif check_extension(name) == ".csv":
                csv_data.append(read_csv(input_path=name, delimiter=delimiter))

        if csv_data:
            write_json(data=csv_data, output_path=output_path, prefix=prefix)
        if json_data:
            write_csv(data=json_data, delimiter=delimiter, output_path=output_path, prefix=prefix)


def check_extension(file: Path) -> str:
    """Checks if is a valid extension.

    Args:
        file (Path): A path file.

    Returns:
        str: A extension file.
    """
    filename, extension = path.splitext(file)
    if extension == ".json" or extension == ".csv":
        return extension
    else:
        raise TypeError("Not a valid file extension.")


def parse_list_to_dict(data: list[list[str]]) -> list[dict[str, str]]:
    """Converts a list of lists into a dictionary list.

    Args:
        data (list[list[str]]): A data file containing a list of lists.

    Returns:
        list[dict[str, str]]: A data file containing a dictionary list.
    """
    column = data[0]
    lines = data[1:]
    """Checks if all lines have values. Some files have special character in last lines."""
    return [dict(zip(column, line)) for line in lines if len(column) == len(line)]


def read_csv(input_path: Path, delimiter: str = ",") -> list[dict[str, str]]:
    """Reads a CSV file and converts it into a dictionary list.

    Args:
        input_path (Path): A path file.
        delimiter (str): Separator for columns.

    Returns:
        list[dict[str, str]]: A data file containing a dictionary list.
    """
    with input_path.open(mode="r") as file:
        data = file.readlines()
    return parse_list_to_dict([line.strip().split(delimiter) for line in data])


def read_json(input_path: Path) -> list[dict[str, str]]:
    """Reads a JSON file and converts it into a dictionary list.

    Args:
        input_path (Path): A path file.

    Returns:
        list[dict[str, str]]: A data file containing a dictionary list.
    """
    return eval(open(input_path, "r").read().replace("null", "None"))


def is_float(value: str) -> bool:
    """Checks if a value is floating.

    Args:
        value (str): A word.

    Returns:
        bool: A boolean value to show if the value is floating.
    """
    try:
        a = float(value)
    except (TypeError, ValueError):
        return False
    else:
        return True


def is_int(value: str) -> bool:
    """Checks if a value is integer.

    Args:
        value (str): A word.

    Returns:
        bool: A boolean value to show if the value is integer.
    """
    try:
        a = float(value)
        b = int(a)
    except (TypeError, ValueError):
        return False
    else:
        return a == b


def write_comma(file, append_comma: bool):
    """Writes comma when needed for JSON file.

    Args:
        file (io.TextIOWrapper): A file to write.
        append_comma (bool): Defines whether the comma will be written.
    """
    if append_comma:
        file.write(",")
    file.write("\n")


def write_json_line(row: tuple[str, str], file, append_comma: bool = True):
    """Writes a string line into a JSON file.

    Args:
        row (tuple): A string line with two values to be written.
        file (io.TextIOWrapper): A file to write.
        append_comma (bool): Defines whether the comma will be written.
    """
    key, value = row
    if not value:
        file.write(f'\t\t"{key}": null')
    elif is_int(value):
        file.write(f'\t\t"{key}": {int(value)}')
    elif is_float(value):
        file.write(f'\t\t"{key}": {float(value)}')
    else:
        file.write(f'\t\t"{key}": "{value}"')
    write_comma(file, append_comma)


def write_dict(data: dict[str, str], file, append_comma: bool = True):
    """Writes a dictionary into a JSON file.

    Args:
        data (dict): A dictionary of strings to be written into a file.
        file (io.TextIOWrapper): A file to write.
        append_comma (bool): Defines whether the comma will be written.
    """
    file.write("\t{\n")
    items = tuple(data.items())
    for row in items[:-1]:
        write_json_line(row, file)
    write_json_line(items[-1], file, append_comma=False)
    file.write("\t}")
    write_comma(file, append_comma)


def write_json(data: list[list[dict[str, str]]], output_path: Path, prefix: str):
    """Convert a CSV into a JSON file.

    Args:
        data (list[list[dict[str, str]]]): A CSV File.
        output_path (Path): A path file where the JSON file will be written.
        prefix (str): Prefix used to prepend to the name of the converted file saved on disk.
    """
    for key, content in enumerate(data):
        file_name = output_path.joinpath(f"{prefix}_{key}.json")
        logger.info("Saving file %s in folder %s", file_name, output_path)
        with file_name.open(mode="w") as file:
            file.write("[\n")
            for row in content[:-1]:
                write_dict(row, file)
            write_dict(content[-1], file, append_comma=False)
            file.write("]\n")


def write_csv(data: list[list[dict[str, str]]], delimiter: str, output_path: Path, prefix: str):
    """Convert a JSON into a CSV file.

    Args:
        data (list[list[dict[str, str]]]): A JSON file.
        delimiter (str): Used to split the file.
        output_path (Path): A path file where the CSV file will be written.
        prefix (str): Prefix used to prepend to the name of the converted file saved on disk.
    """
    for key, content in enumerate(data):
        file_name = output_path.joinpath(f"{prefix}_{key}.csv")
        logger.info("Saving file %s in folder %s", file_name, output_path)

        with file_name.open(mode="w") as file:
            for row in parse_dict_to_list(content):
                file.write(delimiter.join([str(x) if x is not None else "" for x in row]))
                file.write("\n")


def parse_dict_to_list(content: list[dict[str, str]]) -> list[list[str]]:
    """Converts a dictionary list into a list of lists where the first list is the header
    and others were the values.

    Args:
        content (list[dict[str, str]]): The dictionaries to be converted into a list.

    Returns:
        list[list[str]]: A list of strings.
    """
    data = list()
    data.append(list(content[0]))
    for row in content:
        data.append(list(row.values()))
    return data
