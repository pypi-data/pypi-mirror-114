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
    display(df_output.head(60))
    print("{} rows x {} columns".format(*data.shape))

def phrase_build(number, noun_forms=None, prefix_forms=None, grouping_symbol='`'):
    """
    Build correct phrase [prefix word] [number] [noun] in Russian.

    Построение фразы [вводное слово] [число] [существительное] с правильными склонениями.
    Для чисел, заканчивающихся на 11..14, 0, 5..9 используется форма склонения noun_forms[0].
    Для других чисел, заканчивающихся на 1 используется форма склонения noun_forms[1].
    Для других чисел, заканчивающихся на 2..4 используется форма склонения noun_forms[2].
    При вызове функции может быть указано вводное слово в списке pre.
    Для вводного слова используется страдательное причастие в множественном числе - prefix[0],
        единственном числе - prefix[1].
    По умолчанию в качестве примера используется фраза ["Опубликованы"] [number] ["новостей"]

    Parameters
    ----------
    number : int
        Number
    noun_forms : list
        Declensions of noun
    prefix_forms : list
        Declensions of prefix word
    grouping_symbol : str
        Digit grouping symbol

    Returns
    -------
    str
        Phrase with correct declensions [prefix word] [number] [noun]. 
        The digit grouping symbol is applied to the number.

    Examples
    -------
    >>> phrase_build(42)
    Опубликованы 42 новости

    >>> phrase_build(31, ['китов', 'кит', 'кита'], ['Спасены', 'Спасен'])
    Спасен 31 кит

    2021-07-26 (c) Nikolay Ganibaev
    """

    if prefix_forms is None:
        prefix_forms = ['Опубликованы', 'Опубликована']

    if noun_forms is None:
        noun_forms = ['новостей', 'новость', 'новости']

    n = f'{number:,}'.replace(',', grouping_symbol)
    form_prefix = 0
    form_noun = 2
    if (n[-1] == '0') or (n[-1] > '4') or ((len(n) > 1) and (n[-2] == '1')):
        form_noun = 0
    elif n[-1] == '1':
        form_prefix = 1
        form_noun = 1

    return f'{prefix_forms[form_prefix]} {n} {noun_forms[form_noun]}'.strip()

def read_urls_contents(urls_list, max_workers=10, session=None, parser=None, encoding=None, *, 
    max_retries=None, timeout=None, error_page_output=None, mute=False):
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
        session.mount('http://', requests.HTTPAdapter(max_retries=max_retries))
        session.mount('https://', requests.HTTPAdapter(max_retries=max_retries))

    buf = StringIO()
    with pool.ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_load_csv = {executor.submit(url_loader, url, session, timeout, encoding): url for url in urls_list}
        for i, future in enumerate(pool.as_completed(future_load_csv)):
            if not mute:
                print(f"URLs list download: {PROGRESS_WHEEL[i%8]} {i/len(urls_list)*.994:.0%}",end='\r',flush=True)
            url = future_load_csv[future]
            try:
                buf.write(parser(future.result()))
            except Exception as exc:
                if error_page_output is None:
                    raise Exception(f'Download error:\n{url}|{exc}')
                else:
                    error_page_output.write(f'Download error:\n{url}|{exc}')
    buf.seek(0)
    return buf