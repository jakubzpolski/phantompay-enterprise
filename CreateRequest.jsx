import { useState } from 'react'
import { createRequest, getCheckoutUrl } from '../api'

export default function CreateRequest({ onCreated }){
  const [amount, setAmount] = useState('')
  const [desc, setDesc] = useState('')
  const handleCreate = async () => {
    if(!amount) return alert('Enter amount')
    const res = await createRequest(amount, desc)
    const h = res.data.hash
    onCreated(h)
    const chk = await getCheckoutUrl(h)
    window.location.href = chk.data.checkout_url
  }
  return (
    <div>
      <h2>Create Request</h2>
      <input placeholder="Amount" value={amount} onChange={e=>setAmount(e.target.value)} />
      <input placeholder="Description" value={desc} onChange={e=>setDesc(e.target.value)} />
      <button onClick={handleCreate}>Pay</button>
    </div>
  )
}
