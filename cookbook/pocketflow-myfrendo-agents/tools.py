"""
Tool calling capabilities for Myfrendo agents.
Includes N8N, Retell, Twilio integrations and other tools.
"""
import os
import json
from typing import Dict, Any, List


class ToolRegistry:
    """Registry of available tools for personas to call."""

    def __init__(self):
        self.tools = {
            "n8n_trigger_workflow": self.n8n_trigger_workflow,
            "retell_create_call": self.retell_create_call,
            "twilio_send_sms": self.twilio_send_sms,
            "database_query": self.database_query,
            "web_search": self.web_search,
            "calculate_metrics": self.calculate_metrics,
        }

    def call_tool(self, tool_name: str, **kwargs) -> Dict[str, Any]:
        """
        Call a tool by name with given parameters.

        Args:
            tool_name: Name of the tool to call
            **kwargs: Parameters to pass to the tool

        Returns:
            Result from the tool execution
        """
        if tool_name not in self.tools:
            return {"error": f"Tool '{tool_name}' not found"}

        try:
            return self.tools[tool_name](**kwargs)
        except Exception as e:
            return {"error": str(e)}

    def get_available_tools(self) -> List[str]:
        """Get list of available tool names."""
        return list(self.tools.keys())

    # Tool implementations

    def n8n_trigger_workflow(self, workflow_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Trigger an N8N workflow.

        Args:
            workflow_id: The N8N workflow ID
            data: Data to pass to the workflow

        Returns:
            Workflow execution result
        """
        # Mock implementation - replace with actual N8N API call
        print(f"🔧 [N8N] Triggering workflow: {workflow_id}")
        print(f"   Data: {json.dumps(data, indent=2)}")

        return {
            "success": True,
            "workflow_id": workflow_id,
            "execution_id": "exec_12345",
            "status": "running",
            "message": "Workflow triggered successfully"
        }

    def retell_create_call(self, phone_number: str, agent_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a voice call using Retell AI.

        Args:
            phone_number: Phone number to call
            agent_config: Configuration for the voice agent

        Returns:
            Call creation result
        """
        # Mock implementation - replace with actual Retell API call
        print(f"📞 [Retell] Creating call to: {phone_number}")
        print(f"   Agent config: {json.dumps(agent_config, indent=2)}")

        return {
            "success": True,
            "call_id": "call_abc123",
            "status": "initiated",
            "phone_number": phone_number,
            "agent_prompt": agent_config.get("prompt", "")
        }

    def twilio_send_sms(self, to_number: str, message: str) -> Dict[str, Any]:
        """
        Send an SMS using Twilio.

        Args:
            to_number: Recipient phone number
            message: SMS message content

        Returns:
            SMS sending result
        """
        # Mock implementation - replace with actual Twilio API call
        print(f"💬 [Twilio] Sending SMS to: {to_number}")
        print(f"   Message: {message}")

        return {
            "success": True,
            "message_id": "msg_xyz789",
            "status": "sent",
            "to": to_number
        }

    def database_query(self, query: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Execute a database query.

        Args:
            query: SQL query to execute
            params: Query parameters

        Returns:
            Query results
        """
        # Mock implementation - replace with actual database connection
        print(f"🗄️  [Database] Executing query: {query}")
        if params:
            print(f"   Params: {json.dumps(params, indent=2)}")

        return {
            "success": True,
            "rows": [
                {"id": 1, "name": "Oak Realty", "agents": 5, "monthly_revenue": 8500},
                {"id": 2, "name": "Prime Properties", "agents": 3, "monthly_revenue": 4200},
            ],
            "count": 2
        }

    def web_search(self, query: str, num_results: int = 5) -> Dict[str, Any]:
        """
        Perform a web search.

        Args:
            query: Search query
            num_results: Number of results to return

        Returns:
            Search results
        """
        # Mock implementation - replace with actual search API
        print(f"🔍 [Web Search] Searching for: {query}")

        return {
            "success": True,
            "query": query,
            "results": [
                {
                    "title": "Real Estate AI Automation Guide 2024",
                    "url": "https://example.com/article1",
                    "snippet": "How AI voice agents are transforming real estate lead generation..."
                },
                {
                    "title": "Best Practices for Real Estate Cold Calling",
                    "url": "https://example.com/article2",
                    "snippet": "Top strategies for converting cold leads into appointments..."
                }
            ]
        }

    def calculate_metrics(self, metric_type: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate business metrics.

        Args:
            metric_type: Type of metric to calculate (CAC, LTV, conversion_rate, etc.)
            data: Input data for calculation

        Returns:
            Calculated metrics
        """
        print(f"📊 [Metrics] Calculating: {metric_type}")
        print(f"   Input data: {json.dumps(data, indent=2)}")

        # Mock calculations
        results = {}

        if metric_type == "unit_economics":
            cac = data.get("total_marketing_spend", 0) / max(data.get("new_customers", 1), 1)
            ltv = data.get("avg_monthly_revenue", 0) * data.get("avg_lifetime_months", 12)
            results = {
                "CAC": round(cac, 2),
                "LTV": round(ltv, 2),
                "LTV_CAC_ratio": round(ltv / max(cac, 1), 2),
                "payback_period_months": round(cac / max(data.get("avg_monthly_revenue", 1), 1), 2)
            }
        elif metric_type == "conversion_rate":
            calls = data.get("total_calls", 0)
            conversions = data.get("conversions", 0)
            results = {
                "conversion_rate": round((conversions / max(calls, 1)) * 100, 2),
                "total_calls": calls,
                "conversions": conversions
            }

        return {
            "success": True,
            "metric_type": metric_type,
            "results": results
        }


# Global tool registry instance
tool_registry = ToolRegistry()


# Test the tools
if __name__ == "__main__":
    print("Testing tool registry...")
    print(f"\nAvailable tools: {tool_registry.get_available_tools()}")

    print("\n" + "="*50)
    result = tool_registry.call_tool(
        "retell_create_call",
        phone_number="+1234567890",
        agent_config={"prompt": "Hi, this is a test call"}
    )
    print(f"Result: {json.dumps(result, indent=2)}")

    print("\n" + "="*50)
    result = tool_registry.call_tool(
        "calculate_metrics",
        metric_type="unit_economics",
        data={
            "total_marketing_spend": 1000,
            "new_customers": 10,
            "avg_monthly_revenue": 500,
            "avg_lifetime_months": 12
        }
    )
    print(f"Result: {json.dumps(result, indent=2)}")

    print("\n✅ Tool registry working!")
