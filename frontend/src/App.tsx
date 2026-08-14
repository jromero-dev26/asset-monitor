import './App.css'

interface Asset {
  id: number
  name: string
  asset_type: string
  location: string
  status: string
}

function App() {
  const assets: Asset[] = [
    {id: 1, name: 'Pump-101', asset_type: 'Pump', location: 'West Facility', status: 'Running'},
    {id: 2, name: 'Compressor-202', asset_type: 'Compressor', location: 'North Facility', status: 'Stopped'},
    {id: 3, name: 'Generator-301', asset_type: 'Generator', location: 'South Facility', status: 'Maintenance'},
  ]

  return (
    <main>
      <header>
        <h1>Asset Monitor</h1>
        <p>Industrial asset monitoring dashboard</p>
      </header>
      
      <section>
        <h2>Assets</h2>
        
      {assets
        .filter((asset) => asset.status === 'Running')
        .map((asset) => (
          <div key={asset.id}>
            <h3>{asset.name}</h3>
            <p>Type: {asset.asset_type}</p>
            <p>Location: {asset.location}</p>
            <p>Status: {asset.status}</p>
          </div>
        ))}
      </section>
    </main>
  )
}

export default App