import datetime

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import MinMaxScaler
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import acf
from scipy.fft import fft
from src.api.data.model import DataTrendsAndForecast

class TimeseriesAnalyticsService:
    """
    Service class for processing incidents related to time-series data, identifying patterns,
    and generating forecasts using statistical models.
    """

    def process_timeseries_data(
            self,
            overall_kpi_values: list[float],
            latest_kpi_values:list[float],
            forecast_steps: int = 20,
    ) -> DataTrendsAndForecast:
        """
        Processes incidents by splitting the data into parts, identifying patterns in the latest
        and overall trends, and generating a forecast.

        Args:
            kpi_values (list[float]): List of time-series values.
            kpi (str): The column name representing the Key Performance Indicator (e.g., 'voltage').
            incident_id (str): Unique identifier for the incident.
            save_path (str): Path to save generated plots (if plot is True).
            forecast_steps (int): The number of steps to forecast.
            plot (bool): Whether to generate and save plots.

        Returns:
            DataTrendsAndForecast: Contains overall trend, latest trend, and forecasted values.
        """
        # Convert the list to a Pandas Series
        overall_series = pd.Series(overall_kpi_values,dtype=np.float32)
        latest_series=pd.Series(latest_kpi_values,dtype=np.float32)
        if overall_series.empty:
            return DataTrendsAndForecast(
                overall_trend=None,
                latest_trend=None,
                forecast=None
            )

        # Identify the patterns for the latest and overall data
        latest_trend = self.identify_pattern_for_incident(latest_series)
        overall_trend = None

        # Generate forecast for post-incident analysis
        forecast = self.post_incident_forecast(overall_series, forecast_steps).astype(np.float32)
        # Return the analysis results
        return DataTrendsAndForecast(
        overall_trend=overall_trend,
        latest_trend=latest_trend,
        forecast=forecast.tolist()
    )

    def get_trend_categories(self, data: pd.Series) -> tuple:
        """
        Determines the trend category based on the Auto-Correlation Function (ACF) of the data.

        Args:
            data (pd.Series): Time-series data.

        Returns:
            tuple: A category string representing the trend (e.g., 'Nil', 'Average correlation')
                   and the mean ACF value.
        """
        if data.empty:
            return "0", 0.0

        # Calculate ACF value for the series (Auto-Correlation)
        acf_value = acf(data, nlags=1)[-1]
        # Define thresholds for categorization based on ACF value
        acf_lower_value = 0.3
        acf_medium_value = 0.6
        acf_higher_value = 0.9

        # Categorize the fluctuation based on ACF value
        if acf_value < acf_lower_value:
            acf_category = "Nil"
        elif acf_lower_value <= acf_value < acf_medium_value:
            acf_category = "Average correlation"
        elif acf_medium_value <= acf_value < acf_higher_value:
            acf_category = "High correlation"
        else:
            acf_category = "Very High correlation"

        return acf_category, acf_value

    def check_if_series_has_periodic_trend(self, kpi_values: pd.Series) -> bool:
        """
        Checks if the KPI time series exhibits periodic behavior using Fast Fourier Transform (FFT).

        Args:
            kpi_values (pd.Series): Time-series data.

        Returns:
            bool: True if the series exhibits periodic behavior, otherwise False.
        """
        # Perform FFT to analyze the frequency components of the time series
        fft_values = np.abs(fft(kpi_values))  # Get the magnitude of FFT values

        # Define a threshold for significant frequencies
        fft_threshold = np.max(fft_values) * 0.1  # Use 10% of the maximum FFT value as threshold

        # Check if more than one frequency surpasses the threshold
        return np.sum(fft_values > fft_threshold) > 1

    def get_pattern_by_degree_of_angle(self, angle_degrees: float) -> str:
        """
        Categorizes the trend based on the angle of change in degrees.

        Args:
            angle_degrees (float): The angle (in degrees) representing the slope or trend.

        Returns:
            str: The categorized trend (e.g., 'Stable', 'Increasing', 'Decreasing').
        """
        if angle_degrees < -90 or angle_degrees > 90:
            return "Can not determine"

        # Define thresholds for categorizing the angle trend
        start_threshold = 10  # Slight change in angle
        rapid_threshold = 45  # Moderate change in angle

        # Categorize the trend based on the angle
        if 0 <= angle_degrees <= 5:
            return "Stable"
        elif 5 < angle_degrees <= start_threshold:
            return "Started to Increase"
        elif start_threshold < angle_degrees <= rapid_threshold:
            return "Increasing"
        elif rapid_threshold < angle_degrees <= 90:
            return "Rapidly Increasing"
        elif -5 <= angle_degrees < 0:
            return "Stable"
        elif -start_threshold <= angle_degrees < -5:
            return "Started to Decrease"
        elif -rapid_threshold <= angle_degrees < -start_threshold:
            return "Decreasing"
        elif -90 <= angle_degrees < -rapid_threshold:
            return "Rapidly Decreasing"
        else:
            return "Can not determine"

    def identify_pattern_for_incident(self, data: pd.Series) -> str:
        """
        Identifies the fluctuation pattern and trend for a group of data.

        Args:
            data (pd.Series): Time-series data for incident analysis.

        Returns:
            str: The identified trend or pattern.
        """
        if isinstance(data, list):
            data = pd.Series(data)

        # Get ACF category and value
        acf_category, acf_mean = self.get_trend_categories(data)

        # Normalize the data between 0 and 100
        scaler = MinMaxScaler(feature_range=(0, 100))
        scaled_data = scaler.fit_transform(data.values.reshape(-1, 1))

        # Define time index for regression analysis
        seconds = np.arange(1, len(data) + 1)

        # Perform linear regression to determine the slope
        x = seconds.reshape(-1, 1)
        y = scaled_data
        model = LinearRegression().fit(x, y)
        slope = model.coef_[0]
        angle_degrees = np.degrees(np.arctan(slope))  # Convert slope to angle in degrees
        # Determine the trend based on the ACF category and periodicity check
        if acf_category == "Nil":
            if self.check_if_series_has_periodic_trend(data):
                return "Noise"
            else:
                return self.get_pattern_by_degree_of_angle(angle_degrees)
        else:
            if self.check_if_series_has_periodic_trend(data):
                return "Fluctuating"
            else:
                return self.get_pattern_by_degree_of_angle(angle_degrees)

    def post_incident_forecast(self, series: pd.Series, forecast_steps: int) -> pd.Series:
        """
        Performs ARIMA analysis to forecast values post-incident based on time-series data.

        Args:
            series (pd.Series): The input time series data for forecasting.
            forecast_steps (int): Number of steps to forecast.

        Returns:
            pd.Series: The forecasted values.
        """
        if series.empty:
            raise ValueError("Input series is empty. Cannot compute forecast.")

        if not pd.api.types.is_numeric_dtype(series):
            raise ValueError("Input series contains non-numeric values.")

        # Calculate ACF to define ARIMA parameters
        acf_value = acf(series, nlags=1)[-1]

        # Set ARIMA parameters based on ACF value
        p, d, q = (1, 0, 3) if acf_value < 0.5 else (int(acf_value * 10), 0, 0)

        # Drop NaN values and fit ARIMA model
        series = series.dropna().astype(float)

        try:
            # Fit ARIMA model with determined parameters
            model = ARIMA(series, order=(p, d, q), trend="t", enforce_stationarity=False)
            fitted_model = model.fit()

            # Generate forecasts and clip them to a valid range
            forecast = fitted_model.forecast(steps=forecast_steps)
            max_kpi = series.max()
            forecast = np.clip(forecast, 0, 2 * max_kpi)
            return forecast
        except Exception as e:
            print(f"Error during ARIMA forecasting: {e}")
            return pd.Series([])  # Return an empty Series if an error occurs