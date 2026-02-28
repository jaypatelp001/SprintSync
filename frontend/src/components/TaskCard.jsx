/**
 * TaskCard — Individual task display with status actions.
 */
import { useState } from 'react';

const STATUS_CONFIG = {
    todo: { label: 'To Do', emoji: '📋', class: 'status-todo' },
    in_progress: { label: 'In Progress', emoji: '🔄', class: 'status-in-progress' },
    review: { label: 'Review', emoji: '👀', class: 'status-review' },
    done: { label: 'Done', emoji: '✅', class: 'status-done' },
};

const TRANSITIONS = {
    todo: ['in_progress'],
    in_progress: ['review', 'todo'],
    review: ['done', 'in_progress'],
    done: ['todo'],
};

export default function TaskCard({ task, onEdit, onStatusChange, onDelete, onLogTime }) {
    const [showTimeInput, setShowTimeInput] = useState(false);
    const [minutes, setMinutes] = useState('');

    const config = STATUS_CONFIG[task.status] || STATUS_CONFIG.todo;
    const transitions = TRANSITIONS[task.status] || [];

    const handleLogTime = () => {
        const mins = parseInt(minutes, 10);
        if (mins > 0) {
            onLogTime(task.id, mins);
            setMinutes('');
            setShowTimeInput(false);
        }
    };

    return (
        <div className={`task-card ${config.class}`}>
            <div className="task-card-header">
                <span className={`status-badge ${config.class}`}>
                    {config.emoji} {config.label}
                </span>
                <div className="task-actions">
                    <button onClick={() => onEdit(task)} className="btn-icon" title="Edit">✏️</button>
                    <button onClick={() => onDelete(task.id)} className="btn-icon" title="Delete">🗑️</button>
                </div>
            </div>

            <h3 className="task-title">{task.title}</h3>
            {task.description && <p className="task-description">{task.description}</p>}

            <div className="task-meta">
                <span className="time-badge">⏱️ {task.total_minutes} min</span>
                {task.assignee_id && <span className="assignee-badge">👤 User #{task.assignee_id}</span>}
            </div>

            <div className="task-card-footer">
                <div className="status-transitions">
                    {transitions.map(nextStatus => (
                        <button
                            key={nextStatus}
                            onClick={() => onStatusChange(task.id, nextStatus)}
                            className="btn-transition"
                        >
                            → {STATUS_CONFIG[nextStatus]?.label}
                        </button>
                    ))}
                </div>

                <div className="log-time-section">
                    {showTimeInput ? (
                        <div className="time-input-group">
                            <input
                                type="number"
                                value={minutes}
                                onChange={(e) => setMinutes(e.target.value)}
                                placeholder="min"
                                min="1"
                                className="time-input"
                            />
                            <button onClick={handleLogTime} className="btn-sm">Log</button>
                            <button onClick={() => setShowTimeInput(false)} className="btn-sm btn-ghost">✕</button>
                        </div>
                    ) : (
                        <button onClick={() => setShowTimeInput(true)} className="btn-sm btn-ghost">
                            + Log Time
                        </button>
                    )}
                </div>
            </div>
        </div>
    );
}
