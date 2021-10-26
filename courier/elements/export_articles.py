# pylint: disable=redefined-outer-name
import os
import re
from pathlib import Path
from typing import Any, Dict, List, Union

import pandas as pd
from loguru import logger

from courier.article_index import article_index_to_csv
from courier.config import get_config
from courier.elements.assign_page_service import AssignPageService
from courier.elements.consolidate_text_service import ConsolidateTextService
from courier.elements.elements import CourierIssue
from courier.elements.statistics import IssueStatistics
from courier.utils.logging import file_logger

CONFIG = get_config()


class ExtractArticles:
    @staticmethod
    def extract(issue: CourierIssue) -> CourierIssue:
        AssignPageService().assign(issue)
        ConsolidateTextService().consolidate(issue)
        return issue

    @staticmethod
    def statistics(issue: CourierIssue) -> IssueStatistics:
        return IssueStatistics(issue)


def export_articles(
    courier_id: str,
    export_folder: Union[str, os.PathLike] = CONFIG.articles_dir / 'exported',
) -> List[Dict[str, Any]]:

    issue: CourierIssue = CourierIssue(courier_id)
    ExtractArticles.extract(issue)

    Path(export_folder).mkdir(parents=True, exist_ok=True)

    for article in issue.articles:
        if article.catalogue_title is None:
            continue
        safe_title = re.sub(r'[^\w]+', '_', str(article.catalogue_title).lower())
        file = (
            Path(export_folder)
            / f'{article.year or "0000"}_{article.courier_id}_{article.record_number}_{safe_title[:60]}.txt'
        )

        logger.trace(
            f'{courier_id};{article.year};{article.record_number};{len(article.get_assigned_pages())};{len(article.get_not_found_pages())};{len(article.page_numbers)}'
        )

        with open(file, 'w', encoding='utf-8') as fp:
            fp.write(article.get_text())

    return IssueStatistics(issue).errors


if __name__ == '__main__':

    export_folder: Path = CONFIG.articles_dir / 'exported'
    article_index_to_csv(CONFIG.article_index, export_folder)
    stats: List[Dict[str, Any]] = []

    with file_logger(
        Path(export_folder) / 'extract_log.csv', format='{message}', level='TRACE'
    ) as logger:  # noqa: F811
        logger.trace('courier_id;year;record_number;assigned;not_found;total')

        courier_ids = [x[:6] for x in CONFIG.get_courier_ids()]
        for courier_id in courier_ids:
            if courier_id not in CONFIG.article_index.courier_id.values:
                if len(CONFIG.get_issue_article_index(courier_id)) != 0:
                    raise Exception(f'{courier_id} not in article index but has articles')
                continue
            stats += export_articles(courier_id, export_folder)

    pd.DataFrame(stats).to_csv(Path(export_folder) / 'stats.csv', sep=';')