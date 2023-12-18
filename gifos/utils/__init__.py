"""This module initializes the gifos.utils package and provides access to its functions.

The gifos.utils package contains utility functions for the gifos application. These
functions include `calc_age`, `calc_github_rank`, `fetch_github_stats`, and
`upload_imgbb`.
"""

from gifos.utils.calc_age import calc_age
from gifos.utils.calc_github_rank import calc_github_rank
from gifos.utils.fetch_github_stats import fetch_github_stats
from gifos.utils.upload_imgbb import upload_imgbb

__all__ = ["calc_age", "calc_github_rank", "fetch_github_stats", "upload_imgbb"]
