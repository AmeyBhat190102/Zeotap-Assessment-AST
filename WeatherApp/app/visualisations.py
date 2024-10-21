import matplotlib.pyplot as plt

def plot_temperature_trends(daily_summaries):
    dates = [summary['date'] for summary in daily_summaries]
    avg_temps = [summary['avg_temp'] for summary in daily_summaries]

    plt.plot(dates, avg_temps, label="Avg Temp")
    plt.xlabel("Date")
    plt.ylabel("Temperature (°C)")
    plt.title("Temperature Trends")
    plt.legend()
    plt.show()
