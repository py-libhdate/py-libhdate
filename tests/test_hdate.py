import pytest
import hdate
import hdate.hdate_julian as hj

import datetime


HEBREW_YEARS_INFO = {
    # year, dow rosh hashana, length, dow pesach
    5753: (2, 353, 3), 5773: (2, 353, 3), 5777: (2, 353, 3),
    5756: (2, 355, 5), 5759: (2, 355, 5), 5780: (2, 355, 5), 5783: (2, 355, 5),
    5762: (3, 354, 5), 5766: (3, 354, 5), 5769: (3, 354, 5),
    5748: (5, 354, 7), 5751: (5, 354, 7), 5758: (5, 354, 7), 5772: (5, 354, 7),
    5775: (5, 354, 7), 5778: (5, 354, 7),
    5754: (5, 355, 1), 5785: (5, 355, 1),
    5761: (7, 353, 1), 5781: (7, 353, 1),
    5750: (7, 355, 3), 5764: (7, 355, 3), 5767: (7, 355, 3), 5770: (7, 355, 3),
    5788: (7, 355, 3),
    5749: (2, 383, 5), 5790: (2, 383, 5),
    5752: (2, 385, 7), 5776: (2, 385, 7), 5779: (2, 385, 7),
    5755: (3, 384, 7), 5782: (3, 384, 7),
    5765: (5, 383, 1), 5768: (5, 383, 1), 5812: (5, 383, 1),
    5744: (5, 385, 3), 5771: (5, 385, 3), 5774: (5, 385, 3),
    5757: (7, 383, 3), 5784: (7, 383, 3),
    5760: (7, 385, 5), 5763: (7, 385, 5), 5787: (7, 385, 5)
    }


class TestSetDate(object):

    def test_default_today(self):
        assert hdate.set_date(None) == datetime.date.today()

    def test_random_date(self, random_date):
        randomday = datetime.date(*random_date)
        # When calling set_date with no arguments we should get today's date
        assert hdate.set_date(randomday) == randomday

    @pytest.mark.parametrize('execution_number', range(5))
    def test_random_datetime(self, execution_number, random_date):
        randomday = datetime.datetime(*random_date)
        # When calling set_date with no arguments we should get today's date
        assert hdate.set_date(randomday) == randomday

    def test_illegal_value(self):
        with pytest.raises(TypeError):
            hdate.set_date(100)


class TestHDate(object):

    @pytest.fixture
    def default_values(self):
        return hdate.HDate()

    @pytest.fixture
    def random_hdate(self, random_date):
        date = datetime.date(*random_date)
        return hdate.HDate(date)

    def test_default_weekday(self, default_values):
        expected_weekday = datetime.datetime.today().weekday() + 2
        expected_weekday = expected_weekday if expected_weekday < 8 else 1
        assert default_values._weekday == expected_weekday

    @pytest.mark.parametrize('execution_number', range(10))
    def test_random_weekday(self, execution_number, random_hdate):
        expected_weekday = random_hdate._gdate.weekday() + 2
        expected_weekday = expected_weekday if expected_weekday < 8 else 1
        assert random_hdate._weekday == expected_weekday

    @pytest.mark.parametrize('execution_number', range(10))
    def test_random_hdate(self, execution_number, random_hdate):
        _hdate = hdate.HDate()
        _hdate.hdate_set_hdate(random_hdate._h_day, random_hdate._h_month,
                               random_hdate._h_year)
        assert _hdate._h_day == random_hdate._h_day
        assert _hdate._h_month == random_hdate._h_month
        assert _hdate._h_year == random_hdate._h_year
        assert _hdate.jday == random_hdate.jday
        assert _hdate._weekday == random_hdate._weekday
        assert _hdate._h_size_of_year == random_hdate._h_size_of_year
        assert _hdate._h_year_type == random_hdate._h_year_type
        assert _hdate._h_days == random_hdate._h_days
        assert _hdate._h_weeks == random_hdate._h_weeks
        assert _hdate._gdate == random_hdate._gdate

    def test_hj_get_size_of_hebrew_year(self):
        for year, info in HEBREW_YEARS_INFO.items():
            assert hj._get_size_of_hebrew_year(year) == info[1]

    @pytest.mark.parametrize('execution_number', range(10))
    def test_hdate_get_size_of_hebrew_years(self, execution_number,
                                            random_hdate):
        assert (random_hdate._h_size_of_year ==
                hj._get_size_of_hebrew_year(random_hdate._h_year))

    def test_rosh_hashana_day_of_week(self, random_hdate):
        for year, info in HEBREW_YEARS_INFO.items():
            random_hdate.hdate_set_hdate(random_hdate._h_day,
                                         random_hdate._h_month, year)
            assert random_hdate._h_new_year_weekday == info[0]

    def test_pesach_day_of_week(self, random_hdate):
        for year, info in HEBREW_YEARS_INFO.items():
            random_hdate.hdate_set_hdate(15, 7, year)
            assert random_hdate._weekday == info[2]
            assert random_hdate.get_holyday() == 15
