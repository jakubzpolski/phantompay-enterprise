import { useEffect, useState } from 'react'
import { getStatus } from '../api'

export default function Status({ hash }){
  const [status, setStatus] = useState('created')
  useEffect(()=>{
    const id = setInterval(async ()=>{
      try {
        const res = await getStatus(hash)
        setStatus(res.data.status)
      } catch (e) {}
    }, 2000)
    return ()=>clearInterval(id)
  },[hash])
  return <p>Status: {status}</p>
}
