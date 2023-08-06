# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from nereid.contrib.locale import make_lazy_gettext
from trytond.pool import PoolMeta

_ = make_lazy_gettext('payment_gateway_paypal')


class Payment(metaclass=PoolMeta):
    __name__ = 'sale.payment'

    def get_payment_description(self, name):
        if self.method == 'paypal':
            return str(_('Paid by PayPal'))
        return super(Payment, self).get_payment_description(name)
