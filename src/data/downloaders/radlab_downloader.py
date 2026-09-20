"""NASA RadLab Space Radiation Data Safe Downloader.

Responsible for retrieving verified telemetry, dosimeter logs, and environmental
dosimetry datasets from official NASA RadLab / Open Science endpoints.

Rules:
- Only download explicitly requested mission intervals or detector datasets.
- Never overwrite existing raw files silently.
- Record download timestamps, file sizes, and HTTP response status.
"""

from datetime import datetime
import logging
from pathlib import Path
from typing import Optional
import urllib.request
import urllib.error

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def download_radlab_dataset(
    dataset_url: str,
    output_filename: str,
    output_dir: Path = Path("data/raw/space_radiation"),
    overwrite: bool = False,
) -> Optional[Path]:
    """Safely download an audited radiation telemetry or dosimeter file from NASA RadLab.

    Parameters
    ----------
    dataset_url : str
        The official, verified download URL for the dataset file.
    output_filename : str
        Standardized local filename.
    output_dir : Path, optional
        Destination directory, by default 'data/raw/space_radiation'.
    overwrite : bool, optional
        Whether to overwrite if file already exists, default is False.

    Returns
    -------
    Optional[Path]
        Path to the saved raw radiation file, or None if failed.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    target_path = output_dir / output_filename

    if target_path.exists() and not overwrite:
        logger.warning(
            f"Raw radiation file already exists at {target_path}. Skipping to preserve raw data."
        )
        return target_path

    logger.info(f"Initiating verified download from: {dataset_url}")

    try:
        req = urllib.request.Request(
            dataset_url,
            headers={
                "User-Agent": "Space-Pharmacology-Research-Agent/0.1 (Academic Open Science)"
            },
        )
        with urllib.request.urlopen(req, timeout=60) as response:
            if response.status != 200:
                logger.error(f"Download failed from {dataset_url}. HTTP Status: {response.status}")
                return None

            content = response.read()
            with open(target_path, "wb") as f:
                f.write(content)

            file_size = target_path.stat().st_size
            logger.info(
                f"Successfully downloaded radiation dataset -> {target_path} ({file_size} bytes)"
            )
            return target_path

    except urllib.error.HTTPError as e:
        logger.error(f"HTTP Error {e.code} downloading from {dataset_url}: {e.reason}")
    except urllib.error.URLError as e:
        logger.error(f"Network error downloading from {dataset_url}: {e.reason}")
    except Exception as e:
        logger.error(f"Unexpected error downloading radiation dataset: {str(e)}")

    return None


# TODO (Phase 1 Dataset Audit):
# 1. Implement RadLab query builder by mission dates and ISS module coordinates
# 2. Implement automated CSV header inspection and dosimeter detector type validation
