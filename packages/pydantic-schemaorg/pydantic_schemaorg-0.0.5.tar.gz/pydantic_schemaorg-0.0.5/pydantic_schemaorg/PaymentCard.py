from pydantic import StrictBool, Field
from typing import Any, Optional, Union, List
from decimal import Decimal
from pydantic_schemaorg.PaymentMethod import PaymentMethod
from pydantic_schemaorg.FinancialProduct import FinancialProduct


class PaymentCard(PaymentMethod, FinancialProduct):
    """A payment method using a credit, debit, store or other card to associate the payment with"
     "an account.

    See https://schema.org/PaymentCard.

    """
    type_: str = Field("PaymentCard", const=True, alias='@type')
    contactlessPayment: Optional[Union[List[StrictBool], StrictBool]] = Field(
        None,
        description="A secure method for consumers to purchase products or services via debit, credit or smartcards"
     "by using RFID or NFC technology.",
    )
    cashBack: Optional[Union[List[Union[Decimal, StrictBool]], Union[Decimal, StrictBool]]] = Field(
        None,
        description="A cardholder benefit that pays the cardholder a small percentage of their net expenditures.",
    )
    floorLimit: Any = Field(
        None,
        description="A floor limit is the amount of money above which credit card transactions must be authorized.",
    )
    monthlyMinimumRepaymentAmount: Union[List[Union[Decimal, Any]], Union[Decimal, Any]] = Field(
        None,
        description="The minimum payment is the lowest amount of money that one is required to pay on a credit"
     "card statement each month.",
    )
    

PaymentCard.update_forward_refs()
