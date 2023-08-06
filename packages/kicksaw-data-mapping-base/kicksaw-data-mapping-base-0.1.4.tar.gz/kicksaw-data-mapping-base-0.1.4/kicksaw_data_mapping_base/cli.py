import click

from kicksaw_data_mapping_base.download import download_as_csv


@click.group(chain=True)
def kicksaw_mappings(**kwargs):
    pass


@kicksaw_mappings.command("download")
@click.option("-n", "--name", default="data-mapping.csv", help="The file name you want")
def upsert(name):
    download_as_csv(name)
