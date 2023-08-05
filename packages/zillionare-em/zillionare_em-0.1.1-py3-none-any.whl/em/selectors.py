class Selectors:
    captcha_img_src = "#imgValidCode"
    captcha_txt = "#txtValidCode"
    account = "#txtZjzh"
    password = "#txtPwd"
    login_button = "#btnConfirm"
    valid_thru_3h = "#rdsc45"
    notice_btn = "//button[contains(., '知道了')]"

    # buy order page
    stockcode = "#stockCode"
    order_type = "#delegateWay"  # the order type: buy limit/ market price, ..
    price = "#iptPrice"
    shares = "#iptCount"
    confirm_order = "#btnConfirm"
