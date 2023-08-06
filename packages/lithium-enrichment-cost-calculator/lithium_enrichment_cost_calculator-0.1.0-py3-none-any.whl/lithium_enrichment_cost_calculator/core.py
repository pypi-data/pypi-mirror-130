import math
import numpy as np


def find_feed_amount(
    product_amount,
    product_enrichment_fraction,
    tails_enrichment_fraction,
    feed_enrichment_fraction=0.0759,
):
    assert product_enrichment_fraction < 1.0
    assert tails_enrichment_fraction < 1.0
    assert feed_enrichment_fraction < 1.0
    if product_enrichment_fraction > feed_enrichment_fraction:
        assert tails_enrichment_fraction < feed_enrichment_fraction
    if product_enrichment_fraction < feed_enrichment_fraction:
        assert tails_enrichment_fraction > feed_enrichment_fraction

    numerator = product_enrichment_fraction - tails_enrichment_fraction
    denominator = feed_enrichment_fraction - tails_enrichment_fraction

    feed_amount = product_amount * (numerator / denominator)

    return feed_amount


def find_swu_amount(
    product_amount,
    product_enrichment_fraction,
    tails_enrichment_fraction,
    feed_enrichment_fraction,
):

    assert product_enrichment_fraction < 1.0
    assert tails_enrichment_fraction < 1.0
    assert feed_enrichment_fraction < 1.0

    feed_amount = find_feed_amount(
        product_amount=product_amount,
        product_enrichment_fraction=product_enrichment_fraction,
        tails_enrichment_fraction=tails_enrichment_fraction,
        feed_enrichment_fraction=feed_enrichment_fraction,
    )

    tails_amount = feed_amount - product_amount

    feed_term = (
        feed_amount
        * ((2.0 * feed_enrichment_fraction) - 1.0)
        * math.log(feed_enrichment_fraction / (1.0 - feed_enrichment_fraction))
    )
    tails_term = (
        tails_amount
        * ((2.0 * tails_enrichment_fraction) - 1.0)
        * math.log(tails_enrichment_fraction / (1.0 - tails_enrichment_fraction))
    )
    product_term = (
        product_amount
        * ((2.0 * product_enrichment_fraction) - 1.0)
        * math.log(product_enrichment_fraction / (1.0 - product_enrichment_fraction))
    )

    swu = product_term + tails_term - feed_term

    return swu


def find_cost_of_enrichment(
    product_amount,
    product_enrichment_fraction,
    swu_cost,
    tails_cost,
    tails_enrichment_fraction,
    feed_cost,
    feed_enrichment_fraction=0.0759,
):

    assert product_enrichment_fraction < 1.0
    assert tails_enrichment_fraction < 1.0
    assert feed_enrichment_fraction < 1.0

    feed_amount = find_feed_amount(
        product_amount,
        product_enrichment_fraction,
        tails_enrichment_fraction,
        feed_enrichment_fraction,
    )

    tails_amount = feed_amount - product_amount

    swu_amount = find_swu_amount(
        product_amount=product_amount,
        product_enrichment_fraction=product_enrichment_fraction,
        tails_enrichment_fraction=tails_enrichment_fraction,
        feed_enrichment_fraction=feed_enrichment_fraction,
    )

    cost = (
        (swu_cost * swu_amount)
        + (feed_amount * feed_cost)
        - (tails_amount * tails_cost)
    )

    return cost


def find_minimal_cost_of_enrichment(
    product_amount,
    product_enrichment_fraction,
    feed_cost,
    swu_cost,
    tails_cost,
    feed_enrichment_fraction=0.0759,
):
    """Calls the find_cost_of_enrichment iteratively with different values for
    the tails_enrichment_fraction to find the minimal cost of enrichment for
    the given the inputs."""

    # tails_enrichment_fraction is being optimised.
    optimal_tails_enrichment_fraction = None
    minimal_cost = None

    step_size = 0.0000001

    tails_enrichment_fraction_to_try = np.linspace(
        step_size, feed_enrichment_fraction - step_size, 10000
    )
    for counter, tails_enrichment_fraction in enumerate(
        tails_enrichment_fraction_to_try
    ):

        cost = find_cost_of_enrichment(
            product_amount=product_amount,
            product_enrichment_fraction=product_enrichment_fraction,
            swu_cost=swu_cost,
            tails_cost=tails_cost,
            tails_enrichment_fraction=tails_enrichment_fraction,
            feed_cost=feed_cost,
            feed_enrichment_fraction=feed_enrichment_fraction,
        )

        if counter == 0:
            minimal_cost = cost
            optimal_tails_enrichment_fraction = tails_enrichment_fraction

        if cost < minimal_cost:
            minimal_cost = cost
            optimal_tails_enrichment_fraction = tails_enrichment_fraction

    return minimal_cost, optimal_tails_enrichment_fraction
