# Term-Project
___
Group Members: Wes Yang, Aaradh Benara

# Big Idea:
___
Our program is an innovative search tool that combines TheCocktailDB API with the natural language processing capabilities of OpenAI. While traditional cocktail apps only allow searching by specific ingredients such as “vodka” or “rum”, the app enhances the search experience by accepting natural language queries such as “summer fruit cocktail” or “winter warm drinks” and other natural language queries to enhance the search experience. When a user enters such a query, the app utilizes OpenAI's API to interpret the request and suggest appropriate cocktail names, which are then cross-referenced with TheCocktailDB for detailed recipes and instructions. All results are displayed in a clean, scrollable list with cocktail images and basic information.

# Minimum Variable Product(MVP):
___
Basic search interface with support for ingredient-specific searches (e.g., “vodka”) and natural language queries (e.g., “summer fruit drinks”).
Simple results in a scrolling list
Basic cocktail detail view
Cross-referencing with TheCocktailDB using OpenAI's APIs
# Learning Goals:
___
## Shared Learning Goals:
Mastery of application program interfaces for integration with multiple services
Gain experience with natural language processing
Learn effective error handling across multiple APIs
## Individual Goals:
Wes: Produce a coherent web page that combines the use of APIs and self-designed algorithms (API integration).
Aaradh: 
# Implementation Plan:
___
Frontend: Flask templates, CSS
Backend: Python/Flask, API integration
APIs: TheCocktailDB, OpenAI

## Development Phases:
Phase 1: Basic Setup and Core Search
Setup and Infrastructure

Setting up the Python/Flask development environment
Creating a GitHub repository
Configuring API keys and environment variables
Setting up the basic project structure

Phase 2: Smart Search Integration
OpenAI Integration

Setting up OpenAI API connections
Implementing Natural Language Processing

Phase 3: Feature Enhancements
Core functionality

Adding detailed cocktail information
Implement basic “What Can I Make?” functionality
Improve API error handling

Phase 4: Testing and Deployment
Testing

Writing basic unit tests
Performing API Integration Tests
Testing Error Scenarios

Preparing for Deployment

Code cleanup
Documentation
Performance Optimization
Security Review

# Project Timeline
___
Week 1
Start drafting project proposal and timeline
Set up Python/Flask development environment
Configure API keys and environment variables

Week 2:
Integrating the OpenAI API
Search Enhancements and Testing

Week 3
Implement basic “What Can I Make?” functionality
Code refinement

Week 4
Testing and Bug Fixing
Deployment and final testing
# Collaboration Plan:
___
We plan to have daily stand-up sessions through Discord to address any challenges and plan task assignments. We will use iMessage for messaging and Slack channels to ask coding-related questions.

For work distribution, we plan to work together, as we feel it's more efficient to work together rather than dividing up the work, and to give each other a better understanding of how the app works.
# Risks and Limitations:
___
The biggest difficulty is how to better handle integration between multiple APIs.If possible, we download data to minimize API calls
# Additional Course Content
___
Managing multiple API integrations (TheCocktailDB + OpenAI)
API Key Management
Structured error handling
