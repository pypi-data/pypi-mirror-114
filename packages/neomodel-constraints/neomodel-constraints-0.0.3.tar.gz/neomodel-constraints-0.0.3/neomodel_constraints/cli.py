import click

from neomodel_constraints.extractor import NeomodelExtractor
from neomodel_constraints.constraint import Neo4jConstraintTypeMapper


@click.group()
def main(): ...


@main.command()
@click.argument('path')
def extract(path):
    type_mapper = Neo4jConstraintTypeMapper()

    extractor = NeomodelExtractor(path, type_mapper)
    constraints = extractor.extract()
    click.echo('\n'.join(constraints))


@main.command()
@click.argument('uri')
def fetch(uri):
    click.echo(uri)


main.add_command(fetch, 'fetch')
main.add_command(extract, 'extract')
