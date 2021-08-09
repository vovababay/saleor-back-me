from typing import TYPE_CHECKING, Any, List, Optional, Union
from ....checkout import calculations
from saleor.plugins.base_plugin import BasePlugin, ConfigurationTypeField
from prices import Money, MoneyRange, TaxedMoney, TaxedMoneyRange
from ..utils import get_supported_currencies
from . import (
    GatewayConfig,
    authorize,
    capture,
    confirm,
    get_client_token,
    process_payment,
    refund,
    void,
)
import time


GATEWAY_NAME = "Tinkoff"


if TYPE_CHECKING:
    # flake8: noqa
    from . import GatewayResponse, PaymentData, TokenConfig
    from ...interface import CustomerSource
    from ....checkout.models import Checkout, CheckoutLine
    from ....discount import DiscountInfo

    from ....account.models import Address
    from ....order.models import OrderLine, Order
    from ...models import PluginConfiguration

def require_active_plugin(fn):
    def wrapped(self, *args, **kwargs):
        previous = kwargs.get("previous_value", None)
        if not self.active:
            return previous
        return fn(self, *args, **kwargs)
    return wrapped
amount_pay = 0
class TinkoffGatewayPlugin(BasePlugin):
    PLUGIN_ID = "mirumee.payments.tinkoff"
    PLUGIN_NAME = GATEWAY_NAME
    DEFAULT_CONFIGURATION = [
        {"name": "Terminal ID", "value": None},
        {"name": "Terminal password", "value": None},
        {"name": "Use sandbox", "value": True},
        {"name": "Store customers card", "value": False},
        {"name": "Automatic payment capture", "value": True},
        {"name": "Require 3D secure", "value": False},
        {"name": "Supported currencies", "value": ""},
    ]

    CONFIG_STRUCTURE = {
        "Terminal ID": {
            "type": ConfigurationTypeField.SECRET,
            "help_text": "Terminal ID.",
            "label": "Terminal ID",
        },
        "Terminal password": {
            "type": ConfigurationTypeField.SECRET,
            "help_text": "Terminal password.",
            "label": "Terminal password",
        },
        "Use sandbox": {
            "type": ConfigurationTypeField.BOOLEAN,
            "help_text": "Determines if Saleor should use Braintree sandbox API.",
            "label": "Use sandbox",
        },
        "Store customers card": {
            "type": ConfigurationTypeField.BOOLEAN,
            "help_text": "Determines if Saleor should store cards on payments"
            " in Braintree customer.",
            "label": "Store customers card",
        },
        "Automatic payment capture": {
            "type": ConfigurationTypeField.BOOLEAN,
            "help_text": "Determines if Saleor should automaticaly capture payments.",
            "label": "Automatic payment capture",
        },
        "Require 3D secure": {
            "type": ConfigurationTypeField.BOOLEAN,
            "help_text": "Determines if Saleor should enforce 3D secure during payment.",
            "label": "Require 3D secure",
        },
        "Supported currencies": {
            "type": ConfigurationTypeField.STRING,
            "help_text": "Determines currencies supported by gateway."
            " Please enter currency codes separated by a comma.",
            "label": "Supported currencies",
        },
    }

    def __init__(self, *args, **kwargs):
        self.amount = 0
        super().__init__(*args, **kwargs)
        configuration = {item["name"]: item["value"] for item in self.configuration}
        self.config = GatewayConfig(
            gateway_name=GATEWAY_NAME,
            auto_capture=configuration["Automatic payment capture"],
            supported_currencies=configuration["Supported currencies"],
            connection_params={
                "sandbox_mode": configuration["Use sandbox"],
                "terminal_id": configuration["Terminal ID"],
                "terminal_password": configuration["Terminal password"],
            },
            store_customer=configuration["Store customers card"],
            require_3d_secure=configuration["Require 3D secure"],
        )
    #def _skip_plugin(self, previous_value: Union[TaxedMoney, TaxedMoneyRange]) -> bool:
    #    if not self.active or not self.config.access_key:
    #        return True
    def _get_gateway_config(self):
        return self.config
    
    
    @require_active_plugin
    def authorize_payment(
        self, payment_information: "PaymentData", previous_value
    ) -> "GatewayResponse":
        return authorize(payment_information, self._get_gateway_config())

    @require_active_plugin
    def capture_payment(
        self, payment_information: "PaymentData", previous_value
    ) -> "GatewayResponse":
        return capture(payment_information, self._get_gateway_config())

    @require_active_plugin
    def confirm_payment(
        self, payment_information: "PaymentData", previous_value
    ) -> "GatewayResponse":
        return confirm(payment_information, self._get_gateway_config())

    @require_active_plugin
    def refund_payment(
        self, payment_information: "PaymentData", previous_value
    ) -> "GatewayResponse":
        return refund(payment_information, self._get_gateway_config())

    @require_active_plugin
    def void_payment(
        self, payment_information: "PaymentData", previous_value
    ) -> "GatewayResponse":
        return void(payment_information, self._get_gateway_config())

    @require_active_plugin
    def process_payment(
        self, payment_information: "PaymentData", previous_value
    ) -> "GatewayResponse":
        return process_payment(payment_information, self._get_gateway_config())

    @require_active_plugin
    def get_client_token(self, token_config: "TokenConfig", previous_value):
        return get_client_token()

    @require_active_plugin
    def get_supported_currencies(self, previous_value):
        config = self._get_gateway_config()
        return get_supported_currencies(config, GATEWAY_NAME)

    #@require_active_plugin
    def get_payment_config(self, 
        previous_value):
        print(111111111111111111111111111111)
        config = self._get_gateway_config()
        print(f"@@@@@@@@    {self.amount}")
        #print(self.configuration)
        #time.sleep(10)
        global amount_pay
        print(amount_pay)
        
        return [{"field": "amount_pay", "value": self.amount},{"field": "123", "value": "123456"}]

    @require_active_plugin
    def calculate_checkout_total(
        self,
        checkout: "Checkout",
        lines: List["CheckoutLine"],
        discounts: List["DiscountInfo"],
        previous_value: TaxedMoney,
    ) -> TaxedMoney:
        print(222222222222222222222222)
        #if self._skip_plugin(previous_value):
        #    return previous_value
        amount = (
            calculations.checkout_subtotal(
                checkout=checkout, lines=lines, discounts=discounts
            )
            + calculations.checkout_shipping_price(
                checkout=checkout, lines=lines, discounts=discounts
            )
            - checkout.discount
        )
        print(f"!!!!!!  {amount}")
        self.amount = amount.gross.amount
        global amount_pay
        amount_pay = amount.gross.amount
        print(self.amount)
        return (
            calculations.checkout_subtotal(
                checkout=checkout, lines=lines, discounts=discounts
            )
            + calculations.checkout_shipping_price(
                checkout=checkout, lines=lines, discounts=discounts
            )
            - checkout.discount
        )