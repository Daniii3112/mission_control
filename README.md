# Mission Control

A multi-agent system for strategic decision-making and creative content generation.

---

## Overview

Mission Control is an AI-powered system where multiple specialized agents collaborate to:

- analyze strategic decisions  
- generate product ideas  
- create marketing strategies  
- design creative content (e.g. video teasers)

The system is designed as a modular, extensible architecture that simulates real-world team dynamics.

---

## How It Works

The system runs a structured workflow where each agent has a specific role:

- **Director** → defines the mission and makes the final decision  
- **Product Lead** → proposes product options  
- **Brand Lead** → evaluates brand alignment  
- **Marketing Lead** → creates launch angles  
- **Operations Lead** → assesses feasibility  
- **Critical Reviewer** → challenges assumptions and risks  
- **Creative Director** → generates audiovisual concepts  

---

## 🎬 Video Generation

The system can generate a complete `video_plan` for short teaser content:

- creative concept
- scene breakdown
- on-screen text
- visual prompts
- music direction

### ▶️ Example

Run the CLI and select the video option:

python main.py
# select option 3 → create video teaser

## 🛠️ Installation

git clone https://github.com/Daniii3112/mission_control.git
cd mission_control
pip install -r requirements.txt

## ▶️ Usage

### Run in local mode (no API required)

python main.py --stub

### Run with API (OpenAI or Anthropic)

python main.py