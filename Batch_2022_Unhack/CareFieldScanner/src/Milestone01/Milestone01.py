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

    logger.info("Opening the input CF file {}".format(filename))
    with open(filename, 'r') as f:
        logger.info("Opened the input CF file {}".format(filename))
        for line in f.readlines():
            line = line.strip()
            cfId, xMin, xMax, yMin, yMax = line.split(",")
            careFields.append(CareField(float(cfId), float(xMin), float(xMax), float(yMin), float(yMax)))

    logger.info("Complete the careField parser")
    return careFields


def metadataParser(filename: str) -> List[MetaData]:
    metaData: List[MetaData] = []
    logger.info("Opening the input metadata file {}".format(filename))

    with open(filename, 'r') as f:
        logger.info("Opened the input metadata file {}".format(filename))
        f.readline()
        for line in f.readlines():
            line = line.strip()
            mfs, sfs = line.split(",")
            metaData.append(MetaData(float(mfs), float(sfs)))

    logger.info("Complete the metadata parser")
    return metaData


def mfCoverage(mf: MainField, cf: CareField) -> bool:
    print(mf)
    print(cf)
    if (mf.xMin <= cf.xMin and
            mf.yMin <= cf.yMin and
            mf.xMax >= cf.xMax and
            mf.yMax >= cf.yMax):

        return True
    else:
        return False


def main() -> None:

    cf_file = "../../MilestoneInput/01/CareAreas.csv"
    md_file = "../../MilestoneInput/01/metadata.csv"

    careFields = careFieldParser(cf_file)
    metadata = metadataParser(md_file)

    MFS = metadata[0].mfSize
    logger.debug(f"MFS: {MFS}")

    SFS = metadata[0].sfSize
    logger.debug(f"SFS: {SFS}")

    for cf in careFields:
        logger.debug(f"CF: {cf}")

    cf = careFields[0]
    xmin = cf.xMin
    xmax = xmin + MFS
    ymin = cf.yMin
    ymax = ymin + MFS

    mainFields = [MainField(0.0, xmin, xmax, ymin, ymax)]
    subFields = []
    mcnt = 0.0
    scnt = 0.0

    for cf in careFields:
        logger.debug(f"CF: {cf}")
        if not mfCoverage(mainFields[-1], cf):
            mcnt += 1.0
            mainFields.append(
                MainField(mcnt, cf.xMin, cf.xMin + MFS, cf.yMin, cf.yMin + MFS)
            )

        sfsyMin = cf.yMin
        while sfsyMin < cf.yMax:
            sfsyMax = sfsyMin + SFS
            sfsxMin = cf.xMin
            while sfsxMin < cf.xMax:
                sfsxMax = sfsxMin + SFS
                scnt += 1.0
                subFields.append(
                    SubField(scnt, sfsxMin, sfsxMax, sfsyMin, sfsyMax, mcnt)
                )
                sfsxMin += SFS  # Move to the next SubField horizontally
            sfsyMin += SFS

    output_file = "../../MilestoneOutput/Milestone01/mainfields.csv"
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    s_output_file = "../../MilestoneOutput/Milestone01/subfields.csv"
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        for mf in mainFields:
            writer.writerow([mf.id, mf.xMin, mf.xMax, mf.yMin, mf.yMax])

    with open(s_output_file, 'w', newline='') as af:
        writer = csv.writer(af)
        for sf in subFields:
            writer.writerow([sf.id, sf.xMin, sf.xMax, sf.yMin, sf.yMax, sf.mf])

    logger.info("MainField generation complete. Results saved to {}".format(output_file))
    logger.info("SubField generation complete")


if __name__ == "__main__":
    main()
