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


def check_if_sequences_file_has_fasta_extension(sequences_file_path: Path) -> None:
    fasta_extension_types = [".fa", ".faa", ".fasta", ".ffn", ".fna", ".frn"]
    if get_sequences_file_extension(sequences_file_path) not in fasta_extension_types:
        invalid_extension_file_message = "Only FASTA extension files ({0}) are allowed!" \
            .format(", ".join(fasta_extension_types))
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


@click.group()
def splitter_group() -> None:
    pass


@splitter_group.command("split", short_help="Split one multiple sequences file into individual sequences files.")
@click.argument("sequences_file_path", nargs=1, type=Path, required=True)
def split(sequences_file_path: Path) -> None:
    """
    Split one multiple sequences fasta file into individual sequences fasta files.\n
    """
    # BEGIN

    # VALIDATE SEQUENCES FILE (AS FASTA FORMATTED FILE)
    check_if_is_valid_fasta_sequences_file(sequences_file_path)

    # GET SEQUENCES FILE PATH PARENTS
    sequences_file_path_parents = get_sequences_file_path_parents(sequences_file_path)

    # END
    sys.exit(0)


if __name__ == "__main__":
    split()
