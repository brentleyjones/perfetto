#!/usr/bin/env python3
# Copyright (C) 2023 The Android Open Source Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License a
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from python.generators.diff_tests.testing import Path, DataPath, Metric
from python.generators.diff_tests.testing import Csv, Json, TextProto
from python.generators.diff_tests.testing import DiffTestBlueprint
from python.generators.diff_tests.testing import TestSuite


class StdlibIntervals(TestSuite):

  def test_intervals_overlap_count(self):
    return DiffTestBlueprint(
        trace=TextProto(""),
        query="""
        INCLUDE PERFETTO MODULE intervals.overlap;

        WITH data(ts, dur) AS (
          VALUES
            (10, 40),
            (20, 10),
            (25, 10),
            (60, 10),
            (70, 20),
            (80, -1)
        )
        SELECT *
        FROM intervals_overlap_count!(data, ts, dur)
        """,
        out=Csv("""
        "ts","value"
        10,1
        20,2
        25,3
        30,2
        35,1
        50,0
        60,1
        70,1
        80,2
        90,1
        """))

  def test_intervals_overlap_in_table(self):
    return DiffTestBlueprint(
        trace=TextProto(""),
        query="""
        INCLUDE PERFETTO MODULE intervals.overlap;

        WITH data_no_overlaps(ts, dur) AS (
          VALUES
            (10, 10),
            (30, 10)
        ),
        data_with_overlaps(ts, dur) AS (
          VALUES
            (10, 10),
            (15, 10)
        )
        SELECT * FROM (
        SELECT *
        FROM _intervals_overlap_in_table!(data_no_overlaps)
        UNION
        SELECT *
        FROM _intervals_overlap_in_table!(data_with_overlaps)
        )
        """,
        out=Csv("""
        "has_overlaps"
        0
        1
        """))