import { useState } from 'react'
import CreateRequest from './pages/CreateRequest'
import Status from './pages/Status'

export default function App(){
  const [hash, setHash] = useState('')
  return (
    <div style={{maxWidth: 720, margin: '2rem auto', fontFamily: 'system-ui'}}>
      <h1>PhantomPay Pro</h1>
      <CreateRequest onCreated={setHash} />
      {hash && <Status hash={hash} />}
    </div>
  )
}
