import asyncio
from custom_event_loop import TimingEventLoopPolicy


async def get_customer(customer_id):
    print(f"Fetching customer {customer_id}...")
    await asyncio.sleep(3)
    print(f"Customer {customer_id} data received")
    return {"id": customer_id, "name": f"Customer {customer_id}"}


async def get_product(product_id):
    print(f"Fetching product {product_id}...")
    await asyncio.sleep(2)
    print(f"Product {product_id} data received")
    return {"id": product_id, "name": f"Product {product_id}", "price": 99.99}


async def process_payment(order):
    print(
        f"Payment ${order['total']}: {order['customer_name']} {order['product_name']}"
    )
    await asyncio.sleep(1)
    print("Payment complete")


async def process_order(customer_id, product_id):
    async with asyncio.TaskGroup() as tg:
        customer_task = tg.create_task(get_customer(customer_id))
        product_task = tg.create_task(get_product(product_id))

    customer = customer_task.result()
    product = product_task.result()

    order = {
        "order_id": "0-1234",
        "customer_name": customer["name"],
        "product_name": product["name"],
        "total": product["price"],
    }

    await process_payment(order)


if __name__ == "__main__":
    asyncio.set_event_loop_policy(TimingEventLoopPolicy())
    asyncio.run(process_order("C-41", "P-314"))
