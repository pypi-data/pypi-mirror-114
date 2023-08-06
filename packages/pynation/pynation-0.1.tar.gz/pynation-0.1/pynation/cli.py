
import click
from pynation.data import country_data


def return_country(column):

    _country = country_data.get(column.title(), None)

    if _country is None:
        click.secho('Country does not exist. Perhaps, write the full name.', fg='red')
        return
    return _country


@click.group()
def cli1():
    """Gives information about a country"""
    pass


@click.group()
def cli2():
    """Others"""
    pass


@cli1.command()
@click.argument('country_name')
def info(country_name):
    """Brief information about a country."""

    country = return_country(country_name)
    if country:
        click.echo(click.style(
            "\nInformation about {}:\n"
            "  - Two digit abbreviation: {}\n" 
            "  - Three digit abbreviation: {}".format(country_name, country[0], country[1])
        , fg='green'))
    
    
@cli2.command('short')
@click.option('--abbreviate', '-ab', default='2', show_default=True,
              type=click.Choice(['2', '3']),
              help="")
@click.argument('country_name')
def short_code(country_name, abbreviate):

    """Returns the short abbreviation code of a country.
    It can be two digit or three digit country code.
    The default is two digit."""

    value = 0 if abbreviate == '2' else 1
    country = return_country(country_name)
    if country:
        click.secho('The {0} digit country code for {1} is "{2}"'.format(abbreviate, country_name, country[value]), fg="green")


cli = click.CommandCollection(sources=[cli1, cli2])
