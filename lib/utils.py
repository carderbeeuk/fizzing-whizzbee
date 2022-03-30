def build_product_code(ean=None, sku=None, mpn=None, gtin=None, asin=None, upc=None, isbn=None) -> str:
    """builds and returns a product code"""

    if not ean and not sku and not mpn and not gtin and not asin and not upc and not isbn:
        return None

    return f'{ean}_{sku}_{mpn}_{gtin}_{asin}_{upc}_{isbn}'


def build_features_list(featuresDict) -> list:
    """builds a list of features"""

    if not featuresDict:
        return []

    features = []
    for key in featuresDict:
        if len(featuresDict[key]['values']) > 0:
            features.append({
                'label': featuresDict[key]['label'],
                'value': featuresDict[key]['values'][0]['label']
            })
    
    return features


def serialize_offer(offer) -> dict:
    serialised_offer = {
        'product_code': offer.product_code,
        'active': offer.active,
        'product_uuid': offer.product_uuid,
        'offer_id': offer.offer_id,
        'availability': offer.availability,
        'title': offer.title,
        'description': offer.description,
        'author': offer.author,
        'publisher': offer.publisher,
        'price': offer.price,
        'price_without_rebate': offer.price_without_rebate,
        'month_price': offer.month_price,
        'manufacturer': offer.manufacturer,
        'merchant': offer.merchant.name,
        'provider': offer.provider,
        'google_category': offer.google_category.google_category_full_path,
        'google_category_id': offer.google_category.google_category_id,
        'google_category_parent_ids': _get_parent_category_ids(offer.google_category),
        'condition': offer.condition,
        'click_out_url': offer.click_out_url,
        'merchant_landing_url': offer.merchant_landing_url,
        'merchant_mobile_landing_url': offer.merchant_mobile_landing_url,
        'image_large': offer.image_large,
        'image_small': offer.image_small,
        'delivery_time': offer.delivery_time,
        'delivery_cost': offer.delivery_cost,
        'discount_percentage': offer.discount_percentage,
        'currency': offer.currency,
        'country': offer.country,
    }

    return serialised_offer


def _get_parent_category_ids(category_obj) -> list:
    parents = []
    i = 1
    this_cat = category_obj
    while i < category_obj.cardinality:
        parents.append(this_cat.parent_category.google_category_id)
        this_cat = this_cat.parent_category
        i += 1

    return parents