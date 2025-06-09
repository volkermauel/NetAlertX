import sqlite3
import pytest

# -----------------------------------------------------------------------------
# Test unique constraint on Plugins_Objects table
# -----------------------------------------------------------------------------

def create_table(conn):
    conn.execute(
        """CREATE TABLE IF NOT EXISTS Plugins_Objects(
            "Index" INTEGER PRIMARY KEY AUTOINCREMENT,
            Plugin TEXT NOT NULL,
            Object_PrimaryID TEXT NOT NULL,
            Object_SecondaryID TEXT NOT NULL,
            DateTimeCreated TEXT NOT NULL,
            DateTimeChanged TEXT NOT NULL,
            Watched_Value1 TEXT NOT NULL,
            Watched_Value2 TEXT NOT NULL,
            Watched_Value3 TEXT NOT NULL,
            Watched_Value4 TEXT NOT NULL,
            Status TEXT NOT NULL,
            Extra TEXT NOT NULL,
            UserData TEXT NOT NULL,
            ForeignKey TEXT NOT NULL,
            SyncHubNodeName TEXT,
            "HelpVal1" TEXT,
            "HelpVal2" TEXT,
            "HelpVal3" TEXT,
            "HelpVal4" TEXT,
            ObjectGUID TEXT,
            UNIQUE(Plugin, Object_PrimaryID, Object_SecondaryID, UserData)
        );""")


def test_unique_constraint():
    conn = sqlite3.connect(':memory:')
    create_table(conn)
    row = (
        'P', 'mac', 'ip', 'c', 'u', '1', '2', '3', '4',
        'status', 'extra', 'user', 'fk', 'node', 'h1', 'h2', 'h3', 'h4', 'guid'
    )
    conn.execute(
        "INSERT INTO Plugins_Objects (Plugin, Object_PrimaryID, Object_SecondaryID, DateTimeCreated, DateTimeChanged,"
        " Watched_Value1, Watched_Value2, Watched_Value3, Watched_Value4, Status, Extra, UserData, ForeignKey,"
        " SyncHubNodeName, HelpVal1, HelpVal2, HelpVal3, HelpVal4, ObjectGUID)"
        " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        row,
    )
    conn.commit()
    with pytest.raises(sqlite3.IntegrityError):
        conn.execute(
            "INSERT INTO Plugins_Objects (Plugin, Object_PrimaryID, Object_SecondaryID, DateTimeCreated, DateTimeChanged,"
            " Watched_Value1, Watched_Value2, Watched_Value3, Watched_Value4, Status, Extra, UserData, ForeignKey,"
            " SyncHubNodeName, HelpVal1, HelpVal2, HelpVal3, HelpVal4, ObjectGUID)"
            " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            row,
        )

    conn.close()

