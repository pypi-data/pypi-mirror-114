from ..utils.cli import CommandWithPlugins


class SumStatsCommand(CommandWithPlugins):
    """Compute summary statistics on a simulation data set."""

    logging = True

    @classmethod
    def create_argument_parser(cls, namespace=None):
        parser = super().create_argument_parser(namespace=namespace)
        parser.add_argument('--loglevel',
                             default='INFO',
                             action='store',
                             type=str,
                             metavar='INFO',
                             help='Amount of log info: DEBUG, [INFO], '
                                  'WARNING, ERROR, CRITICAL')
        parser.add_argument('--n-cpus', type=int)
        parser.add_argument('--n-replicates', type=int,
                help='only compute summary statistics over up to N replicates '
                     'per scenario, instead of over all replicates, which '
                     'can speed up the calculation')
        parser.add_argument('--overwrite', action='store_true',
                help='overwrite existing summary statistics for this dataset; '
                     'otherwise new statistics are appended to the existing '
                     'statistics (TODO: what is the purpose of appending? '
                     'is that actually useful?)')
        parser.add_argument('--label', default='',
                help='plain text label appended to every row of summary '
                     'statistics output tables, which can be used to '
                     'distinguish individaul sumstats runs')
        parser.add_argument('config', help='path to the simulation config file')
        return parser

    @classmethod
    def run(cls, args):
        from ..summary_statistics import SummaryStatistics

        summary_statistics = SummaryStatistics.from_config_file(args.config,
                plugins=args.plugins)
        summary_statistics.run(n_replicates=args.n_replicates,
                               label=args.label, n_cpus=args.n_cpus,
                               raise_exc=args.debug, overwrite=args.overwrite,
                               progress_bar=True)

        # TODO: Have an option to write plots as well...?
        # #os.chdir(args.save_path + '/' + config['name'])
        # pattern = re.compile('.*' + config['name'] + '_|_[0-9]*.npz$')
        # file_paths = glob.glob('*/*.npz')
        # name_ids = np.unique([re.sub(pattern, '', f)for f in file_paths])
        # print(name_ids)
        # for name_id in name_ids:
        #     do_sum_stats(name_id, config['name'],
        #                  size_chr=config['segment_length'], circular=False)
        # df_sfs, df_ld = load_sum_stats(config['name'])
        # plot_sfs(df_sfs, config['name'])
        # plt.savefig(config['name'] + "_sfs")
        # plot_ld(df_ld, config['name'])
        # plt.savefig(config['name'] + "_ld")
