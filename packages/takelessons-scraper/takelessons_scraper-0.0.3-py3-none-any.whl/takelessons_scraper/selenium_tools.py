def convert_cookies_to_str(cookies):
    cookie_list = [f'{cookie["name"]}={cookie["value"]}' for cookie in cookies]
    return "; ".join(cookie_list)
