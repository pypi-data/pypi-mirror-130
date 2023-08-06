"""Convenient library for data statistics generation."""

import os
import tempfile
import uuid
from typing import Dict, List, Optional, Tuple

import apache_beam as beam
import tensorflow as tf
from apache_beam.io import ReadFromBigQuery
from apache_beam.io import WriteToTFRecord
from apache_beam.options.pipeline_options import PipelineOptions
from data_validation.utils import utils
from data_validation.utils.bigquery_utils import BigQueryConverter
from tensorflow_data_validation import generate_statistics_from_tfrecord
from tensorflow_data_validation.statistics import stats_options as options
from tensorflow_metadata.proto.v0 import statistics_pb2


# TODO: implement generate_statistics_from_orc

def generate_statistics_from_arvo(
    input_file_pattern: str,
    output_path: Optional[str] = None,
    export_path: Optional[str] = None,
    sample_rate: Optional[float] = None,
    nested_fields_config: Optional[Dict[str, List[Tuple[str, str]]]] = None,
    stats_options: options.StatsOptions = options.StatsOptions(),
    pipeline_options: Optional[PipelineOptions] = None,
) -> statistics_pb2.DatasetFeatureStatisticsList:
  """Compute data statistics from Avro file(s).

  Runs a Beam pipeline to compute the data statistics and return the result
  data statistics proto.

  This is a convenience method for users with data stored in Avro format.

  Args:
    input_file_pattern: The file pattern that points to a set of Avro file(s).
    output_path: optional. The file path to output data. If None, we use a
      temporary directory. It will be a TFRecord file containing a single data
      statistics proto, and can be read with the 'load_statistics' API.
      If you run this function on Google Cloud, you must specify an output_path.
      Specifying None may cause an error.
    export_path: optional. The file path to tfrecord file converted from
      Avro file(s).
    sample_rate: optional. The sample rate, over which the statistics is
      computed. If it is set, it overrides sample_rate in stat options.
    nested_fields_config: optional. Declared the fields containing nested value.
     The key is the name of the field. The value is in form of list of tuple,
     in which the first value is used as a key, and the second value is used as
     the value.
    stats_options: optional. `tfdv.StatsOptions` for generating data statistics.
    pipeline_options: optional. Optional beam pipeline options. This allows
      users to specify various beam pipeline execution parameters like pipeline
      runner (DirectRunner or DataflowRunner), cloud dataflow service
      project id, etc.
      See https://cloud.google.com/dataflow/pipelines/specifying-exec-params for
      more details.

  Returns:
    A DatasetFeatureStatisticsList proto.
  """
  output_path, export_path = _validate_path(output_path, export_path)

  if sample_rate:
    stats_options.sample_rate = sample_rate

  # Generate random id for the export folder
  _id = str(uuid.uuid4())

  # Read data from Avro file(s) and convert to TFRecord format
  with beam.Pipeline(options=pipeline_options) as p:
    pcoll = (
        p
        | 'ReadFromAvro' >> beam.io.ReadFromAvro(input_file_pattern)
    )
    if not nested_fields_config:
      pcoll = pcoll | 'ToTFExample' >> beam.Map(utils.dict_to_example)
    else:
      pcoll = pcoll | 'ToTFExample' >> beam.Map(utils.dict_to_example,
                                                nested_fields_config=nested_fields_config)
    pcoll \
    | 'SerializeProto' >> beam.Map(lambda x: x.SerializeToString()) \
    | 'ToTFRecord' >> WriteToTFRecord(
        file_path_prefix=f"{export_path}/{_id}/Features",
        file_name_suffix='.tfrecord.gz')

  data_location = f'{export_path}/{_id}/*.tfrecord.gz'
  stats = generate_statistics_from_tfrecord(
      data_location,
      output_path,
      stats_options,
      pipeline_options)
  return stats


def generate_statistics_from_parquet(
    input_file_pattern: str,
    output_path: Optional[str] = None,
    export_path: Optional[str] = None,
    nested_fields_config: Optional[Dict[str, List[Tuple[str, str]]]] = None,
    stats_options: options.StatsOptions = options.StatsOptions(),
    pipeline_options: Optional[PipelineOptions] = None,
) -> statistics_pb2.DatasetFeatureStatisticsList:
  """Compute data statistics from Parquet file(s).

  Runs a Beam pipeline to compute the data statistics and return the result
  data statistics proto.

  This is a convenience method for users with data stored in Parquet format.

  Args:
    input_file_pattern: The file pattern that points to a set of Parquet file(s).
    output_path: optional. The file path to output data. If None, we use a
      temporary directory. It will be a TFRecord file containing a single data
      statistics proto, and can be read with the 'load_statistics' API.
      If you run this function on Google Cloud, you must specify an output_path.
      Specifying None may cause an error.
    export_path: The file path to tfrecord file converted from Parquet file(s).
    nested_fields_config: optional. Declared the fields containing nested value.
      The key is the name of the field. The value is in form of list of tuple,
      in which the first value is used as a key, and the second value is used as
      the value
    stats_options: optional. `tfdv.StatsOptions` for generating data statistics.
    pipeline_options: optional. Optional beam pipeline options. This allows
      users to specify various beam pipeline execution parameters like pipeline
      runner (DirectRunner or DataflowRunner), cloud dataflow service
      project id, etc.
      See https://cloud.google.com/dataflow/pipelines/specifying-exec-params for
      more details.

  Returns:
    A DatasetFeatureStatisticsList proto.
  """
  output_path, export_path = _validate_path(output_path, export_path)

  # Generate random id for the export folder
  _id = str(uuid.uuid4())

  # Read data from Avro file(s) and convert to TFRecord format
  with beam.Pipeline(options=pipeline_options) as p:
    pcoll = (
        p
        | 'ReadFromParquet' >> beam.io.ReadFromParquet(input_file_pattern)
    )
    if not nested_fields_config:
      pcoll = pcoll | 'ToTFExample' >> beam.Map(utils.dict_to_example)
    else:
      pcoll = pcoll | 'ToTFExample' >> beam.Map(utils.dict_to_example,
                                                nested_fields_config=nested_fields_config)
    pcoll \
    | 'SerializeProto' >> beam.Map(lambda x: x.SerializeToString()) \
    | 'ToTFRecord' >> WriteToTFRecord(
        file_path_prefix=f"{export_path}/{_id}/Features",
        file_name_suffix='.tfrecord.gz')

  data_location = f'{export_path}/{_id}/*.tfrecord.gz'
  stats = generate_statistics_from_tfrecord(
      data_location,
      output_path,
      stats_options,
      pipeline_options)
  return stats


def generate_statistics_from_bigquery(
    table_spec: Optional[str] = None,
    query: Optional[str] = None,
    output_path: Optional[str] = None,
    export_path: Optional[str] = None,
    stats_options: options.StatsOptions = options.StatsOptions(),
    pipeline_options: Optional[PipelineOptions] = None,
) -> statistics_pb2.DatasetFeatureStatisticsList:
  """Compute data statistics from BigQuery table or explicit query.

  Runs a Beam pipeline to compute the data statistics and return the result
  data statistics proto.

  This is a convenience method for users with data can be queried from BigQuery.

  Args:
    table_spec: The fully-qualified BigQuery table name. E.g:
      clouddataflow-readonly:samples.weather_stations
    query: The query to be executed in BigQuery.
    output_path: optional. The file path to output data. If None, we use a
      temporary directory. It will be a TFRecord file containing a single data
      statistics proto, and can be read with the 'load_statistics' API.
      If you run this function on Google Cloud, you must specify an output_path.
      Specifying None may cause an error.
    export_path: The file path to the tfrecord file converted from the queried
      data.
    stats_options: optional. `tfdv.StatsOptions` for generating data statistics.
    pipeline_options: optional. Optional beam pipeline options. This allows
      users to specify various beam pipeline execution parameters like pipeline
      runner (DirectRunner or DataflowRunner), cloud dataflow service
      project id, etc.
      See https://cloud.google.com/dataflow/pipelines/specifying-exec-params for
      more details.

  Returns:
    A DatasetFeatureStatisticsList proto.

  Raises:
    RuntimeError: Only one of query and input_config should be set.
    RuntimeError: One of table_spec and query should be set.
  """
  if table_spec and query:
    raise RuntimeError('Only one of table_spec and query should be set.')

  if not table_spec and not query:
    raise RuntimeError('One of table_spec and query should be set.')

  output_path, export_path = _validate_path(output_path, export_path)

  # Generate random id for the export folder
  _id = str(uuid.uuid4())

  with beam.Pipeline(options=pipeline_options) as p:
    if table_spec:
      pcoll = p | 'ReadFromBigQuery' >> ReadFromBigQuery(
          table_spec=table_spec)
    elif query:
      pcoll = p | 'ReadFromBigQuery' >> ReadFromBigQuery(query=query)
    (pcoll
     | 'ToTFExample' >> beam.Map(BigQueryConverter(query).RowToExample)
     | 'SerializeProto' >> beam.Map(lambda x: x.SerializeToString())
     | 'ToTFRecord' >> WriteToTFRecord(
            file_path_prefix=f"{export_path}/{_id}/data",
            file_name_suffix='.tfrecord.gz'))

  # Generate statistics from TFRecords
  data_location = f'{export_path}/{_id}/*.tfrecord.gz'
  stats = generate_statistics_from_tfrecord(
      data_location,
      output_path,
      stats_options,
      pipeline_options)

  return stats


def _validate_path(output_path, export_path):
  """ Validate whether output path and export path exist. If not return
  the generated one(s)."""
  if output_path is None:
    output_path = os.path.join(tempfile.mkdtemp(), 'FeatureStats.tfrecord')
  output_dir_path = os.path.dirname(output_path)
  if not tf.io.gfile.exists(output_dir_path):
    tf.io.gfile.makedirs(output_dir_path)
  if export_path is None:
    export_path = tempfile.mkdtemp()
  if not tf.io.gfile.exists(export_path):
    tf.io.gfile.makedirs(export_path)
  return output_path, export_path
