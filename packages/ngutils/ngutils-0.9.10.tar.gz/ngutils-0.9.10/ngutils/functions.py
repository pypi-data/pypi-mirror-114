import concurrent.futures as pool
from datetime import date, datetime, timedelta
import io
import pandas as pd
import requests

def view_types(data, dropna=True):
    """
    Вывод отчета с анализом содержимого объекта data, подсчет представленных типов данных
    Parameters
    ----------
    data : DataFrame, Series, dict, list, другой тип, преобразуемый к DataFrame
        Объект DataFrame или приводимый к DataFrame для анализа
    dropna : bool, default True
        Не включать NaN в расчет количества уникальных значений
    Returns
    -------
    None
    
    2021-07-26 (c) Nikolay Ganibaev
    """
    data = pd.DataFrame(data)
    columns_exch = {
        "<class 'str'>": 'str', "<class 'int'>": 'int', "<class 'float'>": 'float',
        "<class 'list'>": 'list', "<class 'dict'>": 'dict',
        "<class 'datetime.datetime'>": 'datetime',
        "<class 'pandas._libs.tslibs.timestamps.Timestamp'>": 'Timestamp',
    }
    df_output = pd.DataFrame(
        data[data[c].notna()][c].apply(type).value_counts() for c in data.columns
    ).fillna(0).astype(int)
    if data.isna().any().any():
        df_output['NaN'] = data.isna().sum()
    df_output['(min)'] = None
    df_output['(max)'] = None
    for i, c in enumerate(data.columns):
        try:
            df_output.loc[c,'(min)'] = data[c].dropna().min()
            df_output.loc[c,'(max)'] = data[c].dropna().max()
        except:
            df_output.loc[c,'(min)'] = data[c].dropna().astype(str).min()
            df_output.loc[c,'(max)'] = data[c].dropna().astype(str).max()

    df_output['(unique)'] = [data[c].astype(str).nunique(dropna) for c in data.columns]
    df_output.columns = [columns_exch.get(str(x), x) for x in df_output.columns]
    if '_Jupyter' in globals():
        display(df_output.head(60))
    else:
        print(df_output.head(60))
    print("{} rows x {} columns".format(*data.shape))


def read_urls_contents(urls_list, max_workers=10, session=None, parser=None, encoding=None, *, 
    max_retries=None, timeout=None, error_page_output=None, status_text=None, mute=False):
    """
    URLs list contents multithread loading to StringIO

    Parameters
    ----------
    urls_list : list
        Iterable list of urls.
    max_workers : int, optional
        The maximum number of threads, by default 10.
    session : requests.Session, optional
        Auth session.
    parser : function, optional
        Function for content preprocessing in main thread.
    encoding : string, optional
        Encoding of the content. By default, the content encoding is determined automatically.
    max_retries : int, optional
        The maximum number of retries for connection. By default, failed connections are not retry.
    timeout : float or tuple, optional
        How many seconds to wait server establish connection and send response. By default, timeout is not define.
    error_page_output : io.StringIO, optional
        StringIO output stream for all runtime errors. By default, the process terminated at the first error.
    status_text : str, optional
        Text for download status, by default 'URLs list download:'.
    mute : boolean, optional
        If mute is True then progress messages will be disabled, default False

    Returns
    -------
    io.StringIO
        String stream for additional processing or use in pd.read_csv

    2021-07-26 (c) Nikolay Ganibaev
    """
    PROGRESS_WHEEL=r'|/—\|/—\ '

    def url_loader(url, session, timeout, encoding):
        """
        Default function for url download
        """
        if encoding is None:
            return session.get(url, timeout=timeout).text
        else:
            return session.get(url, timeout=timeout).content.decode(encoding)

    if session is None:
        session = requests.Session()

    if parser is None:
        parser = str
    
    if max_retries is not None:
        session.mount('http://', requests.adapters.HTTPAdapter(max_retries=max_retries))
        session.mount('https://', requests.adapters.HTTPAdapter(max_retries=max_retries))

    if status_text is None:
        status_text = 'URLs list download:'

    if not mute:
        print(f"{status_text}     0%"+" "*50, end='\r', flush=True)

    buf = io.StringIO()
    with pool.ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_load_csv = {executor.submit(url_loader, url, session, timeout, encoding): url for url in urls_list}
        for i, future in enumerate(pool.as_completed(future_load_csv)):
            if not mute:
                print(f"{status_text} {PROGRESS_WHEEL[i%8]} {i/len(urls_list)*.995:.0%}"+" "*50, end='\r', flush=True)
            url = future_load_csv[future]
            try:
                buf.write(parser(future.result()))
            except Exception as exc:
                if error_page_output is None:
                    raise Exception(f'Download error:\n{url}|{exc}')
                else:
                    error_page_output.write(f'Download error:\n{url}|{exc}\n')

    if not mute:
        print(f"{status_text}   100%"+" "*50)

    buf.seek(0)

    return buf


def accel_steps(max_degree=10):
    """
    Increment yield-counter with acceleration

    Parameters
    ----------
    max_degree : int, optional
        Power of 2 to determine the maximum value of the counter, by default 10.

    Returns
    -------
    int
        counter value

    2021-07-29 (c) Nikolay Ganibaev
    """
    for i in range(int(max_degree)):
        for j in 1, 2, 5:
            yield j*10**i


def tune_steps(number=100):
    """
    Decrement yield-counter fast decrement counter for binary search from [1..number]

    Parameters
    ----------
    number : int, optional
        Upper limit of the search range. By default, 100.

    Returns
    -------
    int
        counter value

    2021-07-29 (c) Nikolay Ganibaev
    """
    while number>1:
        number -= number//2
        yield number
    yield 1