import unittest
from test.test_utils import make_test_atlas, standardise_sql_string
from lumipy.query.expression.window.over import window


class TestWindowFunction(unittest.TestCase):

    def setUp(self) -> None:
        self.atlas = make_test_atlas()
        self.ar = self.atlas.lusid_logs_apprequest()
        self.win = window(
            groups=[self.ar.application, self.ar.method],
            orders=[self.ar.timestamp.ascending()],
        )

    def test_window_first_sql_str(self):
        win_fn = self.win.first(self.ar.duration)
        sql = win_fn.get_sql()
        self.assertEqual(
            standardise_sql_string(sql),
            standardise_sql_string('''FIRST_VALUE([Duration]) OVER(
                    PARTITION BY [Application], [Method]
                    ORDER BY [Timestamp] ASC
                    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
                )''')
        )

    def test_window_last_sql_str(self):
        win_fn = self.win.last(self.ar.duration)
        sql = win_fn.get_sql()
        self.assertEqual(
            standardise_sql_string(sql),
            standardise_sql_string('''LAST_VALUE([Duration]) OVER(
                    PARTITION BY [Application], [Method]
                    ORDER BY [Timestamp] ASC
                    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
                )''')
        )

    def test_window_lag_sql_str(self):
        win_fn = self.win.lag(self.ar.duration)
        sql = win_fn.get_sql()
        self.assertEqual(
            standardise_sql_string(sql),
            standardise_sql_string('''LAG([Duration], 1, null) OVER(
                    PARTITION BY [Application], [Method]
                    ORDER BY [Timestamp] ASC
                    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
                )''')
        )

        win_fn = self.win.lag(self.ar.duration, 5)
        sql = win_fn.get_sql()
        self.assertEqual(
            standardise_sql_string(sql),
            standardise_sql_string('''LAG([Duration], 5, null) OVER(
                    PARTITION BY [Application], [Method]
                    ORDER BY [Timestamp] ASC
                    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
                )''')
        )

        win_fn = self.win.lag(self.ar.duration, 3, 7)
        sql = win_fn.get_sql()
        self.assertEqual(
            standardise_sql_string(sql),
            standardise_sql_string('''LAG([Duration], 3, 7) OVER(
                    PARTITION BY [Application], [Method]
                    ORDER BY [Timestamp] ASC
                    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
                )''')
        )

    def test_window_lead_sql_str(self):
        win_fn = self.win.lead(self.ar.duration)
        sql = win_fn.get_sql()
        self.assertEqual(
            standardise_sql_string(sql),
            standardise_sql_string('''LEAD([Duration], 1, null) OVER(
                    PARTITION BY [Application], [Method]
                    ORDER BY [Timestamp] ASC
                    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
                )''')
        )

        win_fn = self.win.lead(self.ar.duration, 5)
        sql = win_fn.get_sql()
        self.assertEqual(
            standardise_sql_string(sql),
            standardise_sql_string('''LEAD([Duration], 5, null) OVER(
                    PARTITION BY [Application], [Method]
                    ORDER BY [Timestamp] ASC
                    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
                )''')
        )

        win_fn = self.win.lead(self.ar.duration, 3, 7)
        sql = win_fn.get_sql()
        self.assertEqual(
            standardise_sql_string(sql),
            standardise_sql_string('''LEAD([Duration], 3, 7) OVER(
                    PARTITION BY [Application], [Method]
                    ORDER BY [Timestamp] ASC
                    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
                )''')
        )

    def test_window_nth_value(self):
        win_fn = self.win.nth_value(self.ar.duration, 3)
        sql = win_fn.get_sql()
        self.assertEqual(
            standardise_sql_string(sql),
            standardise_sql_string('''NTH_VALUE([Duration], 3) OVER(
                    PARTITION BY [Application], [Method]
                    ORDER BY [Timestamp] ASC
                    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
                )''')
        )

    def test_window_mean_sql_str(self):
        win_fn = self.win.mean(self.ar.duration)
        sql = win_fn.get_sql()
        self.assertEqual(
            standardise_sql_string(sql),
            standardise_sql_string('''AVG([Duration]) OVER(
                    PARTITION BY [Application], [Method]
                    ORDER BY [Timestamp] ASC
                    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
                )''')
        )

    def test_window_count_sql_str(self):
        win_fn = self.win.count(self.ar.duration)
        sql = win_fn.get_sql()
        self.assertEqual(
            standardise_sql_string(sql),
            standardise_sql_string('''COUNT([Duration]) OVER(
                    PARTITION BY [Application], [Method]
                    ORDER BY [Timestamp] ASC
                    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
                )''')
        )

    def test_window_max_sql_str(self):
        win_fn = self.win.max(self.ar.duration)
        sql = win_fn.get_sql()
        self.assertEqual(
            standardise_sql_string(sql),
            standardise_sql_string('''MAX([Duration]) OVER(
                    PARTITION BY [Application], [Method]
                    ORDER BY [Timestamp] ASC
                    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
                )''')
        )

    def test_window_min_sql_str(self):
        win_fn = self.win.min(self.ar.duration)
        sql = win_fn.get_sql()
        self.assertEqual(
            standardise_sql_string(sql),
            standardise_sql_string('''MIN([Duration]) OVER(
                    PARTITION BY [Application], [Method]
                    ORDER BY [Timestamp] ASC
                    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
                )''')
        )

    def test_window_sum_sql_str(self):
        win_fn = self.win.sum(self.ar.duration)
        sql = win_fn.get_sql()
        self.assertEqual(
            standardise_sql_string(sql),
            standardise_sql_string('''TOTAL([Duration]) OVER(
                    PARTITION BY [Application], [Method]
                    ORDER BY [Timestamp] ASC
                    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
                )''')
        )

    def test_window_cume_dist_sql_str(self):
        win_fn = self.win.cume_dist()
        sql = win_fn.get_sql()
        self.assertEqual(
            standardise_sql_string(sql),
            standardise_sql_string('''CUME_DIST() OVER(
                    PARTITION BY [Application], [Method]
                    ORDER BY [Timestamp] ASC
                    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
                )''')
        )

    def test_window_dense_rank_sql_str(self):
        win_fn = self.win.dense_rank()
        sql = win_fn.get_sql()
        self.assertEqual(
            standardise_sql_string(sql),
            standardise_sql_string('''DENSE_RANK() OVER(
                    PARTITION BY [Application], [Method]
                    ORDER BY [Timestamp] ASC
                    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
                )''')
        )

    def test_window_ntile_sql_str(self):
        win_fn = self.win.ntile(3)
        sql = win_fn.get_sql()
        self.assertEqual(
            standardise_sql_string(sql),
            standardise_sql_string('''NTILE(3) OVER(
                    PARTITION BY [Application], [Method]
                    ORDER BY [Timestamp] ASC
                    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
                )''')
        )

    def test_window_rank_sql_str(self):
        win_fn = self.win.rank()
        sql = win_fn.get_sql()
        self.assertEqual(
            standardise_sql_string(sql),
            standardise_sql_string('''RANK() OVER(
                    PARTITION BY [Application], [Method]
                    ORDER BY [Timestamp] ASC
                    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
                )''')
        )

    def test_window_row_number_sql_str(self):
        win_fn = self.win.row_number()
        sql = win_fn.get_sql()
        self.assertEqual(
            standardise_sql_string(sql),
            standardise_sql_string('''ROW_NUMBER() OVER(
                    PARTITION BY [Application], [Method]
                    ORDER BY [Timestamp] ASC
                    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
                )''')
        )

    def test_window_percent_rank_sql_str(self):
        win_fn = self.win.percent_rank()
        sql = win_fn.get_sql()
        self.assertEqual(
            standardise_sql_string(sql),
            standardise_sql_string('''PERCENT_RANK() OVER(
                    PARTITION BY [Application], [Method]
                    ORDER BY [Timestamp] ASC
                    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
                )''')
        )

    def test_window_fn_with_filter_sql_str(self):
        cond = self.ar.application == 'lusid'
        win_fn = self.win.filter(cond).rank()
        sql = win_fn.get_sql()
        self.assertEqual(
            standardise_sql_string(sql),
            standardise_sql_string(f'''RANK() FILTER(WHERE {cond.get_sql()}) OVER(
                    PARTITION BY [Application], [Method]
                    ORDER BY [Timestamp] ASC
                    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
                )''')
        )

    def test_cume_sum_method_on_base_column(self):

        # No stated ordering = sort on row id
        win_fn1 = self.ar.duration.cume_sum()
        sql1 = win_fn1.get_sql()
        self.assertEqual(
            standardise_sql_string(sql1),
            standardise_sql_string('''TOTAL([Duration]) OVER(
                ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
                )''')
            )

        # With ordering = cume sum along another sort such as timestamp
        win_fn2 = self.ar.duration.cume_sum(self.ar.timestamp.ascending())
        sql2 = win_fn2.get_sql()
        self.assertEqual(
            standardise_sql_string(sql2),
            standardise_sql_string('''TOTAL([Duration]) OVER(
                ORDER BY [Timestamp] ASC
                ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
                )''')
            )

    def test_cume_mean_method_on_base_column(self):

        # No stated ordering = sort on row id
        win_fn1 = self.ar.duration.cume_mean()
        sql1 = win_fn1.get_sql()
        self.assertEqual(
            standardise_sql_string(sql1),
            standardise_sql_string('''AVG([Duration]) OVER(
                ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
                )''')
            )

        # With ordering = cume mean along another sort such as timestamp
        win_fn2 = self.ar.duration.cume_mean(self.ar.timestamp.ascending())
        sql2 = win_fn2.get_sql()
        self.assertEqual(
            standardise_sql_string(sql2),
            standardise_sql_string('''AVG([Duration]) OVER(
                ORDER BY [Timestamp] ASC
                ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
                )''')
            )

    def test_cume_min_method_on_base_column(self):

        # No stated ordering = sort on row id
        win_fn1 = self.ar.duration.cume_min()
        sql1 = win_fn1.get_sql()
        self.assertEqual(
            standardise_sql_string(sql1),
            standardise_sql_string('''MIN([Duration]) OVER(
                ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
                )''')
            )

        # With ordering = cume min along another sort such as timestamp
        win_fn2 = self.ar.duration.cume_min(self.ar.timestamp.ascending())
        sql2 = win_fn2.get_sql()
        self.assertEqual(
            standardise_sql_string(sql2),
            standardise_sql_string('''MIN([Duration]) OVER(
                ORDER BY [Timestamp] ASC
                ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
                )''')
            )

    def test_cume_max_method_on_base_column(self):

        # No stated ordering = sort on row id
        win_fn1 = self.ar.duration.cume_max()
        sql1 = win_fn1.get_sql()
        self.assertEqual(
            standardise_sql_string(sql1),
            standardise_sql_string('''MAX([Duration]) OVER(
                ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
                )''')
            )

        # With ordering = cume max along another sort such as timestamp
        win_fn2 = self.ar.duration.cume_max(self.ar.timestamp.ascending())
        sql2 = win_fn2.get_sql()
        self.assertEqual(
            standardise_sql_string(sql2),
            standardise_sql_string('''MAX([Duration]) OVER(
                ORDER BY [Timestamp] ASC
                ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
                )''')
            )

    def test_cume_frac_diff_method_on_base_column(self):

        # No stated ordering = sort on row id
        win_fn1 = self.ar.duration.frac_diff()
        sql1 = win_fn1.get_sql()
        self.assertEqual(
            standardise_sql_string(sql1),
            standardise_sql_string('''
            ([Duration] - LAG([Duration], 1, null) OVER(
                    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
                    )) / LAG([Duration], 1, null) OVER(
                    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
                )
                ''')
            )

        # With ordering = frac diff another sort such as timestamp
        win_fn2 = self.ar.duration.frac_diff(self.ar.timestamp.ascending())
        sql2 = win_fn2.get_sql()
        self.assertEqual(
            standardise_sql_string(sql2),
            standardise_sql_string('''
               ([Duration] - LAG([Duration], 1, null) OVER(
                        ORDER BY [Timestamp] ASC
                        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
                        )) / LAG([Duration], 1, null) OVER(
                        ORDER BY [Timestamp] ASC
                        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
                    ) 
                ''')
            )

        # With ordering and non-default offset (3) = frac diff along another sort such as timestamp and n = 3
        win_fn2 = self.ar.duration.frac_diff(self.ar.timestamp.ascending(), offset=3)
        sql2 = win_fn2.get_sql()
        self.assertEqual(
            standardise_sql_string(sql2),
            standardise_sql_string('''
               ([Duration] - LAG([Duration], 3, null) OVER(
                        ORDER BY [Timestamp] ASC
                        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
                        )) / LAG([Duration], 3, null) OVER(
                        ORDER BY [Timestamp] ASC
                        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
                    ) 
                ''')
            )

    def test_cume_dist_method_on_base_column(self):
        win_fn1 = self.ar.duration.cume_dist()
        sql = win_fn1.get_sql()
        self.assertEqual(
            standardise_sql_string(sql),
            standardise_sql_string('''
            CUME_DIST() OVER(
                    ORDER BY [Duration] ASC
                    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
                )
            ''')
        )
