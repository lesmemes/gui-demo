# -*- coding: utf-8 -*-
import logging

import math
from PyQt5.QtWidgets import QWidget, QMessageBox
from PyQt5.QtCore import pyqtSlot

from decimal import Decimal, ROUND_DOWN
from app.ui.my_account import Ui_MyAccount
from app.models import Profile, init_profile_db
from app.signals import signals
from app import CURRENCY_CODE


log = logging.getLogger(__name__)


class MyAccount(QWidget, Ui_MyAccount):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        from app.models.db import profile_session_scope
        with profile_session_scope() as session:
            self.profile = Profile.get_active(session)
        self.on_profile_changed(self.profile)

        signals.profile_changed.connect(self.on_profile_changed)

    @pyqtSlot(Profile)
    def on_profile_changed(self, new_profile):
        self.profile = new_profile
        self.lbl_wallet_alias.setText(self.profile.alias)
        self.lbl_wallet_address.setText(self.profile.address)

        postdecimal = math.floor(self.profile.balance * 100000000 % 100000000)
        predecimal = self.profile.balance.quantize(Decimal(), rounding=ROUND_DOWN)
        self.lbl_wallet_balance_postdecimal.setText("{}".format(postdecimal))
        self.lbl_wallet_balance_predecimal.setText("{0:n},".format(predecimal))
        self.lbl_wallet_balance_currency.setText(CURRENCY_CODE)
        self.gbox_wallet_my_balance.setToolTip("{0:n} {1}".format(
            self.profile.balance.quantize(Decimal("0.00000001"), rounding=ROUND_DOWN), CURRENCY_CODE
        ))


if __name__ == '__main__':
    import sys
    from PyQt5 import QtWidgets
    from app import helpers
    from app import models
    helpers.init_logging()
    helpers.init_data_dir()
    models.init_profile_db()
    models.init_data_db()

    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('fusion')
    wgt = MyAccount()
    wgt.show()
    sys.exit(app.exec())
