"""Basic database functions"""

import sqlite3

import aiosqlite


def setup():
    """Set up the database if required"""
    con = sqlite3.connect("db/main.db")
    with con:
        con.execute(
            "CREATE TABLE IF NOT EXISTS guilds (id TEXT PRIMARY KEY, prefix TEXT)"
        )
        con.execute("CREATE TABLE IF NOT EXISTS users (id TEXT PRIMARY KEY)")
    con.close()
    print("Database setup completed")


async def add_guild(guild_id: str):
    """Add a guild to the database"""
    async with aiosqlite.connect("db/main.db") as con:
        await con.execute("INSERT INTO guilds VALUES (?, ?)", (guild_id, "#"))
        await con.commit()
        print(f"Added guild {guild_id}!")


async def set_prefix(guild_id: str, prefix: str):
    """Set the prefix of the given guild"""
    async with aiosqlite.connect("db/main.db") as con:
        await con.execute("UPDATE guilds SET prefix=? WHERE id=?", (prefix, guild_id))
        await con.commit()


async def get_prefix(guild_id: str) -> str:
    """Get the prefix of the given guild"""
    async with aiosqlite.connect("db/main.db") as con:
        res = await con.execute("SELECT prefix FROM guilds WHERE id=?", (guild_id,))
        res = await res.fetchone()
    if res is None:
        await add_guild(guild_id)
        return "#"
    return res[0]
