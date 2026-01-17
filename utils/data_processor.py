from collections import defaultdict


def parse_transactions(raw_lines):
    transactions = []

    for line in raw_lines:
        parts = line.split('|')

        if len(parts) != 8:
            continue

        try:
            transaction = {
                'TransactionID': parts[0].strip(),
                'Date': parts[1].strip(),
                'ProductID': parts[2].strip(),
                'ProductName': parts[3].replace(',', '').strip(),
                'Quantity': int(parts[4].replace(',', '').strip()),
                'UnitPrice': float(parts[5].replace(',', '').strip()),
                'CustomerID': parts[6].strip(),
                'Region': parts[7].strip()
            }
            transactions.append(transaction)

        except ValueError:
            continue

    return transactions


def validate_and_filter(transactions, region=None, min_amount=None, max_amount=None):
    valid = []
    invalid = 0

    for t in transactions:
        if (
            not t.get('CustomerID') or
            not t.get('Region') or
            t['Quantity'] <= 0 or
            t['UnitPrice'] <= 0 or
            not t['TransactionID'].startswith('T')
        ):
            invalid += 1
            continue

        t['Amount'] = t['Quantity'] * t['UnitPrice']
        valid.append(t)

    print(f"Total records parsed: {len(transactions)}")
    print(f"Invalid records removed: {invalid}")
    print(f"Valid records after cleaning: {len(valid)}")

    filtered = valid[:]

    if region:
        filtered = [t for t in filtered if t['Region'] == region]

    if min_amount is not None:
        filtered = [t for t in filtered if t['Amount'] >= min_amount]

    if max_amount is not None:
        filtered = [t for t in filtered if t['Amount'] <= max_amount]

    summary = {
        'total_input': len(transactions),
        'invalid': invalid,
        'final_count': len(filtered)
    }

    return filtered, invalid, summary


def calculate_total_revenue(transactions):
    return sum(t['Quantity'] * t['UnitPrice'] for t in transactions)


def region_wise_sales(transactions):
    region_data = defaultdict(lambda: {'total_sales': 0.0, 'transaction_count': 0})

    total_revenue = calculate_total_revenue(transactions)

    for t in transactions:
        revenue = t['Quantity'] * t['UnitPrice']
        region_data[t['Region']]['total_sales'] += revenue
        region_data[t['Region']]['transaction_count'] += 1

    result = {}
    for region, data in region_data.items():
        percent = (data['total_sales'] / total_revenue * 100) if total_revenue else 0
        result[region] = {
            'total_sales': data['total_sales'],
            'transaction_count': data['transaction_count'],
            'percentage': round(percent, 2)
        }

    return result


def top_selling_products(transactions, n=5):
    product_data = defaultdict(lambda: {'qty': 0, 'revenue': 0.0})

    for t in transactions:
        product_data[t['ProductName']]['qty'] += t['Quantity']
        product_data[t['ProductName']]['revenue'] += t['Quantity'] * t['UnitPrice']

    sorted_products = sorted(
        product_data.items(),
        key=lambda x: x[1]['qty'],
        reverse=True
    )

    return [
        (name, data['qty'], data['revenue'])
        for name, data in sorted_products[:n]
    ]


def customer_analysis(transactions):
    customer_data = defaultdict(lambda: {
        'total_spent': 0.0,
        'purchase_count': 0,
        'products': set()
    })

    for t in transactions:
        cid = t['CustomerID']
        amount = t['Quantity'] * t['UnitPrice']

        customer_data[cid]['total_spent'] += amount
        customer_data[cid]['purchase_count'] += 1
        customer_data[cid]['products'].add(t['ProductName'])

    result = {}
    for cid, data in customer_data.items():
        avg = data['total_spent'] / data['purchase_count']
        result[cid] = {
            'total_spent': data['total_spent'],
            'purchase_count': data['purchase_count'],
            'avg_order_value': round(avg, 2),
            'products_bought': list(data['products'])
        }

    return dict(sorted(result.items(), key=lambda x: x[1]['total_spent'], reverse=True))


def daily_sales_trend(transactions):
    daily = defaultdict(lambda: {
        'revenue': 0.0,
        'transaction_count': 0,
        'customers': set()
    })

    for t in transactions:
        amount = t['Quantity'] * t['UnitPrice']
        daily[t['Date']]['revenue'] += amount
        daily[t['Date']]['transaction_count'] += 1
        daily[t['Date']]['customers'].add(t['CustomerID'])

    return {
        date: {
            'revenue': data['revenue'],
            'transaction_count': data['transaction_count'],
            'unique_customers': len(data['customers'])
        }
        for date, data in daily.items()
    }

def find_peak_sales_day(transactions):
    daily = daily_sales_trend(transactions)
    peak = max(daily, key=lambda d: daily[d]['revenue'])
    return (
        peak,
        daily[peak]['revenue'],
        daily[peak]['transaction_count']
    )



def low_performing_products(transactions, threshold=10):
    product_data = defaultdict(lambda: {'qty': 0, 'revenue': 0.0})

    for t in transactions:
        name = t['ProductName']
        product_data[name]['qty'] += t['Quantity']
        product_data[name]['revenue'] += t['Quantity'] * t['UnitPrice']

    return [
        (name, data['qty'], data['revenue'])
        for name, data in product_data.items()
        if data['qty'] < threshold
    ]

