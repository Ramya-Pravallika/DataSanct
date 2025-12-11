import { useState } from 'react'
import UploadPath from './components/UploadPath'
import AgentStatus from './components/AgentStatus'
import DataView from './components/DataView'
import axios from 'axios'
import './index.css'

function App() {
  const [fileId, setFileId] = useState(null)
  const [status, setStatus] = useState('idle') // idle, uploading, analyzing, cleaning, done
  const [analysis, setAnalysis] = useState(null)
  const [cleaningResult, setCleaningResult] = useState(null)
  const [dataType, setDataType] = useState(null) // tabular, image

  const handleUpload = async (file) => {
    setStatus('uploading')
    const formData = new FormData()
    formData.append('file', file)

    try {
      // Direct analysis call
      setStatus('analyzing')
      const res = await axios.post('http://localhost:8000/analyze', formData)

      setFileId(res.data.file_id)
      setAnalysis(res.data)
      setDataType(res.data.type)

      // Simulate "thinking" time for effect, then clean
      setTimeout(() => startCleaning(res.data.file_id, res.data.type), 2500)
    } catch (err) {
      console.error(err)
      setStatus('error')
    }
  }

  const startCleaning = async (id, type) => {
    setStatus('cleaning')
    try {
      // Longer delay for "cleaning" to let the user see the cool terminal logs
      setTimeout(async () => {
        const res = await axios.post(`http://localhost:8000/clean/${id}`)
        setCleaningResult(res.data)
        // Add reasoning to the result object for display
        // In a real app, this comes from the backend. 
        // We hacked agent.py to return it in the plan, but clean endpoint returns stats.
        // Let's pass the plan we got from analysis to the result view for simplicity if needed,
        // but better is to update the cleaning_ops to return specific steps taken.
        // For now, we will merge the analysis plan into the result for display purposes.

        // Wait a bit more for "finishing" effect
        setTimeout(() => setStatus('done'), 1500)
      }, 3000)
    } catch (err) {
      console.error(err)
      setStatus('error')
    }
  }

  // Merge analysis plan reasoning into result for the view
  const finalResult = cleaningResult ? {
    ...cleaningResult,
    plan: analysis?.plan
  } : null

  return (
    <div className="container">
      {status === 'idle' && (
        <div className="hero-text">
          <h1 className="hero-title">DATA SANCT</h1>
          <p className="hero-subtitle">
            Sanctify your data. Amplify your intelligence, Created by Ramya Pravallika Chadalavada.
          </p>
        </div>
      )}

      {status === 'idle' && <UploadPath onUpload={handleUpload} />}

      {(status === 'analyzing' || status === 'cleaning' || status === 'uploading') && (
        <AgentStatus status={status} />
      )}

      {status === 'done' && (
        <DataView
          type={dataType}
          analysis={analysis}
          result={finalResult}
          onReset={() => setStatus('idle')}
        />
      )}
    </div>
  )
}

export default App
