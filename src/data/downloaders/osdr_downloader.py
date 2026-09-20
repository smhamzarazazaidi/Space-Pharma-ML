"""NASA Open Science Data Repository (OSDR) Safe Downloader.

Responsible for retrieving verified study metadata and specific assay files
from the official NASA OSDR REST API endpoints.

Rules:
- Only download explicitly requested study IDs.
- Never overwrite existing raw files silently.
- Record download timestamps, file sizes, and HTTP response headers.
- Never download unverified bulk repositories.
"""

from datetime import datetime
import json
import logging
from pathlib import Path
from typing import Any, Dict, Optional
import urllib.request
import urllib.error

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

OSDR_API_BASE_URL = "https://osdr.nasa.gov/osdr/data/osd/meta"


def download_osdr_study_metadata(
    study_id: str,
    output_dir: Path = Path("data/raw/spaceflight_biological"),
    overwrite: bool = False,
) -> Optional[Path]:
    """Safely fetch metadata for a verified NASA OSDR study.

    Parameters
    ----------
    study_id : str
        The OSDR accession number (e.g., 'OSD-123' or '123').
    output_dir : Path, optional
        Destination folder for raw metadata file, by default 'data/raw/spaceflight_biological'.
    overwrite : bool, optional
        Whether to overwrite if file already exists (default is False to protect raw data).

    Returns
    -------
    Optional[Path]
        Path to the saved metadata file, or None if download failed or file exists.
    """
    clean_id = study_id.upper().replace("OSD-", "").replace("OSDR-", "")
    target_filename = f"OSDR_{clean_id}_metadata.json"
    target_path = output_dir / target_filename

    output_dir.mkdir(parents=True, exist_ok=True)

    if target_path.exists() and not overwrite:
        logger.warning(
            f"Raw file already exists at {target_path}. Skipping download to preserve raw data."
        )
        return target_path

    url = f"{OSDR_API_BASE_URL}/{clean_id}"
    logger.info(f"Connecting to official NASA OSDR endpoint: {url}")

    try:
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Space-Pharmacology-Research-Agent/0.1 (Academic Open Science)",
                "Accept": "application/json",
            },
        )
        with urllib.request.urlopen(req, timeout=30) as response:
            if response.status != 200:
                logger.error(f"Failed to fetch metadata for OSDR-{clean_id}. HTTP {response.status}")
                return None

            payload = json.loads(response.read().decode("utf-8"))
            
            # Enrich payload with download provenance
            payload["_download_provenance"] = {
                "download_timestamp_utc": datetime.utcnow().isoformat(),
                "source_url": url,
                "study_id": f"OSD-{clean_id}",
            }

            with open(target_path, "w", encoding="utf-8") as f:
                json.dump(payload, f, indent=2)

            file_size = target_path.stat().st_size
            logger.info(
                f"Successfully downloaded metadata for OSD-{clean_id} -> {target_path} ({file_size} bytes)"
            )
            return target_path

    except urllib.error.HTTPError as e:
        logger.error(f"HTTP Error {e.code} while fetching OSD-{clean_id}: {e.reason}")
    except urllib.error.URLError as e:
        logger.error(f"Network / URL error for OSD-{clean_id}: {e.reason}")
    except Exception as e:
        logger.error(f"Unexpected error downloading OSD-{clean_id}: {str(e)}")

    return None


# TODO (Phase 1 Dataset Audit):
# 1. Implement download_osdr_assay_file(study_id, file_name, destination)
# 2. Implement automated checksum validation via src.data.validators.file_validator
