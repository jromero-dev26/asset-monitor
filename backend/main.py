from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

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

assets = [
    Asset(
        id=1,
        name="Pump-101",
        asset_type="Pump",
        location="West Facility",
        status="Running",
    ),
    Asset(
        id=2,
        name="Compressor-202",
        asset_type="Compressor",
        location="North Facility",
        status="Stopped",
    ),
]

@app.get("/")
def read_root():
    return {"message": "Asset Monitoring API is running!"}

@app.get("/assets")
def get_assets():
    return assets


@app.get("/assets{asset_id}")
def get_asset(asset_id: int):
    for asset in assets:
        if asset.id == asset_id:
            return asset
    raise HTTPException(status_code=404, detail="Asset not found")

@app.post("/assets", status_code=201)
def create_asset(asset_data: AssetCreate):
    new_id = max((asset.id for asset in assets), default=0) + 1

    new_asset = Asset(
        id=new_id,
        name=asset_data.name,
        asset_type=asset_data.asset_type,
        location=asset_data.location,
        status=asset_data.status,
    )

    assets.append(new_asset)

    return new_asset

@app.put("/assets/{asset_id}")
def update_asset(asset_id: int, asset_data: AssetCreate):
    for index, asset in enumerate(assets):
        if asset.id == asset_id:
            updated_asset = Asset(
                id=asset_id,
                name=asset_data.name,
                asset_type=asset_data.asset_type,
                location=asset_data.location,
                status=asset_data.status,
            )

            assets[index] = updated_asset
            return updated_asset

        raise HTTPException(status_code=404, detail="Asset not found")

@app.delete("/assets/{asset_id}", status_code=204)
def delete_asset(asset_id: int):
    for index, asset in enumerate(assets):
        if asset.id == asset_id:
            assets.pop(index)
            return

    raise HTTPException(status_code=404, detail="Asset not found")

