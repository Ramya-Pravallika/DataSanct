import { motion } from 'framer-motion'
import { Terminal, Cpu, ShieldCheck, Sparkles } from 'lucide-react'
import { useState, useEffect } from 'react'

export default function AgentStatus({ status }) {
    const [logs, setLogs] = useState([])

    useEffect(() => {
        if (status === 'analyzing') {
            simulateLogs([
                "Initializing core agents...",
                "Mounting file system...",
                "Scanning data structure...",
                "Detecting anomalies...",
                "Profiling column distributions...",
                "Generating heuristic model..."
            ])
        } else if (status === 'cleaning') {
            simulateLogs([
                "Loading cleaning strategy...",
                "Optimizing data vectors...",
                "Imputing missing values (Strategy: Adaptive)...",
                "Removing statistical outliers (Alpha: 0.05)...",
                "Denoising signal...",
                "Verifying integrity...",
                "Finalizing dataset..."
            ])
        }
    }, [status])

    const simulateLogs = (messages) => {
        setLogs([])
        messages.forEach((msg, i) => {
            setTimeout(() => {
                setLogs(prev => [...prev, `> ${msg}`])
            }, i * 800)
        })
    }

    return (
        <div className="card" style={{ maxWidth: '800px', margin: '0 auto' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', marginBottom: '2rem', borderBottom: '1px solid var(--border)', paddingBottom: '1rem' }}>
                <div className="loader-ring"><div></div><div></div><div></div><div></div></div>
                <div>
                    <h2 style={{ margin: 0, fontSize: '1.5rem', color: 'var(--primary)', fontWeight: 700 }}>
                        AI Agent Active
                    </h2>
                    <p style={{ margin: 0, color: 'var(--text-muted)', fontFamily: 'var(--font-mono)' }}>
                        Process ID: {Math.random().toString(36).substr(2, 9).toUpperCase()}
                    </p>
                </div>
            </div>

            <div style={{
                background: 'var(--bg-secondary)',
                borderRadius: '0.5rem',
                padding: '1.5rem',
                fontFamily: 'var(--font-mono)',
                border: '1px solid var(--border)',
                minHeight: '300px',
                color: 'var(--text-main)'
            }}>
                <div style={{ display: 'flex', gap: '0.5rem', marginBottom: '1rem', opacity: 0.8 }}>
                    <div style={{ width: 12, height: 12, borderRadius: '50%', background: '#ef4444' }}></div>
                    <div style={{ width: 12, height: 12, borderRadius: '50%', background: '#f59e0b' }}></div>
                    <div style={{ width: 12, height: 12, borderRadius: '50%', background: '#10b981' }}></div>
                </div>

                {logs.map((log, i) => (
                    <motion.div
                        key={i}
                        initial={{ opacity: 0, x: -10 }}
                        animate={{ opacity: 1, x: 0 }}
                        style={{ marginBottom: '0.5rem' }}
                    >
                        {log}
                    </motion.div>
                ))}
                <motion.div
                    animate={{ opacity: [0, 1] }}
                    transition={{ repeat: Infinity, duration: 0.8 }}
                    style={{ display: 'inline-block', width: '10px', height: '1.2em', background: 'var(--primary)', verticalAlign: 'middle' }}
                />
            </div>
        </div>
    )
}
