# Import all schemas for easy access
from .user import UserBase, UserCreate, UserRead, Token, TokenData, OTPRequest, OTPVerify
from .customer import CustomerBase, CustomerCreate, CustomerUpdate, CustomerRead, CustomerWithAddresses
from .address import AddressBase, AddressCreate, AddressUpdate, AddressRead
from .service import ServiceBase, ServiceCreate, ServiceUpdate, ServiceRead
from .order import OrderBase, OrderCreate, OrderUpdate, OrderRead, OrderWithDetails, OrderSummary
from .order_item import OrderItemBase, OrderItemCreate, OrderItemUpdate, OrderItemRead, OrderItemWithService
from .notification import NotificationBase, NotificationCreate, NotificationUpdate, NotificationRead, NotificationStatusUpdate
