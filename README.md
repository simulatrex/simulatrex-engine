<div align="center">
<img src="./docs/assets/header.png" alt="Simulatrex" width="100%" />
</div>
<br/>

<h4 align="center">
    <a href="https://discord.gg/YxdTpQxrbS">
        <img src="https://img.shields.io/static/v1?label=Chat%20on&message=Discord&color=blue&logo=Discord&style=flat-square" alt="Discord">
    </a>
</h4>


<p align="center">
    <p align="center">Enable decision making based on LLM-based simulations
    <br>
    <br>
    <a href="https://github.com/simulatrex/simulatrex-engine/issues/new?assignees=&labels=enhancement&projects=&title=%5BFeature%5D%3A+">Feature Request</a>
</p>

## Start the Playground

Make sure to have the .env files in place following .env.example

1. Setup conda / venv env

2. Install global requirements

```
pip install -r requirements.txt
```

3. Install local simulatrex-engine package

```
pip install -e .
```

4. Start api server

```
cd api
pip install -r requirements.txt
uvicorn server:app --reload --loop asyncio
```

5. Install and run frontend

In a separate terminal:

```
cd playground
bun install
bun run dev
```

Open http://localhost:3000

Start running your simulation.

---

Or via Docker:

```
docker compose up
```

---

<img src="./docs/assets/infrastructure.png" alt="Simulatrex Infrastructure" width="100%" />

## Contributing
To contribute: Clone the repo locally -> Make a change -> Submit a PR with the change. 

Here's how to modify the repo locally: 
Step 1: Clone the repo 
```
git clone https://github.com/simulatrex/simulatrex-engine
```

Step 2: Navigate into the project, setup a new virtual env (recommended) and install dependencies: 
```
cd simulatrex
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Step 3: Submit a PR with your changes! 🚀
- push your fork to your GitHub repo
- submit a PR from there 

# Support / talk with founders
- [Community Discord 💭](https://discord.gg/YxdTpQxrbS)
- Email ✉️ dom@simulatrex.com
