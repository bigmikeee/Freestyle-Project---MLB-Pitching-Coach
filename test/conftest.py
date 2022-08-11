import pytest
import pandas as pd
import datatest as dt

@pytest.fixture(scope='module')
@dt.working_directory(__file__)
def df():
    return pd.read_csv('savant_data.csv')

@pytest.mark.mandatory
def test_pitch_type(df):
    dt.validate(df['pitch_type'], str)

def test_pitch_type(df):
    dt.validate(df['player_name'], str)