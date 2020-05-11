import razorpay
client=razorpay.Client(auth=("rzp_test_2tx97L0V09FUM6","QOWTRaArqW2Gj8O6rUxtEVwR"))
Data = {'amount':5000,"currency":'INR',"receipt":'order_rcptid_11',"payment_capture":1}
val = client.order.create(data=Data)
order_id = val['id'])
