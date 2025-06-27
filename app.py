from flask import Flask, request, jsonify
from pydoll.browser import Chrome
import asyncio

app = Flask(__name__)

async def log_in(email, password, tab):
    try:
        await tab.go_to("https://imgflip.com/login", timeout=10000)
        username_input = await tab.find(id=None, class_name="login-email", name="email", tag_name="input", text=None, timeout=0, find_all=False, raise_exc=True)
        password_input = await tab.find(id=None, class_name="login-pass", name="pass", tag_name="input", text=None, timeout=0, find_all=False, raise_exc=True)
        submit_button = await tab.find(id=None, class_name="b but lrg login-btn", name=None, tag_name="button", text="Login", timeout=0, find_all=False, raise_exc=True)
        await username_input.click()
        await username_input.type_text(email)
        await password_input.click()
        await password_input.type_text(password)
        await submit_button.click()
    finally:
        pass

async def create_post(tab):
    try:
        await tab.go_to("https://imgflip.com/memegenerator/18799628/Blank-White-Template")
        generate_button = await tab.find(id=None, class_name="mm-generate b but", name=None, tag_name="button", text="Generate", timeout=0, find_all=False, raise_exc=True)
        await generate_button.click()
    finally:
        pass

@app.route("/create_post", methods=["POST"])
def create_post_endpoint():
    browser = Chrome()
    tab = asyncio.run(browser.start())
    try:
        data = request.json
        email = data.get("email")
        password = data.get("password")
        meme_count = data.get("meme_count", 5)

        asyncio.run(log_in(email, password, tab))
        count = 0
        while count < meme_count:
            asyncio.run(create_post(tab))
            count += 1
        return jsonify({"message": f"Successfully logged in and generated {meme_count} Memes"})
    finally:
        asyncio.run(browser.stop())


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)