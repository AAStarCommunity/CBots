import logging
import os
from telethon import TelegramClient, events
from telethon.tl.types import Message
from datetime import datetime, timedelta
from command_manager import command_manager, BotType

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class TelegramBot:
    def __init__(self):
        self.api_id = os.getenv('TELEGRAM_API_ID')
        self.api_hash = os.getenv('TELEGRAM_API_HASH')
        self.bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.target_channel = os.getenv('TELEGRAM_TARGET_CHANNEL')
        self.target_group = os.getenv('TELEGRAM_TARGET_GROUP')
        self.client = None
        self.verification_texts = []
        self.last_verification_time = None
        logger.info("TelegramBot initialized")

    async def start(self):
        """Start the Telegram bot"""
        try:
            logger.info("Starting Telegram bot...")
            if not self.api_id or not self.api_hash or not self.bot_token:
                raise ValueError("Missing required environment variables: TELEGRAM_API_ID, TELEGRAM_API_HASH, or TELEGRAM_BOT_TOKEN")
                
            # 使用固定的会话文件名，避免多进程问题
            session_file = "telegram_bot_session"
            self.client = TelegramClient(session_file, self.api_id, self.api_hash)
            
            # 启动客户端
            await self.client.start(bot_token=self.bot_token)
            
            # 注册命令处理器
            command_manager.register_command('start', self.handle_start, BotType.TELEGRAM)
            command_manager.register_command('help', self.handle_help, BotType.TELEGRAM)
            command_manager.register_command('hi', self.handle_hi, BotType.TELEGRAM)
            command_manager.register_command('content', self.handle_content, BotType.TELEGRAM)
            command_manager.register_command('price', self.handle_price, BotType.TELEGRAM)
            command_manager.register_command('event', self.handle_event, BotType.TELEGRAM)
            command_manager.register_command('task', self.handle_task, BotType.TELEGRAM)
            command_manager.register_command('news', self.handle_news, BotType.TELEGRAM)
            command_manager.register_command('PNTs', self.handle_pnts, BotType.TELEGRAM)
            command_manager.register_command('account', self.handle_account, BotType.TELEGRAM)
            
            # 注册消息处理器
            command_manager.register_message_handler(self.handle_message, BotType.TELEGRAM)
            
            # 设置事件处理器
            self.setup_handlers()
            
            logger.info("Telegram bot started successfully")
        except Exception as e:
            logger.error(f"Error starting Telegram bot: {e}", exc_info=True)
            if self.client:
                await self.client.disconnect()
            raise

    def setup_handlers(self):
        """Set up event handlers"""
        try:
            # 注册命令处理器
            @self.client.on(events.NewMessage(pattern='/start'))
            async def start_handler(event):
                await command_manager.process_command('start', event, self)

            @self.client.on(events.NewMessage(pattern='/help'))
            async def help_handler(event):
                await command_manager.process_command('help', event, self)

            @self.client.on(events.NewMessage(pattern='/hi'))
            async def hi_handler(event):
                await command_manager.process_command('hi', event, self)

            @self.client.on(events.NewMessage(pattern='/content'))
            async def content_handler(event):
                await command_manager.process_command('content', event, self)

            @self.client.on(events.NewMessage(pattern='/price'))
            async def price_handler(event):
                await command_manager.process_command('price', event, self)

            @self.client.on(events.NewMessage(pattern='/event'))
            async def event_handler(event):
                await command_manager.process_command('event', event, self)

            @self.client.on(events.NewMessage(pattern='/task'))
            async def task_handler(event):
                await command_manager.process_command('task', event, self)

            @self.client.on(events.NewMessage(pattern='/news'))
            async def news_handler(event):
                await command_manager.process_command('news', event, self)

            @self.client.on(events.NewMessage(pattern='/PNTs'))
            async def pnts_handler(event):
                await command_manager.process_command('PNTs', event, self)

            @self.client.on(events.NewMessage(pattern='/account'))
            async def account_handler(event):
                await command_manager.process_command('account', event, self)

            # 注册消息处理器
            @self.client.on(events.NewMessage)
            async def message_handler(event):
                await command_manager.process_message(event, self)

            # 注册用户状态处理器
            @self.client.on(events.UserUpdate)
            async def user_status_handler(event):
                if event.original_update.status:
                    user = await event.get_user()
                    if user and not user.bot:
                        await event.client.send_message(
                            event.chat_id,
                            f"👋 {user.first_name} is now online!"
                        )

            logger.info("Telegram bot event handlers set up successfully")
        except Exception as e:
            logger.error(f"Error setting up event handlers: {e}", exc_info=True)
            raise

    # 命令处理器
    async def handle_start(self, event):
        """Handle /start command"""
        try:
            user = await event.get_sender()
            username = user.first_name if user else "User"
            await event.reply(f"Hi {username}, welcome to the bot!")
        except Exception as e:
            logger.error(f"Error in handle_start: {e}", exc_info=True)

    async def handle_help(self, event):
        """Handle /help command"""
        try:
            help_text = """
Available commands:
/start - Start the bot
/help - Show this help message
/hi - Say hello
/content - Content management
/price - Price information
/event - Event management
/task - Task management
/news - News updates
/PNTs - PNTs information
/account - Account management
            """
            await event.reply(help_text)
        except Exception as e:
            logger.error(f"Error in handle_help: {e}", exc_info=True)

    async def handle_hi(self, event):
        """Handle /hi command"""
        try:
            user = await event.get_sender()
            username = user.first_name if user else "User"
            await event.reply(f"Hi {username}, nice to meet you!")
        except Exception as e:
            logger.error(f"Error in handle_hi: {e}", exc_info=True)

    async def handle_content(self, event):
        """Handle /content command"""
        try:
            user = await event.get_sender()
            username = user.first_name if user else "User"
            await event.reply(f"Hi {username}, you invoked function: content")
        except Exception as e:
            logger.error(f"Error in handle_content: {e}", exc_info=True)

    async def handle_price(self, event):
        """Handle /price command"""
        try:
            user = await event.get_sender()
            username = user.first_name if user else "User"
            await event.reply(f"Hi {username}, you invoked function: price")
        except Exception as e:
            logger.error(f"Error in handle_price: {e}", exc_info=True)

    async def handle_event(self, event):
        """Handle /event command"""
        try:
            user = await event.get_sender()
            username = user.first_name if user else "User"
            await event.reply(f"Hi {username}, you invoked function: event")
        except Exception as e:
            logger.error(f"Error in handle_event: {e}", exc_info=True)

    async def handle_task(self, event):
        """Handle /task command"""
        try:
            user = await event.get_sender()
            username = user.first_name if user else "User"
            await event.reply(f"Hi {username}, you invoked function: task")
        except Exception as e:
            logger.error(f"Error in handle_task: {e}", exc_info=True)

    async def handle_news(self, event):
        """Handle /news command"""
        try:
            user = await event.get_sender()
            username = user.first_name if user else "User"
            await event.reply(f"Hi {username}, you invoked function: news")
        except Exception as e:
            logger.error(f"Error in handle_news: {e}", exc_info=True)

    async def handle_pnts(self, event):
        """Handle /PNTs command"""
        try:
            user = await event.get_sender()
            username = user.first_name if user else "User"
            await event.reply(f"Hi {username}, you invoked function: PNTs")
        except Exception as e:
            logger.error(f"Error in handle_pnts: {e}", exc_info=True)

    async def handle_account(self, event):
        """Handle /account command"""
        try:
            user = await event.get_sender()
            username = user.first_name if user else "User"
            await event.reply(f"Hi {username}, you invoked function: account")
        except Exception as e:
            logger.error(f"Error in handle_account: {e}", exc_info=True)

    # 消息处理器
    async def handle_message(self, event):
        """Handle regular messages"""
        try:
            user = await event.get_sender()
            username = user.first_name if user else "User"
            message = event.message.message
            
            # 记录消息
            logger.info(f"Received message from {username}: {message}")
            
            # 如果是直接@机器人
            if event.message.mentioned:
                await event.reply(f"Hi {username}, I receive your message: {message}")
        except Exception as e:
            logger.error(f"Error in handle_message: {e}", exc_info=True)

    async def stop(self):
        """Stop the Telegram bot"""
        try:
            if self.client:
                await self.client.disconnect()
                logger.info("Telegram bot stopped successfully")
        except Exception as e:
            logger.error(f"Error stopping Telegram bot: {e}", exc_info=True)
            raise

    async def send_message(self, message: str, chat_id: str, reply_to: int = None):
        """Send a message to a specific chat"""
        try:
            if reply_to:
                await self.client.send_message(chat_id, message, reply_to=reply_to)
            else:
                await self.client.send_message(chat_id, message)
            logger.info(f"Message sent successfully to chat {chat_id}")
        except Exception as e:
            logger.error(f"Error sending message: {e}", exc_info=True)
            raise

    async def generate_verification_text(self):
        """Generate a verification text"""
        try:
            current_time = datetime.now()
            if not self.last_verification_time or (current_time - self.last_verification_time).days >= 1:
                self.verification_texts = []
                self.last_verification_time = current_time
            
            if not self.verification_texts:
                # 生成新的验证文本
                verification_text = f"Verification text for {current_time.strftime('%Y-%m-%d')}"
                self.verification_texts.append(verification_text)
            
            return self.verification_texts[0]
        except Exception as e:
            logger.error(f"Error generating verification text: {e}", exc_info=True)
            return None

    async def send_daily_verification(self):
        """Send daily verification text"""
        try:
            verification_text = await self.generate_verification_text()
            if verification_text and self.target_group:
                await self.send_message(verification_text, self.target_group)
                logger.info("Daily verification text sent successfully")
        except Exception as e:
            logger.error(f"Error sending daily verification: {e}", exc_info=True)
            raise

    async def handle_new_user(self, user_id: int, username: str):
        """Handle new user verification"""
        try:
            verification_text = await self.generate_verification_text()
            if verification_text:
                await self.client.send_message(
                    user_id,
                    f"Welcome {username}! Please verify yourself by sending this text: {verification_text}"
                )
                logger.info(f"Verification message sent to new user {username}")
        except Exception as e:
            logger.error(f"Error handling new user: {e}", exc_info=True)
            raise