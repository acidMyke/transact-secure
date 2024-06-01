# TransactSecure

This repo is part of submission for NUS Lifehack 2024 Hackathon for the team MachineSine.

\*Sub-theme: Tackling Financial Fraud

## Problem Statement

> The escalating threat of financial frauds poses a significant challenge to the financial well-being of individuals and businesses. Current anti-scam strategies are faced with gaps in public awareness, legal limitations and ever evolving scam tactics employed by fraudsters. Implement a comprehensive solution to combat bank scams that effectively addresses the above challenges.

## Solution

<!-- TODO: Add solution description -->

## Team members

Leader: Samuel @SamuelkohP04

Member:

- Wei Sin @weisintai
- Bryan @joe-oemm
- Jun Jie (acidMyke) @acidMyke

## Overview

This project is designed to detect fraudulent transactions using a combination of modern web technologies and machine learning. It leverages TypeScript, Svelte, SvelteKit for the front-end, and Python with Scikit-learn for the back-end machine learning model. Pocketbase is used as the database to store transaction data and manage user information.

## Project Structure

### Frontend:

Built with Svelte and SvelteKit.
TypeScript is used to ensure type safety and catch errors early in the development process.
The user interface allows users to input transaction details and receive a risk assessment.

### Backend and Database:

Pocketbase is used to store and manage transaction records and user data.
Ensures efficient data retrieval and real-time updates for the application.

### ML:

Developed with Python and Scikit-learn.
Handles data processing, model training, and making predictions.
The trained model is serialized using Pickle and loaded for inference during runtime.

## Key Features

### Fraud Detection Model:

Uses a Random Forest classifier to predict whether a transaction is fraudulent based on features such as transaction amount, frequency, and credit rating.
The model is trained on synthetic data generated to simulate real-world transaction patterns.

### Interactive User Interface:

Users can enter transaction details and immediately see the risk assessment (High, Moderate, Low).
Built with Svelte for a fast and responsive user experience.

### Real-time Data Handling:

Pocketbase manages the storage of transaction data and user information.
Real-time updates ensure that the application reflects the most current data.
