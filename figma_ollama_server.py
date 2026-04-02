import logging
import os
import requests
import json
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
name = "figma-ollama-mcp"

logging.basicConfig(
    level=logging.INFO,
    format='%(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(name)

# Get environment variables
FIGMA_ACCESS_TOKEN = os.environ.get('FIGMA_ACCESS_TOKEN')
OLLAMA_API_KEY = os.environ.get('OLLAMA_API_KEY')
OLLAMA_MODEL = os.environ.get('OLLAMA_MODEL', 'deepseek-v3.1:671b-cloud')
FIGMA_FILE_ID = os.environ.get('FIGMA_FILE_ID')

# Create MCP server
mcp = FastMCP(name)

# Figma API functions
def get_figma_file(file_id):
    """Fetch a Figma file by ID"""
    if not FIGMA_ACCESS_TOKEN:
        return {"error": "Figma access token not configured"}
    
    try:
        headers = {"X-FIGMA-TOKEN": FIGMA_ACCESS_TOKEN}
        response = requests.get(f"https://api.figma.com/v1/files/{file_id}", headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Error fetching Figma file: {e}")
        return {"error": f"Failed to fetch Figma file: {e}"}

def get_figma_file_nodes(file_id, node_ids):
    """Fetch specific nodes from a Figma file"""
    if not FIGMA_ACCESS_TOKEN:
        return {"error": "Figma access token not configured"}
    
    try:
        headers = {"X-FIGMA-TOKEN": FIGMA_ACCESS_TOKEN}
        node_params = ",".join(node_ids)
        response = requests.get(
            f"https://api.figma.com/v1/files/{file_id}/nodes?ids={node_params}",
            headers=headers
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Error fetching Figma nodes: {e}")
        return {"error": f"Failed to fetch Figma nodes: {e}"}

# Ollama API function
def ask_ollama(prompt, max_tokens=1000):
    """Send a prompt to Ollama and get a response"""
    if not OLLAMA_API_KEY:
        return "Error: Ollama API key not configured"
    
    try:
        headers = {
            "Authorization": f"Bearer {OLLAMA_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.7,
                "top_p": 0.9,
                "top_k": 40,
                "max_tokens": max_tokens
            }
        }
        
        # Use the appropriate Ollama endpoint
        ollama_endpoint = os.environ.get('OLLAMA_ENDPOINT', 'https://api.ollama.ai/v1/generate')
        
        response = requests.post(
            ollama_endpoint,
            headers=headers,
            json=payload,
            timeout=60
        )
        response.raise_for_status()
        
        result = response.json()
        return result.get("response", "No response generated")
        
    except requests.RequestException as e:
        logger.error(f"Error calling Ollama API: {e}")
        return f"Sorry, I couldn't get a response from the Ollama model: {e}"

# MCP Tools
@mcp.tool()
def get_figma_design_info(file_id: str = None) -> str:
    """Get information about a Figma design file"""
    target_file_id = file_id or FIGMA_FILE_ID
    if not target_file_id:
        return "Error: No Figma file ID provided and FIGMA_FILE_ID not set in environment"
    
    result = get_figma_file(target_file_id)
    if "error" in result:
        return result["error"]
    
    # Extract relevant information
    file_info = {
        "name": result.get("name", "Unknown"),
        "last_modified": result.get("lastModified", "Unknown"),
        "thumbnail_url": result.get("thumbnailUrl", "None"),
        "version": result.get("version", "Unknown"),
        "document": result.get("document", {}).get("name", "Unknown")
    }
    
    return json.dumps(file_info, indent=2)

@mcp.tool()
def generate_code_from_figma(file_id: str = None, node_ids: str = None) -> str:
    """Generate HTML/CSS code from a Figma design"""
    target_file_id = file_id or FIGMA_FILE_ID
    if not target_file_id:
        return "Error: No Figma file ID provided and FIGMA_FILE_ID not set in environment"
    
    # Get Figma file data
    figma_data = get_figma_file(target_file_id)
    if "error" in figma_data:
        return figma_data["error"]
    
    # If specific node IDs are provided, get those nodes
    specific_nodes = None
    if node_ids:
        node_list = [node_id.strip() for node_id in node_ids.split(",")]
        specific_nodes = get_figma_file_nodes(target_file_id, node_list)
        if "error" in specific_nodes:
            return specific_nodes["error"]
    
    # Prepare prompt for Ollama
    prompt = f"""
    Based on this Figma design information, generate clean HTML and CSS code.
    
    Figma File: {figma_data.get('name', 'Unknown')}
    Document Structure: {json.dumps(figma_data.get('document', {}), indent=2)}
    
    {f"Specific Nodes: {json.dumps(specific_nodes, indent=2)}" if specific_nodes else ""}
    
    Please generate:
    1. Semantic HTML structure
    2. CSS styles (preferably using Flexbox/Grid)
    3. Responsive design considerations
    4. Clean, well-commented code
    
    Return the code in a single code block with appropriate language tags.
    """
    
    # Get code from Ollama
    return ask_ollama(prompt, max_tokens=2000)

@mcp.tool()
def describe_and_generate(description: str) -> str:
    """Describe a design and generate HTML/CSS code"""
    prompt = f"""
    Based on this design description, generate clean HTML and CSS code.
    
    Description: {description}
    
    Please generate:
    1. Semantic HTML structure
    2. CSS styles (preferably using Flexbox/Grid)
    3. Responsive design considerations
    4. Clean, well-commented code
    
    Return the code in a single code block with appropriate language tags.
    """
    
    return ask_ollama(prompt, max_tokens=2000)

if __name__ == "__main__":
    logger.info("Starting Figma-Ollama MCP server...")
    mcp.run(transport="stdio")
