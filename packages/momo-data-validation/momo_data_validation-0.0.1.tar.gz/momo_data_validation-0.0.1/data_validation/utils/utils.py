import copy
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional, Set, Tuple

import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow_metadata.proto.v0 import statistics_pb2


@dataclass
class Stats:
  """A class to store statistics data of a feature."""
  name: str = ''
  count: int = 0
  type: str = ''
  num_missing: int = 0
  std_dev: float = 0.0
  num_zeros: int = 0
  mean: float = 0.0
  min: float = 0.0
  median: float = 0.0
  max: float = 0.0
  missing_ratio: float = 0.0
  zero_ratio: float = 0.0


@dataclass
class StatsDataset:
  """A class to store statistics of the whole dataset."""
  stats_list: List[Stats] = field(default_factory=list)


def stats_proto_to_df(
    stats_proto: statistics_pb2.DatasetFeatureStatisticsList
) -> pd.DataFrame:
  """Extract statistics data from proto and convert to pandas DataFrame.

  Args:
    stats_proto: The statistic proto.

  Returns:
     A statistic dataset.
  """
  stats_dataset = extract_stats(stats_proto)
  return pd.DataFrame([asdict(stats) for stats in stats_dataset.stats_list])


def extract_stats(
    stats_proto: statistics_pb2.DatasetFeatureStatisticsList
) -> StatsDataset:
  """Extract statistics data from proto.

  Args:
    stats_proto: The statistics proto.

  Returns:
    A statistic dataset.
  """

  stats_ds = StatsDataset()
  for ds in stats_proto.datasets:
    for feature in ds.features:
      stat_obj = Stats()
      stat_obj.count = ds.num_examples
      stat_obj.name = feature.path.step[0]
      stat_obj.type = feature.Type.keys()[feature.type]
      stat_obj.num_zeros = feature.num_stats.num_zeros
      stat_obj.mean = feature.num_stats.mean
      stat_obj.median = feature.num_stats.median
      stat_obj.max = feature.num_stats.max
      stat_obj.min = feature.num_stats.min
      stat_obj.num_missing = feature.num_stats.common_stats.num_missing
      try:
        stat_obj.missing_ratio = stat_obj.num_missing / stat_obj.count
        stat_obj.zero_ratio = stat_obj.num_zeros / stat_obj.count
      except ZeroDivisionError as err:
        print(f'Exception {err} when compute missing_ratio and zero_ratio')
      stats_ds.stats_list.append(stat_obj)
  return stats_ds


def dataset_to_query(dataset: StatsDataset):
  """ Convert the dataset to query, which will be used to create or replace
  table.

  Args:
    dataset: The statistics dataset

  Returns:
    A 'SELECT' query used to create or replace table
  """
  query = ''
  for index, row in enumerate(dataset.stats_list):
    query += f"SELECT '{row.name}' as name, '{row.type}' as type, " \
             f"{row.count} as count, {row.mean} as mean, " \
             f"{row.std_dev} as std_dev, {row.median} as median, " \
             f"{row.min} as min, {row.max} as max, " \
             f"{row.missing_ratio} as missing_ratio, " \
             f"{row.zero_ratio} as zero_ratio"
    if index != len(dataset.stats_list) - 1:
      query += ' UNION ALL '
  return query


_DEFAULT_ENCODING = 'utf-8'


def _process_dict(
    value: Dict,
    feature: Dict,
    config: List[Tuple[str, str]]
) -> Dict:
  new_feature = copy.deepcopy(feature)
  for k, v in value.items():
    if isinstance(v, int) or isinstance(v, float) or isinstance(v, str):
      new_feature[k] = _to_feature(v)

  for (k1, k2) in config:
    for k, v in zip(value[k1], value[k2]):
      if isinstance(v, int) or isinstance(v, float) or isinstance(v, str):
        new_feature[str(k)] = _to_feature(float(v))
      else:
        raise RuntimeError('Column type {} is not supported.'.format(type(v)))
  return new_feature


def _to_feature(value: Any):
  if value is None:
    return tf.train.Feature()
  elif isinstance(value, int):
    return tf.train.Feature(
        int64_list=tf.train.Int64List(value=[value]))
  elif isinstance(value, float):
    return tf.train.Feature(
        float_list=tf.train.FloatList(value=[value]))
  elif isinstance(value, str):
    return tf.train.Feature(
        bytes_list=tf.train.BytesList(
            value=[value.encode(_DEFAULT_ENCODING)]))
  else:
    raise RuntimeError(f"Type {type(value)} is not supported.")


def dict_to_example(
    instance: Dict[str, Any],
    nested_fields_config: Optional[Dict[str, List[Tuple[str, str]]]] = None,
    ignore_fields: Optional[Set[str]] = None
) -> tf.train.Example:
  """Converts dict to tf example."""

  feature = {}
  for key, value in instance.items():
    if ignore_fields and key in ignore_fields:
      continue

    if isinstance(value, np.ndarray):
      pyval = value.tolist()
    else:
      try:
        pyval = value.item()
      except AttributeError:
        pyval = value

    # Convert bytes to str
    if isinstance(pyval, bytes):
      pyval = pyval.decode(_DEFAULT_ENCODING)
    if pyval is None:
      feature[key] = tf.train.Feature()
    elif isinstance(pyval, int):
      feature[key] = tf.train.Feature(
          int64_list=tf.train.Int64List(value=[pyval]))
    elif isinstance(pyval, float):
      feature[key] = tf.train.Feature(
          float_list=tf.train.FloatList(value=[pyval]))
    elif isinstance(pyval, str):
      feature[key] = tf.train.Feature(
          bytes_list=tf.train.BytesList(
              value=[pyval.encode(_DEFAULT_ENCODING)]))
    elif isinstance(pyval, list):
      if not pyval:
        feature[key] = tf.train.Feature()
      elif isinstance(pyval[0], int):
        feature[key] = tf.train.Feature(
            int64_list=tf.train.Int64List(value=pyval))
      elif isinstance(pyval[0], float):
        feature[key] = tf.train.Feature(
            float_list=tf.train.FloatList(value=pyval))
      elif isinstance(pyval[0], str):
        feature[key] = tf.train.Feature(
            bytes_list=tf.train.BytesList(
                value=[v.encode(_DEFAULT_ENCODING) for v in pyval]))
      else:
        raise RuntimeError('Column type `list of {}` is not supported.'.format(
            type(value[0])))
    elif isinstance(pyval, dict):
      if nested_fields_config and key in nested_fields_config:
        feature = _process_dict(pyval, feature, nested_fields_config[key])
      else:
        continue
    else:
      raise RuntimeError(
          'Column type {} is not supported. If the column type <class \'dict\'>, '
          'please specified the nested_fields_config argument'.format(
              type(value)))
  return tf.train.Example(features=tf.train.Features(feature=feature))
