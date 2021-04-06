import csv

import pandas as pd

from courier.config import CourierConfig

CONFIG = CourierConfig()


def get_overlapping_pages(article_index: pd.DataFrame) -> pd.DataFrame:
    df_pages = article_index[["courier_id", "record_number", "pages"]].explode("pages")
    page_count = df_pages.groupby(["courier_id", "pages"]).size()
    page_count = page_count.reset_index()
    page_count.columns = ["courier_id", "pages", "count"]
    overlapping_pages = page_count[page_count["count"] > 1]
    overlapping_pages = overlapping_pages.rename(columns={"pages": "page"})
    return overlapping_pages


def save_overlapping_pages(overlap_df: pd.DataFrame) -> None:
    overlap_df.to_csv(CONFIG.overlapping_pages, sep="\t", index=False, quoting=csv.QUOTE_NONNUMERIC)


def create_copy_script(overlap_df: pd.DataFrame, output_folder: str = './tmp') -> None:
    overlap_df["#!/bin/bash"] = overlap_df.apply(
        lambda x: f'cp {int(x["courier_id"]):06}eng*_{x["page"]:04}.txt {output_folder}', axis=1
    )
    d = overlap_df["#!/bin/bash"]
    d.to_csv(CONFIG.project_root / 'courier/scripts/copy_overlapping_pages.sh', index=False, header='#!/bin/bash')


# MISSING - Becasuse pdf-sources are missing
# 372603eng*_0012.txt'
# 367693eng*_0018.txt'
# 059709eng*_0024.txt'
# 059709eng*_0011.txt'
# 059709eng*_0007.txt'
