from pathlib import Path
from click.testing import CliRunner
import pytest
import fastasplitter_splitter.splitter
import fastasplitter_splitter.splitter_exceptions
import sys
import runpy


def test_when_number_of_arguments_equals_one_then_ok():
    number_of_arguments_provided = 1
    assert fastasplitter_splitter.splitter.check_if_is_valid_number_of_arguments(number_of_arguments_provided) is None


def test_when_number_of_arguments_not_equals_one_then_throws_invalid_number_of_arguments_exception():
    number_of_arguments_provided = 2
    with pytest.raises(fastasplitter_splitter.splitter_exceptions.InvalidNumberofArgumentsError) as pytest_wrapped_e:
        fastasplitter_splitter.splitter.check_if_is_valid_number_of_arguments(number_of_arguments_provided)
    invalid_number_of_arguments_message = "Invalid number of arguments provided!\n" \
                                          "Expected: 1 argument (FASTA multiple sequences file).\n" \
                                          "Provided: {0} argument(s).".format(number_of_arguments_provided)
    assert pytest_wrapped_e.type == fastasplitter_splitter.splitter_exceptions.InvalidNumberofArgumentsError
    assert str(pytest_wrapped_e.value) == invalid_number_of_arguments_message


def test_when_multiple_sequences_file_not_exists_then_throws_file_not_found_exception():
    inexistent_multiple_sequences_file = Path("inexistent_multiple_sequences.fasta")
    with pytest.raises(FileNotFoundError) as pytest_wrapped_e:
        fastasplitter_splitter.splitter.check_if_multiple_sequences_file_exists(inexistent_multiple_sequences_file)
    file_not_found_message = "FASTA multiple sequences file not found!"
    assert pytest_wrapped_e.type == FileNotFoundError
    assert str(pytest_wrapped_e.value) == file_not_found_message


def test_when_multiple_sequences_file_exists_then_return_multiple_sequences_file_extension():
    multiple_sequences_file_extension_expected = ".fasta"
    temporary_multiple_sequences_file = Path("sequences.fasta")
    with open(temporary_multiple_sequences_file, mode="w"):
        pass
    multiple_sequences_file_extension_returned = fastasplitter_splitter.splitter \
        .get_multiple_sequences_file_extension(temporary_multiple_sequences_file)
    assert multiple_sequences_file_extension_returned == multiple_sequences_file_extension_expected
    temporary_multiple_sequences_file.unlink()


def test_when_multiple_sequences_file_does_not_have_fasta_extension_then_throws_invalid_extension_file_exception():
    temporary_multiple_sequences_file = Path("sequences.txt")
    with open(temporary_multiple_sequences_file, mode="w"):
        pass
    with pytest.raises(fastasplitter_splitter.splitter_exceptions.InvalidExtensionFileError) as pytest_wrapped_e:
        fastasplitter_splitter.splitter \
            .check_if_multiple_sequences_file_has_fasta_extension(temporary_multiple_sequences_file)
    supported_fasta_file_extensions = fastasplitter_splitter.splitter.get_supported_fasta_file_extensions()
    invalid_extension_file_message = "Only FASTA extension files ({0}) are allowed!" \
        .format(", ".join(supported_fasta_file_extensions))
    assert pytest_wrapped_e.type == fastasplitter_splitter.splitter_exceptions.InvalidExtensionFileError
    assert str(pytest_wrapped_e.value) == invalid_extension_file_message
    temporary_multiple_sequences_file.unlink()


def test_when_description_line_is_parsed_then_return_description_lines_count():
    description_line_count_expected = 1
    line = ">ValidDescription1 |text1"
    individual_sequences_start_token = ">"
    description_lines_count_returned = 0
    description_lines_count_returned = fastasplitter_splitter.splitter \
        .parse_description_line(line, individual_sequences_start_token, description_lines_count_returned)
    assert description_lines_count_returned == description_line_count_expected


def test_when_description_line_contains_whitespace_right_after_start_token_then_return_true():
    line = "> InvalidDescription1"
    individual_sequences_start_token = ">"
    assert fastasplitter_splitter.splitter. \
        description_line_contains_whitespace_right_after_start_token(line, individual_sequences_start_token)


def test_when_description_line_contains_no_whitespace_right_after_start_token_then_return_false():
    line = ">ValidDescription1"
    individual_sequences_start_token = ">"
    assert not fastasplitter_splitter.splitter. \
        description_line_contains_whitespace_right_after_start_token(line, individual_sequences_start_token)


def test_when_description_line_has_no_information_after_start_token_then_return_true():
    line = ">"
    individual_sequences_start_token = ">"
    assert fastasplitter_splitter.splitter. \
        description_line_has_no_information_after_start_token(line, individual_sequences_start_token)


def test_when_description_line_has_information_after_start_token_then_return_false():
    line = ">AAA"
    individual_sequences_start_token = ">"
    assert not fastasplitter_splitter.splitter. \
        description_line_has_no_information_after_start_token(line, individual_sequences_start_token)


def test_when_invalid_description_line_is_parsed_then_return_invalid_description_lines_count():
    invalid_description_lines_count_expected = 1
    line = "> InvalidDescription1"
    individual_sequences_start_token = ">"
    invalid_description_lines_count_returned = 0
    invalid_description_lines_count_returned = \
        fastasplitter_splitter.splitter.parse_invalid_description_line(line,
                                                                       individual_sequences_start_token,
                                                                       invalid_description_lines_count_returned)
    assert invalid_description_lines_count_returned == invalid_description_lines_count_expected


def test_when_multiple_sequences_file_is_parsed_then_return_sequences_file_counter():
    description_lines_count_expected = 2
    invalid_description_lines_count_expected = 1
    lines_count_expected = 4
    temporary_multiple_sequences_file = Path("sequences.fasta")
    with open(temporary_multiple_sequences_file, mode="w") as multiple_sequences_file:
        multiple_sequences_file.write("> InvalidDescription1\nAAA\n")
        multiple_sequences_file.write(">ValidDescription1 |text1\nCCC\n")
    description_lines_count_returned, invalid_description_lines_count_returned, lines_count_returned = \
        fastasplitter_splitter.splitter.get_multiple_sequences_file_counters(temporary_multiple_sequences_file)
    assert description_lines_count_returned == description_lines_count_expected
    assert invalid_description_lines_count_returned == invalid_description_lines_count_expected
    assert lines_count_returned == lines_count_expected
    temporary_multiple_sequences_file.unlink()


def test_when_multiple_sequences_file_has_not_any_description_line_then_throws_invalid_formatted_fasta_file_exception():
    temporary_multiple_sequences_file = Path("sequences.fasta")
    with open(temporary_multiple_sequences_file, mode="w") as multiple_sequences_file:
        multiple_sequences_file.write("AAA\n")
        multiple_sequences_file.write("CCC\n")
        multiple_sequences_file.write("GGG\n")
    description_lines_count_returned, invalid_description_lines_count_returned, lines_count_returned = \
        fastasplitter_splitter.splitter.get_multiple_sequences_file_counters(temporary_multiple_sequences_file)
    with pytest.raises(fastasplitter_splitter.splitter_exceptions.InvalidFormattedFastaFileError) as pytest_wrapped_e:
        fastasplitter_splitter.splitter \
            .check_if_multiple_sequences_file_has_any_description_line(temporary_multiple_sequences_file,
                                                                       description_lines_count_returned)
    invalid_formatted_fasta_file_message = "'{0}' does not have any description line!" \
        .format(str(temporary_multiple_sequences_file))
    assert pytest_wrapped_e.type == fastasplitter_splitter.splitter_exceptions.InvalidFormattedFastaFileError
    assert str(pytest_wrapped_e.value) == invalid_formatted_fasta_file_message
    temporary_multiple_sequences_file.unlink()


def test_when_mult_sequences_file_has_invalid_description_lines_then_throws_invalid_formatted_fasta_file_exception():
    temporary_multiple_sequences_file = Path("sequences.fasta")
    with open(temporary_multiple_sequences_file, mode="w") as multiple_sequences_file:
        multiple_sequences_file.write("> InvalidDescription1\nAAA\n")
        multiple_sequences_file.write(">ValidDescription1 |text1\nCCC\n")
        multiple_sequences_file.write(">ValidDescription2|text2\nGGG\n")
        multiple_sequences_file.write("> InvalidDescription2|text2\nTTT\n")
    description_lines_count_returned, invalid_description_lines_count_returned, lines_count_returned = \
        fastasplitter_splitter.splitter.get_multiple_sequences_file_counters(temporary_multiple_sequences_file)
    with pytest.raises(fastasplitter_splitter.splitter_exceptions.InvalidFormattedFastaFileError) as pytest_wrapped_e:
        fastasplitter_splitter.splitter \
            .check_if_multiple_sequences_file_has_any_invalid_description_line(temporary_multiple_sequences_file,
                                                                               invalid_description_lines_count_returned)
    invalid_formatted_fasta_file_message = "'{0}' contains {1} line(s) with invalid description format!" \
        .format(str(temporary_multiple_sequences_file), str(2))
    assert pytest_wrapped_e.type == fastasplitter_splitter.splitter_exceptions.InvalidFormattedFastaFileError
    assert str(pytest_wrapped_e.value) == invalid_formatted_fasta_file_message
    temporary_multiple_sequences_file.unlink()


def test_when_multiple_sequences_file_has_no_data_then_throws_invalid_formatted_fasta_file_exception():
    temporary_multiple_sequences_file = Path("sequences.fasta")
    with open(temporary_multiple_sequences_file, mode="w") as multiple_sequences_file:
        multiple_sequences_file.write(">ValidDescription1")
    description_lines_count_returned, invalid_description_lines_count_returned, lines_count_returned = \
        fastasplitter_splitter.splitter.get_multiple_sequences_file_counters(temporary_multiple_sequences_file)
    with pytest.raises(fastasplitter_splitter.splitter_exceptions.InvalidFormattedFastaFileError) as pytest_wrapped_e:
        fastasplitter_splitter.splitter.check_if_multiple_sequences_file_has_no_data(temporary_multiple_sequences_file,
                                                                                     lines_count_returned)
    invalid_formatted_fasta_file_message = "'{0}' seems a empty fasta file!" \
        .format(str(temporary_multiple_sequences_file))
    assert pytest_wrapped_e.type == fastasplitter_splitter.splitter_exceptions.InvalidFormattedFastaFileError
    assert str(pytest_wrapped_e.value) == invalid_formatted_fasta_file_message
    temporary_multiple_sequences_file.unlink()


def test_when_multiple_sequences_file_has_all_valid_lines_then_ok():
    temporary_multiple_sequences_file = Path("sequences.fasta")
    with open(temporary_multiple_sequences_file, mode="w") as multiple_sequences_file:
        multiple_sequences_file.write(">ValidDescription1|text1\nAAA\n")
        multiple_sequences_file.write(">ValidDescription2 |text2\nCCC\n")
        multiple_sequences_file.write(">ValidDescription3\nGGG\n")
    assert fastasplitter_splitter.splitter \
           .check_if_is_valid_multiple_sequences_file(temporary_multiple_sequences_file) is None
    temporary_multiple_sequences_file.unlink()


def test_when_multiple_sequences_file_path_is_on_the_same_level_then_return_empty_path_underscored_string():
    multiple_sequences_file_same_level_path_parents_underscored_expected = ""
    temporary_multiple_sequences_file = Path("sequences.fasta")
    with open(temporary_multiple_sequences_file, mode="w"):
        pass
    multiple_sequences_file_same_level_path_parents_returned = fastasplitter_splitter.splitter \
        .get_multiple_sequences_file_path_parents(temporary_multiple_sequences_file)
    multiple_sequences_file_same_level_path_parents_underscored_returned = fastasplitter_splitter.splitter \
        .get_multiple_sequences_file_path_parents_underscored(multiple_sequences_file_same_level_path_parents_returned)
    assert multiple_sequences_file_same_level_path_parents_underscored_returned \
           == multiple_sequences_file_same_level_path_parents_underscored_expected
    temporary_multiple_sequences_file.unlink()


def test_when_multiple_sequences_file_path_is_one_level_below_then_return_path_underscored_string():
    multiple_sequences_file_one_level_below_path_parents_underscored_expected = "ParentBelow"
    temporary_directory_one_level_below = Path("ParentBelow")
    temporary_directory_one_level_below.mkdir()
    temporary_multiple_sequences_file = temporary_directory_one_level_below.joinpath("sequences.fasta")
    with open(temporary_multiple_sequences_file, mode="w"):
        pass
    mult_sequences_file_one_level_below_path_parents_returned = fastasplitter_splitter.splitter \
        .get_multiple_sequences_file_path_parents(temporary_multiple_sequences_file)
    multiple_sequences_file_one_level_below_path_parents_underscored_returned = fastasplitter_splitter.splitter \
        .get_multiple_sequences_file_path_parents_underscored(mult_sequences_file_one_level_below_path_parents_returned)
    assert multiple_sequences_file_one_level_below_path_parents_underscored_returned \
           == multiple_sequences_file_one_level_below_path_parents_underscored_expected
    temporary_multiple_sequences_file.unlink()
    temporary_directory_one_level_below.rmdir()


def test_when_multiple_sequences_file_path_is_one_level_above_then_return_path_underscored_string():
    multiple_sequences_file_one_level_above_path_parents_underscored_expected = \
        str(Path.cwd().parent).replace("/", "_").replace("\\", "_") \
        .replace(".", "").replace(":", "_").replace("_", "", 1) + "_ParentAbove"
    temporary_directory_one_level_above = Path.cwd().parent.joinpath("ParentAbove")
    temporary_directory_one_level_above.mkdir()
    temporary_multiple_sequences_file = temporary_directory_one_level_above.joinpath("sequences.fasta")
    with open(temporary_multiple_sequences_file, mode="w"):
        pass
    mult_sequences_file_one_level_above_path_parents_returned = fastasplitter_splitter.splitter \
        .get_multiple_sequences_file_path_parents(temporary_multiple_sequences_file)
    multiple_sequences_file_one_level_above_path_parents_underscored_returned = fastasplitter_splitter.splitter \
        .get_multiple_sequences_file_path_parents_underscored(mult_sequences_file_one_level_above_path_parents_returned)
    assert multiple_sequences_file_one_level_above_path_parents_underscored_returned \
           == multiple_sequences_file_one_level_above_path_parents_underscored_expected
    temporary_multiple_sequences_file.unlink()
    temporary_directory_one_level_above.rmdir()


def test_when_multiple_sequences_file_is_valid_then_return_individual_sequences_name_list():
    individual_sequences_name_list_expected = ["Sequence1", "Sequence2", "Sequence3"]
    temporary_multiple_sequences_file = Path("sequences.fasta")
    with open(temporary_multiple_sequences_file, mode="w") as multiple_sequences_file:
        multiple_sequences_file.write(">Sequence1|text1\nAAA\n")
        multiple_sequences_file.write(">Sequence2 |text2\nCCC\n")
        multiple_sequences_file.write(">Sequence3\nGGG\n")
    individual_sequences_name_list_returned = fastasplitter_splitter.splitter \
        .get_individual_sequences_name_list(temporary_multiple_sequences_file)
    for index in range(len(individual_sequences_name_list_returned)):
        assert individual_sequences_name_list_returned[index] == individual_sequences_name_list_expected[index]
    temporary_multiple_sequences_file.unlink()


def test_when_multiple_sequences_file_is_valid_then_return_individual_sequences_data_list():
    individual_sequences_data_list_expected = ["AAA", "CCC", "GGG"]
    temporary_multiple_sequences_file = Path("sequences.fasta")
    with open(temporary_multiple_sequences_file, mode="w") as multiple_sequences_file:
        multiple_sequences_file.write(">Sequence1|text1\nAAA\n")
        multiple_sequences_file.write(">Sequence2 |text2\nCCC\n")
        multiple_sequences_file.write(">Sequence3\nGGG\n")
    individual_sequences_data_list_returned = fastasplitter_splitter.splitter \
        .get_individual_sequences_data_list(temporary_multiple_sequences_file)
    for index in range(len(individual_sequences_data_list_returned)):
        assert individual_sequences_data_list_returned[index][1] == individual_sequences_data_list_expected[index]
    temporary_multiple_sequences_file.unlink()


def test_when_multiple_sequences_file_is_valid_and_path_is_on_the_same_level_then_split_sequences_and_write_to_disk():
    sequence1_file_expected = Path("Sequence1.fasta")
    sequence2_file_expected = Path("Sequence2.fasta")
    sequence3_file_expected = Path("Sequence3.fasta")
    individual_sequences_files_written_count_expected = 3
    temporary_multiple_sequences_file = Path("sequences.fasta")
    with open(temporary_multiple_sequences_file, mode="w") as multiple_sequences_file:
        multiple_sequences_file.write(">Sequence1|text1\nAAA\n")
        multiple_sequences_file.write(">Sequence2 |text2\nCCC\n")
        multiple_sequences_file.write(">Sequence3\nGGG\n")
    multiple_sequences_file_same_level_path_parents_returned = fastasplitter_splitter.splitter \
        .get_multiple_sequences_file_path_parents(temporary_multiple_sequences_file)
    multiple_sequences_file_extension_returned = fastasplitter_splitter.splitter \
        .get_multiple_sequences_file_extension(temporary_multiple_sequences_file)
    individual_sequences_name_list_returned = fastasplitter_splitter.splitter \
        .get_individual_sequences_name_list(temporary_multiple_sequences_file)
    individual_sequences_data_list_returned = fastasplitter_splitter.splitter \
        .get_individual_sequences_data_list(temporary_multiple_sequences_file)
    individual_sequences_files_written_count_returned = fastasplitter_splitter.splitter \
        .write_individual_sequences_files(multiple_sequences_file_same_level_path_parents_returned,
                                          multiple_sequences_file_extension_returned,
                                          individual_sequences_name_list_returned,
                                          individual_sequences_data_list_returned)
    assert individual_sequences_files_written_count_returned == individual_sequences_files_written_count_expected
    assert sequence1_file_expected.exists()
    assert sequence2_file_expected.exists()
    assert sequence3_file_expected.exists()
    sequence1_file_expected.unlink()
    sequence2_file_expected.unlink()
    sequence3_file_expected.unlink()
    temporary_multiple_sequences_file.unlink()


def test_when_multiple_sequences_file_is_valid_and_path_is_one_level_below_then_split_sequences_and_write_to_disk():
    sequence1_file_expected = Path.cwd().joinpath("ParentBelow").joinpath("Sequence1.fasta")
    sequence2_file_expected = Path.cwd().joinpath("ParentBelow").joinpath("Sequence2.fasta")
    sequence3_file_expected = Path.cwd().joinpath("ParentBelow").joinpath("Sequence3.fasta")
    individual_sequences_files_written_count_expected = 3
    temporary_directory_one_level_below = Path("ParentBelow")
    temporary_directory_one_level_below.mkdir()
    temporary_multiple_sequences_file = temporary_directory_one_level_below.joinpath("sequences.fasta")
    with open(temporary_multiple_sequences_file, mode="w") as multiple_sequences_file:
        multiple_sequences_file.write(">Sequence1|text1\nAAA\n")
        multiple_sequences_file.write(">Sequence2 |text2\nCCC\n")
        multiple_sequences_file.write(">Sequence3\nGGG\n")
    multiple_sequences_file_one_level_below_path_parents_returned = fastasplitter_splitter.splitter \
        .get_multiple_sequences_file_path_parents(temporary_multiple_sequences_file)
    multiple_sequences_file_extension_returned = fastasplitter_splitter.splitter \
        .get_multiple_sequences_file_extension(temporary_multiple_sequences_file)
    individual_sequences_name_list_returned = fastasplitter_splitter.splitter \
        .get_individual_sequences_name_list(temporary_multiple_sequences_file)
    individual_sequences_data_list_returned = fastasplitter_splitter.splitter \
        .get_individual_sequences_data_list(temporary_multiple_sequences_file)
    individual_sequences_files_written_count_returned = fastasplitter_splitter.splitter \
        .write_individual_sequences_files(multiple_sequences_file_one_level_below_path_parents_returned,
                                          multiple_sequences_file_extension_returned,
                                          individual_sequences_name_list_returned,
                                          individual_sequences_data_list_returned)
    assert individual_sequences_files_written_count_returned == individual_sequences_files_written_count_expected
    assert sequence1_file_expected.exists()
    assert sequence2_file_expected.exists()
    assert sequence3_file_expected.exists()
    sequence1_file_expected.unlink()
    sequence2_file_expected.unlink()
    sequence3_file_expected.unlink()
    temporary_multiple_sequences_file.unlink()
    temporary_directory_one_level_below.rmdir()


def test_when_multiple_sequences_file_is_valid_and_path_is_one_level_above_then_split_sequences_and_write_to_disk():
    sequence1_file_expected = Path.cwd().parent.joinpath("ParentAbove").joinpath("Sequence1.fasta")
    sequence2_file_expected = Path.cwd().parent.joinpath("ParentAbove").joinpath("Sequence2.fasta")
    sequence3_file_expected = Path.cwd().parent.joinpath("ParentAbove").joinpath("Sequence3.fasta")
    individual_sequences_files_written_count_expected = 3
    temporary_directory_one_level_above = Path.cwd().parent.joinpath("ParentAbove")
    temporary_directory_one_level_above.mkdir()
    temporary_multiple_sequences_file = temporary_directory_one_level_above.joinpath("sequences.fasta")
    with open(temporary_multiple_sequences_file, mode="w") as multiple_sequences_file:
        multiple_sequences_file.write(">Sequence1|text1\nAAA\n")
        multiple_sequences_file.write(">Sequence2 |text2\nCCC\n")
        multiple_sequences_file.write(">Sequence3\nGGG\n")
    multiple_sequences_file_one_level_above_path_parents_returned = fastasplitter_splitter.splitter \
        .get_multiple_sequences_file_path_parents(temporary_multiple_sequences_file)
    multiple_sequences_file_extension_returned = fastasplitter_splitter.splitter \
        .get_multiple_sequences_file_extension(temporary_multiple_sequences_file)
    individual_sequences_name_list_returned = fastasplitter_splitter.splitter \
        .get_individual_sequences_name_list(temporary_multiple_sequences_file)
    individual_sequences_data_list_returned = fastasplitter_splitter.splitter \
        .get_individual_sequences_data_list(temporary_multiple_sequences_file)
    individual_sequences_files_written_count_returned = fastasplitter_splitter.splitter \
        .write_individual_sequences_files(multiple_sequences_file_one_level_above_path_parents_returned,
                                          multiple_sequences_file_extension_returned,
                                          individual_sequences_name_list_returned,
                                          individual_sequences_data_list_returned)
    assert individual_sequences_files_written_count_returned == individual_sequences_files_written_count_expected
    assert sequence1_file_expected.exists()
    assert sequence2_file_expected.exists()
    assert sequence3_file_expected.exists()
    sequence1_file_expected.unlink()
    sequence2_file_expected.unlink()
    sequence3_file_expected.unlink()
    temporary_multiple_sequences_file.unlink()
    temporary_directory_one_level_above.rmdir()


def test_when_multiple_sequences_file_path_is_on_the_same_level_then_write_sequences_path_list_file_to_disk():
    individual_sequences_path_list_file_expected = Path("Sequences_Path_List.txt")
    individual_sequences_files_path_list_file_path_expected = \
        Path.cwd().joinpath(individual_sequences_path_list_file_expected)
    individual_sequences_path_list_file_data_expected = ["Sequence1.fasta", "Sequence2.fasta", "Sequence3.fasta"]
    temporary_multiple_sequences_file = Path("sequences.fasta")
    with open(temporary_multiple_sequences_file, mode="w") as multiple_sequences_file:
        multiple_sequences_file.write(">Sequence1|text1\nAAA\n")
        multiple_sequences_file.write(">Sequence2 |text2\nCCC\n")
        multiple_sequences_file.write(">Sequence3\nGGG\n")
    multiple_sequences_file_same_level_path_parents_returned = fastasplitter_splitter.splitter \
        .get_multiple_sequences_file_path_parents(temporary_multiple_sequences_file)
    multiple_sequences_file_extension_returned = fastasplitter_splitter.splitter \
        .get_multiple_sequences_file_extension(temporary_multiple_sequences_file)
    individual_sequences_name_list_returned = fastasplitter_splitter.splitter \
        .get_individual_sequences_name_list(temporary_multiple_sequences_file)
    individual_sequences_files_path_list_file_path_returned = fastasplitter_splitter.splitter \
        .write_individual_sequences_files_path_list(multiple_sequences_file_same_level_path_parents_returned,
                                                    multiple_sequences_file_extension_returned,
                                                    individual_sequences_name_list_returned)
    assert individual_sequences_files_path_list_file_path_returned \
           == individual_sequences_files_path_list_file_path_expected
    assert individual_sequences_path_list_file_expected.exists()
    individual_sequences_path_list_file_data_returned = []
    with open(individual_sequences_path_list_file_expected, mode="r") as individual_sequences_files_path_list_file:
        for line in individual_sequences_files_path_list_file:
            individual_sequences_path_list_file_data_returned.append(line.strip())
    for index in range(len(individual_sequences_path_list_file_data_returned)):
        assert individual_sequences_path_list_file_data_returned[index] \
               == individual_sequences_path_list_file_data_expected[index]
    individual_sequences_path_list_file_expected.unlink()
    temporary_multiple_sequences_file.unlink()


def test_when_multiple_sequences_file_path_is_one_level_below_then_write_sequences_path_list_file_to_disk():
    individual_sequences_path_list_file_expected = Path("ParentBelow_Sequences_Path_List.txt")
    individual_sequences_files_path_list_file_path_expected = \
        Path.cwd().joinpath(individual_sequences_path_list_file_expected)
    temporary_directory_one_level_below = Path("ParentBelow")
    temporary_directory_one_level_below.mkdir()
    individual_sequences_path_list_file_data_expected = \
        [str(temporary_directory_one_level_below.joinpath("Sequence1.fasta")),
         str(temporary_directory_one_level_below.joinpath("Sequence2.fasta")),
         str(temporary_directory_one_level_below.joinpath("Sequence3.fasta"))]
    temporary_multiple_sequences_file = temporary_directory_one_level_below.joinpath("sequences.fasta")
    with open(temporary_multiple_sequences_file, mode="w") as multiple_sequences_file:
        multiple_sequences_file.write(">Sequence1|text1\nAAA\n")
        multiple_sequences_file.write(">Sequence2 |text2\nCCC\n")
        multiple_sequences_file.write(">Sequence3\nGGG\n")
    multiple_sequences_file_one_level_below_path_parents_returned = fastasplitter_splitter.splitter \
        .get_multiple_sequences_file_path_parents(temporary_multiple_sequences_file)
    multiple_sequences_file_extension_returned = fastasplitter_splitter.splitter \
        .get_multiple_sequences_file_extension(temporary_multiple_sequences_file)
    individual_sequences_name_list_returned = fastasplitter_splitter.splitter \
        .get_individual_sequences_name_list(temporary_multiple_sequences_file)
    individual_sequences_files_path_list_file_path_returned = fastasplitter_splitter.splitter \
        .write_individual_sequences_files_path_list(multiple_sequences_file_one_level_below_path_parents_returned,
                                                    multiple_sequences_file_extension_returned,
                                                    individual_sequences_name_list_returned)
    assert individual_sequences_files_path_list_file_path_returned \
           == individual_sequences_files_path_list_file_path_expected
    assert individual_sequences_path_list_file_expected.is_file()
    individual_sequences_path_list_file_data_returned = []
    with open(individual_sequences_path_list_file_expected, mode="r") as individual_sequences_files_path_list_file:
        for line in individual_sequences_files_path_list_file:
            individual_sequences_path_list_file_data_returned.append(line.strip())
    for index in range(len(individual_sequences_path_list_file_data_returned)):
        assert individual_sequences_path_list_file_data_returned[index] \
               == individual_sequences_path_list_file_data_expected[index]
    individual_sequences_path_list_file_expected.unlink()
    temporary_multiple_sequences_file.unlink()
    temporary_directory_one_level_below.rmdir()


def test_when_multiple_sequences_file_path_is_one_level_above_then_write_sequences_path_list_file_to_disk():
    individual_sequences_path_list_file_expected = Path.cwd() \
        .joinpath(str(Path.cwd().parent)
                  .replace("/", "_").replace("\\", "_").replace(".", "").replace(":", "_").replace("_", "", 1)
                  + str(Path.cwd().suffix) + "_ParentAbove_Sequences_Path_List.txt")
    individual_sequences_files_path_list_file_path_expected = \
        Path.cwd().joinpath(individual_sequences_path_list_file_expected)
    temporary_directory_one_level_above = Path.cwd().parent.joinpath("ParentAbove")
    temporary_directory_one_level_above.mkdir()
    individual_sequences_path_list_file_data_expected = \
        [str(temporary_directory_one_level_above.joinpath("Sequence1.fasta")),
         str(temporary_directory_one_level_above.joinpath("Sequence2.fasta")),
         str(temporary_directory_one_level_above.joinpath("Sequence3.fasta"))]
    temporary_multiple_sequences_file = temporary_directory_one_level_above.joinpath("sequences.fasta")
    with open(temporary_multiple_sequences_file, mode="w") as multiple_sequences_file:
        multiple_sequences_file.write(">Sequence1|text1\nAAA\n")
        multiple_sequences_file.write(">Sequence2 |text2\nCCC\n")
        multiple_sequences_file.write(">Sequence3\nGGG\n")
    multiple_sequences_file_one_level_above_path_parents_returned = fastasplitter_splitter.splitter \
        .get_multiple_sequences_file_path_parents(temporary_multiple_sequences_file)
    multiple_sequences_file_extension_returned = fastasplitter_splitter.splitter \
        .get_multiple_sequences_file_extension(temporary_multiple_sequences_file)
    individual_sequences_name_list_returned = fastasplitter_splitter.splitter \
        .get_individual_sequences_name_list(temporary_multiple_sequences_file)
    individual_sequences_files_path_list_file_path_returned = fastasplitter_splitter.splitter \
        .write_individual_sequences_files_path_list(multiple_sequences_file_one_level_above_path_parents_returned,
                                                    multiple_sequences_file_extension_returned,
                                                    individual_sequences_name_list_returned)
    assert individual_sequences_files_path_list_file_path_returned \
           == individual_sequences_files_path_list_file_path_expected
    assert individual_sequences_path_list_file_expected.is_file()
    individual_sequences_path_list_file_data_returned = []
    with open(individual_sequences_path_list_file_expected, mode="r") as individual_sequences_files_path_list_file:
        for line in individual_sequences_files_path_list_file:
            individual_sequences_path_list_file_data_returned.append(line.strip())
    for index in range(len(individual_sequences_path_list_file_data_returned)):
        assert individual_sequences_path_list_file_data_returned[index] \
               == individual_sequences_path_list_file_data_expected[index]
    individual_sequences_path_list_file_expected.unlink()
    temporary_multiple_sequences_file.unlink()
    temporary_directory_one_level_above.rmdir()


def test_when_execute_split_command_without_sequences_file_path_argument_then_return_exit_error_code_one():
    runner = CliRunner()
    result = runner.invoke(fastasplitter_splitter.splitter.splitter_group, ["split", ""])
    assert result.return_value is None
    assert result.exit_code == 1
    assert result.exc_info[0] == FileNotFoundError
    assert str(result.exception) == "FASTA multiple sequences file not found!"


def test_when_execute_split_command_with_just_sequences_file_path_then_return_successful_exit_code_zero():
    sequence1_file_expected = Path("Sequence1.fasta")
    sequence2_file_expected = Path("Sequence2.fasta")
    sequence3_file_expected = Path("Sequence3.fasta")
    temporary_multiple_sequences_file = Path("sequences.fasta")
    with open(temporary_multiple_sequences_file, mode="w") as multiple_sequences_file:
        multiple_sequences_file.write(">Sequence1|text1\nAAA\n")
        multiple_sequences_file.write(">Sequence2 |text2\nCCC\n")
        multiple_sequences_file.write(">Sequence3\nGGG\n")
    runner = CliRunner()
    result = runner.invoke(fastasplitter_splitter.splitter.splitter_group,
                           ["split", str(temporary_multiple_sequences_file)])
    assert result.return_value is None
    assert result.exit_code == 0
    assert result.exc_info[0] == SystemExit
    assert result.exception is None
    sequence1_file_expected.unlink()
    sequence2_file_expected.unlink()
    sequence3_file_expected.unlink()
    temporary_multiple_sequences_file.unlink()


def test_when_execute_split_command_with_sequences_file_and_generate_list_paths_then_return_successful_exit_code_zero():
    sequence1_file_expected = Path("Sequence1.fasta")
    sequence2_file_expected = Path("Sequence2.fasta")
    sequence3_file_expected = Path("Sequence3.fasta")
    individual_sequences_files_path_list_file_expected = Path("Sequences_Path_List.txt")
    temporary_multiple_sequences_file = Path("sequences.fasta")
    with open(temporary_multiple_sequences_file, mode="w") as multiple_sequences_file:
        multiple_sequences_file.write(">Sequence1|text1\nAAA\n")
        multiple_sequences_file.write(">Sequence2 |text2\nCCC\n")
        multiple_sequences_file.write(">Sequence3\nGGG\n")
    runner = CliRunner()
    result = runner.invoke(fastasplitter_splitter.splitter.splitter_group,
                           ["split", str(temporary_multiple_sequences_file), "--generate-path-list"])
    assert result.return_value is None
    assert result.exit_code == 0
    assert result.exc_info[0] == SystemExit
    assert result.exception is None
    sequence1_file_expected.unlink()
    sequence2_file_expected.unlink()
    sequence3_file_expected.unlink()
    individual_sequences_files_path_list_file_expected.unlink()
    temporary_multiple_sequences_file.unlink()


def test_when_execute_split_command_with_sequences_file_path_and_verbose_then_return_successful_exit_code_zero():
    sequence1_file_expected = Path("Sequence1.fasta")
    sequence2_file_expected = Path("Sequence2.fasta")
    sequence3_file_expected = Path("Sequence3.fasta")
    temporary_multiple_sequences_file = Path("sequences.fasta")
    split_details_message_expected = "Multiple sequences file (source): {0}\n" \
                                     "Number of individual sequences read from source: {1}\n" \
                                     "Number of individual sequences files written to disk: {2}\n" \
                                     "Location of individual sequences files: {3}\n" \
                                     "Individual sequences files path list file: {4}" \
        .format(str(Path.cwd().joinpath(temporary_multiple_sequences_file)), "3", "3", str(Path.cwd()), "None\n")
    with open(temporary_multiple_sequences_file, mode="w") as multiple_sequences_file:
        multiple_sequences_file.write(">Sequence1|text1\nAAA\n")
        multiple_sequences_file.write(">Sequence2 |text2\nCCC\n")
        multiple_sequences_file.write(">Sequence3\nGGG\n")
    runner = CliRunner()
    result = runner.invoke(fastasplitter_splitter.splitter.splitter_group,
                           ["split", str(temporary_multiple_sequences_file), "--verbose"])
    assert result.return_value is None
    assert result.exit_code == 0
    assert result.exc_info[0] == SystemExit
    assert result.exception is None
    assert result.output == split_details_message_expected
    sequence1_file_expected.unlink()
    sequence2_file_expected.unlink()
    sequence3_file_expected.unlink()
    temporary_multiple_sequences_file.unlink()


def test_when_execute_main_function_without_sequences_file_path_argument_then_throws_file_not_found_exception():
    sys.argv = ["", ""]
    with pytest.raises(FileNotFoundError) as pytest_wrapped_e:
        runpy.run_path("fastasplitter_splitter/splitter.py", run_name="__main__")
    assert pytest_wrapped_e.type == FileNotFoundError
    assert str(pytest_wrapped_e.value) == "FASTA multiple sequences file not found!"
