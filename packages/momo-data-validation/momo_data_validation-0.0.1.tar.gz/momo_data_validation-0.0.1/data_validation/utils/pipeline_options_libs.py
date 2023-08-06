"""Convenient library for config pipeline backend."""

from typing import List, Optional

from apache_beam.options.pipeline_options import GoogleCloudOptions, \
  PipelineOptions, SetupOptions, StandardOptions


def _get_pipeline_options(
    type: str = 'local',
    project_id: Optional[str] = None,
    project_region: Optional[str] = None,
    temp_location: Optional[str] = None,
    extra_packages: Optional[List[str]] = None,
    job_name: Optional[str] = 'beam-job',
    job_endpoint: str = 'localhost:8089'
):
  if type == 'local':
    return direct_pipeline_options()
  elif type == 'dataflow':
    return dataflow_pipeline_options(
        project_id=project_id,
        project_region=project_region,
        temp_location=temp_location,
        extra_packages=extra_packages,
        job_name=job_name
    )
  elif type == 'spark':
    return spark_pipeline_options(job_endpoint=job_endpoint)
  else:
    raise ValueError("Pipeline types should be either local, dataflow or spark")


def dataflow_pipeline_options(
    project_id: str,
    project_region: str,
    temp_location: str,
    extra_packages: List[str],
    job_name: Optional[str] = 'beam-job'
) -> PipelineOptions:
  """Generate pipeline options to run the pipeline with GCP DataFlow. 

  Args:
    project_id: The GCP project ID that provides Dataflow resource.
    project_region: The GCP project REGION that provides Dataflow resource.
    temp_location: The GCS location to store temporary files when running the
      pipeline.
    extra_packages: The list of packages to install in the Dataflow workers.
    job_name: optional. The name of the job.

  Returns:
    A PipelineOptions configured to run with Dataflow.
  """

  options = PipelineOptions()
  # For Cloud execution, set the Cloud Platform project, job_name,
  # temp_location and specify DataflowRunner.
  google_cloud_options = options.view_as(GoogleCloudOptions)
  google_cloud_options.project = project_id
  google_cloud_options.region = project_region
  google_cloud_options.job_name = job_name
  google_cloud_options.temp_location = temp_location

  options.view_as(StandardOptions).runner = 'DataflowRunner'
  setup_options = options.view_as(SetupOptions)
  setup_options.extra_packages = extra_packages
  return options


def spark_pipeline_options(
    job_endpoint: str = 'localhost:8099',
):
  return PipelineOptions([
    "--runner=PortableRunner",
    "--job_endpoint=localhost:8099",
    "--environment_type=LOOPBACK",
  ])


def direct_pipeline_options(
    project_id: Optional[str] = None,
    temp_location: Optional[str] = None
) -> PipelineOptions:
  """Generate pipeline options to run the pipeline with DirectRunner.
  Args:
    project_id: optional. The project ID required when using ReadFromBigQuery
      operation.
    temp_location: optional. The temporary location required when using
      ReadFromBigQuery operation.
  Returns:
    A PipelineOptions configured to run with DirectRunner.
  """

  options = PipelineOptions()
  # Only useful when ReadFromBigQuery is used
  google_cloud_options = options.view_as(GoogleCloudOptions)
  google_cloud_options.project = project_id
  google_cloud_options.temp_location = temp_location

  options.view_as(StandardOptions).runner = 'DirectRunner'
  return options
