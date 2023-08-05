DG Python SDK
===================================

 dougong sdk 工具类

安装
-----
远程下载并安装：

`pip install dg-sdk`


简介
------

为了提高客户接入的便捷性，本系统提供 SDK 方式介入，使用本 SDK 将极大的简化开发者的工作，开发者将无需考虑通信、签名、验签等，只需要关注业务参数的输入。



使用方法
--------

* 初始化SDK

未入网前，可使用以下测试商户参数进行开发测试

.. code:: Python

    import dg_sdk

    huifu_id = "6666000108854952"
    sys_id = "6666000108854952"
    product_id = "YYZY"
    private_key= "MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCxtfk3rjwdpBV81WBy5jIMcDLFdvHckhjGXkmWfaBn7euPRyetEhS4inpr7EvQ5KDUXNBPljI2NVhG/LEGZKvau1MW8j3t7dJ3gWafuVGsCiLJHU79sIRHf11nKOTykX5WxB/7MMwRnZsECuaZyCk7WPuSAlznqbDJdrZTzHhjQzMhjto1qD6+vc0OxyaBFlOY9piBtEfecsvD+6GfQ8exFqwzblJm9iZPYw02DaeUDLFO9Umn7i7gShlj/1Hh8nEM7YitpF/p26o+MC9LHWbIjgzjvNVhSRVmbvWys+3S11Zm/vux6Yzfk0H3fqrksAKSEkLEtEoYKS4wKjHdecztAgMBAAECggEACy1g4WmqCks5tsJM8K0d1L5x0w2qJK9js4ZWpop8Pk0ulbJqAm6ysvCyxnr0Qc0/eFvmFjtiKRqt1LksATTvwjAqB7Vww7hDlpSi+cTUKDfy/CdFwpsJlt2h6E0gKUmRYq+vO0NUcn8xMs3ktyNpxHvSRtqzMTbxEZrP2PFxWPzUKGNyk53FTlJ64YCoGQqWeGhA5LO6QLPHlAxIrvRf9B5dtXQr5XZXVqS9MwjtsRPvQPWiFXxlzvhJRcL/wXehcNextHzpMMgX/idB3HIpIl6XXLKiFUR4rBDJIMiQjQvS6zz2l1zpiJ0vWujVa3IY+PNefRA2ttg1DeC19GYa2QKBgQDh7AkJ7wut7p4qYAdcFEDVhFgP5mnSRyOBGWmClHYE4RIFplPiv4yO0fttAjFuCg4Zaxq49BuV3zshWOEIr72VK6wMa6Z+QbfXNr/1DT6nW+ktgXTw2G9Ts/nZiMrpcsbl7qvwChfJAPvEwnyP7Ckmd9t2WbQisuYZc+Vu8znO7wKBgQDJXskTiExEipQSOcVH5cX/ExVyj9MoLjmJhy3WTTDzGafgEoOPOfej2ZCgF6gCwugXJr+rtgdOpASk8WPACaCePdjdgQ2NVhSfV3op3TtvhgAPf3iI/zCVkZM4I1iZs6KjdHstLCKyAzCFBsowkPbfZBlFX4eO7Bk6XcIZ6x2h4wKBgQDcH64C5s4bb2beZOhm2Dj/kU54V4l93+CBFjCOkXaYdG+p35DWWspqEcCHSt68l8F7FLdZxEbodTPY3w+L9iejI4UkKPN1CzVD1U2dR4VnbY85zmwRiuCVzsM/KCCE61dOi4ktfbgFGhc1dEYHuROzLo8/tlFkiajW3eyLeSM3MwKBgATL3iw57d8gEeDRQXKx9WJa+QLOjDAD0dkFwEC/e+/+Z3I93qZVsiFT+E7n4VeXfuG2SZB0eH4WCApJuZ+EWzAJtxWnkkQQjdMxyTYgD99bKLs1xRA2S9j0K7aFmQGoNrJ//sMXrwfgbZJtk/lOKqMthjCR0u/DjeJHA22MnRsTAoGADXzJs/of0JExvQWwfdIUnSEPs/PgTrrJpo+CAdXnagYHF+InrmvIcNwx6ZzIs+9aGwUt0d/YsSpJkHMfAtTwZjB7sSw8Cg5DZ179Jy3YkKhFPvZv2ZCANa5J74HZNQUrUUL6O4FouZUiLwFlq8YuUPRtkAjYwyS/jwUbhJzqZhQ="
    public_key = "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAkMX8p3GyMw3gk6x72h20NOk3L9+Nn9mOVP6+YoBwCe7Zs4QmYrA/etFRZw2TQrSc51wgtCkJi1/x8Wl7maPL1uH2+77JFlPv7H/F4Lr2I2LXgnllg6PtwOSw/qvGYInVVB4kL85VQl0/8ObyxBUdJ43I0z/u8hJb2gwujSudOGizbeqQXAYrwcNy+e+cjodpPy9unpJjBfa4Wz2eVLLvUYYKZKdRn6pZR2cQsMBvL30K4cFlZqlJ9iP2hTG3gaiZJ9JrjTigwki0g9pbTDXiPACfuF1nOeObvLD22zBbgn1kwgfsqoG67z7g84u2jvfUFCzX1JRgd0xfNorTRkS2RQIDAQAB"

    dg_sdk.DGClient.mer_config = dg_sdk.MerConfig(private_key, public_key, sys_id, product_id, huifu_id)

参数说明：

    +-------------+----------+
    | 参数        | 中文名   |
    +-------------+----------+
    | public_key  | 汇付公钥 |
    +-------------+----------+
    | private_key | 商户私钥 |
    +-------------+----------+
    | sys_id      | 系统号   |
    +-------------+----------+
    | product_id  | 产品号   |
    +-------------+----------+
    | huifu_id    | 商户号   |
    +-------------+----------+

* 接口调用

    * 以支付宝支付为例，根据接口文档说明，构建请求参数体

    .. code:: Python

        required_params = {
            "trade_type": "A_NATIVE",
            "trans_amt": "1.00",
            "goods_desc": "goods_desc",
        }

    * 调用接口

    .. code:: Python

        url = "https://api.huifu.com/v2/trade/payment/jspay"
        result = dg_sdk.request_post(url, required_params)



* 其他调用方式

除了通用的调用接口之外，SDK 还针对部分重要交易接口提供了一种更便捷的方法，

将一些默认、非必须、无需特别关注的参数传递，以及数据脱敏、加密处理进行了封装。

使用方法如下所示：

    .. code:: Python

        response = dg_sdk.ScanPayment.create(trade_type=trade_type,
                                             trans_amt=amount,
                                             goods_desc="goods_desc",
                                             **extra_info)
        print(response)

现支持模块功能列表如下

* 聚合扫码 ScanPayment
    * 聚合正扫 - create
    * 订单查询 - query
    * 退款创建 - refund
    * 退款查询 - refund_query
    * 反扫    - micro_create
    * 关单    - close
    * 关单查询 - close_query

* 线上交易 OnlinePayment
    * 线上交易查询 - query
    * 线上交易退款 - refund
    * 线上退款查询 - refund_query
    * 银联APP支付 - union_app_create
    * 网银支付 - web_page
    * 手机网页支付 - web_page

* 快捷代扣对象 QuickAndHoldPay
    * 支付申请 - apply
    * 快捷支付确认 - confirm
    * 快捷/代扣绑卡申请接口 - bind_card
    * 快捷/代扣绑卡确认接口 - bind_card_confirm
    * 快捷代扣解绑 - un_bind
    * 快捷代扣短信重发时使用 - sms_code
    * 快捷页面版 - page
    * 代扣 - with_hold_pay
    * 线上交易查询 - query
    * 退款 - refund
    * 退款查询 - refund_query
    * 线上快捷代扣用户注册接口 - customer_reg

* 余额支付 AcctPayment
    * 余额支付 - create
    * 余额支付交易查询 - query
    * 余额支付退款 - refund
    * 余额支付退款查询 - refund_query
    * 余额查询 - balance_query

* 代发 Surrogate
    * 代发 - create
    * 查询代发交易 - query

* 取现对象 Drawcash
    * 取现 - create
    * 取现查询 - query

* 延时交易对象 Delaytrans
    * 延时交易确认 - confirm
    * 延时交易确认查询 - confirm_query
    * 延时交易退款 - confirm_refund
    * 交易确认批量信息查询 - query_confirm_list

* 银行卡分期 BankCredit
    * 银行卡分期支付签约 - sign
    * 一段式分期支付 - payment
    * 二段式分期支付申请 - payment_apply
    * 二段式分期支付确认 - payment_confirm
    * 银行卡分期退款 - refund
    * 银行卡分期查询 - query

* 商户对象 Merchant
    * 企业类型商户进件 - create_enterprise
    * 个体户类型商户进件 - create_individual
    * 基本信息修改 - modify
    * 详细信息查询 - query_merch_info
    * 新增总部 - add_headquarters
    * 修改总部 - modify_headquarters
    * 总部商户绑定&解除 - bind_headquarters
    * 查询账户信息 - query_acct_info
    * 商户业务开通 - reg_busi_info
    * 商户业务开通修改 - modify_busi_info
    * 申请单状态查询 - query_apply_status
    * 商户图片资料上传 - upload
    * 商户分账配置 - add_split_config
    * 商户分账配置查询 - query_split_config
    * 商户分期配置 - fenqi_config
    * 商户分期配置详情查询 - query_fenqi_config
    * 活动报名，支持微信 - reg_activities

* 分账用户对象 Member
    * 企业用户基本信息注册 - create_enterprise
    * 个人用户基本信息注册 - create_individual
    * 查询账户信息 - query_acct_info
    * 企业用户基本信息修改 - modify_enter_base_info
    * 个人用户基本信息修改 - modify_individual_base_info
    * 用户业务入驻 - reg_busi_info
    * 用户详情查询 - query_user_detail

* 工具类 DGTools
    * 校验签名 - verify_sign
    * 获取银联用户标识 - union_user_id
    * 使用公钥加密敏感信息 - encrypt_with_public_key



详情参考SDK 接入说明_

.. _接入说明: https://paas.huifu.com/docs/partners/devtools/#/sdk_python
