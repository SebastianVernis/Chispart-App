# Blackbox API 404 Error Fix

## Problem
The application was experiencing a 404 error when making requests to the Blackbox API:
```
Error en la API de Blackbox: 404 Client Error: Not Found for url: https://api.blackbox.ai/chat/completions
Detalle: {"error":{"message":"litellm.NotFoundError: NotFoundError: OpenrouterException - {\"error\":{\"message\":\"No allowed providers are available for the selected model.\",\"code\":404}}. Received Model Group=blackboxai/anthropic/claude-3.5-sonnet\nAvailable Model Group Fallbacks=None"
```

## Root Cause
The code in `main.py` was hardcoded to use `blackboxai/anthropic/claude-3.5-sonnet` as the default model, but this model is not available on the Blackbox API. The configuration files (`config/models.json` and `models.json`) only had `blackboxai/openai/o1` configured as the available model.

## Solution
Updated the code to dynamically use the configured model from the configuration file instead of hardcoded model names.

### Changes Made

1. **main.py - Line ~910 (Code Intent Handler)**
   - **Before**: `code_model = request.model_type or "blackboxai/anthropic/claude-3.5-sonnet"`
   - **After**: 
     ```python
     default_model = orchestrator.models_config.get("models", {}).get("blackbox", {}).get("model", "blackboxai/openai/o1")
     code_model = request.model_type or default_model
     ```

2. **main.py - Line ~1126 (Text Intent Handler)**
   - **Before**: `text_model = request.model_type or "blackboxai/anthropic/claude-3.5-sonnet"`
   - **After**: 
     ```python
     default_model = orchestrator.models_config.get("models", {}).get("blackbox", {}).get("model", "blackboxai/openai/o1")
     text_model = request.model_type or default_model
     ```

3. **HTML Playground Files**
   - Updated placeholder text in:
     - `main.py` (embedded HTML)
     - `static/playground.html`
     - `static/playground_final.html`
     - `static/playground_improved.html`
   - **Before**: `placeholder="blackboxai/openai/o1, blackboxai/anthropic/claude-3.5-sonnet"`
   - **After**: `placeholder="blackboxai/openai/o1 (default)"`

## Testing Results

### Server Startup
✅ Server starts successfully without errors
✅ AI Orchestrator initializes correctly
✅ Configuration loaded from `config/models.json`

### API Endpoint Tests
✅ **Simple text query**: "Hello, what is 2+2?"
   - Response: "2 + 2 = 4."
   - Model used: `blackboxai/openai/o1`
   - Status: 200 OK

✅ **Code query**: "Write a Python function to calculate factorial"
   - Response: Generated Python factorial function
   - Model used: `blackboxai/openai/o1`
   - Status: 200 OK

### Log Verification
✅ No 404 errors in server logs
✅ All requests processed successfully
✅ Correct model (`blackboxai/openai/o1`) used for all requests

## Configuration
The application now correctly uses the model configured in `config/models.json`:
```json
{
  "default_model": "auto",
  "models": {
    "blackbox": {
      "model": "blackboxai/openai/o1",
      "enabled": true,
      "base_url": "https://api.blackbox.ai/chat/completions"
    }
  }
}
```

## Benefits
1. **No more 404 errors**: Uses only available models
2. **Flexible configuration**: Easy to change models via configuration file
3. **Consistent behavior**: All endpoints use the same configured model
4. **Better maintainability**: No hardcoded model names in the code

## How to Use
The application will now automatically use the model configured in `config/models.json`. To change the model:
1. Edit `config/models.json`
2. Update the `models.blackbox.model` field to your desired model
3. Restart the server

Alternatively, you can override the model per request by specifying `model_type` in the API request payload.
