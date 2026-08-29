import sqlite3
from pathlib import Path

from clothing_item import ClothingItem


class Database:

    def __init__(self, db_path: str | Path) -> None:
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._create_table()

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    def _create_table(self) -> None:
        connection = self._connect()

        try:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS clothing_items (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    category TEXT NOT NULL,
                    item_type TEXT NOT NULL DEFAULT '',
                    occasion TEXT NOT NULL,
                    color TEXT NOT NULL,
                    season TEXT NOT NULL,
                    image_path TEXT NOT NULL DEFAULT ''
                )
                """
            )

            connection.commit()

        finally:
            connection.close()

    def save_items(
        self,
        items: list[ClothingItem]
    ) -> None:

        connection = self._connect()

        try:
            connection.execute(
                "DELETE FROM clothing_items"
            )

            for item in items:
                connection.execute(
                    """
                    INSERT INTO clothing_items (
                        id,
                        name,
                        category,
                        item_type,
                        occasion,
                        color,
                        season,
                        image_path
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        item.id,
                        item.name,
                        item.category,
                        item.item_type,
                        item.occasion,
                        item.color,
                        item.season,
                        item.image_path
                    )
                )

            connection.commit()

        finally:
            connection.close()

    def load_items(self) -> list[ClothingItem]:

        connection = self._connect()

        try:
            rows = connection.execute(
                """
                SELECT
                    id,
                    name,
                    category,
                    item_type,
                    occasion,
                    color,
                    season,
                    image_path
                FROM clothing_items
                """
            ).fetchall()

        finally:
            connection.close()

        items = []

        for row in rows:
            (
                item_id,
                name,
                category,
                item_type,
                occasion,
                color,
                season,
                image_path
            ) = row

            item = ClothingItem(
                name,
                category,
                occasion,
                color,
                season,
                item_type,
                image_path,
                item_id
            )

            items.append(item)

        return items

    def has_items(self) -> bool:

        connection = self._connect()

        try:
            result = connection.execute(
                "SELECT COUNT(*) FROM clothing_items"
            ).fetchone()

        finally:
            connection.close()

        return result[0] > 0

    def clear(self) -> None:

        connection = self._connect()

        try:
            connection.execute(
                "DELETE FROM clothing_items"
            )

            connection.commit()

        finally:
            connection.close()