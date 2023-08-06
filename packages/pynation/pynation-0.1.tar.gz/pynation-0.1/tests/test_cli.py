
import pytest
from pynation.cli import cli, return_country
from click.testing import CliRunner

runner = CliRunner()


def test_return_country():
    assert return_country('united s**') is None
    assert return_country('united states of America') == ('US', 'USA', 840)


class TestCli:
    def test_info_correct_country(self):
        result = runner.invoke(cli, ['info', 'Nigeria'])
        assert result.exit_code == 0
        assert "Information about" in result.output
        assert "NGA" in result.output
        assert 'NG' in result.output

    def test_info_wrong_country(self):
        result = runner.invoke(cli, ['info', 'eeieidjjdl'])
        assert 'Country does not exist' in result.output
    
    def test_info_two_digit(self):
        result = runner.invoke(cli, ['short', 'Nigeria'])
        assert result.exit_code == 0
        assert "NGA" not in result.output
        assert 'NG' in result.output
    
    def test_info_three_digit(self):
        result = runner.invoke(cli, ['short', 'Nigeria', '-ab=3'])
        assert result.exit_code == 0
        assert "NGA" in result.output
        assert 'NG' not in result.output.split(' ')

        result1 = runner.invoke(cli, ['short', 'NIGERIA', '-ab=4'])
        assert 'Error' in result1.output
