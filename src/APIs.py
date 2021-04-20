import requests
from google.cloud import bigquery
from requests import async


def metric_value(url, metric):
    query = f'https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={url}&strategy=desktop'
    response = requests.get(query).json()
    metric_response = response['loadingExperience']['metrics'][metric]

    print(f'Metric response: {metric_response}')

    return metric_response


def upload_json_to_bigquery(json_to_upload):

    project_id = '<project_id>'
    dataset_id = '<dataset_id>'
    table_id = '<table_id>'

    client = bigquery.Client(project = project_id)
    dataset = client.dataset(dataset_id)
    table = dataset.table(table_id)


    job_config = bigquery.LoadJobConfig()
    job_config.source_format = bigquery.SourceFormat.NEWLINE_DELIMITED_JSON
    job_config.autodetect = True

    job = client.load_table_from_json(
            [json_to_upload],
            table,
            location = "US",
            job_config = job_config,
        )


def main():
    urls = [] # List containing the URLs to analyse
    metric = 'CUMULATIVE_LAYOUT_SHIFT_SCORE' # Metric to analyse
    for url in urls:
        metric_response = metric_value(url, metric)
        upload_json_to_bigquery(json_to_upload = metric_response)


if __name__ == '__main__':
    main()

