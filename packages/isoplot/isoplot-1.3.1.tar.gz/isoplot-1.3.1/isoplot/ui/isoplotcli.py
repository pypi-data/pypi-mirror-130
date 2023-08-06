"""Module containing the CLI class that will be used during the cli process to get arguments from user and
generate the desired plots"""
import logging
import os
import argparse
import zipfile
import io

from bokeh.resources import CDN
from bokeh.embed import file_html

from isoplot.main.plots import StaticPlot, InteractivePlot, Map
import isoplot.logger

mod_logger = logging.getLogger("isoplot_log.ui.isoplotcli")


def parse_args():
    """
    Parse arguments from user input.

    :return: Argument Parser object
    :rtype: class: argparse.ArgumentParser
    """

    parser = argparse.ArgumentParser("Isoplot2: Plotting isotopic labelling MS data")

    parser.add_argument('input_path', help="Path to datafile")
    parser.add_argument("run_name", help="Name of the current run")
    parser.add_argument("format", help="Format of generated file")
    values = ['corrected_area', 'isotopologue_fraction', 'mean_enrichment']
    parser.add_argument('--value', choices=values, default='isotopologue_fraction',
                        action="store", required=True, nargs='*',
                        help="Select values to plot. This option can be given multiple times")
    parser.add_argument('-m', '--metabolite', default='all',
                        help="Metabolite(s) to plot. For all, type in 'all' ")
    parser.add_argument('-c', '--condition', default='all',
                        help="Condition(s) to plot. For all, type in 'all' ")
    parser.add_argument('-t', '--time', default='all',
                        help="Time(s) to plot. For all, type in 'all' ")
    parser.add_argument("-gt", "--generate_template", action="store_true",
                        help="Generate the template using datafile metadata")
    parser.add_argument("-tp", "--template_path", type=str,
                        help="Path to template file")
    parser.add_argument('-sa', '--stacked_areaplot', action="store_true",
                        help='Create static stacked areaplot')
    parser.add_argument("-bp", "--barplot", action="store_true",
                        help='Create static barplot')
    parser.add_argument('-mb', '--meaned_barplot', action="store_true",
                        help='Create static barplot with meaned replicates')
    parser.add_argument('-IB', '--interactive_barplot', action="store_true",
                        help='Create interactive stacked barplot')
    parser.add_argument('-IM', '--interactive_meanplot', action="store_true",
                        help='Create interactive stacked barplot with meaned replicates')
    parser.add_argument('-IS', '--interactive_areaplot', action="store_true",
                        help='Create interactive stacked areaplot')
    parser.add_argument('-hm', '--static_heatmap', action="store_true",
                        help='Create a static heatmap using mean enrichment data')
    parser.add_argument('-cm', '--static_clustermap', action="store_true",
                        help='Create a static heatmap with clustering using mean enrichment data')
    parser.add_argument('-HM', '--interactive_heatmap', action="store_true",
                        help='Create interactive heatmap using mean enrichment data')
    parser.add_argument('-s', '--stack', action="store_false",
                        help='Add option if barplots should be unstacked')
    parser.add_argument('-v', '--verbose', action="store_true",
                        help='Turns logger to debug mode')
    parser.add_argument('-a', '--annot', action='store_true',
                        help='Add option if annotations should be added on maps')
    parser.add_argument('-z', '--zip', type=str,
                        help="Add option & path to export plots in zip file")
    parser.add_argument('-g', '--galaxy', action='store_true',
                        help='Option for galaxy integration. Not useful for local usage')
    return parser


class IsoplotCli:

    def __init__(self, home=None, run_home=None, static_plot=None, int_plot=None, maps=None, args=None):

        self.parser = parse_args()
        self.home = home
        self.run_home = run_home
        self.static_plot = static_plot
        self.int_plot = int_plot
        self.maps = maps
        self.args = args
        self.metabolites = []
        self.conditions = []
        self.times = []
        self.logger = logging.getLogger("isoplot_log.ui.isoplotcli.IsoplotCli")

    def dir_init(self, plot_type):
        """Initialize directory for plot"""
        wd = self.run_home / plot_type
        if os.path.exists(wd):
            os.chdir(wd)
        else:
            wd.mkdir()
            os.chdir(wd)

    def go_home(self):
        """Exit after work is done"""
        os.chdir(self.home)

    @staticmethod
    def get_cli_input(arg, param, data_object):
        """
        Function to get input from user and check for errors in spelling.
        If an error is detected input is asked once more.
        This function is used for galaxy implementation

        :param arg: list from which strings must be parsed
        :param param: name of what we are looking for
        :type param: str
        :param data_object: IsoplotData object containing final clean dataframe
        :type data_object: class: 'isoplot.dataprep.IsoplotData'

        :return: Desired string after parsing
        :rtype: list

        """

        if arg == "all":
            desire = data_object.dfmerge[param].unique()
        else:
            is_error = True
            while is_error:
                try:
                    # Cli gives list of strings, se we must make words of them
                    desire = [item for item in arg.split(",")]
                    # Checking input for typos
                    for item in desire:
                        if item == "all":
                            break
                        else:
                            if item not in data_object.dfmerge[param].unique():
                                raise KeyError(f"One or more of the chosen {param}(s) were not in list. "
                                               f"Please check and try again. Error: {item}")
                except Exception as e:
                    raise RuntimeError(f"There was a problem while reading input. Error: {e}")

                else:
                    is_error = False
        return desire

    def zip_export(self, figures, zip_file_name):
        """
        Function to save figures in figure list to zip file (taken from
        https://stackoverflow.com/questions/55616877/save-multiple-objects-to-zip-directly-from-memory-in-python)

        :param figures: storage of figures and their respective file names in tuples: (name, fig)
        :type figures: list of tuples
        :param zip_file_name: name of the exported zip file
        :type zip_file_name: str
        """

        self.logger.info(f"Creating archive: {zip_file_name}")
        with zipfile.ZipFile(zip_file_name, mode="w") as zf:
            for fig_name, fig in figures:
                if fig_name.endswith("svg"):
                    buf = io.BytesIO()
                    fig.savefig(buf, format="svg")
                elif fig_name.endswith("html"):
                    html = file_html(fig, CDN, fig_name)
                    buf = io.StringIO(html)
                else:
                    buf = io.BytesIO()
                    fig.savefig(buf)
                self.logger.info(f"Writing image {fig_name} in the archive")
                zf.writestr(fig_name, buf.getvalue())

    def plot_figs(self, metabolite_list, data_object, build_zip=False):
        """
        Function to control which plot methods are called depending on the
        arguments that were parsed

        :param metabolite_list: metabolites to be plotted
        :type metabolite_list: list of str
        :param data_object: object containing the prepared data
        :type data_object: class: 'isoplot.main.dataprep.IsoplotData'
        :param build_zip: should figures be returned and exported in zip
        :type build_zip: bool
        """

        if build_zip:
            figures = []

        for metabolite in metabolite_list:
            for value in self.args.value:
                self.static_plot = StaticPlot(self.args.stack, value, data_object.dfmerge,
                                              self.args.run_name, metabolite, self.conditions, self.times,
                                              self.args.format, display=False, rtrn=build_zip)

                self.int_plot = InteractivePlot(self.args.stack, value, data_object.dfmerge,
                                                self.args.run_name, metabolite, self.conditions, self.times,
                                                display=False, rtrn=build_zip)

                # STATIC PLOTS
                if self.args.stacked_areaplot:
                    plot_name = "Static_Areaplots"
                    if build_zip:
                        fig = self.static_plot.stacked_areaplot()
                        fname = plot_name + "_" + self.static_plot.static_fig_name
                        figures.append((fname, fig))
                    else:
                        self.dir_init(plot_name)
                        self.static_plot.stacked_areaplot()
                if self.args.barplot and not (value == "mean_enrichment"):
                    plot_name = "Static_barplots"
                    if build_zip:
                        fig = self.static_plot.barplot()
                        fname = plot_name + "_" + self.static_plot.static_fig_name
                        figures.append((fname, fig))
                    else:
                        self.dir_init(plot_name)
                        self.static_plot.barplot()
                if self.args.meaned_barplot and not (value == "mean_enrichment"):
                    plot_name = "Static_barplots_SD"
                    if build_zip:
                        fig = self.static_plot.mean_barplot()
                        fname = plot_name + "_" + self.static_plot.static_fig_name
                        figures.append((fname, fig))
                    else:
                        self.dir_init(plot_name)
                        self.static_plot.mean_barplot()
                if self.args.barplot and (value == "mean_enrichment"):
                    plot_name = "Static_barplots"
                    if build_zip:
                        fig = self.static_plot.mean_enrichment_plot()
                        fname = plot_name + "_" + self.static_plot.static_fig_name
                        figures.append((fname, fig))
                    else:
                        self.dir_init(plot_name)
                        self.static_plot.mean_enrichment_plot()
                if self.args.meaned_barplot and (value == "mean_enrichment"):
                    plot_name = "Static_barplots_SD"
                    if build_zip:
                        fig = self.static_plot.mean_enrichment_meanplot()
                        fname = plot_name + "_" + self.static_plot.static_fig_name
                        figures.append((fname, fig))
                    else:
                        self.dir_init(plot_name)
                        self.static_plot.mean_enrichment_meanplot()
                # INTERACTIVE PLOTS
                if self.args.interactive_barplot and not (value == "mean_enrichment"):
                    plot_name = "Interactive_barplots"
                    if build_zip:
                        fig = self.int_plot.stacked_barplot()
                        fname = plot_name + "_" + self.int_plot.filename
                        figures.append((fname, fig))
                    else:
                        self.dir_init(plot_name)
                        self.int_plot.stacked_barplot()
                if self.args.interactive_barplot and not self.args.stack:
                    plot_name = "Interactive_unstacked_barplots"
                    if build_zip:
                        fig = self.int_plot.unstacked_barplot()
                        fname = plot_name + "_" + self.int_plot.filename
                        figures.append((fname, fig))
                    else:
                        self.dir_init(plot_name)
                        self.int_plot.unstacked_barplot()
                if self.args.interactive_meanplot and not (value == "mean_enrichment"):
                    plot_name = "Interactive_barplots_SD"
                    if build_zip:
                        fig = self.int_plot.stacked_meanplot()
                        fname = plot_name + "_" + self.int_plot.filename
                        figures.append((fname, fig))
                    else:
                        self.dir_init(plot_name)
                        self.int_plot.stacked_meanplot()
                if self.args.interactive_meanplot and not self.args.stack:
                    plot_name = "Interactive_barplots_SD"
                    if build_zip:
                        fig = self.int_plot.unstacked_meanplot()
                        fname = plot_name + "_" + self.int_plot.filename
                        figures.append((fname, fig))
                    else:
                        self.dir_init(plot_name)
                        self.int_plot.unstacked_meanplot()
                if self.args.interactive_barplot and (value == "mean_enrichment"):
                    plot_name = "Interactive_barplots"
                    if build_zip:
                        fig = self.int_plot.mean_enrichment_plot()
                        fname = plot_name + "_" + self.int_plot.filename
                        figures.append((fname, fig))
                    else:
                        self.dir_init(plot_name)
                        self.int_plot.mean_enrichment_plot()
                if self.args.interactive_meanplot and (value == "mean_enrichment"):
                    plot_name = "Interactive_barplots_SD"
                    if build_zip:
                        fig = self.int_plot.mean_enrichment_meanplot()
                        fname = plot_name + "_" + self.int_plot.filename
                        figures.append((fname, fig))
                    else:
                        self.dir_init(plot_name)
                        self.int_plot.mean_enrichment_meanplot()
                if self.args.interactive_areaplot:
                    plot_name = "Interactive_stackplots"
                    if build_zip:
                        fig = self.int_plot.stacked_areaplot()
                        fname = plot_name + "_" + self.int_plot.filename
                        figures.append((fname, fig))
                    else:
                        self.dir_init(plot_name)
                        self.int_plot.stacked_areaplot()
        # MAPS
        self.maps = Map(data_object.dfmerge, self.args.run_name, self.args.annot, self.args.format, rtrn=build_zip)
        if self.args.static_heatmap:
            plot_name = "static_heatmap"
            if build_zip:
                fig = self.maps.build_heatmap()
                fname = plot_name + f".{self.maps.fmt}"
                figures.append((fname, fig))
            else:
                self.dir_init(plot_name)
                self.maps.build_heatmap()
        if self.args.static_clustermap:
            plot_name = "static_clustermap"
            if build_zip:
                fig = self.maps.build_clustermap()
                fname = plot_name + f".{self.maps.fmt}"
                figures.append((fname, fig))
            else:
                self.dir_init(plot_name)
                self.maps.build_clustermap()
        if self.args.interactive_heatmap:
            self.maps.fmt = "html"
            plot_name = "interactive_heatmap"
            if build_zip:
                fig = self.maps.build_interactive_heatmap()
                fname = plot_name + f".{self.maps.fmt}"
                figures.append((fname, fig))
            else:
                self.dir_init(plot_name)
                self.maps.build_interactive_heatmap()
        if build_zip:
            self.zip_export(figures, self.args.zip)
        if not self.args.galaxy:
            self.go_home()

    def initialize_cli(self):
        """Launch argument parsing and perform checks"""

        self.args = self.parser.parse_args()
        handle = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handle.setFormatter(formatter)
        if self.args.verbose:
            handle.setLevel(logging.DEBUG)
        else:
            handle.setLevel(logging.INFO)
        self.logger.addHandler(handle)

        # Check for typos and input errors
        valid_formats = ['png', 'svg', 'pdf', 'jpeg', 'html']
        forbidden_characters = ["*", ".", '"', "/", "\\", "[", "]", ":", ";", "|", ","]

        if not os.path.exists(self.args.input_path):
            raise RuntimeError(f"Input path does not lead to valid file. "
                               f"Please check path: {self.args.input_path}")

        if self.args.format not in valid_formats:
            raise RuntimeError("Format must be png, svg, pdf, jpeg or html")

        for char in forbidden_characters:
            if char in self.args.run_name:
                raise RuntimeError(f"Invalid character in run name. "
                                   f"Forbidden characters are: {forbidden_characters}")

        if self.args.template_path and not os.path.exists(self.args.template_path):
            raise RuntimeError(f"Template path does not lead to valid file. "
                               f"Please check path: {self.args.template_path}")
