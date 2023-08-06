import pandas as pd


def get_ele_use(epi: pd.Series, freq="H", negative_trend_check=True):
    if not isinstance(epi, pd.Series):
        raise TypeError("INPUT EPI NOT pandas.Series TYPE!")
    if not isinstance(epi.index, pd.DatetimeIndex):
        raise TypeError("INPUT EPI INDEX NOT datetime TYPE!")
    epi_dif = epi.sort_index().diff().fillna(0)
    if negative_trend_check:
        if (epi_dif < 0).any():
            raise ValueError("EPI DATA HAS NEGATIVE TREND!")
    ele = epi_dif.resample(freq).sum()
    return ele


if __name__ == '__main__':
    x = pd.Series(index=pd.date_range("2021-01-01", "2021-02-01"), data=0)
    print(get_ele_use(x))
