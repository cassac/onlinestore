import random
import string

def generate_order_id():
	chars = string.ascii_uppercase + string.digits
	order_number = "".join(random.choice(chars) for _ in range(8))
	return order_number