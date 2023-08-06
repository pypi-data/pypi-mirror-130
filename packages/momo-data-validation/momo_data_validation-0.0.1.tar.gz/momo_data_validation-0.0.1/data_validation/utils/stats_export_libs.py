"""Convenient library for export statistics data."""

from datetime import datetime
from typing import Optional

import pandas as pd
import tensorflow_data_validation as tfdv
from data_validation.utils.utils import stats_proto_to_df
from google.cloud import bigquery
from tensorflow_metadata.proto.v0 import schema_pb2
from tensorflow_metadata.proto.v0 import statistics_pb2


def write_schema_to_gcs(
    file_path: str,
    schema: schema_pb2.Schema,
):
  """ Write schema to GCS.

  Args:
    file_path: The location to store the write the schema on GCS
    schema: The schema proto.
  """
  tfdv.write_schema_text(schema, file_path)


def load_stats_to_bigquery_partition_by_timestamp(
    destination: str,
    stats_proto: Optional[statistics_pb2.DatasetFeatureStatisticsList] = None,
    statistics_path: Optional[str] = None,
) -> bigquery.LoadJob:
  """Extract statistics and load to BigQuery

  Args:
    destination: The destination table to use for loading the data.
      If it is an existing table, the schema of the DataFrame must match
      the schema of the destination table. If the table does not yet exist,
      the schema is inferred from the DataFrame. If a string is passed in,
      this method attempts to create a table reference from a string using
      google.cloud.bigquery.table.TableReference.from_string().
    stats_proto: optional. The statistics proto.
    statistics_path: optional. The file path to statistics proto.

  Returns:
    A LoadJob object after the job is completed.

  Raises:
    ValueError: One of stats_proto and statistics_path should be set.
    ValueError: Only one of stats_proto and statistics_path should be set.
  """

  if not stats_proto and not statistics_path:
    raise ValueError("One of stats_proto and statistics_path should be set")

  if stats_proto and statistics_path:
    raise ValueError(
        "Only one of stats_proto and statistics_path should be set.")

  if statistics_path:
    stats_proto = tfdv.load_statistics(statistics_path)
    statistics = stats_proto
  else:
    statistics = stats_proto

  stats_df = stats_proto_to_df(statistics)
  TIMESTAMP = 'timestamp'
  # Add timestamp column to the df
  stats_df.insert(
      loc=len(stats_df.columns),
      column=TIMESTAMP,
      value=[pd.Timestamp(datetime.now()) for _ in range(len(stats_df))]
  )

  client = bigquery.Client()
  job_config = bigquery.LoadJobConfig(
      # Since string columns use the "object" dtype, pass in a (partial) schema
      # to ensure the correct BigQuery data type.
      schema=[
        bigquery.SchemaField("type", "STRING"),
        bigquery.SchemaField("name", "STRING")
      ],
      time_partitioning=bigquery.table.TimePartitioning(
          type_=bigquery.TimePartitioningType.DAY,
          field=TIMESTAMP  # field to use for partitioning
      )
  )

  load_job = client.load_table_from_dataframe(
      stats_df,
      destination=destination,
      job_config=job_config
  )

  result = load_job.result()
  return result
