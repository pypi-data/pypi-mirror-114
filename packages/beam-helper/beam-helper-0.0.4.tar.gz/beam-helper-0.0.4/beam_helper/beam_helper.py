import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions, StandardOptions, SetupOptions, GoogleCloudOptions
import yaml

__all__ = ['generate_config', 'build_tasks']

class ExtractFromSource(beam.PTransform):
    def __init__(self, source_type: str, task: dict):
        self.source_type = source_type
        self.task = task

    def expand(self, pcoll):
        if self.source_type == 'BigQuery':
            return (pcoll | 'read from bq' >> beam.io.ReadFromBigQuery(query=self.task['task']['source_query'],
                                                                            use_standard_sql=True))
        elif self.source_type == 'Local':
            return (pcoll | 'read from local' >> beam.io.ReadFromText(file_pattern=self.task['task']['local_path'],
                                                                          skip_header_lines=self.task['task']['skip_header_lines'],
                                                                          compression_type=self.task['task']['input_compression']))

class GetFormat(beam.DoFn):
    def process(self, element, num_cols: int, column_names: list):
        dic = {}
        for col in range(0, num_cols):
            li = [column_names[num_cols-num_cols-col], element[num_cols-num_cols-col]]
            dic[li[0]] = li[1]
        return [dic]
        
class ApplyFormat(beam.PTransform):
    def __init__(self, task: dict):
        self.task = task
    
    def expand(self, pcoll):
        return (pcoll | 'format data' >> beam.ParDo(GetFormat(), num_cols=self.task['task']['num_cols'], column_names=self.task['task']['column_names']))


class SplitTransform(beam.DoFn):
    def process(self, element, delimiter):
        yield element.split(delimiter)
        
class ReplaceTransform(beam.DoFn):
    def process(self, element, column, find_value, replace_value):
        element[column] = element[column].replace(find_value, replace_value)        
        return [element]
    
class FilterTransformIn(beam.DoFn):
    def process(self, element, column, value):
        for c,v in zip(column, value):
            if element[c] == v:
                yield element
                
class FilterTransformNotIn(beam.DoFn):
    def process(self, element, column, value):
        for c,v in zip(column, value):
            if element[c] != v:
                yield element

class EvalLambda(object):
    def __init__(self, column, lambda_func):
        self.column = column
        self.lambda_func = lambda_func
        
    def run(self):
        return beam.Filter(eval(self.lambda_func))


class ApplyTransform(beam.PTransform):
    def __init__(self, transform_type: str, task: dict):
        self.transform_type = transform_type
        self.task = task
        
    def expand(self, pcoll):
        if self.transform_type == 'Filter':
            if self.task['task']['filter']['condition'] == "IN":
                return (pcoll | 'filter values' >> beam.ParDo(FilterTransformIn(), column=self.task['task']['filter']['column'], value=self.task['task']['filter']['value']))
            elif self.task['task']['filter']['condition'] == "NOT IN":
                return (pcoll | 'filter values' >> beam.ParDo(FilterTransformNotIn(), column=self.task['task']['filter']['column'], value=self.task['task']['filter']['value']))
        elif self.transform_type == 'Replace':
            return (pcoll | 'replace value' >> beam.ParDo(ReplaceTransform(), column=self.task['task']['replace']['column'], find_value=self.task['task']['replace']['find_value'], replace_value=self.task['task']['replace']['replace_value']))
        elif self.transform_type == 'Split':
            return (pcoll | 'split by delimiter' >> beam.ParDo(SplitTransform(), delimiter=self.task['task']['split']['delimiter']))
        elif self.transform_type == 'Lambda':
            return (pcoll | 'apply lambda' >> EvalLambda(column=self.task['task']['filter']['column'], lambda_func=self.task['task']['filter']['lambda']).run())

class WriteToSink(beam.PTransform):
    def __init__(self, sink_type: str, task: dict):
        self.sink_type = sink_type
        self.task = task

    def expand(self, pcoll):
        if self.sink_type == 'BigQuery':
            return (pcoll | 'write to bq' >> beam.io.WriteToBigQuery(table=self.task['task']['output_table'],
                create_disposition=self.task['task']['create_disposition'],
                write_disposition=self.task['task']['write_disposition'],
                custom_gcs_temp_location=self.task['task']['gcs_temp']))
        elif self.sink_type == 'Local':
            return (pcoll | 'write to local' >> beam.io.WriteToText(file_path_prefix=self.task['task']['file_prefix'],
                                    file_name_suffix=self.task['task']['file_suffix'],
                                    num_shards=self.task['task']['num_shards'],
                                    compression_type=self.task['task']['output_compression']))
        elif self.sink_type == 'Print':
            return (pcoll | 'print' >> beam.Map(print))


def build_tasks():
    tasks = {}
    cfg = yaml.load(open('pipeline_config.yaml', 'r'), Loader=yaml.FullLoader)
    pipeline = beam.Pipeline(options=PipelineOptions().from_dictionary({**cfg['env_options']}))
    for task, i in zip(cfg['pipeline_tasks'], range(len(cfg['pipeline_tasks']))):
        task_type = task['task']['task_type']
        if task_type == 'READ':
            source_type = task['task']['source_type']
            tasks[task['task']['task_name']] = ExtractFromSource(source_type, task)
        elif task_type == 'VALIDATE':
            pass
        elif task_type == 'TRANSFORM':
            transform_type = task['task']['transform_type']
            tasks[task['task']['task_name']] = ApplyTransform(transform_type, task)
        elif task_type == 'FORMAT':
            num_cols = task['task']['num_cols']
            col_names = task['task']['column_names']
            tasks[task['task']['task_name']] = ApplyFormat(task)
        elif task['task']['task_type'] == 'WRITE':
            sink_type = task['task']['sink_type']
            tasks[task['task']['task_name']] = WriteToSink(sink_type, task)
    return pipeline, tasks


def get_config_env_options():
    env_block = """env_options:
    runner: ##The runner you wish to use (str). Options include ('DirectRunner', 'DataFlowRunner', 'FlinkRunner')
    project: ##The google cloud project name (str).
    temp_location: ##The temporary gcs location to use with bigquery read/write tasks (str).
    region: ##The google cloud region (str)
    job_name: ##Name for the job if deployed to dataflow runner (str).
    sa_email:  ##Service account to run the job as if deployed to dataflow (str).
    network:  ##The google cloud network vpc name (str)
    subnetwork:  ##The google cloud subnet name (str).
    use_public_ips:  ##Whether to use internal ips only or permit external ips for workers (bool).\n\n
pipeline_tasks:\n\n"""
    return env_block

def get_config_tasks():
    task_block = """
    - task:
        task_name: 
        task_type: 
        source_type: 
        source_query: 
        num_cols: 
        column_names: 
        gcs_path: 
        gcs_temp: 
        input_compression: 
        skip_header_lines: 
        local_path: 
        sink_type: 
        output_table: 
        create_disposition: 
        write_disposition: 
        schema: 
        num_shards: 
        output_compression: 
        file_prefix: 
        file_suffix: 
        transform_type:
        filter:
            column: 
            lambda: 
            value:
        split:
            delimiter: 
        replace:
            column:
            find_value: 
            replace_value:
        join_type:
        join_keys:\n\n"""
    return task_block

def generate_config(num_tasks: int):
    with open('pipeline_config.yaml', 'w') as yaml_config:
        env_options = get_config_env_options()
        yaml_config.write(env_options)
        
    with open('pipeline_config.yaml', 'a') as yaml_config:
        task_options = get_config_tasks()
        for i in range(0, num_tasks):
            yaml_config.write(f'##Task{i+1}\n' + task_options)