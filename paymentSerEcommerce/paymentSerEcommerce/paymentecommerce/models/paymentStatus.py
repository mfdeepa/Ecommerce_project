from enum import Enum

class PaymentStatus(Enum):
    SUCCESS = 'SUCCESS'
    FAILED = 'FAILED'
    RECONCILED = 'RECONCILED'
    PENDING = 'PENDING'
    REFUNDED = 'REFUNDED'
    CANCELLED = 'CANCELLED'
