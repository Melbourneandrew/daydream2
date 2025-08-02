#!/usr/bin/env python3
"""
Application entry point for development server
"""
import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app", host="0.0.0.0", port=8000, reload=True, log_level="info"
    )
