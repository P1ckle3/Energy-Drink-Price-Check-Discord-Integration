# Discord Bot message sender
A simple script to send a message on a discord bot as a PBL approach to learning python. 

---

# Webhook Link

Replace the link variable with your discord webhook link before use. 

```Python
    load_dotenv()
    link = os.getenv("WEBHOOK_URL")

    hook = Webhook(link)
```