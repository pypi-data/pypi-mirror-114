import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

from flask_scenario_testing.analysis.report_sections.ReportSection import ReportSection
from flask_scenario_testing.analysis.services.ComputeTransactionSignature import ComputeTransactionSignature
import json


class PlotTransactionSignatures(ReportSection):
    def __init__(self, service: ComputeTransactionSignature, options):
        ReportSection.__init__(self)
        self.color_idx = 0
        self.service = service

    def print(self, _) -> None:
        signatures = [(scenario, self.service.compute_signature(scenario)) for scenario in self.service.scenarios()]

        result = []

        for idx, service_time in enumerate(signatures[0][1]):
            result.append(dict(
                name=service_time.endpoint_name,
                old_service_time=service_time.value,
                new_service_time=signatures[1][1][idx].value
            ))

        print(json.dumps(result, indent=2))
        print(result)
        exit(-1)

        # self.plot_absolute_signatures(signatures)
        # self.plot_relative_signatures(signatures, show_percents=False)
        self.plot_recall_and_precision(signatures)
        # self.plot_relative_signatures(signatures, show_percents=True)

    def plot_absolute_signatures(self, signatures):
        figure = plt.figure()
        ax = plt.gca()
        ax.grid(True, which='both')

        plt.title('Transaction signatures (absolute)')

        for scenario, signature in signatures:
            plt.gcf().subplots_adjust(bottom=0.5)
            plt.xticks(rotation=80)
            plt.plot([s.endpoint_name for s in signature], [s.value for s in signature], label=scenario.name())

        plt.xlabel('Endpoint')
        plt.legend()
        self.add_figure(figure)

    def plot_relative_signatures(self, signatures, show_percents=False):
        figure = plt.figure()
        ax = plt.gca()
        ax.grid(True, which='both')

        base_scenario, base_signature = signatures[0]

        for scenario, signature in signatures[1:-1]:
            plt.gcf().subplots_adjust(bottom=0.5)
            plt.xticks(rotation=80)
            x_values = [s.endpoint_name for s in signature]

            if not show_percents:
                plt.title('Transaction signatures (absolute difference)')

                ax = plt.gca()
                ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: '{}ms'.format(x)))
                y_values = [s.value - base_signature[idx].value for idx, s in enumerate(signature)]
            else:
                plt.title('Transaction signatures (percentual difference)')

                ax = plt.gca()
                ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: '{}%'.format(x)))
                y_values = [(s.value - base_signature[idx].value) / base_signature[idx].value * 100 for idx, s in
                            enumerate(signature)]

            plt.plot(x_values, y_values, label=scenario.name())

        plt.xlabel('Endpoint')
        plt.legend()
        self.add_figure(figure)

    def plot_recall_and_precision(self, signatures):
        figure = plt.figure()
        signature1 = signatures[0][1]
        signature2 = signatures[1][1]

        diffs = []
        for i, service_time_1 in enumerate(signature1):
            diff = service_time_1.value - signature2[i].value
            diffs.append(diff)

        start = min(diffs) - 10
        end = max(diffs) + 10

        x_values = []
        false_positive_counts = []
        while start < end:
            x_values.append(start)
            false_positive_count = 0
            for i, service_time_1 in enumerate(signature1):
                diff = service_time_1.value - signature2[i].value

                if diff > start and service_time_1.endpoint_name != 'api.add_user':
                    false_positive_count += 1

            false_positive_counts.append(false_positive_count)
            start += 1

        plt.plot(x_values, false_positive_counts)
        self.add_figure(figure)
