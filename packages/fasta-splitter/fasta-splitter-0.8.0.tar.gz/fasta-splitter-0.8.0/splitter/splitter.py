from pathlib import Path
from typing import Tuple
import click
import splitter.splitter_exceptions
import sys


def check_if_is_valid_number_of_arguments(number_of_arguments_provided: int) -> None:
    if number_of_arguments_provided != 1:
        invalid_number_of_arguments_message = "Invalid number of arguments provided!\n" \
                                              "Expected: 1 argument (FASTA sequences file).\n" \
                                              "Provided: {0} argument(s).".format(number_of_arguments_provided)
        raise splitter.splitter_exceptions.InvalidNumberofArgumentsError(invalid_number_of_arguments_message)


def check_if_sequences_file_exists(sequences_file_path: Path) -> None:
    if not sequences_file_path.is_file():
        file_not_found_message = "FASTA sequences file not found!"
        raise FileNotFoundError(file_not_found_message)


def get_sequences_file_extension(sequences_file_path: Path) -> str:
    return sequences_file_path.suffix


def get_supported_fasta_file_extensions() -> list:
    return [".fa", ".faa", ".fasta", ".ffn", ".fna", ".frn"]


def check_if_sequences_file_has_fasta_extension(sequences_file_path: Path) -> None:
    supported_fasta_file_extensions = get_supported_fasta_file_extensions()
    if get_sequences_file_extension(sequences_file_path) not in supported_fasta_file_extensions:
        invalid_extension_file_message = "Only FASTA extension files ({0}) are allowed!" \
            .format(", ".join(supported_fasta_file_extensions))
        raise splitter.splitter_exceptions.InvalidExtensionFileError(invalid_extension_file_message)


def parse_description_line(line: str,
                           sequences_start_token: str,
                           description_lines_count: int) -> int:
    if line.startswith(sequences_start_token):
        description_lines_count = description_lines_count + 1
    return description_lines_count


def parse_invalid_description_line(line: str,
                                   sequences_start_token: str,
                                   invalid_description_lines_count: int) -> int:
    if line.startswith(sequences_start_token) and line.split(" ", 1)[0] == sequences_start_token:
        invalid_description_lines_count = invalid_description_lines_count + 1
    return invalid_description_lines_count


def parse_sequences_file_line(line: str,
                              description_lines_count: int,
                              invalid_description_lines_count: int,
                              lines_count: int) -> Tuple[int, int, int]:
    sequences_start_token = ">"
    description_lines_count = parse_description_line(line,
                                                     sequences_start_token,
                                                     description_lines_count)
    invalid_description_lines_count = parse_invalid_description_line(line,
                                                                     sequences_start_token,
                                                                     invalid_description_lines_count)
    lines_count = lines_count + 1
    return description_lines_count, invalid_description_lines_count, lines_count


def get_sequences_file_counters(sequences_file_path: Path) -> Tuple[int, int, int]:
    description_lines_count = 0
    invalid_description_lines_count = 0
    lines_count = 0
    with open(sequences_file_path, mode="r") as sequences_file:
        for line in sequences_file:
            description_lines_count, invalid_description_lines_count, lines_count = \
                parse_sequences_file_line(line,
                                          description_lines_count,
                                          invalid_description_lines_count,
                                          lines_count)
    return description_lines_count, invalid_description_lines_count, lines_count


def check_if_sequences_file_has_any_description_line(sequences_file_path: Path,
                                                     description_lines_count: int) -> None:
    if description_lines_count == 0:
        invalid_formatted_fasta_file_message = "'{0}' does not have any description line!" \
            .format(str(sequences_file_path))
        raise splitter.splitter_exceptions.InvalidFormattedFastaFileError(invalid_formatted_fasta_file_message)


def check_if_sequences_file_has_any_invalid_description_line(sequences_file_path: Path,
                                                             invalid_description_lines_count: int) -> None:
    if invalid_description_lines_count != 0:
        invalid_formatted_fasta_file_message = "'{0}' contains {1} line(s) with invalid description format!" \
            .format(str(sequences_file_path), str(invalid_description_lines_count))
        raise splitter.splitter_exceptions.InvalidFormattedFastaFileError(invalid_formatted_fasta_file_message)


def check_if_sequences_file_has_no_data(sequences_file_path: Path,
                                        lines_count: int) -> None:
    if lines_count < 2:
        invalid_formatted_fasta_file_message = "'{0}' seems a empty fasta file!".format(str(sequences_file_path))
        raise splitter.splitter_exceptions.InvalidFormattedFastaFileError(invalid_formatted_fasta_file_message)


def check_if_is_valid_fasta_sequences_file(sequences_file_path: Path) -> None:
    check_if_sequences_file_exists(sequences_file_path)
    check_if_sequences_file_has_fasta_extension(sequences_file_path)
    description_lines_count, invalid_description_lines_count, lines_count = \
        get_sequences_file_counters(sequences_file_path)
    check_if_sequences_file_has_any_description_line(sequences_file_path, description_lines_count)
    check_if_sequences_file_has_any_invalid_description_line(sequences_file_path, invalid_description_lines_count)
    check_if_sequences_file_has_no_data(sequences_file_path, lines_count)


def get_sequences_file_path_parents(sequences_file_path: Path) -> Path:
    return Path(sequences_file_path.parents[0])


def get_sequences_file_path_parents_underscored(sequences_file_path_parents: Path) -> str:
    sequences_file_path_parents_underscored = str(sequences_file_path_parents) \
        .replace("/", "_").replace("\\", "_").replace(".", "").replace(":", "")
    if len(sequences_file_path_parents_underscored) > 0 and sequences_file_path_parents_underscored[0] == "_":
        sequences_file_path_parents_underscored = sequences_file_path_parents_underscored.replace("_", "", 1)
    return sequences_file_path_parents_underscored


def get_sequences_name_list(sequences_file_path: Path) -> list:
    sequences_start_token = ">"
    sequences_name_list = []
    with open(sequences_file_path, mode="r") as fasta_sequences_file:
        for line in fasta_sequences_file:
            line = line.strip()
            if line.startswith(sequences_start_token):
                sequence_name = line.split("|", 1)[0].replace(sequences_start_token, "").replace(" ", "")
                sequences_name_list.append(sequence_name)
    return sequences_name_list


def get_sequences_data_list(sequences_file_path: Path) -> list:
    sequences_start_token = ">"
    sequences_data_list = []
    current_sequence_data = []
    with open(sequences_file_path, mode="r") as sequences_file:
        for line in sequences_file:
            line = line.strip()
            if line.startswith(sequences_start_token) and current_sequence_data:
                sequences_data_list.append(current_sequence_data[:])
                current_sequence_data = []
            current_sequence_data.append(line)
        sequences_data_list.append(current_sequence_data)
    return sequences_data_list


def write_sequences_fasta_files_from_sequences_lists(sequences_file_path_parents: Path,
                                                     sequences_file_extension: str,
                                                     sequences_name_list: list,
                                                     sequences_data_list: list) -> None:
    wrote_sequences_fasta_files_count = 0
    for index_name in range(len(sequences_name_list)):
        sequence_file_name = sequences_name_list[index_name] + sequences_file_extension
        with open(sequences_file_path_parents.joinpath(sequence_file_name), mode="w") as sequence_file:
            sequence_data = sequences_data_list[index_name]
            for index_data in range(len(sequence_data)):
                sequence_file.write(sequence_data[index_data] + "\n")
        wrote_sequences_fasta_files_count = wrote_sequences_fasta_files_count + 1


def write_sequences_fasta_files_path_list(sequences_file_path_parents: Path,
                                          sequences_file_extension: str,
                                          sequences_name_list: list) -> None:
    sequences_file_path_parents_underscored = get_sequences_file_path_parents_underscored(sequences_file_path_parents)
    if len(sequences_file_path_parents_underscored) > 0:
        sequences_list_file_name = sequences_file_path_parents_underscored + "_Sequences_List.txt"
    else:
        sequences_list_file_name = "Sequences_List.txt"
    sequences_fasta_files_index_count = 0
    with open(Path(sequences_list_file_name), mode="w") as sequences_list_file:
        for index_name in range(len(sequences_name_list)):
            sequence_file_name = sequences_name_list[index_name] + sequences_file_extension
            sequences_list_file.write(str(Path(sequences_file_path_parents, sequence_file_name)) + "\n")
            sequences_fasta_files_index_count = sequences_fasta_files_index_count + 1


@click.group()
def splitter_group() -> None:
    pass


@splitter_group.command("split",
                        short_help="Split one multiple sequences file into individual sequences files.")
@click.argument("multiple_sequences_file_path",
                nargs=1,
                type=Path,
                required=True)
@click.option("--generate-path-list",
              is_flag=True,
              help="Generate a list containing location (path) of the splitted individual sequences files.")
def split(multiple_sequences_file_path: Path,
          generate_path_list: bool) -> None:
    """
    Split one multiple sequences fasta file into individual sequences fasta files.\n
    1. Input:\n
    1.1 MULTIPLE_SEQUENCES_FILE_PATH - Location (path) of the multiple sequences fasta source file to be splitted.\n
    2. Output:\n
    2.1 Sequences Files - Individual fasta files generated after running this split command.
    They are saved in the same directory path where the multiple sequences fasta source file is located.\n
    Notice that the multiple sequences fasta source file stays untouched.\n
    2.2 Sequences Path File List [Optional] - List (.txt) containing the location (path)
    of the splitted individual sequences files.
    It is generated in the current directory path where the user ran this split command.\n
    Use --generate-path-list option flag to activate this function.
    """
    # BEGIN

    # VALIDATE MULTIPLE SEQUENCES FILE (AS FASTA FORMATTED FILE)
    check_if_is_valid_fasta_sequences_file(multiple_sequences_file_path)

    # GET MULTIPLE SEQUENCES FILE PATH PARENTS
    sequences_file_path_parents = get_sequences_file_path_parents(multiple_sequences_file_path)

    # GET MULTIPLE SEQUENCES FILE EXTENSION
    sequences_file_extension = get_sequences_file_extension(multiple_sequences_file_path)

    # READ MULTIPLE SEQUENCES FILE AND GET SEQUENCES NAME LIST
    sequences_name_list = get_sequences_name_list(multiple_sequences_file_path)

    # READ MULTIPLE SEQUENCES FILE AND GET SEQUENCES DATA LIST
    sequences_data_list = get_sequences_data_list(multiple_sequences_file_path)

    # WRITE SEQUENCES FASTA FILES (SPLITTING ORIGINAL FASTA MULTIPLE SEQUENCES FILE INTO INDIVIDUAL SEQUENCES FILES)
    write_sequences_fasta_files_from_sequences_lists(sequences_file_path_parents,
                                                     sequences_file_extension,
                                                     sequences_name_list,
                                                     sequences_data_list)

    if generate_path_list:
        # WRITE INDIVIDUAL SEQUENCES FASTA FILES PATH LIST (LOCATION OF INDIVIDUAL SEQUENCES FILES)
        write_sequences_fasta_files_path_list(sequences_file_path_parents,
                                              sequences_file_extension,
                                              sequences_name_list)

    # END
    sys.exit(0)


if __name__ == "__main__":
    split()
