from celery import shared_task
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from datetime import datetime

@shared_task
def generate_crm_report():
    # Set up GraphQL client
    transport = RequestsHTTPTransport(url='http://localhost:8000/graphql')
    client = Client(transport=transport, fetch_schema_from_transport=True)

    # Define GraphQL query
    query = gql("""
        query {
            crmReport {
                totalCustomers
                totalOrders
                totalRevenue
            }
        }
    """)

    try:
        response = client.execute(query)
        report = response.get('crmReport', {})
        total_customers = report.get('totalCustomers', 0)
        total_orders = report.get('totalOrders', 0)
        total_revenue = report.get('totalRevenue', 0)

        # Log the report
        with open('/tmp/crm_report_log.txt', 'a') as f:
            f.write(
                f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - "
                f"Report: {total_customers} customers, {total_orders} orders, {total_revenue} revenue\n"
            )
    except Exception as e:
        with open('/tmp/crm_report_log.txt', 'a') as f:
            f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Error: {str(e)}\n")