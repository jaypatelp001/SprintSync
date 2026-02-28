/**
 * TaskModal — Create / Edit task with AI Suggest integration and user dropdown.
 */
import { useState, useEffect } from 'react';
import { api } from '../api';

export default function TaskModal({ task, onSave, onClose }) {
    const [title, setTitle] = useState(task?.title || '');
    const [description, setDescription] = useState(task?.description || '');
    const [assigneeId, setAssigneeId] = useState(task?.assignee_id || '');
    const [totalMinutes, setTotalMinutes] = useState(task?.total_minutes || 0);
    const [error, setError] = useState('');
    const [saving, setSaving] = useState(false);
    const [aiLoading, setAiLoading] = useState(false);
    const [users, setUsers] = useState([]);

    useEffect(() => {
        api.listUsers()
            .then(setUsers)
            .catch(() => setUsers([]));
    }, []);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setSaving(true);
        setError('');

        try {
            const data = {
                title,
                description: description || null,
                total_minutes: parseInt(totalMinutes, 10) || 0,
            };
            if (assigneeId) data.assignee_id = parseInt(assigneeId, 10);

            await onSave(data);
        } catch (err) {
            setError(err.message);
        } finally {
            setSaving(false);
        }
    };

    const handleAiSuggest = async () => {
        if (!title.trim()) {
            setError('Enter a title first to get AI suggestions');
            return;
        }

        setAiLoading(true);
        setError('');

        try {
            const data = await api.aiSuggest('description', title);
            setDescription(data.suggestion);
        } catch (err) {
            setError(err.message);
        } finally {
            setAiLoading(false);
        }
    };

    return (
        <div className="modal-overlay" onClick={onClose}>
            <div className="modal-content" onClick={(e) => e.stopPropagation()}>
                <div className="modal-header">
                    <h2>{task ? 'Edit Task' : 'Create Task'}</h2>
                    <button onClick={onClose} className="btn-close">✕</button>
                </div>

                {error && <div className="error-banner">{error}</div>}

                <form onSubmit={handleSubmit}>
                    <div className="form-group">
                        <label htmlFor="task-title">Title</label>
                        <div className="input-with-action">
                            <input
                                id="task-title"
                                type="text"
                                value={title}
                                onChange={(e) => setTitle(e.target.value)}
                                placeholder="Enter task title"
                                required
                                autoFocus
                            />
                            <button
                                type="button"
                                onClick={handleAiSuggest}
                                className="btn-ai"
                                disabled={aiLoading}
                                title="AI will generate a description from this title"
                            >
                                {aiLoading ? '⏳' : '🤖'} AI Suggest
                            </button>
                        </div>
                    </div>

                    <div className="form-group">
                        <label htmlFor="task-description">Description</label>
                        <textarea
                            id="task-description"
                            value={description}
                            onChange={(e) => setDescription(e.target.value)}
                            placeholder="Describe the task (or use AI Suggest)"
                            rows={4}
                        />
                    </div>

                    <div className="form-row">
                        <div className="form-group">
                            <label htmlFor="task-assignee">Assign To</label>
                            <select
                                id="task-assignee"
                                value={assigneeId}
                                onChange={(e) => setAssigneeId(e.target.value)}
                            >
                                <option value="">Unassigned</option>
                                {users.map(u => (
                                    <option key={u.id} value={u.id}>{u.username}</option>
                                ))}
                            </select>
                        </div>

                        <div className="form-group">
                            <label htmlFor="task-minutes">Minutes Logged</label>
                            <input
                                id="task-minutes"
                                type="number"
                                value={totalMinutes}
                                onChange={(e) => setTotalMinutes(e.target.value)}
                                min="0"
                            />
                        </div>
                    </div>

                    <div className="modal-footer">
                        <button type="button" onClick={onClose} className="btn-ghost">
                            Cancel
                        </button>
                        <button type="submit" className="btn-primary" disabled={saving}>
                            {saving ? 'Saving...' : (task ? 'Update' : 'Create')}
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
}
