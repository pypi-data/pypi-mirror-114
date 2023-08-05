from typing import List, Callable
from pyspark.sql import SparkSession, DataFrame
import shutil
import os
from streamstate_utils.generic_wrapper import dev_file_wrapper
from streamstate_utils.structs import InputStruct
import json
import sys


def helper_for_file(
    app_name: str,
    max_file_age: str,
    base_folder: str,
    process: Callable[[List[DataFrame]], DataFrame],
    inputs: List[InputStruct],
    spark: SparkSession,
    expecteds: List[dict],
):
    """
    This will be used for unit testing developer code
    Major inputs:

    process is the logic for manipulating streaming dataframes
    inputs is a list of "topic" names, example records from topic, and schema for topic
    expecteds is a list of expected output
    """
    file_dir = app_name
    try:
        shutil.rmtree(file_dir)
        print("folder exists, deleting")
    except:
        print("folder doesn't exist, creating")

    os.mkdir(file_dir)
    for input in inputs:
        os.mkdir(os.path.join(file_dir, input.topic))

    df = dev_file_wrapper(
        app_name,
        max_file_age,
        base_folder,
        process,
        inputs,
        spark,
    )
    file_name = "localfile.json"

    for input in inputs:
        file_path = os.path.join(file_dir, input.topic, file_name)
        with open(file_path, mode="w") as test_file:
            json.dump(input.sample, test_file)
    q = df.writeStream.format("memory").queryName(app_name).outputMode("append").start()
    try:
        assert q.isActive
        q.processAllAvailable()
        df = spark.sql(f"select * from {app_name}")
        result = df.collect()
        assert len(result) == len(expecteds)
        for row in result:
            dict_row = row.asDict()
            print(dict_row)
            assert dict_row in expecteds, f"{dict_row} is not in {expecteds}"
    finally:
        q.stop()
        shutil.rmtree(file_dir)


def main():

    [_name, current_path, path_to_inputs, path_to_outputs] = sys.argv
    # input_schema = marshmallow_dataclass.class_schema(InputStruct)()
    sys.path.append(current_path)
    from process import process  # type: ignore

    with open(path_to_inputs) as f:
        inputs = [InputStruct(**v) for v in json.load(f)]
    with open(path_to_outputs) as f:
        outputs = json.load(f)
    spark = SparkSession.builder.master("local").appName("tests").getOrCreate()
    helper_for_file(
        "testprocess", "2d", ".", process, inputs, spark, outputs  # type: ignore
    )
