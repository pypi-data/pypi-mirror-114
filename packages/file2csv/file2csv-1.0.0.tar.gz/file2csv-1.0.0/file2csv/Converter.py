import json
from enum import Enum, unique
from os.path import abspath, exists
from concurrent.futures import ThreadPoolExecutor


@unique
class Encodings(Enum):
    """
      Python encodings
      ascii()
      bin()
      bytes()
      chr()
      hex()
      int()
      oct()
      ord()
      str()  
    """
    UTF8 = 'utf-8'
    UTF16 = 'utf-16'
    UTF32 = 'utf-32'
    ASCII = 'ascii'
    BINARY = 'binary'
    OCTAL = 'octal'
    HEXADECIMAL = 'hexadecimal'
    CP1252 = 'cp1252'
    WINDOWS1252 = 'windows-1252'
    UNICODEESCAPE = 'unicode-escape'


class Converter(object):
    # def __init__(self, fixedfile, csvfile):
    def __init__(self, **kwargs):
        """ Converter(fixedfile=None, csvfile=None, columns=None)
                The Converter class.
                Please always use *kwargs* in the constructor.
                - *fixedfile*: Pass the input file name
                - *csvfile*: Pass the output file name
                - *specfile*: columns configuration
                """
        super(Converter, self).__init__()
        self._fixedfile = kwargs.get("fixedfile", None)
        self._csvfile = kwargs.get("csvfile", None)
        self._specfile = kwargs.get("specfile", None)
        self._columns = []
        self._offsets = []
        self._fixed_with_encoding = 'windows-1252'
        self._included_header = False
        self._delimited_encoding = 'utf-8'

    def __str__(self):
        return f'Input file name is "{self._fixedfile}", File format specification is "{self._specfile}", and output file name is "{self._csvfile}"'

    def __repr__(self):
        return f'Converter(fixedfile="{self._fixedfile}", csvfile="{self._csvfile}", specfile="{self._specfile}")'

    def encoder_spec(self):
        def get_metadata(spec_file: str) -> tuple[bool, list[str], list[int], str, bool, str]:
            """
              spec for columns
              ----------------

              {
              "ColumnNames": [
                  "f1",
                  "f2",
                  "f3",
                  "f4",
                  "f5",
                  "f6",
                  "f7",
                  "f8",
                  "f9",
                  "f10"
              ],
              "Offsets": [
                  "5",
                  "12",
                  "3",
                  "2",
                  "13",
                  "7",
                  "10",
                  "13",
                  "20",
                  "13"
              ],
              "FixedWidthEncoding": "windows-1252",
              "IncludeHeader": "True",
              "DelimitedEncoding": "utf-8"
            }
            """
            parsed = False
            columns = []
            offsets = []
            fixed_with_encoding = "windows-1252"
            included_header = True
            delimited_encoding = "utf-8"

            def result() -> tuple[bool, list[str], list[int], str, bool, str]:
                return (parsed, columns, offsets, fixed_with_encoding, included_header, delimited_encoding)

            if spec_file == None:
                return result()

            # read spec file
            f_path = abspath(spec_file)
            if not exists(f_path):
                print(f"The spec file {f_path} does not exist")
                parsed = False
                return result()

            with open(f_path, 'r') as specfile:
                data = specfile.read()

            # parse spec file content
            obj = json.loads(data)

            try:
                columns = obj['ColumnNames']
                if len(columns) == 0:
                    parsed = False
                    return result()
            except Exception as ex:
                print(f"Error in parsing ColumnNames: {str(ex)}")
                parsed = False
                return result()

            try:
                offsets = [int(offset) for offset in obj['Offsets']]
                if len(offsets) == 0:
                    parsed = False
                    return result()
            except Exception as ex:
                print(f"Error in parsing Offsets: {str(ex)}")
                parsed = False
                return result()

            try:
                fixed_with_encoding = obj['FixedWidthEncoding']
            except Exception as ex:
                print(f"Error in parsing FixedWidthEncoding: {str(ex)}")
                parsed = False
                return result()

            parsed = True
            return result()

        (parsed, columns, offsets, fixed_with_encoding, included_header,
         delimited_encoding) = get_metadata(self._specfile)
        result = (parsed, columns, offsets, fixed_with_encoding,
                  included_header, delimited_encoding)
        if not parsed:
            return result
        self._offsets = offsets
        self._fixed_with_encoding = fixed_with_encoding
        self._included_header = included_header
        self._delimited_encoding = delimited_encoding
        return result

    def encode(self):
        """
        spec for columns
        ----------------

        {
        "ColumnNames": [
            "f1",
            "f2",
            "f3",
            "f4",
            "f5",
            "f6",
            "f7",
            "f8",
            "f9",
            "f10"
        ],
        "Offsets": [
            "5",
            "12",
            "3",
            "2",
            "13",
            "7",
            "10",
            "13",
            "20",
            "13"
        ],
        "FixedWidthEncoding": "windows-1252",
        "IncludeHeader": "True",
        "DelimitedEncoding": "utf-8"
      }
        """
        pass
