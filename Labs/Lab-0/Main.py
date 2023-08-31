from datetime import datetime
# Collect two dates.
# Print the time between those two dates.

start_date = input("Enter start date MM-Day-Year: ")
end_date = input("Enter end date MM-Day-Year: ")
start = datetime(int(start_date[6:10]), int(start_date[0:2]), int(start_date[3:5]) )
end = datetime(int(end_date[6:]), int(end_date[:2]), int(end_date[3:5]))
days_apart = abs((start - end)).days
years_apart = days_apart / 365
print("from {} to {} is a difference of {} (days), {:.1f} (months), {:.1f} years."
      .format(start_date, end_date, days_apart, years_apart * 12, years_apart))
