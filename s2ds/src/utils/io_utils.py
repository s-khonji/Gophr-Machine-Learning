# input/output utility functions

def read_file_as_string(query_file_path):
    """reads and returns file at given file path as string

    Parameters:
    query_file_path (str): path to file

    Returns:
    str: read string
    """

    file = open(query_file_path, mode = 'r')
    string = file.read()
    file.close()

    return string
