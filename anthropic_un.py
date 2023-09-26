from claude2_api.client import (
    ClaudeAPIClient,
    SendMessageResponse,
    MessageRateLimitError,
)
from claude2_api.session import SessionData

cookie_header_value = "intercom-device-id-lupk8zyo=a059cc36-f309-42b6-8c10-f5e603c5a7eb; sessionKey=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; __stripe_mid=afd45c38-3556-4708-b519-a1509332f36f74a7cb; cf_clearance=4yAc56E7MptxUG.EJN1pWxKJLcR9jzKhXc2t1m6NqUI-1694775156-0-1-5033a261.b3fef32c.732fd81-0.2.1694775156; intercom-session-lupk8zyo=bm5qVXg3cSs1WjRiZTVjVkNhKys3aDg5Y2VIYkt3b1JEU2F6ejFiQS9GK0sxUEJCRDVBaW1TQ24vSGZFU1YxMS0tUnI0bzMrbW5wZGtXUitoWDRtSVdOQT09--bc6d234a91f31ae01d807bbaba8e933f82a56c54; __cf_bm=TlxMeBh5xNLb8UzALyoCOm3f2yfS4vvTj5DwQ8L9LA8-1694802984-0-AeqUw25mBTNf1JMNMx6f0qE+6YG6xDOTtD6r0ioqT8geQ3Ug7qky6RsxdVk4NOTlE/up1iyvnALBqna+rf3Wmhs="
user_agent = "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36"

data = SessionData(cookie_header_value, user_agent)

client = ClaudeAPIClient(data)

chat_id = client.create_chat()
if not chat_id:
    print(f"\nMessage limit hit, cannot create chat...")
    quit()

try:
    res: SendMessageResponse = client.send_message(
        chat_id, "Hello!", timeout=240
    )
    if res.answer:
        print(res.answer)
    else:
        print(f"\nError code {res.status_code}, response -> {res.error_response}")
except MessageRateLimitError as e:
    print(f"\nMessage limit hit, resets at {e.resetDate}")
    print(f"\n{e.sleep_sec} seconds left until -> {e.resetTimestamp}")
    quit()
finally:
    client.delete_chat(chat_id)

all_chat_ids = client.get_all_chat_ids()
for chat in all_chat_ids:
    client.delete_chat(chat)
