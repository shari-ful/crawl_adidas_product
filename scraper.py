from requests import Session

BASE_URL = 'https://shop.adidas.jp'

session = Session()

def get_item_info(url):
    item_ids = []

    for i in range(1,6):

        response = session.get(url+str(i))
        json_object = response.json()

        item_ids.extend(list(json_object["articles"].keys()))

    data_list = []
    for item_id in item_ids:
        prod_url = f'https://shop.adidas.jp/f/v2/web/pub/products/article/{item_id}/'

        vals = {
            "category": json_object["articles"][item_id]["brand_name"],
            "prod_url": BASE_URL + json_object["articles"][item_id]["link_detail_page"], 
            "max_image_len": 0,
            "max_review_len": 0        
        }

        prod_details = fetch_item_data(prod_url)
        all_details = {**vals, **prod_details}

        if all_details["image_len"] > all_details["max_image_len"]:
            all_details["max_image_len"] = all_details["image_len"]

        if all_details["review_len"] > all_details["max_review_len"]:
            all_details["max_review_len"] = all_details["review_len"]

        data_list.append(all_details)
        
    return data_list

def fetch_item_data(url: str):
    response = session.get(url)
    json_obj = response.json()

    vals = {
        "name": json_obj["page"]["head"]["title"],
        "breadcrumbs": '/'.join([breadcrumb["label"] for breadcrumb in json_obj["page"]["breadcrumbs"]]),
        "price": json_obj["product"]["article"]["price"]["current"]["withTax"],
        # "co-ordinate": json_obj["item"]["article"]["coordinates"]["articles"]
        "available_sizes": '/'.join([sku["sizeName"] for sku in json_obj["product"]["article"]["skus"]]),
        "review_count": json_obj["product"]["model"]["review"]["reviewCount"],
        "avg_review": json_obj["product"]["model"]["review"]["ratingAvg"]
    }
    #images
    images = json_obj["product"]["article"]["image"]["details"]
    img = 1
    for image in images:  
        vals[f"image_{img}"] =  image["imageUrl"]["medium"]
        img += 1
    vals['image_len'] = len(images)

    #co-ordinates
    co_ordinates = json_obj["product"]["article"]["coordinates"]
    if co_ordinates:
        vals["cp_name"] = co_ordinates["articles"][0]["name"]
        vals["cp_price"] = co_ordinates["articles"][0]["price"]["current"]["withTax"]
        vals["cp_number"] = co_ordinates["articles"][0]["articleCode"]
        vals["cp_img_url"] = co_ordinates["articles"][0]["image"]
        vals["cp_prod_url"] = BASE_URL + co_ordinates["articles"][0]["articleCode"]

    else:
        vals["cp_name"] = ''
        vals["cp_price"] = ''
        vals["cp_number"] = ''
        vals["cp_img_url"] = ''
        vals["cp_prod_url"] = ''

    #description
    description = json_obj["product"]["article"]["description"]
    if description:
        vals["dsr_title"] = description["messages"]["title"] or None
        vals["dsr_general"] = description["messages"]["mainText"] or None
        vals["dsr_itemize"] = str(description["messages"]["breads"]) or None

    #reviews
    reviews = json_obj["product"]["model"]["review"]["reviewSeoLd"]
    rvs = 1
    for review in reviews:  
        vals[f"review_date_{rvs}"] =  review["datePublished"] or None
        vals[f"review_rating_{rvs}"] = review["reviewRating"]["ratingValue"] or None
        vals[f"given_by_{rvs}"] = review["name"] or None
        vals[f"body_{rvs}"] = review["reviewBody"] or None
        rvs += 1
    vals["review_len"] = len(reviews)

    model = json_obj["product"]["article"]["modelCode"]
   
    vals["size_chart"] =  str(get_size_chart_value(model))
          

    return vals


def get_size_chart_value(model):
    result_dict = {}
    size_url = f'https://shop.adidas.jp/f/v1/pub/size_chart/{model}'
    size_res = session.get(size_url).json()
    data = size_res["size_chart"]

    result_dict = {}
    if data:

        for size_key, size_values in data["0"]["body"].items():
            size_name = size_values["0"]["value"]
            size_data = [f"{data['0']['header']['0'][elem_key]['value']}={elem_value['value']}" for elem_key, elem_value in size_values.items() if elem_key != "0"]
            result_dict[size_name] = ", ".join(size_data)

    return result_dict

    