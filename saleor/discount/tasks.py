from ..celeryconf import app
from datetime import datetime, timedelta
import time
from ..discount.models import Sale

@app.task
def update_value_discount(discount_pk):
    discount = Sale.objects.get(pk=discount_pk)
    discount.value = 80
    discount.save()
    tomorrow = datetime.now() + timedelta(days=1)
    print(tomorrow.date())
    return True
