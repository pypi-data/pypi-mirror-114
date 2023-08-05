from typing import List
from pyspark.sql.types import (
    IntegerType,
    StringType,
    StructField,
    StructType,
    BooleanType,
    LongType,
    DoubleType,
    FloatType,
    DataType,
)
from streamstate_utils.structs import SchemaStruct


def _convert_type(avro_type: str) -> DataType:
    avro_type_conversion = {
        "boolean": BooleanType(),
        "int": IntegerType(),
        "long": LongType(),
        "float": FloatType(),
        "double": DoubleType(),
        "string": StringType(),
    }
    return avro_type_conversion[avro_type]


def map_avro_to_spark_schema(fields: List[SchemaStruct]) -> StructType:
    """
    Converts schema defined by list of dictionaries of "name", "type" attributes
    into Spark schema
    ...

    Attributes
    ----------
    fields: List of "Avro schemas"
    """
    return StructType(
        [StructField(field.name, _convert_type(field.type), True) for field in fields]
    )
