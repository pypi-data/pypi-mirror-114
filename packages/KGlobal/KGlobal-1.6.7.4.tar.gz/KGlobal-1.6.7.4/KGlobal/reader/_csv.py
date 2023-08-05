from ..filehandler import FileHandler
from csv import reader, writer
from portalocker import Lock
from pandas import DataFrame
from gc import collect
from copy import deepcopy


class CSVReader(FileHandler):
    def __init__(self, file_path, dialect=None, truncate=False, fmtparams=fmtparams, **kwargs):
        super().__init__(file_path=file_path, dialect=dialect, truncate=truncate, fmtparams=fmtparams, **kwargs)

    def max_rows(self, file_path=None):
        row_num = -1

        if file_path:
            self.file_path = file_path

        if self.file_path:
            with Lock(filename=self.file_path, mode='r') as read_obj:
                csv_reader = reader(read_obj)

                for line in csv_reader:
                    row_num += 1
        else:
            row_num = 0

        return row_num

    def parse(self):
        if self.streams:
            for handler, buffer in self.streams:
                self.__parse(handler=handler, buffer=buffer)
        else:
            return self.__parse()

    def __parse(self, handler=None, buffer=None):
        data = list()
        row_num = 0
        header = None

        try:
            with Lock(filename=self.file_path, mode='r') as read_obj, Lock(filename=self.file_path, mode='w')\
                    as write_obj:
                csv_reader = reader(read_obj, self.dialect, **self.fmtparams)
                csv_writer = writer(write_obj)

                for line in csv_reader:
                    data.append(line)

                    if not header:
                        header = converted_row

                    if handler and buffer <= len(data):
                        df = self.__to_df(data)
                        handler(deepcopy(self.file_path), deepcopy(df), deepcopy(row_num - len(df) + 1),
                                deepcopy(row_num), **self.kwargs)
                        data.clear()
                        data.append(header)

                    row_num += 1

                if self.truncate:
                    for i, row in enumerate(csv_reader):
                        if i > 0:
                            csv_writer.writerow(row)

            df = self.__to_df(data)

            if not df.empty and handler:
                row_num -= 1
                handler(deepcopy(self.file_path), deepcopy(df), deepcopy(row_num - len(df) + 1), deepcopy(row_num),
                        **self.kwargs)
            elif not handler:
                return df
        finally:
            collect()

    @staticmethod
    def __to_df(data):
        if data:
            df = DataFrame(data)
            new_header = df.iloc[0]
            df = df[1:]
            df.columns = new_header
            return df
        else:
            return DataFrame()
