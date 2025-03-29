# Business Startup Advisor with MCP Agents

This project demonstrates the use of agent-based systems and the Model Context Protocol to create a comprehensive business startup advisor. It utilizes specialized AI agents to analyze various aspects of a business idea, providing a structured and insightful startup plan.

## Overview

The system consists of several AI agents, each focusing on a specific area of business planning:

* **Market Research Agent:** Analyzes market size, trends, and opportunities.
* **Competitor Analysis Agent:** Identifies and analyzes key competitors.
* **Business Model Agent:** Recommends viable business models.
* **Financial Analysis Agent:** Generates financial projections.
* **Legal & Compliance Agent:** Identifies relevant legal and regulatory requirements.

These agents collaborate using the MCP to provide a holistic startup plan, demonstrating the power of agent-based systems in tackling complex tasks.

## Prerequisites

* Python 3.8 or later
* `pip` package manager
* API Keys:
    * Anthropic API Key (for Claude models)
    * Exa API Key (for competitor analysis)

## Installation

1.  **Clone the repository (if applicable):**

    ```bash
    git clone https://github.com/pathanjalisrinivasan/Business-Startup-Advisor.md
    cd Business-Startup-Advisor
    ```

2.  **Install required Python packages:**

    ```bash
    pip install agno python-dotenv pydantic mcp duckduckgo-search exa-py
    ```

3.  **Set up environment variables:**

    * Create a `.env` file in the same directory as your script.
    * Add your API keys to the `.env` file:

        ```
        ANTHROPIC_API_KEY=your_anthropic_api_key
        EXA_API_KEY=your_exa_api_key
        ```

## Usage

1.  **Run the script:**

    ```bash
    python business_planner.py
    ```

2.  **Provide your business idea:**

    * The script will prompt you to enter a business idea.
    * The agents will then analyze your idea and provide a comprehensive startup plan.

## Code Structure

* `business_planner.py`: Contains the main script that defines and runs the MCP agents.
* `.env`: Stores API keys (should not be committed to version control).

## Dependencies

* `agno`: Agent-based framework.
* `python-dotenv`: Loads environment variables from a `.env` file.
* `pydantic`: Data validation and settings management.
* `mcp`: Model Context Protocol.
* `duckduckgo-search`: DuckDuckGo search library.
* `exa-py`: Exa search library.

## Troubleshooting

* **ModuleNotFoundError: No module named 'agno' or other dependencies:**
    * Ensure you have installed all required packages using `pip install`.
* **API Key Errors:**
    * Verify that your API keys are correctly set in the `.env` file.
    * Ensure your API keys are valid.
* **Errors related to network connections:**
    * Verify you have a stable internet connection.

## Future Enhancements

* Integration with other data sources and APIs.
* Improved user interface for input and output.
* More specialized agents for specific business domains.
* Ability to save and load startup plans.
* Add more robust error handling.

## Contributing
If you’d like to contribute to this project, feel free to open an issue or submit a pull request. Your feedback and contributions are welcome!
