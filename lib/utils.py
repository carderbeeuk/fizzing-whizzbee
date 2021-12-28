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