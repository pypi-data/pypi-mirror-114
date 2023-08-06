import logging

from .read import read_ipynb
from .utils import GREEN, LIGHTPURPLE, NC, RED


def assert_no_errors(errors):
    assert errors == [] or errors is None


def test_ipynb(notebook_filename, debug):

    # First read the ipynb notebook into a python dictionary
    nb, errors = read_ipynb(notebook_filename, True, debug)

    print("")
    print(LIGHTPURPLE, "*".center(80, "*"), NC)
    print(LIGHTPURPLE, "Testing output notebook:\n", NC, notebook_filename)

    # Check for errors
    logging.info("Testing output notebook" + str(notebook_filename))

    test_result = False
    try:
        test_result = assert_no_errors(errors)
        test_result = True
    except AssertionError as e:
        print("")
        print(RED, "AssertionError", NC)
        print(e)
        logging.error("AssertionError")
        logging.error(e)
    except BaseException as e:
        print("")
        print(RED, "Unknown error", NC)
        print(e)
        logging.error("Unknown error")
        logging.error(e)

    # Print final result
    COLOR = GREEN if test_result else RED
    print(COLOR, "-".center(80, "-"))
    print(COLOR, " test result: " + str(test_result))
    print(COLOR, "-".center(80, "-"), NC)

    # Log results
    logging.info("test result: " + str(test_result))
    logging.info("Done testing " + str(notebook_filename))

    print(LIGHTPURPLE, "Done testing")
    print(LIGHTPURPLE, "*".center(80, "*"), NC)
    print("")

    return test_result
