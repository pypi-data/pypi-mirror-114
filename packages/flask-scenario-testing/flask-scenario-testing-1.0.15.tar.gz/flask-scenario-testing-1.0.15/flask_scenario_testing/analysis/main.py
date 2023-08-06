import argparse
import os
from datetime import timedelta

from matplotlib import pyplot as plt

from flask_scenario_testing.analysis.Results import Results
from flask_scenario_testing.analysis.report_sections.PlotTransactionSignatures import PlotTransactionSignatures
from flask_scenario_testing.analysis.segmenters.TimeWindowedSegmenter import TimeWindowedSegmenter
from flask_scenario_testing.analysis.services.ComputeTransactionSignature import ComputeTransactionSignature
from flask_scenario_testing.analysis.support.Averager import Averager
import psutil
import json


def main2():
    with open(os.path.abspath('data.json'), 'r') as f:
        runs = json.load(f)

        plt.figure()

        for run in runs:
            plt.figure()

            print('Processing {}'.format(run['name']))
            print(run['data'])

            diffs = []
            for item in run['data']:
                diffs.append(item['new_service_time'] - item['old_service_time'])

            threshold = min(diffs) - 10
            end = max(diffs) + 10
            all_false_positive_counts = []
            all_true_positive_counts = []
            all_false_negative_counts = []
            all_true_negative_counts = []

            thresholds = []

            while threshold < end:
                thresholds.append(threshold)

                false_positive_count = 0
                true_positive_count = 0
                true_negative_count = 0
                false_negative_count = 0

                for item in run['data']:
                    diff = item['new_service_time'] - item['old_service_time']
                    if diff >= threshold and not item['regression']:
                        false_positive_count += 1
                    if diff >= threshold and item['regression']:
                        true_positive_count += 1
                    if diff < threshold and not item['regression']:
                        true_negative_count += 1
                    if diff < threshold and item['regression']:
                        false_negative_count += 1

                all_false_positive_counts.append(false_positive_count)
                all_true_positive_counts.append(true_positive_count)
                all_false_negative_counts.append(false_negative_count)
                all_true_negative_counts.append(true_negative_count)
                threshold += 1

            plt.plot(thresholds, all_false_positive_counts, label='False positives')
            plt.plot(thresholds, all_true_positive_counts, label='True positives')
            plt.plot(thresholds, all_false_negative_counts, label='False negatives')
            plt.plot(thresholds, all_true_negative_counts, label='True negatives')

            plt.xlabel('Service time diff threshold')
            plt.legend()
            plt.show()


        print(runs[0])
        exit(-1)


def main():
    parser = argparse.ArgumentParser(description='Run a simulation')
    parser.add_argument('file', metavar='file', type=str, help='File to analyse')
    args = parser.parse_args()

    absolute_output_dir = os.path.abspath(args.file)

    psutil.cpu_percent()
    results = Results.from_json(absolute_output_dir)

    segmenter = TimeWindowedSegmenter(timedelta(seconds=30))
    averager = Averager(segmenter, should_round=False)
    rounding_averager = Averager(segmenter, should_round=True)

    summary_sections = [
        # EndpointOverview(),
        # SimulationDetails(),
        # PlotCpuUsageOverTime(service=ComputeCpuUsageOverTime(results, averager=averager)),
        # PlotCpuUsageAgainstLatency('api.add_user', service=ComputeCpuUsageAgainstLatency(
        #     results=results,
        #     averager=rounding_averager)
        # ),
        # PlotLatenciesOverTime(['articles.get_articles', 'articles.favorite_an_article'], averager),
        PlotTransactionSignatures(
            ComputeTransactionSignature(results, segmenter), options=dict(
                plot_absolute=True,
                plot_relative=False,
                plot_percentual_relative=False
            )
        )
    ]

    for section in summary_sections:
        section.print(results)
        print()


if __name__ == '__main__':
    main2()
