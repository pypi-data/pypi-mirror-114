import aiomysql
import asyncpg # troll

from typing import Optional, Sequence, Any, AsyncGenerator

class fatFuckSQL: #postgresql
    def __init__(self): # blank init vars
        self._pool = None

    @classmethod
    async def connect(self, db: str, host: str, password: str, user: str):
        self = self()
        
        self._pool = await asyncpg.create_pool(
            user=user,
            password=password,
            database=db,
            host=host
        )
        
        return self
    
    async def fetch(self, query: str, *args):
        async with self._pool.acquire() as con:
            if args: # stupid asyncpg
                return await con.fetch(query, *args)
            else:
                return await con.fetch(query)

    async def fetchval(self, query: str, *args):
        async with self._pool.acquire() as con:
            if args: # stupid asyncpg
                return await con.fetchval(query, *args)
            else:
                return await con.fetchval(query)

    async def fetchrow(self, query: str, *args):
        async with self._pool.acquire() as con:
            if args: # stupid asyncpg
                return await con.fetchrow(query, *args)
            else:
                return await con.fetchrow(query)

    async def execute(self, query: str, *args):
        async with self._pool.acquire() as con:
            if args: # stupid asyncpg
                return await con.execute(query, *args)
            else:
                return await con.execute(query)
            
    async def iter(self, query: str, *args): # fetch() but iteration
        async with self._pool.acquire() as con:
            if args: # stupid asyncpg
                rows = await con.fetch(query, *args)
            else:
                rows = await con.fetch(query)
            
            for row in rows:
                yield row

    async def close(self):
        await self._pool.close()

class fatFawkSQL: # mysql/mariadb
    def __init__(self):
        self._pool: Optional[aiomysql.Pool] = None
    
    @classmethod
    async def connect(cls, db: str, host: str, password: str, user: str) -> 'fatFawkSQL':
        self = cls()
        
        self._pool = await aiomysql.create_pool(
            user=user,
            password=password,
            db=db,
            host=host,
            autocommit=True
        )
        
        return self
        
    async def fetch(self, query: str, params: Sequence[Any] = []) -> tuple[Optional[dict[str, Any]], ...]:
        async with self._pool.acquire() as con:
            async with con.cursor(aiomysql.DictCursor) as cur:
                await cur.execute(query, params)
                return await cur.fetchall()
            
    async def fetchval(self, query: str, params: Sequence[Any] = []) -> Optional[Any]:
        async with self._pool.acquire() as con:
            async with con.cursor(aiomysql.DictCursor) as cur:
                await cur.execute(query, params)
                
                if (row := await cur.fetchone()):
                    values = row.values()
                    return list(values)[0]
                
                return None
        
    async def fetchrow(self, query: str, params: Sequence[Any] = []) -> Optional[dict[str, Any]]:
        async with self._pool.acquire() as con:
            async with con.cursor(aiomysql.DictCursor) as cur:
                await cur.execute(query, params)
                return await cur.fetchone()
            
    async def execute(self, query: str, params: Sequence[Any] = []):
        async with self._pool.acquire() as con:
            async with con.cursor(aiomysql.Cursor) as cur:
                await cur.execute(query, params)
                await con.commit()
                
                return cur.lastrowid
            
    async def iter(self, query: str, params: Sequence[Any] = []) -> AsyncGenerator[Optional[dict[str, Any]], None]:
        async with self._pool.acquire() as con:
            async with con.cursor(aiomysql.DictCursor) as cur:
                await cur.execute(query, params)
                
                async for row in cur:
                    yield row
                    
    async def close(self) -> None:
        self._pool.close()
        await self._pool.wait_closed()