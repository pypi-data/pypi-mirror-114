from namefiles import construct_filename, disassemble_filename, FILENAME_VALIDATOR, \
    FilenameParts
import pytest

def test_construct_filenames():
    resulting_filename = construct_filename(identifier="basename")
    assert resulting_filename == "basename"

    resulting_filename = construct_filename(
        filename_template="{identifier}{sub_id}",
        identifier="A",
        sub_id="TEST",
        extension=".txt"
    )
    assert resulting_filename == "A#TEST"


def test_construct_filename_identifier_exceptions():
    with pytest.raises(ValueError):
        construct_filename()
        construct_filename(idendifier="?")


def test_construct_filename_sub_id_exceptions():
    with pytest.raises(ValueError):
        construct_filename(identifier="a", sub_id="a")
        construct_filename(identifier="a", sub_id="?ABC")
        construct_filename(identifier="a", sub_id="01234")


def test_construct_filename_source_id():
    with pytest.raises(ValueError):
        construct_filename(idendifier="a", source_id="c3po")
        construct_filename(idendifier="a", source_id="?c3po")
        construct_filename(idendifier="a", source_id="A-too-long-entry")


def _compare_disassembling_before_after(filename_to_check):
    """
    This function used disassemble_filename to get all name parts. Afterwards
    the parts are reassembled using construct_filename.

    Raises:
        assertion error if filename_to_check is not equal with the reassembled
        filename, which indicates a wrong filename convention jsonschema or
        wrong code.

    Args:
        filename_to_check(str):
            The filename to disassemble, reassemble and compare with.

    """
    fileparts = disassemble_filename(filename_to_check)
    reassembled_filename = construct_filename(**fileparts)
    assert filename_to_check == reassembled_filename


def test_alot_of_filenames():
    filenames_to_test = [
        "a",
        "a.txt",
        "a.long-context.txt",
        "a#SUB.txt",
        "a#SUB.long-context.txt",
        "an_id#SUB0#export#_0.000E+1_00320.export.txt",
        "a#A#source#_export_0_a_ab_cba.abc.txt"
    ]
    for filename in filenames_to_test:
        _compare_disassembling_before_after(filename)

def test_context_in_filenames():
    """
    >>> test_context_in_filenames()
    """
    test_giver = FilenameParts.disassemble("Zebra.mikes.cage")
    assert test_giver.context == "mikes"
    test_giver = FilenameParts.disassemble("Zebra#ZOO.mikes.cage")
    assert test_giver.context == "mikes"


def test_exceptions_in_disassemble_filename():
    class HasNoSchemaAttribute:
        pass

    with pytest.raises(AttributeError):
        disassemble_filename("test/path.txt", filename_validator=HasNoSchemaAttribute())
