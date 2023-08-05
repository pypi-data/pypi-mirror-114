from pathlib import Path
from click.testing import CliRunner
import pytest
import splitter.splitter
import splitter.splitter_exceptions
import sys
import runpy


def test_when_number_of_arguments_equals_one_then_ok():
    number_of_arguments_provided = 1
    assert splitter.splitter \
           .check_if_is_valid_number_of_arguments(number_of_arguments_provided) is None


def test_when_number_of_arguments_not_equals_one_then_throws_invalid_number_of_arguments_exception():
    number_of_arguments_provided = 2
    with pytest.raises(splitter.splitter_exceptions.InvalidNumberofArgumentsError) as pytest_wrapped_e:
        splitter.splitter.check_if_is_valid_number_of_arguments(number_of_arguments_provided)
    invalid_number_of_arguments_message = "Invalid number of arguments provided!\n" \
                                          "Expected: 1 argument (FASTA sequences file).\n" \
                                          "Provided: {0} argument(s).".format(number_of_arguments_provided)
    assert pytest_wrapped_e.type == splitter.splitter_exceptions.InvalidNumberofArgumentsError
    assert str(pytest_wrapped_e.value) == invalid_number_of_arguments_message


def test_when_sequences_file_not_exists_then_throws_file_not_found_exception():
    inexistent_sequences_file = Path("inexistent_sequences.fasta")
    with pytest.raises(FileNotFoundError) as pytest_wrapped_e:
        splitter.splitter.check_if_sequences_file_exists(inexistent_sequences_file)
    file_not_found_message = "FASTA sequences file not found!"
    assert pytest_wrapped_e.type == FileNotFoundError
    assert str(pytest_wrapped_e.value) == file_not_found_message


def test_when_sequences_file_exists_then_return_sequences_file_extension():
    sequences_file_extension_expected = ".fasta"
    temporary_sequences_file = Path("sequences.fasta")
    with open(temporary_sequences_file, mode="w"):
        pass
    sequences_file_extension_returned = splitter.splitter \
        .get_sequences_file_extension(temporary_sequences_file)
    assert sequences_file_extension_returned == sequences_file_extension_expected
    temporary_sequences_file.unlink()


def test_when_sequences_file_does_not_have_fasta_extension_then_throws_invalid_extension_file_exception():
    temporary_sequences_file = Path("sequences.txt")
    with open(temporary_sequences_file, mode="w"):
        pass
    with pytest.raises(splitter.splitter_exceptions.InvalidExtensionFileError) as pytest_wrapped_e:
        splitter.splitter.check_if_sequences_file_has_fasta_extension(temporary_sequences_file)
    fasta_extension_types = [".fa", ".faa", ".fasta", ".ffn", ".fna", ".frn"]
    invalid_extension_file_message = "Only FASTA extension files ({0}) are allowed!" \
        .format(", ".join(fasta_extension_types))
    assert pytest_wrapped_e.type == splitter.splitter_exceptions.InvalidExtensionFileError
    assert str(pytest_wrapped_e.value) == invalid_extension_file_message
    temporary_sequences_file.unlink()


def test_when_description_line_is_parsed_then_return_description_lines_count():
    description_line_count_expected = 1
    line = ">ValidDescription1 |text1\n"
    sequences_start_token = ">"
    description_lines_count_returned = 0
    description_lines_count_returned = splitter.splitter \
        .parse_description_line(line, sequences_start_token, description_lines_count_returned)
    assert description_lines_count_returned == description_line_count_expected


def test_when_invalid_description_line_is_parsed_then_return_invalid_description_lines_count():
    invalid_description_lines_count_expected = 1
    line = "> InvalidDescription1\n"
    sequences_start_token = ">"
    invalid_description_lines_count_returned = 0
    invalid_description_lines_count_returned = splitter.splitter \
        .parse_invalid_description_line(line, sequences_start_token, invalid_description_lines_count_returned)
    assert invalid_description_lines_count_returned == invalid_description_lines_count_expected


def test_when_sequences_file_is_parsed_then_return_sequences_file_counter():
    description_lines_count_expected = 2
    invalid_description_lines_count_expected = 1
    lines_count_expected = 4
    temporary_sequences_file = Path("sequences.fasta")
    with open(temporary_sequences_file, mode="w") as sequences_file:
        sequences_file.write("> InvalidDescription1\nAAA\n")
        sequences_file.write(">ValidDescription1 |text1\nCCC\n")
    description_lines_count_returned, invalid_description_lines_count_returned, lines_count_returned = \
        splitter.splitter.get_sequences_file_counters(temporary_sequences_file)
    assert description_lines_count_returned == description_lines_count_expected
    assert invalid_description_lines_count_returned == invalid_description_lines_count_expected
    assert lines_count_returned == lines_count_expected
    temporary_sequences_file.unlink()


def test_when_fasta_sequences_file_has_not_any_description_line_then_throws_invalid_formatted_fasta_file_exception():
    temporary_sequences_file = Path("sequences.fasta")
    with open(temporary_sequences_file, mode="w") as sequences_file:
        sequences_file.write("AAA\n")
        sequences_file.write("CCC\n")
        sequences_file.write("GGG\n")
    description_lines_count_returned, invalid_description_lines_count_returned, lines_count_returned = \
        splitter.splitter.get_sequences_file_counters(temporary_sequences_file)
    with pytest.raises(splitter.splitter_exceptions.InvalidFormattedFastaFileError) as pytest_wrapped_e:
        splitter.splitter \
            .check_if_sequences_file_has_any_description_line(temporary_sequences_file,
                                                              description_lines_count_returned)
    invalid_formatted_fasta_file_message = "'{0}' does not have any description line!" \
        .format(str(temporary_sequences_file))
    assert pytest_wrapped_e.type == splitter.splitter_exceptions.InvalidFormattedFastaFileError
    assert str(pytest_wrapped_e.value) == invalid_formatted_fasta_file_message
    temporary_sequences_file.unlink()


def test_when_fasta_sequences_file_has_invalid_description_lines_then_throws_invalid_formatted_fasta_file_exception():
    temporary_sequences_file = Path("sequences.fasta")
    with open(temporary_sequences_file, mode="w") as sequences_file:
        sequences_file.write("> InvalidDescription1\nAAA\n")
        sequences_file.write(">ValidDescription1 |text1\nCCC\n")
        sequences_file.write(">ValidDescription2|text2\nGGG\n")
        sequences_file.write("> InvalidDescription2|text2\nTTT\n")
    description_lines_count_returned, invalid_description_lines_count_returned, lines_count_returned = \
        splitter.splitter.get_sequences_file_counters(temporary_sequences_file)
    with pytest.raises(splitter.splitter_exceptions.InvalidFormattedFastaFileError) as pytest_wrapped_e:
        splitter.splitter \
            .check_if_sequences_file_has_any_invalid_description_line(temporary_sequences_file,
                                                                      invalid_description_lines_count_returned)
    invalid_formatted_fasta_file_message = "'{0}' contains {1} line(s) with invalid description format!" \
        .format(str(temporary_sequences_file), str(2))
    assert pytest_wrapped_e.type == splitter.splitter_exceptions.InvalidFormattedFastaFileError
    assert str(pytest_wrapped_e.value) == invalid_formatted_fasta_file_message
    temporary_sequences_file.unlink()


def test_when_fasta_sequences_file_has_no_data_then_throws_invalid_formatted_fasta_file_exception():
    temporary_sequences_file = Path("sequences.fasta")
    with open(temporary_sequences_file, mode="w") as sequences_file:
        sequences_file.write(">ValidDescription1\n")
    description_lines_count_returned, invalid_description_lines_count_returned, lines_count_returned = \
        splitter.splitter.get_sequences_file_counters(temporary_sequences_file)
    with pytest.raises(splitter.splitter_exceptions.InvalidFormattedFastaFileError) as pytest_wrapped_e:
        splitter.splitter.check_if_sequences_file_has_no_data(temporary_sequences_file,
                                                              lines_count_returned)
    invalid_formatted_fasta_file_message = "'{0}' seems a empty fasta file!".format(str(temporary_sequences_file))
    assert pytest_wrapped_e.type == splitter.splitter_exceptions.InvalidFormattedFastaFileError
    assert str(pytest_wrapped_e.value) == invalid_formatted_fasta_file_message
    temporary_sequences_file.unlink()


def test_when_fasta_sequences_file_has_all_valid_lines_then_ok():
    temporary_sequences_file = Path("sequences.fasta")
    with open(temporary_sequences_file, mode="w") as sequences_file:
        sequences_file.write(">ValidDescription1|text1\nAAA\n")
        sequences_file.write(">ValidDescription2 |text2\nCCC\n")
        sequences_file.write(">ValidDescription3\nGGG\n")
    assert splitter.splitter \
           .check_if_is_valid_fasta_sequences_file(temporary_sequences_file) is None
    temporary_sequences_file.unlink()


def test_when_fasta_sequences_file_path_is_on_the_same_level_then_return_empty_path_underscored_string():
    sequences_file_same_level_path_parents_underscored_expected = ""
    temporary_sequences_file = Path("sequences.fasta")
    with open(temporary_sequences_file, mode="w"):
        pass
    sequences_file_same_level_path_parents_returned = splitter.splitter \
        .get_sequences_file_path_parents(temporary_sequences_file)
    sequences_file_same_level_path_parents_underscored_returned = splitter.splitter \
        .get_sequences_file_path_parents_underscored(sequences_file_same_level_path_parents_returned)
    assert sequences_file_same_level_path_parents_underscored_returned \
           == sequences_file_same_level_path_parents_underscored_expected
    temporary_sequences_file.unlink()


def test_when_fasta_sequences_file_path_is_one_level_below_then_return_path_underscored_string():
    sequences_file_one_level_below_path_parents_underscored_expected = "ParentBelow"
    temporary_sequences_directory_one_level_below = Path("ParentBelow")
    temporary_sequences_directory_one_level_below.mkdir()
    temporary_sequences_file = temporary_sequences_directory_one_level_below.joinpath("sequences.fasta")
    with open(temporary_sequences_file, mode="w"):
        pass
    sequences_file_one_level_below_path_parents_returned = splitter.splitter \
        .get_sequences_file_path_parents(temporary_sequences_file)
    sequences_file_one_level_below_path_parents_underscored_returned = splitter.splitter \
        .get_sequences_file_path_parents_underscored(sequences_file_one_level_below_path_parents_returned)
    assert sequences_file_one_level_below_path_parents_underscored_returned \
           == sequences_file_one_level_below_path_parents_underscored_expected
    temporary_sequences_file.unlink()
    temporary_sequences_directory_one_level_below.rmdir()


def test_when_fasta_sequences_file_path_is_one_level_above_then_return_path_underscored_string():
    sequences_file_one_level_above_path_parents_underscored_expected = \
        str(Path.cwd().parent).replace("/", "_").replace("\\", "_") \
        .replace(".", "").replace(":", "_").replace("_", "", 1) + "_ParentAbove"
    temporary_sequences_directory_one_level_above = Path.cwd().parent.joinpath("ParentAbove")
    temporary_sequences_directory_one_level_above.mkdir()
    temporary_sequences_file = temporary_sequences_directory_one_level_above.joinpath("sequences.fasta")
    with open(temporary_sequences_file, mode="w"):
        pass
    sequences_file_one_level_above_path_parents_returned = splitter.splitter \
        .get_sequences_file_path_parents(temporary_sequences_file)
    sequences_file_one_level_above_path_parents_underscored_returned = splitter.splitter \
        .get_sequences_file_path_parents_underscored(sequences_file_one_level_above_path_parents_returned)
    assert sequences_file_one_level_above_path_parents_underscored_returned \
           == sequences_file_one_level_above_path_parents_underscored_expected
    temporary_sequences_file.unlink()
    temporary_sequences_directory_one_level_above.rmdir()


def test_when_fasta_sequences_file_is_valid_then_return_sequences_name_list():
    sequences_name_list_expected = ["Sequence1", "Sequence2", "Sequence3"]
    temporary_sequences_file = Path("sequences.fasta")
    with open(temporary_sequences_file, mode="w") as sequences_file:
        sequences_file.write(">Sequence1|text1\nAAA\n")
        sequences_file.write(">Sequence2 |text2\nCCC\n")
        sequences_file.write(">Sequence3\nGGG\n")
    sequences_name_list_returned = splitter.splitter \
        .get_sequences_name_list(temporary_sequences_file)
    for index in range(len(sequences_name_list_returned)):
        assert sequences_name_list_returned[index] == sequences_name_list_expected[index]
    temporary_sequences_file.unlink()


def test_when_fasta_sequences_file_is_valid_then_return_sequences_data_list():
    sequences_data_list_expected = ["AAA", "CCC", "GGG"]
    temporary_sequences_file = Path("sequences.fasta")
    with open(temporary_sequences_file, mode="w") as sequences_file:
        sequences_file.write(">Sequence1|text1\nAAA\n")
        sequences_file.write(">Sequence2 |text2\nCCC\n")
        sequences_file.write(">Sequence3\nGGG\n")
    sequences_data_list_returned = splitter.splitter \
        .get_sequences_data_list(temporary_sequences_file)
    for index in range(len(sequences_data_list_returned)):
        assert sequences_data_list_returned[index][1] == sequences_data_list_expected[index]
    temporary_sequences_file.unlink()


def test_when_execute_split_command_without_sequences_file_path_argument_then_return_exit_error_code_one():
    runner = CliRunner()
    result = runner.invoke(splitter.splitter.splitter_group, ["split", ""])
    assert result.return_value is None
    assert result.exit_code == 1
    assert result.exc_info[0] == FileNotFoundError
    assert str(result.exception) == "FASTA sequences file not found!"


def test_when_execute_split_command_with_sequences_file_path_argument_then_return_successful_exit_code_zero():
    temporary_sequences_file = Path("sequences.fasta")
    with open(temporary_sequences_file, mode="w") as sequences_file:
        sequences_file.write(">Sequence1|text1\nAAA\n")
        sequences_file.write(">Sequence2 |text2\nCCC\n")
        sequences_file.write(">Sequence3\nGGG\n")
    runner = CliRunner()
    result = runner.invoke(splitter.splitter.splitter_group,
                           ["split", str(temporary_sequences_file)])
    assert result.return_value is None
    assert result.exit_code == 0
    assert result.exc_info[0] == SystemExit
    assert result.exception is None
    temporary_sequences_file.unlink()


def test_when_execute_main_function_without_sequences_file_path_argument_then_throws_file_not_found_exception():
    sys.argv = ["", ""]
    with pytest.raises(FileNotFoundError) as pytest_wrapped_e:
        runpy.run_path("splitter/splitter.py", run_name="__main__")
    assert pytest_wrapped_e.type == FileNotFoundError
    assert str(pytest_wrapped_e.value) == "FASTA sequences file not found!"
