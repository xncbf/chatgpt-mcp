import subprocess
import time
from mcp.server.fastmcp import FastMCP
from chatgpt_mcp.chatgpt_automation import ChatGPTAutomation, check_chatgpt_access


def is_conversation_complete() -> bool:
    """Check if ChatGPT conversation is complete using external AppleScript.
    
    Returns:
        True if conversation is complete, False if still in progress
    """
    try:
        automation = ChatGPTAutomation()
        screen_data = automation.read_screen_content()
        
        if screen_data.get("status") == "success":
            indicators = screen_data.get("indicators", {})
            
            # Simple check: only use conversationComplete indicator
            return indicators.get("conversationComplete", False)
        else:
            # If we can't read the screen, assume not complete for safety
            return False
            
    except Exception:
        # If any error occurs, assume not complete for safety
        return False


def wait_for_response_completion(max_wait_time: int = 300, check_interval: float = 0.5) -> bool:
    """Wait for ChatGPT response to complete.
    
    Args:
        max_wait_time: Maximum time to wait in seconds
        check_interval: How often to check for completion in seconds
        
    Returns:
        True if response completed within time limit, False if timed out
    """
    start_time = time.time()
    
    while time.time() - start_time < max_wait_time:
        if is_conversation_complete():
            return True
        time.sleep(check_interval)
    
    return False


def get_current_conversation_text() -> str:
    """Get the current conversation text from ChatGPT.
    
    Returns:
        Current conversation text
    """
    try:
        automation = ChatGPTAutomation()
        screen_data = automation.read_screen_content()
        
        if screen_data.get("status") == "success":
            texts = screen_data.get("texts", [])
            current_content = "\n".join(texts)
            
            # Clean up UI text
            cleaned_result = current_content.strip()
            cleaned_result = cleaned_result.replace('Regenerate', '').replace('Continue generating', '').replace('▍', '').strip()
            
            return cleaned_result if cleaned_result else "No response received from ChatGPT."
        else:
            return "Failed to read ChatGPT screen."
            
    except Exception as e:
        return f"Error reading conversation: {str(e)}"


async def get_chatgpt_response() -> str:
    """Get the latest response from ChatGPT after sending a message.
    
    Returns:
        ChatGPT's latest response text
    """
    try:
        # Wait for response to complete
        if wait_for_response_completion():
            return get_current_conversation_text()
        else:
            return "Timeout: ChatGPT response did not complete within the time limit."
        
    except Exception as e:
        raise Exception(f"Failed to get response from ChatGPT: {str(e)}")


async def ask_chatgpt(prompt: str) -> str:
    """Send a prompt to ChatGPT and return the response.
    
    Args:
        prompt: The text to send to ChatGPT
    
    Returns:
        ChatGPT's response
    """
    await check_chatgpt_access()
    
    try:
        # 프롬프트에서 개행 문자 제거 및 더블쿼츠를 싱글쿼츠로 변경
        cleaned_prompt = prompt.replace('\n', ' ').replace('\r', ' ').replace('"', "'").strip()
        
        # Activate ChatGPT and send message using keystroke
        automation = ChatGPTAutomation()
        automation.activate_chatgpt()
        automation.send_message_with_keystroke(cleaned_prompt)
        
        # Get the response
        response = await get_chatgpt_response()
        return response
        
    except Exception as e:
        raise Exception(f"Failed to send message to ChatGPT: {str(e)}")


def setup_mcp_tools(mcp: FastMCP):
    """MCP 도구들을 설정"""
    
    @mcp.tool()
    async def ask_chatgpt_tool(prompt: str) -> str:
        """Send a prompt to ChatGPT and return the response."""
        return await ask_chatgpt(prompt)

    @mcp.tool()
    async def get_chatgpt_response_tool() -> str:
        """Get the latest response from ChatGPT after sending a message."""
        return await get_chatgpt_response()
