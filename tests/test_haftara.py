"""Tests for Haftara module."""

from hdate import HDateInfo, HebrewDate, Months
from hdate.translator import set_language


class TestHaftara:
    """Test Haftara database and lookup functionality."""

    def test_haftara_bereshit_hebrew(self) -> None:
        """Test Bereshit Haftara in Hebrew."""
        set_language("he")
        # Bereshit shabbat in 5785: 23 Tishrei 5785
        h = HDateInfo(HebrewDate(5785, Months.TISHREI, 23))
        assert h.haftara == 'ישעיהו מ"ב, ה'

    def test_haftara_bereshit_english(self) -> None:
        """Test Bereshit Haftara in English."""
        set_language("en")
        h = HDateInfo(HebrewDate(5785, Months.TISHREI, 23))
        assert h.haftara == "Isaiah 42:5"

    def test_haftara_bereshit_french(self) -> None:
        """Test Bereshit Haftara in French."""
        set_language("fr")
        h = HDateInfo(HebrewDate(5785, Months.TISHREI, 23))
        assert h.haftara == "Isaïe 42:5"

    def test_shabbat_machar_chodesh(self) -> None:
        """Test Shabbat Machar Chodesh Haftara when Shabbat falls on 29 Tishrei 5784."""
        set_language("he")
        h = HDateInfo(HebrewDate(5784, Months.TISHREI, 29))
        assert h.haftara == "שמואל א כ, יח"

    def test_special_shabbat_shekalim(self) -> None:
        """Test Shabbat Shekalim Haftara."""
        set_language("he")
        # Shabbat Shekalim 5784 (leap year): 24 Adar I 5784 (Mar 4, 2024 - Shabbat on 24 Adar I, 1 Adar II is Sunday)
        h = HDateInfo(HebrewDate(5784, Months.ADAR_I, 24))
        assert h.haftara == 'מלכים ב י"ב, א'

    def test_special_shabbat_zachor(self) -> None:
        """Test Shabbat Zachor Haftara."""
        set_language("he")
        # Shabbat Zachor 5784: 13 Adar II 5784 (Mar 23, 2024)
        h = HDateInfo(HebrewDate(5784, Months.ADAR_II, 13))
        assert h.haftara == 'שמואל א ט"ו, ב'

    def test_shabbat_nachamu(self) -> None:
        """Test Shabbat Nachamu (1st of Consolation) Haftara."""
        set_language("he")
        # Shabbat Nachamu 5784: 13 Av 5784 (Aug 17, 2024)
        h = HDateInfo(HebrewDate(5784, Months.AV, 13))
        assert h.haftara == "ישעיהו מ', א"

    def test_rosh_hashana_haftara(self) -> None:
        """Test Rosh Hashana Day 1 & Day 2 Haftara."""
        set_language("he")
        h1 = HDateInfo(HebrewDate(5785, Months.TISHREI, 1))
        assert h1.haftara == "שמואל א א, א"

        h2 = HDateInfo(HebrewDate(5785, Months.TISHREI, 2))
        assert h2.haftara == 'ירמיהו ל"א, א'

    def test_simchat_torah_israel_vs_diaspora(self) -> None:
        """Test Simchat Torah Haftara in Israel and Diaspora."""
        set_language("he")
        # In Israel, 22 Tishrei is Simchat Torah
        h_israel = HDateInfo(HebrewDate(5785, Months.TISHREI, 22), diaspora=False)
        assert h_israel.haftara == "יהושע א, א"

        # In Diaspora, 22 Tishrei is Shemini Atzeret and 23 Tishrei is Simchat Torah
        h_diaspora_22 = HDateInfo(HebrewDate(5785, Months.TISHREI, 22), diaspora=True)
        assert h_diaspora_22.haftara == "מלכים א ח, נד"

        h_diaspora_23 = HDateInfo(HebrewDate(5785, Months.TISHREI, 23), diaspora=True)
        assert h_diaspora_23.haftara == "יהושע א, א"

    def test_tisha_bav_haftara(self) -> None:
        """Test Tisha B'Av Haftara."""
        set_language("he")
        h = HDateInfo(HebrewDate(5784, Months.AV, 9))
        assert h.haftara == "ירמיהו ח, יג"
