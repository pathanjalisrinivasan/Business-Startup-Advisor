import asyncio
import os
from textwrap import dedent
from typing import List, Dict, Optional, Any
from dotenv import load_dotenv  # Added for .env support

from agno.agent import Agent
from agno.models.anthropic.claude import Claude
from agno.team import Team
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.exa import ExaTools
from agno.tools.mcp import MCPTools
from mcp import StdioServerParameters
from pydantic import BaseModel, Field

# Load environment variables from .env file
load_dotenv()

# Define response models
class MarketAnalysis(BaseModel):
    market_size: str = Field(description="Estimated market size in dollars")
    growth_rate: str = Field(description="Annual growth rate of the market")
    key_trends: List[str] = Field(description="Major trends affecting the market")
    target_demographics: List[str] = Field(description="Key customer segments")
    barriers_to_entry: List[str] = Field(description="Challenges for new entrants")
    opportunities: List[str] = Field(description="Potential opportunities in the market")


class CompetitorInfo(BaseModel):
    name: str
    description: str
    strengths: List[str]
    weaknesses: List[str]
    market_share: Optional[str] = None
    pricing_strategy: Optional[str] = None
    unique_selling_points: List[str]
    website: Optional[str] = None


class BusinessModel(BaseModel):
    name: str = Field(description="Name or type of the business model")
    description: str = Field(description="Description of how the model works")
    revenue_streams: List[str] = Field(description="Ways the business will make money")
    cost_structure: List[str] = Field(description="Major costs for the business")
    key_resources: List[str] = Field(description="Critical resources needed")
    key_activities: List[str] = Field(description="Essential activities for success")
    value_proposition: str = Field(description="Core value offered to customers")
    scalability: str = Field(description="Potential for growth and scaling")
    risks: List[str] = Field(description="Potential risks of this model")


class FinancialProjection(BaseModel):
    startup_costs: Dict[str, str] = Field(description="Initial costs to start the business")
    monthly_operating_costs: Dict[str, str] = Field(description="Recurring monthly expenses")
    revenue_projections: Dict[str, str] = Field(description="Estimated revenue for different timeframes")
    break_even_analysis: str = Field(description="When the business might break even")
    funding_requirements: Optional[str] = Field(description="Amount of funding potentially needed")
    potential_roi: Optional[str] = Field(description="Estimated return on investment")


class StartupPlan(BaseModel):
    business_name: Optional[str] = None
    industry: str
    market_analysis: MarketAnalysis
    competitors: List[CompetitorInfo]
    recommended_business_models: List[BusinessModel]
    financial_projections: FinancialProjection
    next_steps: List[str] = Field(description="Recommended actions to take")
    resources: Optional[List[str]] = None


async def run_team():
    # Get API keys from environment (loaded from .env file)
    anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
    exa_api_key = os.getenv("EXA_API_KEY")
    
    if not anthropic_api_key:
        raise ValueError("ANTHROPIC_API_KEY is not set in the .env file")
    
    # Define each agent's tools
    market_research_tools = DuckDuckGoTools(cache_results=True)
    competitor_analysis_tools = ExaTools(api_key=exa_api_key)
    business_model_tools = DuckDuckGoTools(cache_results=True)
    financial_analysis_tools = DuckDuckGoTools(cache_results=True)
    legal_compliance_tools = DuckDuckGoTools(cache_results=True)

    # Create agents with Claude model
    market_research_agent = Agent(
        name="Market Research",
        role="Market Research Specialist",
        model=Claude("claude-3-7-sonnet-20250219"),
        tools=[market_research_tools],
        instructions=dedent("""\
            You are a market research specialist. Your role is to:
            1. Analyze market size, growth trends, and opportunities for new businesses
            2. Identify key demographics and customer segments
            3. Determine market needs and gaps that could be addressed
            4. Assess barriers to entry and market challenges
            5. Identify current market trends and future projections
            
            Provide comprehensive research about the specified industry or business idea.
            Always include specific data points and statistics when available.\
        """),
        add_datetime_to_instructions=True,
    )

    competitor_analysis_agent = Agent(
        name="Competitor Analysis",
        role="Competitive Intelligence Analyst",
        model=Claude("claude-3-7-sonnet-20250219"),
        tools=[competitor_analysis_tools],
        instructions=dedent("""\
            You are a competitive intelligence analyst. Your role is to:
            1. Identify major competitors in the specified market
            2. Analyze their strengths and weaknesses
            3. Examine their pricing strategies and market positioning
            4. Identify their unique selling propositions
            5. Find potential gaps or weaknesses that a new business could exploit
            
            Provide detailed analysis of at least 3-5 key competitors in the space.
            Include specific examples of their strategies and market positions.\
        """),
        add_datetime_to_instructions=True,
    )

    business_model_agent = Agent(
        name="Business Model",
        role="Business Model Strategist",
        model=Claude("claude-3-7-sonnet-20250219"),
        tools=[business_model_tools],
        instructions=dedent("""\
            You are a business model strategist. Your role is to:
            1. Recommend appropriate business models for the proposed venture
            2. Analyze revenue streams and cost structures
            3. Define value propositions that would resonate with target customers
            4. Identify key resources, activities, and partnerships needed
            5. Evaluate scalability and growth potential
            
            Suggest at least 2-3 viable business models for the proposed business.
            Be specific about how each model would work in practice.\
        """),
        add_datetime_to_instructions=True,
    )

    financial_analysis_agent = Agent(
        name="Financial Analysis",
        role="Financial Analyst",
        model=Claude("claude-3-7-sonnet-20250219"),
        tools=[financial_analysis_tools],
        instructions=dedent("""\
            You are a financial analyst specializing in startups. Your role is to:
            1. Estimate startup costs and initial capital requirements
            2. Project monthly operating expenses
            3. Create revenue projections for the first 1-3 years
            4. Perform break-even analysis
            5. Suggest funding options and investment requirements
            
            Provide realistic financial projections based on the industry and business model.
            Include specific costs and revenue figures whenever possible.\
        """),
        add_datetime_to_instructions=True,
    )

    legal_compliance_agent = Agent(
        name="Legal & Compliance",
        role="Legal & Regulatory Advisor",
        model=Claude("claude-3-7-sonnet-20250219"),
        tools=[legal_compliance_tools],
        instructions=dedent("""\
            You are a legal and regulatory advisor for startups. Your role is to:
            1. Identify key legal requirements for business formation
            2. Outline necessary licenses and permits
            3. Highlight industry-specific regulations
            4. Advise on intellectual property protection
            5. Point out potential legal risks and compliance issues
            
            Provide general legal guidance for the proposed business.
            Note that your advice is informational and entrepreneurs should 
            consult with a qualified attorney for specific legal questions.\
        """),
        add_datetime_to_instructions=True,
    )

    # Create and run the team
    team = Team(
        name="Business Startup Advisor",
        mode="coordinate",
        model=Claude("claude-3-7-sonnet-20250219"),
        members=[
            market_research_agent,
            competitor_analysis_agent,
            business_model_agent,
            financial_analysis_agent,
            legal_compliance_agent,
        ],
        instructions=[
            "First, understand the business idea and industry thoroughly.",
            "Have the Market Research agent analyze the market size, trends, and opportunities.",
            "Then, have the Competitor Analysis agent identify and analyze key competitors.",
            "Next, have the Business Model agent recommend viable business models based on the market and competitive landscape.",
            "Have the Financial Analysis agent create realistic financial projections based on the business models.",
            "Have the Legal & Compliance agent identify key legal requirements and regulatory considerations.",
            "Finally, synthesize all information into a comprehensive startup plan with specific, actionable advice.",
            "Continue asking individual team members until you have ALL the information you need.",
        ],
        response_model=StartupPlan,
        show_tool_calls=True,
        markdown=True,
        debug_mode=True,
        show_members_responses=True,
        add_datetime_to_instructions=True,
    )

    # Execute the team's task with the user's business idea
    await team.aprint_response(
        dedent("""\
        I'm thinking of starting a subscription-based meal preparation service that 
        focuses on sustainable, locally-sourced ingredients and targets busy professionals.
        The service would deliver pre-portioned ingredients and recipes weekly.
        I'm planning to launch in Austin, Texas first, then expand to other cities.
        What should I know before starting this business? What are my chances of success?
        """)
    )


if __name__ == "__main__":
    asyncio.run(run_team())