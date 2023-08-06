"""
Generates the default configuration for all sections.
"""
import configparser
import socket


def set_defaults():
    """
    Generates the default configuration for all sections.
    :return: configparser.ConfigParser object
    """

    config = configparser.ConfigParser(allow_no_value=True)

    common = {
        'csv_import_folder': '',
        'csv_export_folder': '',
        # Export headers you want, those missing in the import will be added 
        # with empty data.        
        'csv_export_headers': ('Series_reference', 'Period', 'ELEE'),
        'csv_delimiter': ';',
        # Options: https://docs.python.org/3.5/library/codecs.html#text-encodings
        # use mbcs for ansi on python prior 3.6
        'csv_encoding': 'utf-8',
        # You can use column types, like int64, np.float64 if you want to specify
        # Or you can use type object if you don't want conversion or avoid NaN errors
        # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_csv.html
        # example: {'column name': 'object'}
        'dtype': {}
    }

    config['common'] = common

    return config
