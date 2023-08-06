"""Utilities for BigQuery"""

from typing import Any, Dict, Optional

import tensorflow as tf
from google.cloud import bigquery


class BigQueryConverter:
  """Help class for bigquery result row to tf example conversion."""

  def __init__(self, query: str, project_id: Optional[str] = None):
    """Instantiate a BigQueryConverter object.
    Args:
      query: the query statement to get the type information.
      project_id: optional. The GCP project ID to run the query job. Default to
        the GCP project ID set by the gcloud environment on the machine.
    """
    client = bigquery.Client(project_id)
    # Dummy query to get the type information for each field.
    query_job = client.query(f'SELECT * FROM ({query}) LIMIT 0')
    results = query_job.result()
    self._type_map = {}
    for field in results.schema:
      self._type_map[field.name] = field.field_type

  def RowToExample(self, instance: Dict[str, Any]) -> tf.train.Example:
    """Convert bigquery result row to tf example."""
    return row_to_example(self._type_map, instance)


def row_to_example(
    field_to_type: Dict[str, str],
    field_name_to_data: Dict[str, Any]
) -> tf.train.Example:
  """Convert bigquery result row to tf example.
  Args:
  field_to_type: The name of the field to its type from BigQuery.
  field_name_to_data: The data need to be converted from BigQuery that
      contains field name and data.
  Returns:
  A tf.train.Example that converted from the BigQuery row. Note that BOOLEAN
  type in BigQuery result will be converted to int in tf.train.Example.
  Raises:
  RuntimeError: If the data type is not supported to be converted.
      Only INTEGER, BOOLEAN, FLOAT, STRING is supported now.
  """
  feature = {}
  for key, value in field_name_to_data.items():
    data_type = field_to_type[key]

    if value is None:
      feature[key] = tf.train.Feature()
      continue

    value_list = value if isinstance(value, list) else [value]
    if data_type in ('INTEGER', 'BOOLEAN'):
      feature[key] = tf.train.Feature(
          int64_list=tf.train.Int64List(value=value_list))
    elif data_type == 'FLOAT':
      feature[key] = tf.train.Feature(
          float_list=tf.train.FloatList(value=value_list))
    elif data_type == 'STRING':
      feature[key] = tf.train.Feature(
          bytes_list=tf.train.BytesList(
              value=[tf.compat.as_bytes(elem) for elem in value_list]))
    else:
      raise RuntimeError(
          'BigQuery column type {} is not supported.'.format(data_type))

  return tf.train.Example(features=tf.train.Features(feature=feature))
