"""
Alasmia Main Entry Point
Starts: Ollama + Telegram Bot
100% CPU-based AI Companion
"""

import asyncio
import aiohttp
import sys

async def check_ollama():
    """Check if Ollama is running and has the model"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"http://localhost:11434/api/tags", timeout=5) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    models = [m['name'] for m in data.get('models', [])]
                    return models
    except:
        return None

async def main():
    print("""
╔═══════════════════════════════════════════╗
║       🤖 ALASMIA - AI Companion         ║
║       100% CPU • No GPU Required         ║
║       Telegram: @Alasmiabot              ║
╚═══════════════════════════════════════════╝
    """)
    
    # Check Ollama
    print("🔍 Checking Ollama...")
    models = await check_ollama()
    
    if models is None:
        print("❌ Ollama not running!")
        print("   Run: sudo ollama serve")
        sys.exit(1)
    
    print(f"✅ Ollama connected. Models: {models}")
    
    # Check if qwen2.5:14b is available
    if any('qwen2.5:14b' in m for m in models):
        print("✅ Qwen 2.5 14B ready!")
    else:
        print("⚠️  Qwen 2.5 14B not downloaded yet")
        print(f"   Available: {models}")
        print("   Download with: sudo ollama pull qwen2.5:14b")
        sys.exit(1)
    
    # Import and start bot
    sys.path.insert(0, '/home/ubuntu/alasmia/alasmia-core')
    from core import get_core
    from skills import SkillEngine
    from telegram_bot import AlasmiaBot
    
    # Initialize
    print("🚀 Initializing Alasmia...")
    core = get_core()
    skill_engine = SkillEngine(core)
    bot = AlasmiaBot(core, skill_engine)
    
    print("")
    print("═══════════════════════════════════════════")
    print("     ✅ ALASMIA is LIVE!")
    print("═══════════════════════════════════════════")
    print("   Telegram: @Alasmiabot")
    print("   Model: qwen2.5:14b (CPU inference)")
    print("")
    print("   Commands:")
    print("   /start - Introduce yourself")
    print("   /profile - See your relationship")
    print("   /skills - See available skills")
    print("   /reset - Start fresh")
    print("")
    print("   Press Ctrl+C to stop")
    print("═══════════════════════════════════════════")
    print("")
    
    try:
        await bot.start()
    except KeyboardInterrupt:
        print("\n👋 Shutting down...")
        await bot.stop()

if __name__ == "__main__":
    asyncio.run(main())