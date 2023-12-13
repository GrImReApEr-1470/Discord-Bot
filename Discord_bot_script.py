#pip install mysql
#pip install mysql-connector-python
#pip install discord


import discord
from discord.ext import commands
import mysql.connector
import secrets

db_config = {
    "host": "sql12.freesqldatabase.com",
    "user": "sql12670091",
    "password": "VCI1TgY3Zx",
    "database": "sql12670091",
}

# Connect to the MySQL server
db = mysql.connector.connect(**db_config)
cursor = db.cursor()


# The SQL table is already created using the following query:
# create_table_query = """
# CREATE TABLE auth_tokens (
#     server_id BIGINT PRIMARY KEY,
#     auth_token VARCHAR(255) NOT NULL
# );
# """

# Define intents
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.reactions = True
intents.message_content = True
intents.presences = True
intents.members = True

# Create a bot instance with intents and a command prefix
bot = commands.Bot(command_prefix='g!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    print('------')

@bot.event
async def on_guild_join(guild):
    # Generate a unique auth token for the new server
    auth_token = secrets.token_urlsafe(16)  # Change the length as needed

    # Insert the server ID and auth token into the database
    insert_query = "INSERT INTO auth_tokens (server_id, auth_token) VALUES (%s, %s)"
    data = (guild.id, auth_token)
    cursor.execute(insert_query, data)
    db.commit()

@bot.command(name='hello', help='Print "Hello World" along with the server name')
async def hello(ctx):
    server_id = ctx.guild.id
    auth_token = get_auth_token(server_id)
    if auth_token:
        await ctx.send(f'Hello World {ctx.guild.name}!')
    else:
        await ctx.send('Authentication token not found. Please add the bot to the server again.')

def get_auth_token(server_id):
    cursor.execute("SELECT auth_token FROM auth_tokens WHERE server_id = %s", (server_id,))
    result = cursor.fetchone()
    return result[0] if result else None

# Run the bot with its token
bot.run('MTE4NDQ0NjM3MzY4NTM3NDk3Ng.G2XcF0.OXYQvy8RX6qtus7XEGu0M5fER3zf6-DBVjf5LE')
