"""Process that runs during Command-Line Interface usage"""

import datetime
import os
import logging
from pathlib import Path
import sys

from isoplot.main.dataprep import IsoplotData
from isoplot.ui.isoplotcli import IsoplotCli
from isoplot.ui.isoplot_notebook import check_version
import isoplot.logger

# noinspection PyBroadException
def main():
    # We start by checking the version of isoplot before cli initialization
    check_version('isoplot')
    cli = IsoplotCli()
    cli.initialize_cli()
    if not cli.args.galaxy:
        # Initialize path to root directory (directory containing data file)
        cli.home = Path(cli.args.input_path).parents[0]
        os.chdir(cli.home)
        # Get time and date for the run directory name
        now = datetime.datetime.now()
        date_time = now.strftime("%d%m%Y_%Hh%Mmn")
        # Initialize run name and run directory
        run_name = cli.args.run_name + "_" + date_time
        cli.run_home = cli.home / run_name
        cli.run_home.mkdir()
    # Prepare logger
    logger = logging.getLogger("isoplot_log.main.cli_process")
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # If not in galaxy instance, then we create file handler for the logger (Galaxy redirects stderr to file already)
    if not cli.args.galaxy:
        fhandle = logging.FileHandler(cli.run_home / "run_info.txt")  # Log run info to txt file
        fhandle.setFormatter(formatter)
        logger.addHandler(fhandle)
        if cli.args.verbose:
            fhandle.setLevel(logging.DEBUG)
        else:
            fhandle.setLevel(logging.INFO)
    handle = logging.StreamHandler()
    handle.setFormatter(formatter)
    logger.addHandler(handle)
    if cli.args.verbose:
        handle.setLevel(logging.DEBUG)
    else:
        handle.setLevel(logging.INFO)
    # Start work
    logger.debug("Generate Data Object")
    try:
        data = IsoplotData(cli.args.input_path, cli.args.verbose)
        data.get_data()
    except Exception as dataload_err:
        raise RuntimeError(f"Error while loading data. \n Error: {dataload_err}")
    if cli.args.generate_template:
        logger.debug("Generating template")
        try:
            data.generate_template()
        except Exception:
            logger.exception(f"There was an error while generating the template for the run {cli.args.run_name}.")
            sys.exit()
        else:
            logger.info(f"Template has been generated. Check destination folder at {cli.home}")
            sys.exit()
    if not cli.args.galaxy:
        os.chdir(cli.run_home)
    if hasattr(cli.args, 'template_path'):
        try:
            logger.debug("Loading template")
            data.get_template(cli.args.template_path)
            logger.debug("Merging data")
            data.merge_data()
            logger.debug("Preparing data")
            if cli.args.galaxy:
                data.prepare_data(export=False)  # Data export is sent through StringIO to stream
            else:
                data.prepare_data(export=True)
        except Exception:
            logger.exception("There was a problem while loading the template")
            sys.exit()
    # Get lists of parameters for plots
    try:
        cli.metabolites = IsoplotCli.get_cli_input(cli.args.metabolite, "metabolite", data)
        cli.conditions = IsoplotCli.get_cli_input(cli.args.condition, "condition", data)
        cli.times = IsoplotCli.get_cli_input(cli.args.time, "time", data)
    except Exception:
        logger.exception("There was an error while parsing cli input information")
    logger.info("-------------------------------")
    logger.info("Cli has been initialized. Parameters are as follows")
    logger.info(f"Run name: {cli.args.run_name}")
    logger.info(f"Input data path: {cli.args.input_path}")
    logger.info(f"Template path: {cli.args.template_path}")
    logger.info(f"Chosen format: {cli.args.format}")
    logger.info(f"Data to plot: {cli.args.value}")
    logger.info(f"Chosen metabolites: {cli.metabolites}")
    logger.info(f"Chosen conditions: {cli.conditions}")
    logger.info(f"Chosen times: {cli.times}")
    if hasattr(cli.args, 'z'):
        logger.info(f"Zip: {cli.args.zip}")
    logger.info("-------------------------------")
    logger.info("Creating plots...")
    try:
        if hasattr(cli.args, 'z'):
            cli.plot_figs(cli.metabolites, data, build_zip=True)
        else:
            cli.plot_figs(cli.metabolites, data)
    except Exception:
        logger.exception("There was a problem during the creation of the plots")
    else:
        logger.info("Plots created. Run is terminated")
        if not cli.args.galaxy:
            sys.exit()

if __name__ == "__main__":
    main()
