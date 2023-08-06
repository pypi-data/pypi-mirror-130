from .models import *


class DoesNotExist(Exception):
    pass


class User:
    def __init__(self, uid: int, uuid, owner: int):
        self.id = uid
        self.uuid = uuid
        self.owner = owner

    def __repr__(self):
        return str({"id": self.id, "uuid": self.uuid, "owner": self.owner})


class Region:
    def __init__(
        self,
        rid: int,
        x1: int,
        y1: int,
        z1: int,
        x2: int,
        y2: int,
        z2: int,
        wid: int,
        players: [User],
    ):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.z1 = z1
        self.z2 = z2
        self.wid = wid
        self.id = rid
        self.players = players

    def __repr__(self):
        return str(
            {
                "id": self.id,
                "wid": self.wid,
                "x1": self.x1,
                "y1": self.y1,
                "z1": self.z1,
                "x2": self.x2,
                "y2": self.y2,
                "z2": self.z2,
                "players": self.players,
            }
        )


class WorldGuard:
    def __init__(self, database: DB):
        self.db = database.database
        self.table_prefix = database.table_prefix
        self.model: list[str] = []

    def reconnect(self):
        if not self.db.is_connected:
            self.db.reconnect(attempts=10, delay=1)

    def get_region(self, x: int, y: int, z: int) -> Region:
        self.reconnect()
        with self.db.cursor() as cursor:
            cursor.execute(
                f"SELECT * FROM {self.table_prefix}region_cuboid WHERE "
                "min_x <= %(x)s AND min_y <= %(y)s AND min_z <= %(z)s AND "
                "max_x >= %(x)s AND max_y >= %(y)s AND max_z >= %(z)s",
                {"x": x, "y": y, "z": z},
            )
            result = cursor.fetchall()
            try:
                result = result[0]
            except IndexError:
                raise DoesNotExist
            cursor.execute(
                f"SELECT * FROM {self.table_prefix}region_players WHERE region_id = %(rid)s",
                {"rid": result[0]},
            )
            pl_result = cursor.fetchall()
            players = []
            for pl in pl_result:
                cursor.execute(
                    f"SELECT * FROM {self.table_prefix}user WHERE id = %(uid)s",
                    {"uid": pl[2]},
                )
                res = cursor.fetchall()
                uuid = res[0][2]
                players.append(User(pl[2], uuid, pl[3]))
            return Region(
                rid=result[0],
                wid=result[1],
                x1=result[2],
                y1=result[3],
                z1=result[4],
                x2=result[5],
                y2=result[6],
                z2=result[7],
                players=players,
            )

    def get_owner_regions(self, uuid: str, owner: int = 1) -> [Region]:
        self.reconnect()
        with self.db.cursor() as cursor:
            cursor.execute(
                f"SELECT * FROM {self.table_prefix}user WHERE uuid = %(uuid)s",
                {"uuid": uuid},
            )
            res = cursor.fetchall()
            try:
                res = res[0]
            except IndexError:
                raise DoesNotExist
            user = User(res[0], uuid, 0)
            cursor.execute(
                f"SELECT * FROM {self.table_prefix}region_players WHERE user_id = %(uid)s AND owner = %(owner)s",
                {"uid": user.id, "owner": owner},
            )
            res = cursor.fetchall()
            region_ids = []
            for i in res:
                region_ids.append(i[0])
            regions = []
            for i in region_ids:
                cursor.execute(
                    f"SELECT * FROM {self.table_prefix}region_cuboid WHERE region_id = %(rid)s",
                    {"rid": i},
                )
                obj = cursor.fetchall()[0]
                regions.append(self.get_region(obj[2], obj[3], obj[4]))
            return regions
