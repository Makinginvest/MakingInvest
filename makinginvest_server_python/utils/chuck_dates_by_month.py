from datetime import datetime
from dateutil.relativedelta import relativedelta


def chuck_dates_by_month(startDate: datetime, endDate: datetime):
    chunks = []

    # Adjust the startDate to the beginning of the month
    startDate = startDate.replace(day=1)

    # Adjust the endDate to the end of the month
    endDate = (endDate + relativedelta(months=1)).replace(day=1) - relativedelta(days=1)

    current_start = startDate

    while current_start <= endDate:
        current_end = current_start + relativedelta(months=1) - relativedelta(days=1)
        chunks.append({"startDate": current_start, "endDate": current_end})
        current_start += relativedelta(months=1)

    return chunks
