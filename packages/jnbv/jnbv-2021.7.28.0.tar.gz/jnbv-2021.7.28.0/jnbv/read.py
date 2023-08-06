import logging
import nbformat
import os

from .utils import (
    BLUE,
    CYAN,
    LIGHTPURPLE,
    NC,
    RED,
    YELLOW,
    from_nbnode,
    print_cropped_output,
)


def read_ipynb(path, quiet, debug):

    if not quiet:
        print("")
        print(LIGHTPURPLE, "*".center(80, "*"), NC)
        print(LIGHTPURPLE, "Reading output notebook", NC, path)
        print("")

        logging.info("Reading " + str(path))

    nb = []
    errors = []

    # Check if the file exists and is accessible
    if not os.access(path, os.R_OK):
        error_message = "FILE NOT ACCESSIBLE"
        not quiet and print(RED, error_message, NC)
        errors.append(error_message)

    else:
        # Read the notebook
        nb = nbformat.read(path, nbformat.current_nbformat)

        # Loop over cells, look for errors
        for cell in nb.cells:
            debug and print(cell)

            # Skip some types of cells
            if "cell_type" in cell:
                if cell["cell_type"] == "markdown":
                    debug and print(YELLOW, "skipping cell_type:",
                                    cell["cell_type"], NC)
                    continue

            if not quiet and "source" in cell and "cell_type" in cell:
                if cell["cell_type"] == "code" and cell["source"] != "":
                    logging.info("cell source: " + str(cell["source"]))
                    print(BLUE, "-".center(80, "-"), NC)
                    print(BLUE, "source: ", NC, cell["source"])

            errors = print_cell_output(cell, quiet, errors)

    if not quiet:
        logging.info("Done reading " + str(path))

        print(LIGHTPURPLE, "Done reading")
        print(LIGHTPURPLE, "*".center(80, "*"), NC)
        print("")

    if debug and nb != []:
        nb_dict = from_nbnode(nb)
        print(nb_dict)

    return nb, errors


def print_cell_output(cell, quiet, errors):

    if "outputs" in cell:
        COLOR = CYAN

        if len(cell["outputs"]) == 0:

            if not quiet:
                print(COLOR, "cell output: ", str(cell["outputs"]), NC)
                logging.info("cell output: " + str(cell["outputs"]))
                print(BLUE, "-".center(80, "-"), NC)
                print("")
        else:
            for output in cell["outputs"]:

                # Search for errors in the output
                if output.output_type == "error":
                    errors.append(output)
                    logging.error("cell output: " + str(output))
                    COLOR = RED
                else:
                    logging.info("cell output: " + str(output))

                if not quiet:
                    print(COLOR, "cell output: ", NC)
                    print_cropped_output(output)

            if not quiet and len(cell["outputs"]) > 0:
                print(BLUE, "-".center(80, "-"), NC)
                print("")

    return errors
