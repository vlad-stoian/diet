# -*- coding: utf-8 -*-

__version__ = "1.0.0"

import os
import yaml
import zipfile
import argparse
import tempfile
import logging


def main():
    """Minifies the pivotal file"""
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


    parser = argparse.ArgumentParser()

    parser.add_argument("--input", help="the .pivotal tile path", required=True)
    parser.add_argument("--output", help="the .pivotal tile path", required=True)
    args = parser.parse_args()
    tile_path = args.input

    logging.debug("Tile path: %s", tile_path)

    initial_size = os.path.getsize(tile_path)
    logging.info("Initial size: %d MB", initial_size >> 20)

    jobs_used = {}

    with tempfile.TemporaryDirectory() as temp_dir:
        logging.debug("Temp dir: %s", temp_dir)
        with zipfile.ZipFile(tile_path) as tile_zip:
            tile_zip.extractall(temp_dir)

        top_level_files = os.listdir(temp_dir)
        logging.debug("Extracted file: %s", top_level_files)

        releases_path = os.path.join(temp_dir, 'releases')
        release_tgzs = os.listdir(releases_path)
        logging.debug("Releases: %s", release_tgzs)

        product_manifest_path = os.path.join(temp_dir, 'product.MF')
        with open(product_manifest_path, 'r') as product_manifest_file:
            product_manifest = yaml.load(product_manifest_file)
            logging.debug("Manifest: %s", product_manifest)

        product_metadata_path = os.path.join(temp_dir, 'metadata', 'p_rabbitmq.yml') # TODO: don't hardcode
        with open(product_metadata_path, 'r') as product_metadata_file:
            product_metadata = yaml.load(product_metadata_file)
            # logging.debug("Metadata: %s", product_metadata)
        for job_type in product_metadata["job_types"]:
            for template in job_type["templates"]:
                jobs_used.setdefault(template["release"], []).append(template['name'])

        logging.debug("Jobs used: %s", jobs_used)

        for release_tgz_path in release_tgzs:
            print(release_tgz_path)


