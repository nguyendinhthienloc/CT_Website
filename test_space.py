from gradio_client import Client

client = Client("locnguyen0304/hf-sentiment-api")
result = client.predict(
		text="Hello!!",
		api_name="/predict"
)
print(result)
