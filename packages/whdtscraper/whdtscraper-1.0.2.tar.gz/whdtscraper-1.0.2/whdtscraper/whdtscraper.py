import re
import requests
from datetime import datetime, date, timedelta
from typing import Optional, Any, Union, Literal

WIKI_URL = 'https://dumps.wikimedia.org/other/mediawiki_history'


def _scrape(url: str, regex: str) -> list[str]:
    # do request
    response = requests.get(url)
    # get html response
    html = response.text
    # return extracted parts matching regex
    return re.findall(regex, html)


def _scrape_multiple(url: str, regex: str, groups: list[str]) -> dict[str, str]:
    # do request
    response = requests.get(url)
    # get html response
    html = response.text
    # return extracted parts matching regex
    matches = re.finditer(regex, html)
    return [
        {group: match.group(group) for group in groups}
        for match in matches
    ]


def fetch_latest_version(*, wikies: bool = False, lang: str = None, wikitype: str = None, dumps: bool = False, start: str = None, end: str = None) -> Optional[dict[str, Any]]:
    """Fetch the last version of the wikimedia history dump

    The version is the year-month of the release of the dumps

    Keyword parameters:
    wikies (bool, default=False): If for each returned version the wikies will be fetched
    lang (str, default=None): If the wikies argument is True, the language of the wikies to return (a wiki name starts with the language).
    wikitype (str, default=None): If the wikies argument is True, the wiki type of the wikies to return (a wiki name ends with the wiki type).
    dumps (bool, default=false): If for each returned wiki the wikies will be fetched
    start (date, default=None): If the wikies and dumps arguments are True, retrieve only the dumps newer than this date
    end (date, default=None): If the wikies and dumps arguments are True, retrieve only the dumps older than this date

    Returns:
    dict:   A dict with "version" (str) for the version year-month and "url" (str) for the url of that version.
            In addition, "wikies" will contain the fetched wikies if the argument was set to True.
            If no version is found, None is returned.
    """

    # assign url and regex
    url = WIKI_URL
    regex = r'<a href="(?P<version>\d+-\d+)\/">'
    # fetch versions
    versions = _scrape(url, regex)
    # if no version is found, return None
    if not versions:
        return None
    # get the last version
    versions.sort(reverse=True)
    last_version = versions[0]
    # get list of resulting objects
    result = {
        'version': last_version,
        'url': f'{url}/{last_version}'
    }
    # if include wikies, do it
    if wikies:
        result = [
            {
                **result,
                'wikies': fetch_wikies(result['version'], lang=lang, wikitype=wikitype, dumps=dumps, start=start, end=end)
            }
        ]
    # return result
    return result


def fetch_versions(*, wikies: bool = False, lang: str = None, wikitype: str = None, dumps: bool = False, start: str = None, end: str = None) -> list[dict[str, Any]]:
    """Fetch the versions of the wikimedia history dump

    The versions are the year-month of the release of the dumps

    Keyword parameters:
    wikies (bool, default=False): If for each returned version the wikies will be fetched
    lang (str, default=None): If the wikies argument is True, the language of the wikies to return (a wiki name starts with the language).
    wikitype (str, default=None): If the wikies argument is True, the wiki type of the wikies to return (a wiki name ends with the wiki type).
    dumps (bool, default=false): If for each returned wiki the wikies will be fetched
    start (date, default=None): If the wikies and dumps arguments are True, retrieve only the dumps newer than this date
    end (date, default=None): If the wikies and dumps arguments are True, retrieve only the dumps older than this date

    Returns:
    list:   A list of dicts with "version" (str) for the version year-month and "url" (str) for the url of that version.
            In addition, "wikies" will contain the fetched wikies if the argument was set to True.
    """

    # assign url and regex
    url = WIKI_URL
    regex = r'<a href="(?P<version>\d+-\d+)\/">'
    # fetch versions
    versions = _scrape(url, regex)
    # sort versions by descending order
    versions.sort(reverse=True)
    # get list of resulting objects
    result = [{
        'version': version,
        'url': f'{url}/{version}'
    } for version in versions]
    # if include wikies, do it
    if wikies:
        result = [
            {
                **version,
                'wikies': fetch_wikies(version['version'], lang=lang, wikitype=wikitype, dumps=dumps, start=start, end=end)
            } for version in result
        ]
    # return result
    return result


def fetch_wikies(version: str, /, *, lang: Optional[str] = None, wikitype: Optional[str] = None, dumps: bool = False, start: str = None, end: str = None) -> list[dict[str, Any]]:
    """Fetch the wikies of a version of the wikimedia history dump

    Parameters:
    version (str): The version whose wikies will be returned. If "latest" is passed, the latest version is retrieved.

    Keyword parameters:
    lang (str, default=None): The language of the wikies to return (a wiki name starts with the language).
    wikitype (str, default=None): The wiki type of the wikies to return (a wiki name ends with the wiki type).
    dumps (bool, default=false): If for each returned wiki the dumps will be fetched
    start (date, default=None): If the dumps argument is True, retrieve only the dumps newer than this date
    end (date, default=None): If the dumps argument is True, retrieve only the dumps older than this date

    Returns:
    list:   A list of dicts with "wiki" (str) for the wiki name and "url" (str) for the url of that wiki.
            In addition, if the "dumps" argument is True, a "dumps" (list) field contain the fetched dumps.
    """
    # if version is "latest", get the latest version
    version = fetch_latest_version()['version'] if version == 'latest' else version
    # assign url and regex
    url = f'{WIKI_URL}/{version}'
    regex = r'<a href="(?P<wiki>\w+)\/">'
    # fetch wikies
    wikies = _scrape(url, regex)
    # get list of resulting objects
    result = [{
        'wiki': wiki,
        'url': f'{url}/{wiki}'
    } for wiki in wikies]
    # filter element by lang or wikitype
    if lang is not None:
        result = [wiki for wiki in result if wiki['wiki'].startswith(lang)]
    if wikitype is not None:
        result = [wiki for wiki in result if wiki['wiki'].endswith(wikitype)]
    # if include dumps, do it
    if dumps:
        result = [
            {
                **wiki,
                'dumps': fetch_dumps(version, wiki['wiki'], start=start, end=end)
            } for wiki in result
        ]
    # return result
    return result


def fetch_dumps(version: str, wiki: str, /, *, start: Optional[date] = None, end: Optional[date] = None) -> list[dict[str, Any]]:
    """Fetch the dumps of a wiki of the wikimedia history dump

    Parameters:
    version (str): The version of the wiki
    wiki (str): The wiki whose dumps will be returned

    Keyword parameters:
    start (date, default=None): Retrieve only the dumps newer than this date
    end (date, default=None): Retrieve only the dumps older than this date

    Returns:
    list:   A list of dicts with "filename" (str) for dump file name, "time" (str) for the time of the data ("all-time", year or year-month),
            "lastUpdate" (datetime) for the last update date, "bytes" (int) for the size in bytes of the file,
            "from" (date) for the start date of the data and "to (date) for the end date of the data, "url" (string) the url of the file.
    """

    def last_month_day(month: int):
        d = date(1999, (month % 12) + 1, 1) - timedelta(days=1)
        return d.day

    def parse_time(time: str) -> dict[Optional[Union[date, Literal['all-time']]]]:
        if (time == 'all-time'):
            return {'from': None, 'to': None}
        month_and_year = time.split('-')
        year = int(month_and_year[0])
        if len(month_and_year) > 1:
            month = int(month_and_year[1])
            return {'from': date(year, month, 1), 'to': date(year, month, last_month_day(month))}
        else:
            return {'from': date(year, 1, 1), 'to': date(year, 12, 31)}

    # if version is "latest", get the latest version
    version = fetch_latest_version()['version'] if version == 'latest' else version
    # assign url and regex
    url = f'{WIKI_URL}/{version}/{wiki}'
    regex = fr'<a href="(?P<filename>{version}\.{wiki}\.(?P<time>[\w\d-]+)\.tsv\.bz2)">.*</a>\s+(?P<lastUpdate>\d{{2}}-\w{{3}}-\d{{4}} \d{{2}}:\d{{2}})\s+(?P<bytes>\d+)'
    groups = ['filename', 'time', 'lastUpdate', 'bytes']
    # fetch dumps
    dumps = _scrape_multiple(url, regex, groups)
    # get list of resulting objects
    result = [{
        **dump,
        **parse_time(dump['time']),
        'lastUpdate': datetime.strptime(dump['lastUpdate'], '%d-%b-%Y %H:%M'),
        'url': f'{url}/{dump["filename"]}'
    } for dump in dumps]
    # filter element by start and end
    if start is not None:
        result = [dump for dump in result if dump['from'] is None or dump['from'] >= start]
    if end is not None:
        result = [dump for dump in result if dump['to'] is None or dump['to'] <= end]
    # return result
    return result
