from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
from datetime import datetime, timedelta
import asyncio

async def send_order_reminders():
    # Set up GraphQL client
    transport = AIOHTTPTransport(url="http://localhost:8000/graphql")
    client = Client(transport=transport, fetch_schema_from_transport=True)

    # Define the GraphQL query for orders within the last 7 days
    query = gql("""
        query {
            orders(orderDate_Gte: "%s") {
                edges {
                    node {
                        id
                        customer {
                            email
                        }
                    }
                }
            }
        }
    """ % (datetime.now() - timedelta(days=7)).isoformat())

    try:
        # Execute the query
        result = await client.execute_async(query)
        
        # Get current timestamp for logging
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Open log file
        with open("/tmp/order_reminders_log.txt", "a") as log_file:
            # Process and log each order
            for edge in result["orders"]["edges"]:
                order_id = edge["node"]["id"]
                customer_email = edge["node"]["customer"]["email"]
                log_file.write(f"[{timestamp}] Order ID: {order_id}, Customer Email: {customer_email}\n")
        
        print("Order reminders processed!")
        
    except Exception as e:
        print(f"Error processing reminders: {str(e)}")

if __name__ == "__main__":
    asyncio.run(send_order_reminders())