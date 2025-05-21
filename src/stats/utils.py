from datetime import datetime, timedelta

def calculate_date_steps(start_date: datetime, end_date: datetime, steps=10) -> list[datetime]:
    total_days = (end_date - start_date).days
    step_days = max(total_days // steps, 1) if steps > 0 else 1
    
    dates = []
    current_date = start_date
    
    for _ in range(steps):
        dates.append(current_date)
        current_date += timedelta(days=step_days)
        if current_date > end_date:
            break
    
    if dates[-1] < end_date:
        dates.append(end_date)
    
    return dates
