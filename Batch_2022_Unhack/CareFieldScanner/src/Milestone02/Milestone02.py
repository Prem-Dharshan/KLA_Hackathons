import csv
import os
import sys
import logging
from typing import List

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.custom_logging import setup_logger
from src.ADT.CareField import CareField
from src.ADT.MainField import MainField
from src.ADT.SubField import SubField
from src.ADT.MetaData import MetaData

logger = setup_logger(level=logging.DEBUG)


def careFieldParser(filename: str) -> List[CareField]:
    careFields: List[CareField] = []

    logger.info(f"Starting to parse CareField data from {filename}")
    with open(filename, 'r') as f:
        for line in f.readlines():
            line = line.strip()
            cfId, xMin, xMax, yMin, yMax = line.split(",")
            careFields.append(CareField(float(cfId), float(xMin), float(xMax), float(yMin), float(yMax)))

    logger.info(f"Parsed {len(careFields)} CareFields from {filename}")
    return careFields


def metadataParser(filename: str) -> List[MetaData]:
    metaData: List[MetaData] = []

    logger.info(f"Starting to parse metadata from {filename}")
    with open(filename, 'r') as f:
        f.readline()  # Skip header
        for line in f.readlines():
            line = line.strip()
            mfs, sfs = line.split(",")
            metaData.append(MetaData(float(mfs), float(sfs)))

    logger.info(f"Parsed metadata: Main Field Size = {metaData[0].mfSize}, Sub Field Size = {metaData[0].sfSize}")
    return metaData


def mfCoverage(mf: MainField, cf: CareField) -> bool:
    """Check if a MainField completely covers a CareField."""
    return (mf.xMin <= cf.xMin and
            mf.yMin <= cf.yMin and
            mf.xMax >= cf.xMax and
            mf.yMax >= cf.yMax)


def main() -> None:

    cf_file = "../../MilestoneInput/02/CareAreas.csv"
    md_file = "../../MilestoneInput/02/metadata.csv"

    logger.info("Starting MainField and SubField generation process.")

    # Parse input files
    careFields = careFieldParser(cf_file)
    metadata = metadataParser(md_file)

    # Initialize metadata values
    MFS = metadata[0].mfSize
    SFS = metadata[0].sfSize
    logger.info(f"Using Main Field Size (MFS): {MFS}, Sub Field Size (SFS): {SFS}")

    # Initialize fields
    mainFields = []
    subFields = []
    mcnt = 0.0
    scnt = 0.0

    # Generate MainFields and SubFields
    logger.info("Starting field generation...")
    for cf in careFields:

        logger.debug(f"Processing CareField {cf.id} with bounds ({cf.xMin}, {cf.yMin}, {cf.xMax}, {cf.yMax})")

        covering_id = None
        for mf in mainFields:
            if mfCoverage(mf, cf):
                covering_id = mf.id
                break
        # covering_id = next((mf.id for mf in mainFields if mfCoverage(mf, cf)), None)

        if not covering_id:
            mcnt += 1.0
            new_mf = MainField(mcnt, cf.xMin, cf.xMin + MFS, cf.yMin, cf.yMin + MFS)
            mainFields.append(new_mf)
            logger.info(f"Created MainField {mcnt} covering bounds ({new_mf.xMin}, {new_mf.yMin}, {new_mf.xMax}, {new_mf.yMax})")
            covering_id = new_mf.id
        else:
            logger.debug(f"{cf} is covered by MainField {covering_id}.")

        sfxMin = cf.xMin
        sfyMin = cf.yMin
        curry = sfyMin

        while curry <= cf.yMax:
            currx = sfxMin
            while currx <= cf.xMax:
                subFields.append(SubField(scnt, currx, currx + SFS, curry, curry + SFS, covering_id))
                logger.info(f"Created SubField {subFields[-1]}")
                currx += SFS
                scnt += 1
            curry += SFS



    logger.info(f"Generated {len(mainFields)} MainFields and {len(subFields)} SubFields.")

    # Output files
    output_file = "../../MilestoneOutput/Milestone02/mainfields.csv"
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    s_output_file = "../../MilestoneOutput/Milestone02/subfields.csv"

    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        for mf in mainFields:
            writer.writerow([mf.id, mf.xMin, mf.xMax, mf.yMin, mf.yMax])
    logger.info(f"MainFields written to {output_file}")

    with open(s_output_file, 'w', newline='') as af:
        writer = csv.writer(af)
        for sf in subFields:
            writer.writerow([sf.id, sf.xMin, sf.xMax, sf.yMin, sf.yMax, sf.mf])
    logger.info(f"SubFields written to {s_output_file}")

    logger.info("Field generation process completed successfully.")


if __name__ == "__main__":
    main()
