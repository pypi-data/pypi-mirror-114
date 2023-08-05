import click

from wikiusers.dataloader import MhdLoader
from wikiusers.rawprocessor import RawProcessor
from wikiusers.postprocessor import PostProcessor

from .utils import select_languages, DEFAULT_ARGUMENTS


@click.group(help="Tool to analyze the wikimedia history dump tsv and obtain per-user information")
def cli():
    pass


@cli.command(help='Downloads the assets if needed and saves per-user raw information on mongodb')
@click.option('-u', '--dburl', type=click.STRING, default=DEFAULT_ARGUMENTS['DATABASE_URL'], show_default=True, help='The uri to MongoDB')
@click.option('-s', '--sync-data', type=click.BOOL, default=DEFAULT_ARGUMENTS['SYNC_DATA'], show_default=True, help='If the dataset will be synced before the processing (by downloading missing datasets or newest version)')
@click.option('-i', '--datasets-dir', type=click.STRING, default=DEFAULT_ARGUMENTS['DATASETS_DIR'], show_default=True, help='The path to the datasets folder')
@click.option('-l', '--langs', type=click.STRING, multiple=True, default=[DEFAULT_ARGUMENTS['LANGUAGE']], show_default=True, help='The languages that you want to process. If "all" is passed, all the languages are selected')
@click.option('-p', '--parallelize/--no-parallelize', is_flag=True, default=DEFAULT_ARGUMENTS['PARALLELIZE'], show_default=True, help='If processing the various datasets files in parallel')
@click.option('-n', '--n-processes', type=click.INT, default=DEFAULT_ARGUMENTS['N_PROCESSES'], show_default=True, help='If parallelize is active, specifies the number of parallel processes. Default is the number of cores of the CPU')
@click.option('-d', '--dbname', type=click.STRING, default=DEFAULT_ARGUMENTS['DATABASE_PREFIX'], show_default=True, help='The name of the MongoDB database where the result will be saved')
@click.option('-f', '--force/--no-force', is_flag=True, default=DEFAULT_ARGUMENTS['FORCE'], show_default=True, help='If already populated collections will be dropped and reprocessed')
@click.option('--skip/--no-skip', is_flag=True, default=DEFAULT_ARGUMENTS['SKIP'], show_default=True, help='If already populated collections will be skipped')
@click.option('-e', '--erase-datasets/--no-erase-datasets', is_flag=True, default=DEFAULT_ARGUMENTS['ERASE_DATASETS'], show_default=True, help='If the datasets files will be erased after having been processed.')
@click.option('-c', '--choose-langs/--no-choose-langs', is_flag=True, show_default=False, help='If the user will be asked to select the languages')
def rawprocess(*, dburl: str, sync_data: bool, datasets_dir: str, langs: list[str], parallelize: bool, n_processes: int, dbname: str, force: bool, skip: bool, erase_datasets: bool, choose_langs: bool):
    if choose_langs:
        loader = MhdLoader(datasets_dir, DEFAULT_ARGUMENTS['LANGUAGE'])
        available_langs = loader.get_available_langs()
        langs = select_languages(available_langs, langs)
    elif 'all' in langs:
        loader = MhdLoader(datasets_dir, DEFAULT_ARGUMENTS['LANGUAGE'])
        langs = loader.get_available_langs()

    rawprocessor = RawProcessor(dburl, sync_data, datasets_dir, langs, parallelize,
                                n_processes, dbname, force, skip, erase_datasets)
    rawprocessor.process()


@cli.group(help="Given an already populated raw collection, postprocesses it, creating/updating a new collection")
def postprocess():
    pass


@postprocess.command(help='Postprocesses the users of the raw collection')
@click.option('-u', '--dburl', type=click.STRING, default=DEFAULT_ARGUMENTS['DATABASE_URL'], show_default=True, help='The uri to MongoDB')
@click.option('-d', '--dbname', type=click.STRING, default=DEFAULT_ARGUMENTS['DATABASE_PREFIX'], show_default=True, help='The name of the MongoDB database where the result will be saved')
@click.option('-l', '--langs', type=click.STRING, multiple=True, default=[DEFAULT_ARGUMENTS['LANGUAGE']], show_default=True, help='The languages that you want to process. If "all" is passed, all the languages are selected')
@click.option('-b', '--batch-size', type=click.INT, default=DEFAULT_ARGUMENTS['BATCH_SIZE'], show_default=True, help='Users from mongodb are taken and updated in batches. This option specifies the batch size')
@click.option('-f', '--force/--no-force', is_flag=True, default=DEFAULT_ARGUMENTS['FORCE'], show_default=True, help='If already populated collections will be dropped and reprocessed')
@click.option('-c', '--choose-langs/--no-choose-langs', is_flag=True, show_default=False, help='If the user will be asked to select the languages')
def users(*, dburl: str, dbname: str, langs: list[str], batch_size: int, force: bool, choose_langs: bool):
    if choose_langs:
        available_langs = PostProcessor.get_available_langs(dburl, dbname)
        langs = select_languages(available_langs, langs)
    elif 'all' in langs:
        langs = PostProcessor.get_available_langs(dburl, dbname)

    postprocessor = PostProcessor(
        dburl, DEFAULT_ARGUMENTS['DATASETS_DIR'], dbname, langs, batch_size, force)
    postprocessor.process_users()


@postprocess.command(help='Postprocesses the users of the raw collection')
@click.option('-u', '--dburl', type=click.STRING, default=DEFAULT_ARGUMENTS['DATABASE_URL'], show_default=True, help='The uri to MongoDB')
@click.option('-i', '--datasets-dir', type=click.STRING, default=DEFAULT_ARGUMENTS['DATASETS_DIR'], show_default=True, help='The path to the datasets folder')
@click.option('-d', '--dbname', type=click.STRING, default=DEFAULT_ARGUMENTS['DATABASE_PREFIX'], show_default=True, help='The name of the MongoDB database where the result will be saved')
@click.option('-l', '--langs', type=click.STRING, multiple=True, default=[DEFAULT_ARGUMENTS['LANGUAGE']], show_default=True, help='The languages that you want to process. If "all" is passed, all the languages are selected')
@click.option('-b', '--batch-size', type=click.INT, default=DEFAULT_ARGUMENTS['BATCH_SIZE'], show_default=True, help='Users from mongodb are taken and updated in batches. This option specifies the batch size')
@click.option('-c', '--choose-langs/--no-choose-langs', is_flag=True, show_default=False, help='If the user will be asked to select the languages')
def sex(*, dburl: str, datasets_dir: str, dbname: str, langs: list[str], batch_size: int, choose_langs: bool):
    if choose_langs:
        available_langs = PostProcessor.get_available_langs(dbname)
        langs = select_languages(available_langs, langs)
    elif 'all' in langs:
        langs = PostProcessor.get_available_langs(dbname)

    postprocessor = PostProcessor(
        dburl, datasets_dir, dbname, langs, batch_size, DEFAULT_ARGUMENTS['FORCE'])
    postprocessor.process_sex()


@cli.group(help="Handles the datasets")
def datasets():
    pass


@datasets.command(help='Synces the datasets, by downloading the missing datasets')
@click.option('-i', '--datasets-dir', type=click.STRING, default=DEFAULT_ARGUMENTS['DATASETS_DIR'], show_default=True, help='The path to the datasets folder')
@click.option('-l', '--lang', type=click.STRING, default=DEFAULT_ARGUMENTS['LANGUAGE'], show_default=True, help='The language that you want to process')
def sync(*, datasets_dir: str, lang: str):
    loader = MhdLoader(datasets_dir, lang)
    loader.sync_wikies()


@datasets.command(help='Show available langs for the mhd datasets')
@click.option('-i', '--datasets-dir', type=click.STRING, default=DEFAULT_ARGUMENTS['DATASETS_DIR'], show_default=True, help='The path to the datasets folder')
def list(*, datasets_dir: str):
    loader = MhdLoader(datasets_dir, DEFAULT_ARGUMENTS['LANGUAGE'])
    langs = loader.get_available_langs()
    langs_list = "\n".join(langs)
    click.echo(click.style(
        'Downloadable datasets are available in:', fg='yellow', bold=True))
    click.echo(click.style(f'{langs_list}', fg='blue', bold=True))


@datasets.command(help='Show downloaded langs for the mhd datasets')
@click.option('-i', '--datasets-dir', type=click.STRING, default=DEFAULT_ARGUMENTS['DATASETS_DIR'], show_default=True, help='The path to the datasets folder')
def local(*, datasets_dir: str):
    loader = MhdLoader(datasets_dir, DEFAULT_ARGUMENTS['LANGUAGE'])
    langs = loader.get_local_langs()
    langs_list = "\n".join(langs)
    click.echo(click.style(
        'Downloaded datasets are available in:', fg='yellow', bold=True))
    click.echo(click.style(f'{langs_list}', fg='blue', bold=True))


@cli.group(help="Handles the database")
def database():
    pass


@database.command(help='Show raw processed languages')
@click.option('-u', '--dburl', type=click.STRING, default=DEFAULT_ARGUMENTS['DATABASE_URL'], show_default=True, help='The uri to MongoDB')
@click.option('-d', '--dbname', type=click.STRING, default=DEFAULT_ARGUMENTS['DATABASE_PREFIX'], show_default=True, help='The prefix of the database name')
def rawprocessed(*, dburl: str, dbname: str):
    langs = PostProcessor.get_available_langs(dburl, dbname)
    langs_list = "\n".join(langs)
    click.echo(click.style(
        'Raw processed collections are in:', fg='yellow', bold=True))
    click.echo(click.style(f'{langs_list}', fg='blue', bold=True))


@database.command(help='Show post processed languages')
@click.option('-u', '--dburl', type=click.STRING, default=DEFAULT_ARGUMENTS['DATABASE_URL'], show_default=True, help='The uri to MongoDB')
@click.option('-d', '--dbname', type=click.STRING, default=DEFAULT_ARGUMENTS['DATABASE_PREFIX'], show_default=True, help='The prefix of the database name')
def postprocessed(*, dburl: str, dbname: str):
    langs = PostProcessor.get_processed_langs(dburl, dbname)
    langs_list = "\n".join(langs)
    click.echo(click.style(
        'Post processed collections are in:', fg='yellow', bold=True))
    click.echo(click.style(f'{langs_list}', fg='blue', bold=True))


def run():
    cli()


if __name__ == '__main__':
    run()
