from .models import *


class DoesNotExist(Exception):
    pass


class Coords:
    def __init__(
        self, x1: int, y1: int, z1: int, x2: int = None, y2: int = None, z2: int = None
    ):
        self.is_cuboid = True if x2 else False
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.z1 = z1
        self.z2 = z2


class User:
    def __init__(self, user, uuid, rowid: int):
        self.user = user
        self.uuid = uuid
        self.rowid = rowid

    def __repr__(self):
        return f"User(rowid: {str(self.rowid)}; user: {self.user}; uuid: {self.uuid})"


class Interaction:
    def __init__(self, x, y, z, time, *args, **kwargs):
        self.x = x
        self.y = y
        self.z = z
        self.time = time

    def __repr__(self):
        return (
            "Interaction(coords: "
            + str(self.x)
            + ", "
            + str(self.y)
            + ", "
            + str(self.z)
            + "; time: "
            + str(self.time)
            + ")"
        )


class BlockInteraction(Interaction):
    def __init__(self, *args, type_, user, action, data, rolled_back):
        super().__init__(*args)
        self.type = type_
        self.user = user
        self.action = action
        self.data = data
        self.rolled_back = rolled_back

    def __repr__(self):
        return (
            "BlockInteraction(coords: "
            + str(self.x)
            + ", "
            + str(self.y)
            + ", "
            + str(self.z)
            + "; "
            + "time: "
            + str(self.time)
            + "; type: "
            + str(self.type)
            + "; action: "
            + str(self.action)
            + "; data: "
            + str(self.data)
            + "; rolled_back: "
            + str(self.rolled_back)
            + "; user: "
            + str(self.user)
            + ")"
        )


class CoreProtect:
    def __init__(self, database: DB):
        self.db = database.database
        self.table_prefix = database.table_prefix
        self.model: list[str] = []

    def reconnect(self):
        if not self.db.is_connected:
            self.db.reconnect(attempts=10, delay=1)

    def get_block_interactions(
        self,
        wid: int,
        coords: Coords,
        time: int,
        page: int = 1,
        limit: int = 20,
        user: int = None,
        data: int = None,
        type_: int = None,
        rolled_back: int = None,
        action: int = None,
    ) -> [BlockInteraction]:
        self.reconnect()
        row_max = page * limit
        page_start = row_max - limit
        if page_start < 0:
            page_start = 0
        coords_part = "AND x >= %(x1)s AND y >= %(y1)s AND z >= %(z1)s"
        if coords.is_cuboid:
            coords_part += " AND x <= %(x2)s AND y <= %(y2)s AND z <= %(z2)s"
        additional = ""
        if user:
            additional += "AND user = %(user)s "
        if data:
            additional += "AND data = %(data)s "
        if type_:
            additional += "AND type = %(type)s "
        if rolled_back:
            additional += "AND rolled_back = %(rolled_back)s "
        if action:
            additional += "AND action = %(action)s "
        with self.db.cursor() as cursor:
            cursor.execute(
                "SELECT time,user,action,type,data,rolled_back,x,y,z FROM "
                f"{self.table_prefix}block WHERE wid = %(wid)s {coords_part} AND action IN(0, 1) "
                f"AND time >= %(time)s {additional} ORDER BY rowid DESC LIMIT %(page)s, %(limit)s",
                {
                    "wid": wid,
                    "x1": coords.x1,
                    "y1": coords.y1,
                    "z1": coords.z1,
                    "x2": coords.x2,
                    "y2": coords.y2,
                    "z2": coords.z2,
                    "time": time,
                    "page": page_start,
                    "limit": limit,
                    "user": user,
                    "data": data,
                    "type": type_,
                    "rolled_back": rolled_back,
                },
            )
            result = cursor.fetchall()
            return [
                BlockInteraction(
                    inter[6],
                    inter[7],
                    inter[8],
                    inter[0],
                    type_=inter[3],
                    user=inter[1],
                    action=inter[2],
                    data=inter[4],
                    rolled_back=inter[5],
                )
                for inter in result
            ]

    def get_user_by_id(self, rowid: int) -> User:
        self.reconnect()
        with self.db.cursor() as cursor:
            cursor.execute(
                f"SELECT user,uuid FROM {self.table_prefix}user WHERE rowid = %(rowid)s",
                {"rowid": rowid},
            )
            result = cursor.fetchall()
            try:
                result = result[0]
            except IndexError:
                raise DoesNotExist
            return User(result[0], result[1], rowid)
