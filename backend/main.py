from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from database import get_connection


app = FastAPI()

class Asset(BaseModel):
    id: int
    name: str
    asset_type: str
    location: str
    status: str

class AssetCreate(BaseModel):
    name: str
    asset_type: str
    location: str
    status: str

@app.get("/")
def read_root():
    return {"message": "Asset Monitoring API is running!"}

@app.get("/assets")
def get_assets():
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM assets ORDER BY id;")
            assets = cursor.fetchall()

        return assets


@app.get("/assets/{asset_id}")
def get_asset(asset_id: int):
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM assets WHERE id = %s;",
                (asset_id,),
            )
            asset = cursor.fetchone()

        if asset is None:
            raise HTTPException(status_code=404, detail="Asset not found")

        return asset

@app.post("/assets", status_code=201)
def create_asset(asset_data: AssetCreate):
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO assets (name, asset_type, location, status)
                VALUES (%s, %s, %s, %s)
                RETURNING *;
                """,
                (
                    asset_data.name,
                    asset_data.asset_type,
                    asset_data.location,
                    asset_data.status,
                )
            )

            new_asset = cursor.fetchone()

    return new_asset


@app.put("/assets/{asset_id}")
def update_asset(asset_id: int, asset_data: AssetCreate):
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE assets
                SET name = %s,
                    asset_type = %s,
                    location = %s,
                    status = %s
                WHERE id = %s
                RETURNING *;
                """,
                (
                    asset_data.name,
                    asset_data.asset_type,
                    asset_data.location,
                    asset_data.status,
                    asset_id,
                ),
            )

            updated_asset = cursor.fetchone()

    if updated_asset is None:
        raise HTTPException(status_code=404, detail="Asset not found")

    return updated_asset


@app.delete("/assets/{asset_id}", status_code=204)
def delete_asset(asset_id: int):
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM assets
                WHERE id = %s
                RETURNING id;
                """,
                (asset_id,),
            )

            deleted_asset = cursor.fetchone()

    if deleted_asset is None:
        raise HTTPException(status_code=404, detail="Asset not found")

    return