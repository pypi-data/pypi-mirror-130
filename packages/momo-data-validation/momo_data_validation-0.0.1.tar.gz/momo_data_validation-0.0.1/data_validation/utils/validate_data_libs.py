from typing import Any, Dict, List, Optional, Tuple

import tensorflow_data_validation as tfdv
from apache_beam.options.pipeline_options import PipelineOptions
from data_validation.utils.stats_gen_libs import generate_statistics_from_arvo, \
  generate_statistics_from_parquet
from tensorflow_data_validation.statistics import stats_options as options
from tensorflow_metadata.proto.v0 import schema_pb2


def validate_data_from_gcs(
    input_file_pattern: str,
    output_path: str,
    export_path: str,
    file_extension: str,
    nested_fields_config: Optional[Dict[str, List[Tuple[str, str]]]] = None,
    schema: Optional[schema_pb2.Schema] = None,
    schema_location: Optional[str] = None,
    original_stats_location: Optional[str] = None,
    drift_options: Optional[Dict[str, Any]] = None,
    skew_options: Optional[Dict[str, Any]] = None,
    stats_options: options.StatsOptions = options.StatsOptions(),
    pipeline_options: Optional[PipelineOptions] = None,
) -> Tuple[Any, Any, Any, Any]:
  """Validate data from GCS against schema and detect anomalies,
  including skew and drift.

  Args:
    input_file_pattern: The glob file pattern that points to a set of file(s).
    output_path: The file path to the generated statistics proto.
    export_path: The file path to the tfrecord file converted from the data.
    file_extension: The file extensions of the input data. Currently support
      Avro and Parquet.
    nested_fields_config: optional.
    schema: optional. The schema proto object.
    schema_location: optional. The path to the schema proto.
    original_stats_location: optional.
    drift_options: optional. The options to register features for detecting
      drift anomalies.
    skew_options: optional. The options to register features for detecting skew
      anomalies.
    stats_options: optional. `tfdv.StatsOptions` for generating data statistics.
    pipeline_options: optional. Optional beam pipeline options. This allows
      users to specify various beam pipeline execution parameters like pipeline
      runner (DirectRunner or DataflowRunner), cloud dataflow service
      project id, etc.
      See https://cloud.google.com/dataflow/pipelines/specifying-exec-params for
      more details.

  Returns:
    A statistics proto, schema anomalies, skew anomalies, and drift anomalies
  """

  stats = None
  if file_extension == "avro":
    stats = generate_statistics_from_arvo(
        input_file_pattern=input_file_pattern,
        output_path=output_path,
        export_path=export_path,
        nested_fields_config=nested_fields_config,
        stats_options=stats_options,
        pipeline_options=pipeline_options
    )
  elif file_extension == "parquet":
    stats = generate_statistics_from_parquet(
        input_file_pattern=input_file_pattern,
        output_path=output_path,
        export_path=export_path,
        stats_options=stats_options,
        pipeline_options=pipeline_options
    )

  assert stats is not None
  schema_anomalies = None
  skew_anomalies = None
  drift_anomalies = None
  if schema or schema_location:
    original_schema = schema if schema else tfdv.load_schema_text(
        schema_location)
    schema_anomalies = tfdv.validate_statistics(stats, original_schema)
    if original_stats_location:
      original_stats = tfdv.load_statistics(original_stats_location)
      schema = _setup_feature(original_schema, skew_options=skew_options,
                              drift_options=drift_options)
      skew_anomalies = tfdv.validate_statistics(
          statistics=original_stats,
          schema=schema,
          serving_statistics=stats)

      drift_anomalies = tfdv.validate_statistics(
          statistics=original_stats,
          schema=schema,
          previous_statistics=stats)
  return stats, schema_anomalies, skew_anomalies, drift_anomalies


def _setup_feature(
    schema: schema_pb2.Schema,
    skew_options: Optional[Dict[str, Any]] = None,
    drift_options: Optional[Dict[str, Any]] = None,
) -> schema_pb2.Schema:
  """Configure feature to detect drift and skew anomalies.

  Args:
    schema:
    skew_options:
    drift_options:

  Returns:
    A schema_pb2.Schema proto.
  """
  if skew_options:
    for k, v in skew_options:
      tfdv.get_feature(schema,
                       k).skew_comparator.infinity_norm.threshold = v
  if drift_options:
    for k, v in drift_options:
      tfdv.get_feature(schema,
                       k).drift_comparator.infinity_norm.threshold = v
  return schema


def validate_data_from_bigquery():
  """Validate data from Bigquery."""
  pass
