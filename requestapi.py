import asyncio
import requests

async def make_request(url):
    print("i was here ")
    response = await asyncio.to_thread(requests.get, url)
    print(url)
    return response.json()

async def main():
    urls = [f"http://0.0.0.0:5100/extract?neuralearn-{i}" for i in range(100)]
    #urls = [f"https://flask-save-chan.onrender.com/save/600/{i*600}/2" for i in range(120,200)]#200
    
    tasks = [make_request(url) for url in urls]

    results = await asyncio.gather(*tasks)
    print(results)

if __name__ == "__main__":
    asyncio.run(main())