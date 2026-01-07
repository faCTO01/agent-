import logging
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from agents.agent_registry import AgentRegistry

logging.basicConfig(level=logging.INFO)

# ---------------------------------------------------------
#  Завантаження агентів
# ---------------------------------------------------------
registry = AgentRegistry()
registry.load_agents()

# ---------------------------------------------------------
#  Команда /run
# ---------------------------------------------------------
async def run_agent(update, context):
    if len(context.args) < 2:
        await update.message.reply_text("❗ Формат: /run <agent> <task>")
        return

    agent_name = context.args[0]
    task = " ".join(context.args[1:])

    agent_class = registry.get_agent(agent_name)
    if not agent_class:
        await update.message.reply_text(f"❌ Агент '{agent_name}' не знайдений.")
        return

    agent = agent_class()
    result = agent.run(task)

    await update.message.reply_text(result)

# ---------------------------------------------------------
#  Вільний чат → ISCRY1
# ---------------------------------------------------------
async def free_chat(update, context):
    text = update.message.text.strip()

    if text.startswith("/"):
        return

    agent_class = registry.get_agent("ISCRY1")
    agent = agent_class()

    result = agent.run(text)
    await update.message.reply_text(result)

# ---------------------------------------------------------
#  Команда /agents
# ---------------------------------------------------------
async def list_agents(update, context):
    agents = registry.list_agents()
    await update.message.reply_text("Доступні агенти:\n" + "\n".join(agents))

# ---------------------------------------------------------
#  Запуск Telegram бота
# ---------------------------------------------------------
def main():
    print(">>> Telegram Command Center starting...")

    app = Application.builder().token("7937136792:AAEdEMgHBPf0gusTjrmV_m-RLzGdrXHt7Ao").build()

    app.add_handler(CommandHandler("run", run_agent))
    app.add_handler(CommandHandler("agents", list_agents))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, free_chat))

    print("🔥 Telegram Command Center запущено.")
    app.run_polling()

if __name__ == "__main__":
    main()
