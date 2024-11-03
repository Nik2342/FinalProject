from src.reports import spending_by_category
from src.services import get_bank_operations
from src.views import main_page


def all_func():
    main_page()
    get_bank_operations()
    spending_by_category()
