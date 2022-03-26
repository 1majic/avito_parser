import sqlite3


def startDB():
    global conn, cursor
    conn = sqlite3.connect("blocks.db")
    cursor = conn.cursor()


def AddNewBlock(params):
    cursor.execute(f"INSERT INTO blocks VALUES({params});")


def GetAllBlocks():
    cursor.execute(f"select links from blocks")
    return cursor.fetchall()


def GetNewBlocks(blocks):
    cursor.execute(f"select links from blocks where page = 1")
    first_page_blocks = cursor.fetchall()
    newBlocks = []
    for i in blocks:
        if i not in first_page_blocks:
            newBlocks.append()
    return newBlocks