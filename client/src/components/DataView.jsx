import { Download, RefreshCw, AlertTriangle, CheckCircle, FileText } from 'lucide-react'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export default function DataView({ type, analysis, result, fileId, onReset }) {

    const handleDownload = () => {
        if (result && result.download_url) {
            window.location.href = `${API_URL}${result.download_url}`
        }
    }

    return (
        <div style={{ animation: 'fadeIn 0.6s ease' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '3rem' }}>
                <div>
                    <h2 style={{
                        margin: '0 0 0.5rem 0',
                        fontSize: '2rem',
                        color: 'var(--text-main)',
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
                    <button className="btn" onClick={handleDownload} style={{ background: 'var(--primary)' }}>
                        <Download size={18} /> Download Asset
                    </button>
                </div>
            </div>

            <div className="stats-grid" style={{ marginBottom: '2rem' }}>
                {type === 'tabular' && (
                    <>
                        <div className="stat-card">
                            <div className="stat-value">{result?.stats?.original_rows?.toLocaleString() || 0}</div>
                            <div className="stat-label">Original Rows</div>
                        </div>
                        <div className="stat-card">
                            <div className="stat-value">{result?.stats?.original_columns || 0}</div>
                            <div className="stat-label">Original Columns</div>
                        </div>
                        <div className="stat-card" style={{ borderColor: 'var(--accent)' }}>
                            <div className="stat-value" style={{ color: 'var(--primary)' }}>
                                {result?.stats?.cleaned_rows?.toLocaleString() || 0}
                            </div>
                            <div className="stat-label">Cleaned Rows</div>
                        </div>
                        <div className="stat-card" style={{ borderColor: 'var(--accent)' }}>
                            <div className="stat-value" style={{ color: 'var(--primary)' }}>
                                {result?.stats?.cleaned_columns || 0}
                            </div>
                            <div className="stat-label">Cleaned Columns</div>
                        </div>
                        <div className="stat-card" style={{ borderColor: 'var(--error)' }}>
                            <div className="stat-value" style={{ color: 'var(--error)' }}>
                                {result?.report?.removed_columns?.length || result?.stats?.removed_columns || 0}
                            </div>
                            <div className="stat-label">Columns Deleted</div>
                        </div>
                        <div className="stat-card" style={{ borderColor: 'var(--error)' }}>
                            <div className="stat-value" style={{ color: 'var(--error)' }}>
                                {result?.stats?.removed_rows?.toLocaleString() || 0}
                            </div>
                            <div className="stat-label">Rows Removed</div>
                            <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginTop: '0.2rem' }}>
                                {result?.report?.outliers_removed || 0} Outliers • {result?.report?.duplicates_removed || 0} Duplicates
                            </div>
                        </div>
                        <div className="stat-card" style={{ borderColor: 'var(--accent)' }}>
                            <div className="stat-value" style={{ color: 'var(--primary)' }}>
                                {result?.report?.imputed_columns?.length || 0}
                            </div>
                            <div className="stat-label">Columns Imputed</div>
                            <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginTop: '0.2rem' }}>
                                {(() => {
                                    const imputed = result?.report?.imputed_columns || []
                                    const mean = imputed.filter(c => c.includes('(mean)')).length
                                    const median = imputed.filter(c => c.includes('(median)')).length
                                    const mode = imputed.filter(c => c.includes('(mode)')).length
                                    const parts = []
                                    if (mean > 0) parts.push(`${mean} Mean`)
                                    if (median > 0) parts.push(`${median} Median`)
                                    if (mode > 0) parts.push(`${mode} Mode`)
                                    return parts.join(' • ') || 'None'
                                })()}
                            </div>
                        </div>
                    </>
                )}

                {type === 'image' && (
                    <div className="stat-card" style={{ borderColor: 'var(--accent)' }}>
                        <div className="stat-value" style={{ color: 'var(--primary)' }}>100%</div>
                        <div className="stat-label">Noise Filtered</div>
                    </div>
                )}
            </div>

            <div className="card">
                <h3 style={{ marginBottom: '1.5rem', display: 'flex', alignItems: 'center', gap: '0.8rem' }}>
                    <FileText style={{ color: 'var(--text-muted)' }} /> Agent Report
                </h3>

                {/* Tabular Cleanup Report */}
                {type === 'tabular' && result?.report && (
                    <div style={{ marginBottom: '2rem', display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
                        {result.report.removed_columns.length > 0 && (
                            <div style={{ background: '#fff1f2', padding: '1rem', borderRadius: '0.5rem', border: '1px solid var(--error)' }}>
                                <h4 style={{ margin: '0 0 0.5rem 0', color: 'var(--error)', fontSize: '0.9rem' }}>REMOVED COLUMNS (High Nulls)</h4>
                                <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
                                    {result.report.removed_columns.map(col => (
                                        <span key={col} style={{ background: 'white', padding: '0.2rem 0.6rem', borderRadius: '4px', fontSize: '0.8rem', color: 'var(--error)', border: '1px solid var(--error)' }}>
                                            {col}
                                        </span>
                                    ))}
                                </div>
                            </div>
                        )}

                        {result.report.imputed_columns.length > 0 && (
                            <div style={{ background: 'var(--bg-secondary)', padding: '1rem', borderRadius: '0.5rem', border: '1px solid var(--accent)' }}>
                                <h4 style={{ margin: '0 0 0.5rem 0', color: 'var(--primary)', fontSize: '0.9rem' }}>IMPUTED COLUMNS</h4>
                                <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
                                    {result.report.imputed_columns.map(col => (
                                        <span key={col} style={{ background: 'white', padding: '0.2rem 0.6rem', borderRadius: '4px', fontSize: '0.8rem', color: 'var(--primary)', border: '1px solid var(--accent)' }}>
                                            {col}
                                        </span>
                                    ))}
                                </div>
                            </div>
                        )}
                    </div>
                )}

                {/* Logic Reasoning Display */}
                {result?.plan?.reasoning && (
                    <div style={{ marginBottom: '2rem', background: 'var(--bg-secondary)', padding: '1.5rem', borderRadius: '0.75rem', border: '1px solid var(--border)' }}>
                        <h4 style={{ margin: '0 0 1rem 0', color: 'var(--text-muted)', fontFamily: 'var(--font-mono)', fontSize: '0.9rem' }}>EXECUTION LOG:</h4>
                        <ul style={{ listStyle: 'none', padding: 0, margin: 0, fontFamily: 'var(--font-mono)', color: 'var(--text-main)', fontSize: '0.9rem' }}>
                            {result.plan.reasoning.map((r, i) => (
                                <li key={i} style={{ marginBottom: '0.5rem', display: 'flex', gap: '0.8rem' }}>
                                    <span style={{ color: 'var(--primary)' }}>{'>'}</span> {r}
                                </li>
                            ))}
                            <li style={{ color: 'var(--primary)', marginTop: '1rem', display: 'flex', gap: '0.8rem' }}>
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
                                src={(() => {
                                    // Extract file extension from download_url (e.g., /download/cleaned_abc123.jpg -> jpg)
                                    const ext = result.download_url.split('.').pop()
                                    return `${API_URL}/uploads/${fileId}.${ext}`
                                })()}
                                className="comparison-img"
                                alt="Original"
                            />
                        </div>
                        <div className="comparison-col">
                            <p style={{ textAlign: 'center', color: 'var(--primary)', marginBottom: '1rem', fontFamily: 'var(--font-mono)' }}>PROCESSED OUTPUT</p>
                            <img
                                src={`${API_URL}${result.download_url}`}
                                className="comparison-img"
                                style={{ boxShadow: '0 0 20px rgba(45, 106, 79, 0.1)', borderColor: 'var(--primary)' }}
                                alt="Cleaned"
                            />
                        </div>
                    </div>
                )}
            </div>
        </div>
    )
}
