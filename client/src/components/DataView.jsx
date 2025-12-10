import { Download, RefreshCw, AlertTriangle, CheckCircle, FileText } from 'lucide-react'

export default function DataView({ type, analysis, result, onReset }) {

    const handleDownload = () => {
        if (result && result.download_url) {
            window.location.href = `http://localhost:8000${result.download_url}`
        }
    }

    return (
        <div style={{ animation: 'fadeIn 0.6s ease' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '3rem' }}>
                <div>
                    <h2 style={{
                        margin: '0 0 0.5rem 0',
                        fontSize: '2rem',
                        background: 'var(--secondary-gradient)',
                        WebkitBackgroundClip: 'text',
                        WebkitTextFillColor: 'transparent',
                        fontWeight: 800
                    }}>
                        Mission Accomplished
                    </h2>
                    <p style={{ color: 'var(--text-muted)', margin: 0, fontSize: '1.1rem' }}>
                        Data has been purified and verified.
                    </p>
                </div>
                <div style={{ display: 'flex', gap: '1rem' }}>
                    <button className="btn btn-secondary" onClick={onReset}>
                        <RefreshCw size={18} /> New Task
                    </button>
                    <button className="btn" onClick={handleDownload} style={{ background: 'var(--secondary-gradient)' }}>
                        <Download size={18} /> Download Asset
                    </button>
                </div>
            </div>

            <div className="stats-grid">
                {type === 'tabular' && result?.stats && (
                    <>
                        <div className="stat-card">
                            <div className="stat-value">{result.stats.original_rows.toLocaleString()}</div>
                            <div className="stat-label">Original Rows</div>
                        </div>
                        <div className="stat-card" style={{ borderColor: 'rgba(16, 185, 129, 0.2)' }}>
                            <div className="stat-value" style={{ color: '#34d399' }}>
                                {result.stats.cleaned_rows.toLocaleString()}
                            </div>
                            <div className="stat-label">Cleaned Rows</div>
                        </div>
                        <div className="stat-card" style={{ borderColor: 'rgba(239, 68, 68, 0.2)' }}>
                            <div className="stat-value" style={{ color: '#f87171' }}>
                                {result.stats.removed_rows.toLocaleString()}
                            </div>
                            <div className="stat-label">Anomalies Burned</div>
                        </div>
                    </>
                )}

                {type === 'image' && (
                    <div className="stat-card" style={{ borderColor: 'rgba(59, 130, 246, 0.2)' }}>
                        <div className="stat-value" style={{ color: '#60a5fa' }}>100%</div>
                        <div className="stat-label">Noise Filtered</div>
                    </div>
                )}
            </div>

            <div className="card">
                <h3 style={{ marginBottom: '1.5rem', display: 'flex', alignItems: 'center', gap: '0.8rem' }}>
                    <FileText className="text-muted" /> Agent Report
                </h3>

                {/* Logic Reasoning Display */}
                {result?.plan?.reasoning && (
                    <div style={{ marginBottom: '2rem', background: 'rgba(0,0,0,0.3)', padding: '1.5rem', borderRadius: '0.75rem', border: '1px solid rgba(255,255,255,0.05)' }}>
                        <h4 style={{ margin: '0 0 1rem 0', color: '#a1a1aa', fontFamily: 'var(--font-mono)', fontSize: '0.9rem' }}>EXECUTION LOG:</h4>
                        <ul style={{ listStyle: 'none', padding: 0, margin: 0, fontFamily: 'var(--font-mono)', color: '#e4e4e7' }}>
                            {result.plan.reasoning.map((r, i) => (
                                <li key={i} style={{ marginBottom: '0.5rem', display: 'flex', gap: '0.8rem' }}>
                                    <span style={{ color: 'var(--primary)' }}>{'>'}</span> {r}
                                </li>
                            ))}
                            <li style={{ color: '#10b981', marginTop: '1rem', display: 'flex', gap: '0.8rem' }}>
                                <span>{'>'}</span> STATUS: OPTIMIZED
                            </li>
                        </ul>
                    </div>
                )}

                {/* Visuals */}
                {type === 'image' && (
                    <div className="comparison-view">
                        <div className="comparison-col">
                            <p style={{ textAlign: 'center', color: 'var(--text-muted)', marginBottom: '1rem', fontFamily: 'var(--font-mono)' }}>RAW INPUT</p>
                            <img
                                src={`http://localhost:8000/uploads/${result.download_url.split('cleaned_')[1]}`}
                                className="comparison-img"
                                alt="Original"
                            />
                        </div>
                        <div className="comparison-col">
                            <p style={{ textAlign: 'center', color: '#10b981', marginBottom: '1rem', fontFamily: 'var(--font-mono)' }}>PROCESSED OUTPUT</p>
                            <img
                                src={`http://localhost:8000${result.download_url}`}
                                className="comparison-img"
                                style={{ boxShadow: '0 0 30px rgba(16, 185, 129, 0.2)', borderColor: '#059669' }}
                                alt="Cleaned"
                            />
                        </div>
                    </div>
                )}
            </div>
        </div>
    )
}
