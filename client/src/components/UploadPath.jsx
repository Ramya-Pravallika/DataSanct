import { useRef, useState } from 'react'
import { Upload, Database, Image as ImageIcon, Sparkles } from 'lucide-react'

export default function UploadPath({ onUpload }) {
    const [dragActive, setDragActive] = useState(false)
    const inputRef = useRef(null)

    const handleDrag = (e) => {
        e.preventDefault()
        e.stopPropagation()
        if (e.type === 'dragenter' || e.type === 'dragover') {
            setDragActive(true)
        } else if (e.type === 'dragleave') {
            setDragActive(false)
        }
    }

    const handleDrop = (e) => {
        e.preventDefault()
        e.stopPropagation()
        setDragActive(false)
        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            onUpload(e.dataTransfer.files[0])
        }
    }

    const handleChange = (e) => {
        e.preventDefault()
        if (e.target.files && e.target.files[0]) {
            onUpload(e.target.files[0])
        }
    }

    return (
        <div className="card" style={{ maxWidth: '800px', margin: '0 auto' }}>
            <div
                className={`upload-zone ${dragActive ? 'drag-active' : ''}`}
                onDragEnter={handleDrag}
                onDragLeave={handleDrag}
                onDragOver={handleDrag}
                onDrop={handleDrop}
                onClick={() => inputRef.current.click()}
            >
                <input
                    ref={inputRef}
                    type="file"
                    style={{ display: 'none' }}
                    onChange={handleChange}
                    accept=".csv,.xlsx,.xls,.zip,.jpg,.jpeg,.png"
                />

                <div style={{ position: 'relative', display: 'inline-block' }}>
                    <Upload className="icon-large" />
                    <Sparkles size={24} style={{ position: 'absolute', top: -10, right: -10, color: '#d946ef', animation: 'bounce 2s infinite' }} />
                </div>

                <h2 style={{ margin: '0 0 1rem 0', fontSize: '1.8rem' }}>Initiate Data Sequence</h2>
                <p style={{ color: 'var(--text-muted)', maxWidth: '400px', margin: '0 auto', fontSize: '1.1rem' }}>
                    Drag & Drop your raw datasets (CSV, Excel, ZIP) or visual assets (Images) here.
                </p>

                <div style={{ marginTop: '3rem', display: 'flex', justifyContent: 'center', gap: '3rem' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.8rem', color: 'var(--text-muted)', fontSize: '0.9rem', fontFamily: 'var(--font-mono)' }}>
                        <Database size={18} color="#3b82f6" /> TABULAR
                    </div>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.8rem', color: 'var(--text-muted)', fontSize: '0.9rem', fontFamily: 'var(--font-mono)' }}>
                        <ImageIcon size={18} color="#ec4899" /> VISUAL
                    </div>
                </div>
            </div>
        </div>
    )
}
