from .service import make_request, format_alert
from . import mcp, NWS_API_BASE, JIRA_API_BASE

@mcp.tool()
async def get_alerts(state: str) -> str:
    """Get weather alerts for a US state.

    Args:
        state: Two-letter US state code (e.g. CA, NY)
    """
    url = f"{NWS_API_BASE}/alerts/active/area/{state}"
    data = await make_request(url, "GET")

    if not data or "features" not in data:
        return "Unable to fetch alerts or no alerts found."

    if not data["features"]:
        return "No active alerts for this state."

    alerts = [format_alert(feature) for feature in data["features"]]
    return "\n---\n".join(alerts)

@mcp.tool()
async def get_forecast(latitude: float, longitude: float) -> str:
    """Get weather forecast for a location.

    Args:
        latitude: Latitude of the location
        longitude: Longitude of the location
    """
    # First get the forecast grid endpoint
    points_url = f"{NWS_API_BASE}/points/{latitude},{longitude}"
    points_data = await make_request(points_url, "GET")

    if not points_data:
        return "Unable to fetch forecast data for this location."

    # Get the forecast URL from the points response
    forecast_url = points_data["properties"]["forecast"]
    forecast_data = await make_request(forecast_url, "GET")

    if not forecast_data:
        return "Unable to fetch detailed forecast."

    # Format the periods into a readable forecast
    periods = forecast_data["properties"]["periods"]
    forecasts = []
    for period in periods[:5]:  # Only show next 5 periods
        forecast = f"""
{period['name']}:
Temperature: {period['temperature']}°{period['temperatureUnit']}
Wind: {period['windSpeed']} {period['windDirection']}
Forecast: {period['detailedForecast']}
"""
        forecasts.append(forecast)

    return "\n---\n".join(forecasts)

@mcp.tool()
async def sync() -> str | None:
    """Sync the JIRA issue search MCP server."""
    response = await make_request(f"{JIRA_API_BASE}/sync", "POST")
    return f"{response}"

@mcp.tool()
async def query(query_term: str, is_key: bool) -> str | None:
    """Query the JIRA issue search MCP server."""
    if is_key:
        response = await make_request(f"{JIRA_API_BASE}/query?key={query_term}", "GET")
    else:
        response = await make_request(f"{JIRA_API_BASE}/query?q={query_term}", "GET")

    return f"{response}"

@mcp.tool()
async def suggest(key: str) -> str | None:
    """Suggest possible queries for the JIRA issue search MCP server."""
    response = await make_request(f"{JIRA_API_BASE}/suggest?key={key}", "GET")
 
    return f"{response}"