# Lint as: python3
# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Tests for evaluators.jackknife."""

import functools

from absl.testing import absltest
import apache_beam as beam
from apache_beam.testing import util
import numpy as np

from tensorflow_model_analysis import types
from tensorflow_model_analysis.evaluators import confidence_intervals_util
from tensorflow_model_analysis.evaluators import jackknife
from tensorflow_model_analysis.metrics import binary_confusion_matrices
from tensorflow_model_analysis.metrics import metric_types


class ListCombineFn(beam.CombineFn):

  def __init__(self, extract_output_append=None):
    self._extract_output_append = extract_output_append

  def create_accumulator(self):
    return []

  def add_input(self, accumulator, element):
    return accumulator + [element]

  def merge_accumulators(self, accumulators):
    return functools.reduce(list.__add__, accumulators)

  def extract_output(self, accumulator):
    if self._extract_output_append:
      return accumulator + [self._extract_output_append]
    else:
      return accumulator


class ListCombineFnExtractOutputNotImplemented(ListCombineFn):

  def extract_output(self, accumulator):
    raise NotImplementedError(
        'extract_output intentionally not implement to verify behavior. We '
        'would like to be able to mock a combine_fn and then call '
        'combine_fn.extract_output.assert_not_called().')


class ListCombineFnAddInputNotImplemented(ListCombineFn):

  def add_input(self, accumulator, element):
    raise NotImplementedError(
        'add_input intentionally not implement to verify behavior. We would '
        'like to be able to mock a combine_fn and then call '
        'combine_fn.add_input.assert_not_called().')


class JackknifeTest(absltest.TestCase):

  def test_accumulate_only_combiner(self):
    with beam.Pipeline() as pipeline:
      result = (
          pipeline
          | 'Create' >> beam.Create([1, 2])
          | 'AccumulateOnlyCombine' >> beam.CombineGlobally(
              jackknife._AccumulateOnlyCombineFn(
                  ListCombineFnExtractOutputNotImplemented(
                      extract_output_append=3))))

      def check_result(got_pcoll):
        self.assertLen(got_pcoll, 1)
        self.assertEqual(got_pcoll[0], [1, 2])

      util.assert_that(result, check_result)

  def test_accumulator_combiner(self):
    with beam.Pipeline() as pipeline:
      result = (
          pipeline
          | 'Create' >> beam.Create([[1], [2]])
          | 'AccumulatorCombine' >> beam.CombineGlobally(
              jackknife._AccumulatorCombineFn(
                  ListCombineFnAddInputNotImplemented(extract_output_append=3)))
      )

      def check_result(got_pcoll):
        self.assertLen(got_pcoll, 1)
        self.assertEqual(got_pcoll[0], [1, 2, 3])

      util.assert_that(result, check_result)

  def test_jackknife_sample_combine_fn(self):
    x_key = metric_types.MetricKey('x')
    y_key = metric_types.MetricKey('y')
    cm_key = metric_types.MetricKey('confusion_matrix')
    cm_metric = binary_confusion_matrices.Matrices(
        thresholds=[0.5], tp=[0], fp=[1], tn=[2], fn=[3])
    slice_key1 = (('slice_feature', 1),)
    slice_key2 = (('slice_feature', 2),)
    samples = [
        # unsampled value for slice 1
        (slice_key1,
         confidence_intervals_util.SampleMetrics(
             sample_id=jackknife._FULL_SAMPLE_ID,
             metrics={
                 x_key: 1.6,
                 y_key: 16,
                 cm_key: cm_metric,
                 jackknife._JACKKNIFE_EXAMPLE_COUNT_METRIC_KEY: 100,
             })),
        # sample values 1 of 2 for slice 1
        (slice_key1,
         confidence_intervals_util.SampleMetrics(
             sample_id=0, metrics={
                 x_key: 1,
                 y_key: 10,
                 cm_key: cm_metric,
             })),
        # sample values 2 of 2 for slice 1
        (slice_key1,
         confidence_intervals_util.SampleMetrics(
             sample_id=1, metrics={
                 x_key: 2,
                 y_key: 20,
                 cm_key: cm_metric,
             })),
        # unsampled value for slice 2
        (slice_key2,
         confidence_intervals_util.SampleMetrics(
             sample_id=jackknife._FULL_SAMPLE_ID,
             metrics={
                 x_key: 3.3,
                 y_key: 33,
                 cm_key: cm_metric,
                 jackknife._JACKKNIFE_EXAMPLE_COUNT_METRIC_KEY: 1000,
             })),
        # sample values 1 of 2 for slice 2
        (slice_key2,
         confidence_intervals_util.SampleMetrics(
             sample_id=0, metrics={
                 x_key: 2,
                 y_key: 20,
                 cm_key: cm_metric,
             })),
        # sample values 2 of 2 for slice 2
        (slice_key2,
         confidence_intervals_util.SampleMetrics(
             sample_id=1, metrics={
                 x_key: 4,
                 y_key: 40,
                 cm_key: cm_metric,
             })),
    ]

    with beam.Pipeline() as pipeline:
      result = (
          pipeline
          | 'Create' >> beam.Create(samples, reshuffle=False)
          | 'CombineJackknifeSamplesPerKey' >> beam.CombinePerKey(
              jackknife._JackknifeSampleCombineFn(num_jackknife_samples=2)))

      # For standard error calculations, see delete-d jackknife formula in:
      # https://www.stat.berkeley.edu/~hhuang/STAT152/Jackknife-Bootstrap.pdf
      # Rather than normalize by all possible n-choose-d samples, we normalize
      # by the actual number of samples (2).
      def check_result(got_pcoll):
        expected_pcoll = [
            (
                slice_key1,
                {
                    x_key:
                        types.ValueWithTDistribution(
                            sample_mean=1.5,
                            # sample_standard_deviation=0.5
                            sample_standard_deviation=(
                                ((100 - 100 / 2) /
                                 (100 / 2)) * np.var([1, 2], ddof=1))**0.5,
                            sample_degrees_of_freedom=1,
                            unsampled_value=1.6),
                    y_key:
                        types.ValueWithTDistribution(
                            sample_mean=15.,
                            # sample_standard_deviation=5,
                            sample_standard_deviation=(
                                ((100 - 100 / 2) /
                                 (100 / 2)) * np.var([10, 20], ddof=1))**0.5,
                            sample_degrees_of_freedom=1,
                            unsampled_value=16),
                    cm_key:
                        cm_metric,
                    jackknife._JACKKNIFE_EXAMPLE_COUNT_METRIC_KEY:
                        100,
                }),
            (
                slice_key2,
                {
                    x_key:
                        types.ValueWithTDistribution(
                            sample_mean=3.,
                            # sample_standard_deviation=1,
                            sample_standard_deviation=(
                                ((1000 - 1000 / 2) /
                                 (1000 / 2)) * np.var([2, 4], ddof=1))**0.5,
                            sample_degrees_of_freedom=1,
                            unsampled_value=3.3),
                    y_key:
                        types.ValueWithTDistribution(
                            sample_mean=30.,
                            # sample_standard_deviation=10,
                            sample_standard_deviation=(
                                ((1000 - 1000 / 2) /
                                 (1000 / 2)) * np.var([20, 40], ddof=1))**0.5,
                            sample_degrees_of_freedom=1,
                            unsampled_value=33),
                    cm_key:
                        cm_metric,
                    jackknife._JACKKNIFE_EXAMPLE_COUNT_METRIC_KEY:
                        1000,
                }),
        ]
        self.assertCountEqual(expected_pcoll, got_pcoll)

      util.assert_that(result, check_result)

  def test_jackknife_sample_combine_fn_small_samples(self):
    metric_key = metric_types.MetricKey('metric')
    slice_key1 = (('slice_feature', 1),)
    slice_key2 = (('slice_feature', 2),)
    # the sample value is irrelevant for this test as we only verify counters.
    sample_value = {metric_key: 42}
    samples = [
        # unsampled value for slice 1
        (slice_key1,
         confidence_intervals_util.SampleMetrics(
             sample_id=jackknife._FULL_SAMPLE_ID,
             metrics={
                 metric_key: 2.1,
                 jackknife._JACKKNIFE_EXAMPLE_COUNT_METRIC_KEY: 16
             })),
        # 5 sample values for slice 1
        (slice_key1,
         confidence_intervals_util.SampleMetrics(
             sample_id=0, metrics=sample_value)),
        (slice_key1,
         confidence_intervals_util.SampleMetrics(
             sample_id=1, metrics=sample_value)),
        (slice_key1,
         confidence_intervals_util.SampleMetrics(
             sample_id=2, metrics=sample_value)),
        (slice_key1,
         confidence_intervals_util.SampleMetrics(
             sample_id=3, metrics=sample_value)),
        (slice_key1,
         confidence_intervals_util.SampleMetrics(
             sample_id=4, metrics=sample_value)),
        # unsampled value for slice 2
        (slice_key2,
         confidence_intervals_util.SampleMetrics(
             sample_id=jackknife._FULL_SAMPLE_ID,
             metrics={
                 metric_key: 6.3,
                 jackknife._JACKKNIFE_EXAMPLE_COUNT_METRIC_KEY: 10000
             })),
        # 5 sample values for slice 2
        (slice_key2,
         confidence_intervals_util.SampleMetrics(
             sample_id=0, metrics=sample_value)),
        (slice_key2,
         confidence_intervals_util.SampleMetrics(
             sample_id=1, metrics=sample_value)),
        (slice_key2,
         confidence_intervals_util.SampleMetrics(
             sample_id=2, metrics=sample_value)),
        (slice_key2,
         confidence_intervals_util.SampleMetrics(
             sample_id=3, metrics=sample_value)),
        (slice_key2,
         confidence_intervals_util.SampleMetrics(
             sample_id=4, metrics=sample_value)),
    ]

    with beam.Pipeline() as pipeline:
      _ = (
          pipeline
          | 'Create' >> beam.Create(samples, reshuffle=False)
          | 'CombineJackknifeSamplesPerKey' >> beam.CombinePerKey(
              jackknife._JackknifeSampleCombineFn(num_jackknife_samples=5)))

      result = pipeline.run()
      # we expect one bad jackknife samples counter increment for slice1.
      # slice1: num_samples=5, n=16, d=3.2, sqrt(n)=4, d < sqrt(n) = True
      # slice2: num_samples=5, n=10000, d=2000, sqrt(n)=100, d < sqrt(n) = False
      metric_filter = beam.metrics.metric.MetricsFilter().with_name(
          'num_slices_with_small_jackknife_samples')
      counters = result.metrics().query(filter=metric_filter)['counters']
      self.assertLen(counters, 1)
      self.assertEqual(1, counters[0].committed)

      # verify total slice counter
      metric_filter = beam.metrics.metric.MetricsFilter().with_name(
          'num_slices')
      counters = result.metrics().query(filter=metric_filter)['counters']
      self.assertLen(counters, 1)
      self.assertEqual(2, counters[0].committed)


if __name__ == '__main__':
  absltest.main()
