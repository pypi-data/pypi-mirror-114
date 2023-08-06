from pathlib import Path
from typing import Tuple
import click
import fastasplitter_splitter.splitter_exceptions
import sys


def check_if_is_valid_number_of_arguments(number_of_arguments_provided: int) -> None:
    if number_of_arguments_provided != 1:
        invalid_number_of_arguments_message = "Invalid number of arguments provided!\n" \
                                              "Expected: 1 argument (FASTA multiple sequences file).\n" \
                                              "Provided: {0} argument(s).".format(number_of_arguments_provided)
        raise fastasplitter_splitter.splitter_exceptions \
            .InvalidNumberofArgumentsError(invalid_number_of_arguments_message)


def check_if_multiple_sequences_file_exists(multiple_sequences_file_path: Path) -> None:
    if not multiple_sequences_file_path.is_file():
        file_not_found_message = "FASTA multiple sequences file not found!"
        raise FileNotFoundError(file_not_found_message)


def get_multiple_sequences_file_extension(multiple_sequences_file_path: Path) -> str:
    return multiple_sequences_file_path.suffix


def get_supported_fasta_file_extensions() -> list:
    return [".fa", ".faa", ".fasta", ".ffn", ".fna", ".frn"]


def check_if_multiple_sequences_file_has_fasta_extension(multiple_sequences_file_path: Path) -> None:
    supported_fasta_file_extensions = get_supported_fasta_file_extensions()
    if get_multiple_sequences_file_extension(multiple_sequences_file_path) not in supported_fasta_file_extensions:
        invalid_extension_file_message = "Only FASTA extension files ({0}) are allowed!" \
            .format(", ".join(supported_fasta_file_extensions))
        raise fastasplitter_splitter.splitter_exceptions.InvalidExtensionFileError(invalid_extension_file_message)


def parse_description_line(line: str,
                           individual_sequences_start_token: str,
                           description_lines_count: int) -> int:
    if line.startswith(individual_sequences_start_token):
        description_lines_count = description_lines_count + 1
    return description_lines_count


def description_line_contains_whitespace_right_after_start_token(line: str,
                                                                 individual_sequences_start_token: str) -> bool:
    return line.startswith(individual_sequences_start_token) and \
           line.split(" ", 1)[0] == individual_sequences_start_token


def description_line_has_no_information_after_start_token(line: str,
                                                          individual_sequences_start_token: str) -> bool:
    return line.startswith(individual_sequences_start_token) and \
           line.split(individual_sequences_start_token, 1)[1] == ""


def parse_invalid_description_line(line: str,
                                   individual_sequences_start_token: str,
                                   invalid_description_lines_count: int) -> int:
    if description_line_contains_whitespace_right_after_start_token(line, individual_sequences_start_token) or \
            description_line_has_no_information_after_start_token(line, individual_sequences_start_token):
        invalid_description_lines_count = invalid_description_lines_count + 1
    return invalid_description_lines_count


def parse_multiple_sequences_file_line(line: str,
                                       description_lines_count: int,
                                       invalid_description_lines_count: int,
                                       lines_count: int) -> Tuple[int, int, int]:
    individual_sequences_start_token = ">"
    description_lines_count = parse_description_line(line,
                                                     individual_sequences_start_token,
                                                     description_lines_count)
    invalid_description_lines_count = parse_invalid_description_line(line,
                                                                     individual_sequences_start_token,
                                                                     invalid_description_lines_count)
    lines_count = lines_count + 1
    return description_lines_count, invalid_description_lines_count, lines_count


def get_multiple_sequences_file_counters(multiple_sequences_file_path: Path) -> Tuple[int, int, int]:
    description_lines_count = 0
    invalid_description_lines_count = 0
    lines_count = 0
    with open(multiple_sequences_file_path, mode="r") as multiple_sequences_file:
        for line in multiple_sequences_file:
            description_lines_count, invalid_description_lines_count, lines_count = \
                parse_multiple_sequences_file_line(line,
                                                   description_lines_count,
                                                   invalid_description_lines_count,
                                                   lines_count)
    return description_lines_count, invalid_description_lines_count, lines_count


def check_if_multiple_sequences_file_has_any_description_line(multiple_sequences_file_path: Path,
                                                              description_lines_count: int) -> None:
    if description_lines_count == 0:
        invalid_formatted_fasta_file_message = "'{0}' does not have any description line!" \
            .format(str(multiple_sequences_file_path))
        raise fastasplitter_splitter.splitter_exceptions \
            .InvalidFormattedFastaFileError(invalid_formatted_fasta_file_message)


def check_if_multiple_sequences_file_has_any_invalid_description_line(multiple_sequences_file_path: Path,
                                                                      invalid_description_lines_count: int) -> None:
    if invalid_description_lines_count != 0:
        invalid_formatted_fasta_file_message = "'{0}' contains {1} line(s) with invalid description format!" \
            .format(str(multiple_sequences_file_path), str(invalid_description_lines_count))
        raise fastasplitter_splitter.splitter_exceptions \
            .InvalidFormattedFastaFileError(invalid_formatted_fasta_file_message)


def check_if_multiple_sequences_file_has_no_data(multiple_sequences_file_path: Path,
                                                 lines_count: int) -> None:
    if lines_count < 2:
        invalid_formatted_fasta_file_message = "'{0}' seems a empty fasta file!"\
            .format(str(multiple_sequences_file_path))
        raise fastasplitter_splitter.splitter_exceptions \
            .InvalidFormattedFastaFileError(invalid_formatted_fasta_file_message)


def check_if_is_valid_multiple_sequences_file(multiple_sequences_file_path: Path) -> None:
    check_if_multiple_sequences_file_exists(multiple_sequences_file_path)
    check_if_multiple_sequences_file_has_fasta_extension(multiple_sequences_file_path)
    description_lines_count, invalid_description_lines_count, lines_count = \
        get_multiple_sequences_file_counters(multiple_sequences_file_path)
    check_if_multiple_sequences_file_has_any_description_line(multiple_sequences_file_path, description_lines_count)
    check_if_multiple_sequences_file_has_any_invalid_description_line(multiple_sequences_file_path,
                                                                      invalid_description_lines_count)
    check_if_multiple_sequences_file_has_no_data(multiple_sequences_file_path, lines_count)


def get_multiple_sequences_file_path_parents(multiple_sequences_file_path: Path) -> Path:
    return Path(multiple_sequences_file_path.parents[0])


def get_multiple_sequences_file_path_parents_underscored(multiple_sequences_file_path_parents: Path) -> str:
    multiple_sequences_file_path_parents_underscored = str(multiple_sequences_file_path_parents) \
        .replace("/", "_").replace("\\", "_").replace(".", "").replace(":", "")
    if len(multiple_sequences_file_path_parents_underscored) > 0 and \
            multiple_sequences_file_path_parents_underscored[0] == "_":
        multiple_sequences_file_path_parents_underscored = \
            multiple_sequences_file_path_parents_underscored.replace("_", "", 1)
    return multiple_sequences_file_path_parents_underscored


def get_individual_sequences_name_list(multiple_sequences_file_path: Path) -> list:
    individual_sequences_start_token = ">"
    individual_sequences_name_list = []
    with open(multiple_sequences_file_path, mode="r") as multiple_sequences_file:
        for line in multiple_sequences_file:
            line = line.strip()
            if line.startswith(individual_sequences_start_token):
                individual_sequence_name = line.split("|", 1)[0] \
                    .replace(individual_sequences_start_token, "").replace(" ", "")
                individual_sequences_name_list.append(individual_sequence_name)
    return individual_sequences_name_list


def get_individual_sequences_data_list(multiple_sequences_file_path: Path) -> list:
    individual_sequences_start_token = ">"
    individual_sequences_data_list = []
    current_individual_sequence_data = []
    with open(multiple_sequences_file_path, mode="r") as multiple_sequences_file:
        for line in multiple_sequences_file:
            line = line.strip()
            if line.startswith(individual_sequences_start_token) and current_individual_sequence_data:
                individual_sequences_data_list.append(current_individual_sequence_data[:])
                current_individual_sequence_data = []
            current_individual_sequence_data.append(line)
        individual_sequences_data_list.append(current_individual_sequence_data)
    return individual_sequences_data_list


def write_individual_sequences_files(multiple_sequences_file_path_parents: Path,
                                     multiple_sequences_file_extension: str,
                                     individual_sequences_name_list: list,
                                     individual_sequences_data_list: list) -> int:
    individual_sequences_files_written_count = 0
    for index_name in range(len(individual_sequences_name_list)):
        individual_sequence_file_name = individual_sequences_name_list[index_name] + multiple_sequences_file_extension
        with open(multiple_sequences_file_path_parents.joinpath(individual_sequence_file_name),
                  mode="w") as individual_sequence_file:
            individual_sequence_data = individual_sequences_data_list[index_name]
            for index_data in range(len(individual_sequence_data)):
                individual_sequence_file.write(individual_sequence_data[index_data] + "\n")
        individual_sequences_files_written_count = individual_sequences_files_written_count + 1
    return individual_sequences_files_written_count


def write_individual_sequences_files_path_list(multiple_sequences_file_path_parents: Path,
                                               multiple_sequences_file_extension: str,
                                               individual_sequences_name_list: list) -> Path:
    multiple_sequences_file_path_parents_underscored = \
        get_multiple_sequences_file_path_parents_underscored(multiple_sequences_file_path_parents)
    individual_sequences_files_path_list_file_prefix_name = ""
    if len(multiple_sequences_file_path_parents_underscored) > 0:
        individual_sequences_files_path_list_file_prefix_name = multiple_sequences_file_path_parents_underscored + "_"
    individual_sequences_files_path_list_file_name = \
        individual_sequences_files_path_list_file_prefix_name + "Sequences_Path_List.txt"
    individual_sequences_files_path_list_file_path = Path.cwd().joinpath(individual_sequences_files_path_list_file_name)
    sequences_fasta_files_index_count = 0
    with open(individual_sequences_files_path_list_file_path,
              mode="w") as individual_sequences_files_path_list_file_name:
        for index_name in range(len(individual_sequences_name_list)):
            sequence_file_name = individual_sequences_name_list[index_name] + multiple_sequences_file_extension
            individual_sequences_files_path_list_file_name.write(str(Path(multiple_sequences_file_path_parents,
                                                                     sequence_file_name)) + "\n")
            sequences_fasta_files_index_count = sequences_fasta_files_index_count + 1
    return individual_sequences_files_path_list_file_path


def print_split_details(multiple_sequences_file_full_path: Path,
                        individual_sequences_read_count: int,
                        individual_sequences_files_written_count: int,
                        individual_sequences_files_path: Path,
                        individual_sequences_files_path_list_file_path: Path) -> None:
    split_details_message = "Multiple sequences file (source): {0}\n" \
                            "Number of individual sequences read from source: {1}\n" \
                            "Number of individual sequences files written to disk: {2}\n" \
                            "Location of individual sequences files: {3}\n" \
                            "Individual sequences files path list file: {4}" \
        .format(str(multiple_sequences_file_full_path),
                str(individual_sequences_read_count),
                str(individual_sequences_files_written_count),
                str(individual_sequences_files_path),
                str(individual_sequences_files_path_list_file_path))
    print(split_details_message)


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
              help="Generate a list containing location (path) of the resulting individual sequences files.")
@click.option("--verbose",
              is_flag=True,
              help="Show details about running split command.")
def split(multiple_sequences_file_path: Path,
          generate_path_list: bool,
          verbose: bool) -> None:
    """
    Split one multiple sequences fasta file into individual sequences fasta files.\n
    1. Input:\n
    1.1 MULTIPLE_SEQUENCES_FILE_PATH - Location (path) of the multiple sequences fasta source file to be splitted.\n
    2. Output:\n
    2.1 Individual Sequences Files - Individual sequences fasta files generated after running split command.
    They are saved in the same path where the multiple sequences fasta source file is located.
    Their names are determined by the information stated before pipe symbol (|) in their description lines.
    Notice that the multiple sequences fasta source file stays untouched after split command execution.\n
    2.2 Individual Sequences Path List Text File [Optional] - List containing the location (path)
    of the resulting individual sequences fasta files.
    Its name is determined by multiple sequences fasta source file location.
    It is generated in the current path where the user ran split command.\n
    Use --generate-path-list option flag to activate this function.\n
    2.3 Splitting Details [Optional] - Show details of split command execution:
    multiple sequences fasta source file location, number of individual sequences read from source file,
    number of individual sequences files written to disk, individual sequences files location
    and individual sequences files path list file location (if generated).\n
    Use --verbose option flag to activate this function.\n
    """
    # BEGIN

    # VALIDATE MULTIPLE SEQUENCES FILE (AS FASTA FORMATTED FILE)
    check_if_is_valid_multiple_sequences_file(multiple_sequences_file_path)

    # GET MULTIPLE SEQUENCES FILE PATH PARENTS
    multiple_sequences_file_path_parents = get_multiple_sequences_file_path_parents(multiple_sequences_file_path)

    # GET MULTIPLE SEQUENCES FILE EXTENSION
    multiple_sequences_file_extension = get_multiple_sequences_file_extension(multiple_sequences_file_path)

    # READ MULTIPLE SEQUENCES FILE AND GET INDIVIDUAL SEQUENCES NAME LIST
    individual_sequences_name_list = get_individual_sequences_name_list(multiple_sequences_file_path)

    # READ MULTIPLE SEQUENCES FILE AND GET INDIVIDUAL SEQUENCES DATA LIST
    individual_sequences_data_list = get_individual_sequences_data_list(multiple_sequences_file_path)

    # WRITE INDIVIDUAL SEQUENCES FASTA FILES
    individual_sequences_files_written_count = \
        write_individual_sequences_files(multiple_sequences_file_path_parents,
                                         multiple_sequences_file_extension,
                                         individual_sequences_name_list,
                                         individual_sequences_data_list)

    individual_sequences_files_path_list_file_path = None
    if generate_path_list:
        # WRITE INDIVIDUAL SEQUENCES FASTA FILES PATH (LOCATION) LIST
        individual_sequences_files_path_list_file_path = \
            write_individual_sequences_files_path_list(multiple_sequences_file_path_parents,
                                                       multiple_sequences_file_extension,
                                                       individual_sequences_name_list)

    if verbose:
        # SHOW DETAILS ABOUT RUNNING THIS SPLIT COMMAND
        multiple_sequences_file_full_path = Path.cwd().joinpath(multiple_sequences_file_path)
        individual_sequences_read_count = len(individual_sequences_name_list)
        individual_sequences_files_path = Path.cwd().joinpath(multiple_sequences_file_path_parents)
        print_split_details(multiple_sequences_file_full_path,
                            individual_sequences_read_count,
                            individual_sequences_files_written_count,
                            individual_sequences_files_path,
                            individual_sequences_files_path_list_file_path)

    # END
    sys.exit(0)


if __name__ == "__main__":
    split()
