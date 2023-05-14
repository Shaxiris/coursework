import programs.main as main
import pytest


def test_main_correct():
    assert main.main() is None


def test_main_incorrect_path():
    main.PATH = "operations.json"
    with pytest.raises(FileNotFoundError):
        main.main()


def test_main_break():
    main.PATH = "sources/reduced_for_test.json"
    assert main.main() is None