import csv
import codecs
from musiio_validate_tsv.utils import clean_data, type_map
import musiio_validate_tsv.exceptions as exceptions

default_fields_config = {
    "audio url": {
        "required": True,
        "clean": False,
        "internal_id": "audio_url"
    },
    "master id": {
        "required": False,
        "internal_id": "customer_track_id"
    },
    "filename": {
        "required": True,
        "internal_id": "customer_filename"
    },
    "primary track id": {
        "required": False,
        "internal_id": "primary_customer_track_id"
    },
    "version": {
        "required": False,
        "internal_id": "version"
    },
    "title": {
        "required": False,
        "internal_id": "title"
    },
    "album": {
        "required": False,
        "internal_id": "album"
    },
    "artist": {
        "required": False,
        "internal_id": "artist"
    },
    "year": {
        "required": False,
        "internal_id": "year"
    },
    "region": {
        "required": False,
        "internal_id": "region"
    },
    "language": {
        "required": False,
        "internal_id": "language"
    },
    "explicit": {
        "required": False,
        "internal_id": "explicit",
        "map_values": {
            "Yes": 1,
            "No": 0,
            "1": 1,
            "0": 0,
            "True": 1,
            "False": 0
        }
    },
    "genre": {
        "required": False,
        "internal_id": "genres"
    },
    "moods": {
        "required": False,
        "internal_id": "moods"
    },
    "style": {
        "required": False,
        "internal_id": "style"
    },
    "instruments": {
        "required": False,
        "internal_id": "instruments"
    },
    "description": {
        "required": False,
        "internal_id": "description"
    },
    "keywords": {
        "required": False,
        "internal_id": "keywords"
    },
    "related ids": {
        "required": False,
        "internal_id": "related_ids"
    }
}


class ValidateTSV:
    def __init__(self, fields_config=None):
        self.fields_config = fields_config if fields_config is not None else default_fields_config

    def __get_field_index_map(self, header, custom_fields):
        """

        :param header: array - list of columns
        :param custom_fields: dict - A dictionary containing a mapping of custom columns that are present and their
        corresponding configuration
        :return: dict - A dictionary containing a mapping of column names to the indexes of the columns
        """
        field_index_map = {}

        for idx, field in enumerate(header):
            field_name = field.lower()
            if field_name in self.fields_config or field_name in custom_fields:
                field_index_map[field_name] = idx

        return field_index_map

    def process_row(self, field_index_map, row, custom_fields):
        """
        Process a single row of a tsv and return the data in dictionary. Throws an error if there is any error in the data
        :param field_index_map: dict - A dictionary containing a mapping of column names to the indexes of the columns
        :param row: array - A list containing the data for the columns
        :param custom_fields: dict - A dictionary containing a mapping of custom columns that are present and their
        corresponding configuration
        :return: dict - A mapping containing the columns and the row data
        """
        processed_row = {}
        aggregate_fields = {**self.fields_config, **custom_fields}
        for field in aggregate_fields:
            if field in field_index_map:
                column_index = field_index_map[field]
                if column_index >= len(row):
                    error = "Column {} not present for row. Please check for missing data in row.".format(field)
                    raise exceptions.TSVColumnUnsetError(error)

                data = row[column_index]

                if aggregate_fields[field]["required"] and not data:
                    error = "Missing required field : {}".format(field)
                    raise exceptions.TSVMissingRequiredFieldError(error)

                if aggregate_fields[field].get("clean", True):
                    data = clean_data(text=data)

                field_type = aggregate_fields[field].get("type", None)
                if field_type:
                    if field_type in type_map:
                        try:
                            multiple = True if field in custom_fields else False
                            data = type_map[field_type](data, multiple)
                        except:
                            if data is None or data.strip() == "":
                                continue
                            error = "Invalid field value for type: {} field: {}".format(field_type, field)
                            raise exceptions.TSVInvalidFieldValueError(error)
                    else:
                        error = "Invalid field type: {} for field: {}".format(field_type, field)
                        raise exceptions.TSVInvalidFieldTypeError(error)

                internal_id = aggregate_fields[field]['internal_id']
                if field in custom_fields:
                    if "custom_properties" not in processed_row:
                        processed_row["custom_properties"] = {}

                    processed_row["custom_properties"][internal_id] = data
                else:
                    if data.strip() == "":
                        continue
                    map_values = aggregate_fields[field].get("map_values", None)
                    if map_values:
                        if data in map_values:
                            data = map_values[data]
                        else:
                            error = "Invalid field value for field: {} Supported values: {}".format(field,
                                                                                                    list(map_values.keys()))
                            raise exceptions.TSVInvalidFieldValueError(error)
                    processed_row[internal_id] = data

            elif aggregate_fields[field]["required"]:
                error = "Missing required field : {}".format(field)
                raise exceptions.TSVMissingRequiredFieldError(error)

        return processed_row

    def process_tsv(self, tsv_file_path, custom_fields=None, max_errors=10):
        """
        Process the tsv at the path and return list containing a mapping of the row data. If errors are present,
        then return a list of errors.
        :param tsv_file_path: string - The path to the tsv file
        :param custom_fields: dict -  A dictionary containing a mapping of custom columns that are present and their
        corresponding configuration
        :param max_errors: int - The maximum number of errors to be returned
        :return: tuple - Returns a tuple (errors, processed_data). The errors are list of errors for each row that
        failed. If no errors it is set to None. The processed_data is a list of dictionaries containing the data
        for each row. If there are errors, this is set to None.
        """
        if custom_fields is None:
            custom_fields = {}

        with codecs.open(tsv_file_path, "r", encoding="utf-8") as f:
            reader = csv.reader(f, delimiter="\t", quoting=csv.QUOTE_NONE)
            header = next(reader, None)
            no_of_columns = len(header)

            field_index_map = self.__get_field_index_map(header, custom_fields=custom_fields)
            processed_rows = []
            errors = []
            # Set row number to 2 as header row is row 1 in the file
            row_number = 2

            for row in reader:
                processed_row = None
                error = None
                try:
                    if no_of_columns != len(row):
                        raise exceptions.TSVInconsistentColumnRowError(
                            "Invalid Row - The number of items in the row: {} do not match the number of columns: {}. "
                            "Can you please check the row for missing/additional items "
                            "or missing/additional tabs.".format(len(row), no_of_columns))
                    processed_row = self.process_row(field_index_map=field_index_map, row=row,
                                                      custom_fields=custom_fields)
                except exceptions.TSVException as tsv_exception:
                    error = tsv_exception.message
                except Exception:
                    error = "Unexpected error for row."

                if error is not None:
                    errors.append({
                        'row_number': row_number,
                        'error_message': error
                    })
                else:
                    processed_rows.append(processed_row)

                if len(errors) == max_errors:
                    break

                row_number += 1

            if len(errors) > 0:
                return errors, None

            return None, processed_rows












