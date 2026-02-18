def apply_pricing(scraped_price, discount, minimum_price, flat_discount):
    """
    Applies discount and minimum price rules.

    :param scraped_price: float (exact park price)
    :param discount: float (percentage value or dollar value)
    :param minimum_price: float
    :param flat_discount: bool
        - True  → discount is a dollar amount
        - False → discount is a percentage (0.10 = 10%)
    :return: int (final rounded price)
    """

    if flat_discount:
        discounted = scraped_price - discount
    else:
        discounted = scraped_price * (1 - discount)

    rounded_price = round(discounted)

    return max(rounded_price, minimum_price)