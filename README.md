# Cyberpunk RPG Game Using AWS

## Overview

This project is a Cyberpunk-themed Role-Playing Game (RPG) built using **AWS** (Amazon Web Services). Players can immerse themselves in a futuristic, dystopian world while interacting with NPCs, completing missions, and making decisions that impact the game world. The game leverages cloud services such as AWS Lambda, DynamoDB, and S3 for scalability, data storage, and efficient game state management.

## Features

- **Cyberpunk World**: Explore a dystopian future filled with neon lights, high-tech gadgets, and low-life streets.
- **Character Creation & Progression**: Create a unique character, level up, and unlock new abilities as you progress.
- **Dynamic Conversations**: Converse with NPCs powered by AI, where player choices affect story outcomes.
- **Mission System**: Complete various side quests and main story missions.
- **AWS-Powered Backend**: All game data is stored and processed on AWS, ensuring scalability and real-time synchronization across devices.
- **Cloud-Saved Game State**: Game progress is saved to the cloud, allowing players to continue their adventures on any device.

## Tech Stack

- **AWS Lambda**: Serverless backend for handling game logic and player actions.
- **Amazon DynamoDB**: NoSQL database for storing player data, game state, and world information.
- **Amazon S3**: Storage for game assets like images, music, and other media files.
- **AWS API Gateway**: API to interact with the Lambda functions from the frontend.
- **AWS CloudFormation**: Infrastructure as code for easy deployment of the necessary AWS services.
- **Python**: Game logic and backend API written in Python.

## Getting Started

To run the game locally and set up the cloud services, follow these steps:

### Prerequisites

- **AWS Account**: Create an AWS account if you don't have one already.
- **AWS CLI**: Install and configure AWS CLI for deploying resources.
- **Python 3.8+**: Ensure you have Python installed.
- **Serverless Framework (optional)**: If you want to deploy the Lambda functions, install the Serverless Framework.

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/arka-kxqi/cyberpunk-rpg-aws.git
   cd cyberpunk-rpg-aws
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up AWS services:
   - Deploy the necessary Lambda functions and resources using AWS CloudFormation or the Serverless Framework.
   - Configure DynamoDB tables, S3 buckets, and API Gateway.

4. Set up your game frontend to interact with the AWS backend:
   - Integrate API calls from the frontend to the AWS Lambda functions.
   - Display game state from DynamoDB and allow user input through web interfaces or a terminal-based interface.

### Running the Game Locally

If you want to run the backend locally before deploying it to AWS, follow these steps:

1. Start the Flask or FastAPI server (if using one for local testing):
   ```bash
   python app.py
   ```

2. Test the Lambda functions locally using tools like [SAM CLI](https://aws.amazon.com/serverless/sam/).

### Deploying to AWS

If you're ready to deploy the game to the cloud, you can use the Serverless Framework:

1. Install Serverless Framework:
   ```bash
   npm install -g serverless
   ```

2. Deploy the game:
   ```bash
   serverless deploy
   ```

   This will deploy all the necessary AWS resources such as Lambda functions, DynamoDB tables, and API Gateway.

## Gameplay

- **Character Creation**: Upon starting, players will create their characters, selecting from a variety of cyberpunk archetypes, skills, and attributes.
- **Missions**: Players can choose to pursue main storyline missions or engage in side quests.
- **Interactions**: The game's conversation system uses AI to generate NPC responses dynamically based on the player’s choices.
- **Progression**: As the player completes missions, they will gain experience and level up, unlocking new abilities and items.

## AWS Resources

### AWS Lambda
Lambda functions are used to handle game events, process player inputs, and update the game state. Each function is responsible for a specific part of the game, like:
- Handling character creation
- Managing inventory and quests
- Storing game progress in DynamoDB

### DynamoDB
DynamoDB is used to store game state, including:
- Player profiles and inventory
- Progression of main and side missions
- NPC interaction history

### S3
S3 is used to store assets such as:
- Game images (character portraits, map assets)
- Audio files for background music and sound effects
- JSON files for NPC dialogue trees and mission scripts

### API Gateway
API Gateway connects the frontend to the Lambda functions, allowing for real-time interactions in the game. This is where player actions and game updates are sent.
