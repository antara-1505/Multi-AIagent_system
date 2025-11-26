# from google.adk.agents import Agent
# from google.adk.tools.agent_tool import AgentTool

# from sub_agents.comms_agent.CommsAgent import comms_agent
# from sub_agents.coordinator_agent.CoordinatorAgent import coordinator_agent
# from sub_agents.rescue_agent.RescueAgent import rescue_agent
# from sub_agents.supply_agent.SupplyAgent import supply_agent
# from sub_agents.surveillance_agent.SurveillanceAgent import surveillance_agent

# root_agent = Agent(
#     name = "greeting_agent",
#     model = "gemini-2.0-flash",
#     description= "Greeting agent",
#     instruction=  """
#     You are a manager agent that is responsible for overseeing the work of the other agents.

#     Always delegate the task to the appropriate agent. Use your best judgement to
#     determine which agent to delegate to. 
#     """,
#     sub_agents=[surveillance_agent, comms_agent],   
# )


